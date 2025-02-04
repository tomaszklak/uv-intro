# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version, "version:", requests.__version__, "status:", r.status_code)
