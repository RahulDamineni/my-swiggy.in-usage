import requests
import logging
import random
import json
import sys

logging.basicConfig(
    filename='app.log',
    filemode='w',
)


session_headers = {
    "Host": "www.swiggy.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.swiggy.com/my-account/orders",
    "Content-Type": "application/json",
    "__fetch_req__": "true",
    "Connection": "keep-alive",
    "Cookie": "__SW=a78CmkM9ny0ZSxRPd131lmQ0iLxp8iUT; _device_id=54835a47-c695-4ba4-b4e6-4f31dc8f69d4; _sid=fx5de04a-e050-4437-b89f-89547b489a59; visid_incap_1554223=Nlvf77NHT/aJ0FX0Re8+UYNh1VwAAAAAQUIPAAAAAAAJPuWPpzg+I4uxXcwUz78z; nlbi_1554223=WMAEH4o3YVivztQPo1DVjgAAAAA4H3U2MJV2j3Yv31bdpsHC; incap_ses_974_1554223=KrdHBx4IQBZcF2vih1iEDYNh1VwAAAAAg3lQF/H1d9ChrhM4BIN3iw==; _gcl_au=1.1.1835890805.1557488005; _ga=GA1.2.1201998732.1557488006; _gid=GA1.2.380177314.1557488006; fontsLoaded=1;" "_is_logged_in=1; _session_tid=b920341899981a11a112bd5a90415553881f436f1dda15ac065f7ad12f42eb010827b5d534dbd50184e0e51815ed66c81d375c92c38f6c58dff856553a09689f7d8ca0d18cba46544b9abbdd0881308c7ed7e030d481a06188879416e13d53ab2bd09775ca731a6faffad4b399e32649; customer_city=bangalore; adl=true;" '''userLocation={%22address%22:%2217th%20D%20Main%20Rd%2C%20KHB%20Block%20Koramangala%2C%205th%20Block%2C%20Koramangala%2C%20Bengaluru%2C%20Karnataka%20560047%2C%20India%22%2C%22area%22:%22Koramangala%22%2C%22id%22:%2213389814%22%2C%22lat%22:%2212.935756%22%2C%22lng%22:%2277.619047%22}; _gat_UA-53591212-4=1s'''
}

status_code = 200
latest_order_id = 40545448658
from_order_id = latest_order_id
all_orders = []
while status_code == 200:

    endpoint = f'https://www.swiggy.com/dapi/order/all?order_id={from_order_id}'
    try:
        response = requests.get(endpoint, headers=session_headers)
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

    try:
        status_code = response.status_code
        orders = response.json()["data"]["orders"]
        from_order_id = orders[-1]["order_id"]
        all_orders += orders
    except KeyError as e:
        logging.exception("Looks like we've reached the end of the history. Exiting", e)
        sys.exit(0)

    with open("all_orders.json", "w+") as out:
        json.dump(fp=out, obj=all_orders)
    print(f'Dumped {len(all_orders)} orders so far...')
