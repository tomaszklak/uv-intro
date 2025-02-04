import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version, "requests:", requests.__version__, "status:", r.status_code)
