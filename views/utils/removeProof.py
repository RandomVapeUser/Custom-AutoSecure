import requests

def removeProof(amrp: str, apicanary: str, amsc: str, proofID: str):

    remove = requests.post(
        "https://account.live.com/API/Proofs/DeleteProof",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
            "canary": apicanary
        },
        data = {
            "proofId": proofID,
            "uiflvr": 1001,
            "uaid": "da90e97a55cf431385e2dd217c6ba873",
            "scid": 100109,
            "hpgid": 201030
        },
    )

    print(remove.headers)
    print(remove.cookies)
    print(remove.text)

    