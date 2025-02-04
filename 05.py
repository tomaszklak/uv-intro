# /// script
# dependencies = [
#     "requests",
# ]
# ///
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__, "status:", r.status_code)
