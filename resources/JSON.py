#  http://20.197.0.180/

import requests

auth_resp = requests.post("http://20.197.0.180/api/auth/", json={ "email": "kane@gmail.com", "password": "plain8435" })

if auth_resp.status_code == 200:
    print(auth_resp.json())
    headers = {
        "Authorization": f"Token {auth_resp.json()['token']}"
    }
    resp = requests.get("http://20.197.0.180/api/employee/view/employee/", headers=headers)
    print(resp.json())
else:
    print(auth_resp.json())

