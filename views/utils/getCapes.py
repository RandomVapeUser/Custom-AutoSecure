import requests

def getCapes() :

    ssid = "eyJraWQiOiIwNDkxODEiLCJhbGciOiJSUzI1NiJ9.eeyJ4dWlkIjoiMjUzNTQ0MTMxNTgxNjk3OSIsImFnZyI6IkFkdWx0Iiwic3ViIjoiYWE0ZWU3MzMtMjUyYy00MTFjLWI1NTktNDIyNmQwOTdlZjA0IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsibWluZWNyYWZ0X25ldCIsIm9yZGVyc18yMDIyIiwidHdvZmFjdG9yYXV0aCIsIm11bHRpcGxheWVyIiwibXNhbWlncmF0aW9uX3N0YWdlNCJdLCJwcm9maWxlcyI6eyJtYyI6IjUyMWIxNzUwLTU3NjUtNGY5Zi04M2YzLWJjMTllMjA2ZDM1NyJ9LCJwbGF0Zm9ybSI6IldFQiIsInBmZCI6W3sidHlwZSI6Im1jIiwiaWQiOiI1MjFiMTc1MC01NzY1LTRmOWYtODNmMy1iYzE5ZTIwNmQzNTciLCJuYW1lIjoiRmVtYm95S2l0dGVuU2FsIn1dLCJuYmYiOjE3NjQxMDAyMDQsImV4cCI6MTc2NDE4NjYwNCwiaWF0IjoxNzY0MTAwMjA0LCJhaWQiOiI3ZDVjODQzYi1mZTI2LTQ1ZjctOTA3My1iNjgzYjJhYzdlYzMifQ.b443Rm_B3sMBuua0q4LrPZbnc5gPfWJyBfQq96d9EVq1SqDrhMWAGTbVIPvRsoEHLUtapmKXgneUWeiOPEHnnoKWKAoXWFLnjNcKtCvJwba4PfuHVVjHtkAybx3F_frnrlcaPc1UiDec47ySHJH1fFwvS7pHjlOozeTLsmOJQAOucN4hbNFH50cgA1Yi6qTp-KtAC9c01SSSQfqFFE6UIWtZ3gsU8DxqCjFKv5kKOdsaBB3EPoKHJCJuquTBO10kVkc9dVNc38VAl9O2Oc7e7vHeIroQwChfo9Vb9O0Y7h-bC7ykDV6yHhBozZeDYyES42_wXG1w72qVUciQ1jLDhA"
    response = requests.get(
        url = "https://api.minecraftservices.com/minecraft/profile",
        headers = {
            "Authorization": f"Bearer {ssid}"
        }
    )

    if "capes" in response.json():
        return response.json()["capes"]
    else:
        return None