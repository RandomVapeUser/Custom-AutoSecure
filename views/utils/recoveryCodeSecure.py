import requests
import re

def recoveryCodeSecure(email: str, recoveryCode: str, new_email: str, new_password: str):
    
    data = requests.get(
        url = f"https://account.live.com/ResetPassword.aspx?wreply=https://login.live.com/oauth20_authorize.srf&mn={email}"
    )

    amsc = dict(data.cookies)["amsc"]
    match = re.search(r"var\s+ServerData=(.*?)(?=;|$)", data.text).group(1)

    print(match)

