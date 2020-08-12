# coding:utf-8

import requests


url = "https://auth.chegg.com/auth/_ajax/auth/v1/login"


headers = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
"origin": "https://www.chegg.com",
# "referer":" https://www.chegg.com/auth?type=simplifiedstudy&action=signup&data=sCS_P_control&redirect=%2Fcheckoutinterstitial%2Fhwh%2F%3Fredirect%3Dhwh%26command%3D1041%2Cb21f63d6-ffb1-3380-aad1-6df6dcff5d9f%2C1%2CNETSUITE",
}


data = { 
    "clientId": "CHGG",
    "email": "wolegequ9@gmail.com",
    "password": "myHAMB2020",
    "version": "2.121.22",
    "profileId": "CS_STREAMLINE",
}



http = requests.post(url=url, headers=headers, data=data)
print(http.status_code)
print(http.text)