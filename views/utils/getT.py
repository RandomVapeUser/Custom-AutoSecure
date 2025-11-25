import requests

def getT(msaauth: str, amsc: str):

    fetchT = requests.get(
        url = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708978285&rver=7.5.2156.0&wp=SA_20MIN&wreply=https://account.live.com/proofs/Add?apt=2&uaid=0637740e739c48f6bf118445d579a786&lc=1033&id=38936&mkt=en-US&uaid=0637740e739c48f6bf118445d579a786",
        headers = {
            "cookie": f"__Host-MSAAUTH=${msaauth}; amsc=${amsc}"
        },
        allow_redirects = False
    )

    