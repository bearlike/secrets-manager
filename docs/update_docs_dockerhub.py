#!/usr/bin/env python3

import requests
import sys
from dotenv import load_dotenv
import os

load_dotenv()


def check_code(req, data=None, allow=[]):
    if req.status_code != 200 and req.status_code not in allow:
        if data is not None:
            if "login_2fa_token" in data.keys():
                data["login_2fa_token"] = "<redacted>"
            print(f"sent_data={data}")
        json = req.json()
        print(f"code={req.status_code}, json={json}")
        # print(f"headers={req.request.headers}")
        sys.exit(-1)


def main():
    host = "https://hub.docker.com"
    # Login
    url = f"{host}/v2/users/login?refresh_token=true"
    data = {
        "username": os.environ.get("DOCKERHUB_USERNAME"),
        "password": os.environ.get("DOCKERHUB_PASSWORD")
    }
    token_2fa_req = requests.post(url, data)
    check_code(token_2fa_req, allow=[401])
    login_2fa_token = token_2fa_req.json()['login_2fa_token']

    # Second factor authentication
    url = f"{host}/v2/users/2fa-login?refresh_token=true"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    fa_code = str(input("Enter your 2FA key: "))
    data = {
        "login_2fa_token": login_2fa_token,
        "code": fa_code
    }
    token_req = requests.post(url, data, headers=headers)
    check_code(token_req, data=data)
    TOKEN = token_req.json()['token']

    # update docs
    namespace, repository = "krishnaalagiri", "apitest"
    url = f"{host}/v2/repositories/{namespace}/{repository}/"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    docker_desc = open("docs\\README_dockerhub.md", "r").read()
    data = {
        "full_description": docker_desc,
    }
    update_req = requests.post(url, data, headers=headers)
    check_code(update_req)
    print(update_req.json())


if __name__ == "__main__":
    main()
