# /// script
# dependencies = [
#     "requests<2.30",
# ]
# ///
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__, "status:", r.status_code)
