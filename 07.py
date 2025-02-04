#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
import requests
import sys
r = requests.get('https://nordvpn.com')
print("python:", sys.version, "requests:", requests.__version__, "status:", r.status_code)
