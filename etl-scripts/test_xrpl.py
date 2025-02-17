from xrpl.clients import JsonRpcClient
from xrpl.models.requests import Ledger
from xrpl.utils import ripple_time_to_datetime

# Connect to the XRPL
client = JsonRpcClient("https://s1.ripple.com:51234")

# Fetch the latest validated closed ledger index from the XRPL network
try:
    ledger_request = Ledger(ledger_index="ledger_index")  
    response = client.request(ledger_request)
    ledger_index = response.result["ledger_index"]
    ledger_close_time = response.result['ledger']['close_time']

    # Fetch the data of the latest ledger index
    request = Ledger(
        ledger_index=ledger_index,
        transactions=True,
        expand=True,
        binary=False
    )
    response = client.request(request)
    transactions = response.result['ledger']['transactions']
except Exception as e:
    print(f"Failed to fetch ledger data: {e}")
    exit(1)

payment_details = []

for transaction in transactions:
    tx_json = transaction.get('tx_json')
    meta_json = transaction.get('meta')
    
    if tx_json.get('TransactionType') == 'Payment' and meta_json.get('TransactionResult') == 'tesSUCCESS':
        try:
            # Convert Ripple time to Python datetime
            transaction_time = ripple_time_to_datetime(ledger_close_time)
            
            # Format the date as MM/DD/YY
            formatted_date = transaction_time.strftime('%m/%d/%y')
            # Convert Ripple time to Python datetime
            transaction_time = ripple_time_to_datetime(ledger_close_time)
            
            payment_details.append({
                'date': transaction_time  # Adding the date here
            })
        except KeyError as ke:
            print(f"KeyError for transaction: {ke}. Transaction data: {tx_json}")

# Optionally, print or process payment_details further
count = len(payment_details)

# Print the count
print(f"Number of successful transactions: {count}")