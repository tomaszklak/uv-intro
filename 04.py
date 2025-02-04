# /// script
# dependencies = [
#     "requests",
# ]
# [tool.uv]
# exclude-newer = "2023-04-27T00:00:00Z"
# ///
import requests
r = requests.get('https://nordvpn.com')
print("requests:", requests.__version__, "status:", r.status_code)
