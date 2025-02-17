
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import LedgerData
import pandas as pd
import numpy as np
import xrpl
import time
import datetime

 


now = datetime.datetime.now()
print("The current time is:", now)


 #Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s2.ripple.com:51234/"
client = JsonRpcClient(JSON_RPC_URL) 

address = "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn"

ledgerdata = xrpl.models.requests.LedgerData(ledger_index="validated", limit="200", offset="0")

xrp_accountroot = xrpl.account.get_account_root(address,client) 


try:
    balance_drops = xrpl.account.get_balance(address,client)
    balance_xrp = balance_drops / 1_000_000
    print(f"The balance for the account {address} is {balance_xrp:.6f} XRP.")
except Exception as e:
    print(f"An error occurred: {e}")

