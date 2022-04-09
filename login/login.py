from pathlib import Path
import json

from bs4 import BeautifulSoup

from constant import *


def login_times(session):
    username, password = get_login_detail()
    payload = {
        "username": username,
        "password": password,
        "rememberusername": "0",
        "anchor": "",
        "logintoken": "",
    }

    print("Logging in...")
    login_page = session.get(TIMES_LOGIN_URL)
    assert login_page.status_code == 200

    login_page_soup = BeautifulSoup(login_page.content, 'lxml')
    login_token = login_page_soup.find("input", {"name": "logintoken"})['value']
    payload['logintoken'] = login_token
    main_page = session.post(TIMES_LOGIN_URL, data=payload)

    # TODO: Need to handle login fail cases
    assert main_page.status_code == 200
    print("Login successful")

    return main_page

def get_login_detail():
    if not (PERSONAL_PATH).is_file():
        print("It looks like you are logining in for the first time.")
        print("Please provide your username and password information.")
        personal = dict()
        username = input("Username: ")
        password = input("Password: ")
        personal['username'] = username
        personal['password'] = password
        print("Your username and password will be stored in: " + str(PERSONAL_PATH))
        DATA_PATH.mkdir(parents=True, exist_ok=True)
        with open(PERSONAL_PATH, 'w') as f:
            json.dump(personal, f)

        return (username, password)

    else:
        with open(PERSONAL_PATH) as f:
            personal = json.load(f)
            username = personal['username']
            password = personal['password']

        return (username, password)
