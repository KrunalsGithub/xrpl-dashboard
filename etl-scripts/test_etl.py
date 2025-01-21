import pandas as pd
import numpy as np
import xrpl



 #Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://s2.ripple.com:51234/"
client = JsonRpcClient(JSON_RPC_URL)


