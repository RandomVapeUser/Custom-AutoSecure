import requests
import re
import urllib.parse

def decode(code):
    decoded_url = urllib.parse.unquote(code)
    decoded_text = re.sub(
        r'\\u([0-9A-Fa-f]{4})',
        lambda match: chr(int(match.group(1), 16)),
        decoded_url
    )
    
    return decoded_text

def getCookies():
    canary = None
    apicanary = None
    amsc = None
    
    data = requests.get(
        url="https://account.live.com/password/reset",
        allow_redirects=False
    )
    
    apicanary = decode(re.search(r'"apiCanary":"([^"]+)"', data.text).group(1))
    canary = decode(re.search(r'"sCanary":"([^"]*)"', data.text).group(1))
    
    for cookie in data.cookies:
        if cookie.name == "amsc":
            amsc = cookie.value
            break
    
    return [canary, apicanary, amsc]