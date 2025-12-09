import requests

# Request might be timing out...?
def getAccountInfo(amrp: str, amsc: str):

    print("Getting Account Info")
    response = requests.get(
        "https://account.microsoft.com/home/api/profile/personal-info",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
            "canary": "no"
        }
    )
    print(response.status_code)
    print(response.text)