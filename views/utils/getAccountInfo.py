import requests

def getAccountInfo(amrp: str, amsc: str):

    response = requests.get(
        "https://account.microsoft.com/profile/api/v1/personal-info",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
        }
    )

    print(response.text)