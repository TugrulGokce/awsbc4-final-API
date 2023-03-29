from Call_API import CallerAPI
import asyncio
import threading
import multiprocessing
import sys

caller = CallerAPI()
smarket = str(sys.argv[1])
if smarket in ["coinbase", "bitfinex", "gateio"]:
    if asyncio.run(caller.are_apis_available()):
        print("APIS are available.")
        while True:
            try:
                asyncio.run(caller.start_writing(smarket))
            except:
                pass
else:
    raise ValueError(f"Invalid stock market. You can use {smarket}")
