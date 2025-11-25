import requests
import base64
import json
import re

# Spamming this endpoint gets you ratelimited for 1~2 minutes
def getXBL(mssauth: str) -> dict:

    data = requests.get(
        url = "https://sisu.xboxlive.com/connect/XboxLive/?state=login&cobrandId=8058f65d-ce06-4c30-9559-473c9275a65d&tid=896928775&ru=https://www.minecraft.net/en-us/login&aid=1142970254",
        allow_redirects = False,
    )
    
    location = data.headers.get('Location')
    if not location:
        return None
    
    acessTokenRedirect = requests.get(
        url = location,
        headers = {
            "Cookie": f"__Host-MSAAUTH={mssauth}"
        },
        allow_redirects = False
    )

    location = acessTokenRedirect.headers.get('Location')
    if not location:
        return None
    
    accessTokenRedirect = requests.get(
        url = location,
        allow_redirects = False
    )

    # https://www.minecraft.net/en-us/login#state=login&accessToken=<token>
    location = accessTokenRedirect.headers.get('Location')
    if not location:
        return None
    
    token = re.search(r'accessToken=([^&#]+)', location)
    if not token:
        return None
    
    accessToken = token.group(1) + "=" * ((4 - len(token.group(1)) % 4) % 4)

    decoded_data = base64.b64decode(accessToken).decode('utf-8')
    json_data = json.loads(decoded_data)

    uhs = json_data[0].get('Item2',{}).get('DisplayClaims',{}).get('xui',[{}])[0].get('uhs')

    xsts = ""
    for item in json_data:
        if item.get('Item1') == "rp://api.minecraftservices.com/":
            xsts = item.get('Item2', {}).get('Token', '')
            break
        
    return {"xbl": f"XBL3.0 x={uhs};{xsts}"}