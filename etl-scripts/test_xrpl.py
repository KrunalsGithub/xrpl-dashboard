from xrpl.clients import JsonRpcClient
from xrpl.models.requests import Ledger
from xrpl.utils import ripple_time_to_datetime
import pytz
from datetime import datetime, timedelta

# Connect to the XRPL
client = JsonRpcClient("https://s1.ripple.com:51234")

def get_latest_validated_ledger():

    request = Ledger(ledger_index="validated")
    response = client.request(request)
    return response.result["ledger_index"]

def ledger_get_data(ledger_index):
# Fetch the latest validated closed ledger index from the XRPL network
    try:
        
        # Fetch the data of the latest ledger index
        request = Ledger(
            ledger_index=ledger_index,
            transactions=False,
            expand=False,
            binary=False
        )

        response = client.request(request)
        return response.result.get('ledger', None)

    except Exception as e:
        print(f"Failed to fetch ledger data: {e}")
        return None

def binary_search_ledger(target_time):
    target_time = target_time.astimezone(pytz.UTC) 
    latest_index = get_latest_validated_ledger()

    low_index = 0
    high_index = latest_index
    closest_ledger = None

    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2

        #FETCH DATA FOR LEDGER[MID]
        ledger_data = ledger_get_data(mid_index)

        if ledger_data is not None:
            ledger_close_time = ripple_time_to_datetime(ledger_data['close_time'])

            if ledger_close_time < target_time:
                low_index = mid_index + 1
                closest_ledger = mid_index
            elif ledger_close_time > target_time:
                high_index = mid_index - 1
            else:
                return mid_index

        if low_index == high_index and closest_ledger is None:
            return low_index

    return closest_ledger


def get_monthly_closed_ledgers(year):
    monthly_counts = {}

    for month in range(1, 13):

        start_time = datetime(year, month, 1, 0,0,0, tzinfo=pytz.UTC)

        if month == 12: 
            next_month = datetime(year + 1, 1, 1, 0,0,0, tzinfo=pytz.UTC)
        else:
            next_month =  datetime(year, month + 1, 1, 0,0,0, tzinfo=pytz.UTC)
        
        end_time = next_month - timedelta(seconds=1)


        first_ledger = binary_search_ledger(start_time)
        last_ledger = binary_search_ledger(end_time)

        if first_ledger is not None and last_ledger is not None:
            ledger_count = max(0, last_ledger - first_ledger)
        else:
            ledger_count = 0

        monthly_counts[f"{year}-{month:02d}"] = ledger_count

    return monthly_counts
    
year = 2023
result = get_monthly_closed_ledgers(year)

for month, count in result.items():
    print(f"Month: {month}, Closed Ledgers: {count}")