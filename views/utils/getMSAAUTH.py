from views.utils.getLiveData import getLiveData
from views.utils.getCookies import getCookies
import requests
import random
import string

# Gets __Host-MSAAUTH
def getMSAAUTH(email: str, flowToken: str, code: str= None):
    data = getLiveData() # [UrlPost, ppft, cookies]
    
    if flowToken is not None:
        loginData = requests.post(
            url = data["urlPost"],
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            cookies = data["cookies"],
            data={
                "login": email,
                "loginfmt": email,
                "slk": flowToken,
                "psRNGCSLK": flowToken,
                "type": "21",
                "PPFT": data["ppft"]
            }
        )

    elif code:
        
        cookies = ""
        set_cookie_headers = response.headers.get('set-cookie')
        if set_cookie_headers:
            for cookie_header in set_cookie_headers.split(','):
                cookies += cookie_header.split(";")[0] + "; "

        loginData = requests.post(
            url = data["urlPost"],
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": data["cookies"]
            },
            data={
                "login": email,
                "loginfmt": email,
                "SentProofIDE" : flowToken,
                "otc": code,
                "type": "27",
                "PPFT": data["ppft"]
            }
        )

    print(loginData.headers)
    if "__Host-MSAAUTH" in loginData.cookies:
        MSAAUTH = loginData.cookies["__Host-MSAAUTH"]
        print(f"MSAAUTH Cookie: {MSAAUTH}")
    else:
        print("Failed to retrieve MSAAUTH cookie.")
        print(loginData.headers)

    polish = requests.post(
        url = "https://login.live.com/ppsecure/post.srf?uaid=c81c108c53b249209366161b56d8122b&pid=0&opid=C0104E8D0A7E348F&route=C532_SN1",
        headers = {
            "Cookie" : f"__Host-MSAAUTH={MSAAUTH}",
        },
        allow_redirects = False
    )

    if 200 <= loginData.status_code < 400:
        return MSAAUTH
    else:
        return None