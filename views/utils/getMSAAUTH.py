from views.utils.getLiveData import getLiveData
from views.utils.getCookies import getCookies
import requests
import random
import string

# Generate random SentProofIDE
def generateId(length = 8):
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    val = random.choice(string.ascii_lowercase)

    for _ in range(1, length):
        ret_val += random.choice(charset)

    return val

# Gets __Host-MSAAUTH
def getMSAAUTH(email: str, flowToken: str = None, code: str= None):
    data = getLiveData() # [UrlPost, ppft, cookies]
    
    if flowToken is not None:
        loginData = requests.post(
            url=data["urlPost"],
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
    
        randomId = generateId(33)
        loginData = requests.post(
            url=data["urlPost"],
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": data["cookies"]
            },
            data={
                "login": email,
                "loginfmt": email,
                "SentProofIDE" : randomId,
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

    if 200 <= polish.status_code < 400:
        return MSAAUTH
    else:
        return None