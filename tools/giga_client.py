import os
import uuid

import requests
import urllib3
from dotenv import load_dotenv

load_dotenv()

OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")
SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token() -> str:
    if not AUTH_KEY:
        raise Exception("GIGACHAT_AUTH_KEY not set in environment")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {AUTH_KEY}",
    }
    data = {
        "scope": SCOPE,
    }

    resp = requests.post(
        OAUTH_URL, headers=headers, data=data, timeout=10, verify=False
    )
    resp.raise_for_status()
    body = resp.json()

    token = body.get("access_token")
    if not token:
        raise Exception(f"No access_token in response: {body}")

    return token


def chat_completion(prompt: str, access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Client-ID": "pytest-smoke",
        "X-Request-ID": str(uuid.uuid4()),
    }

    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
    }

    resp = requests.post(
        CHAT_URL, headers=headers, json=payload, timeout=30, verify=False
    )
    resp.raise_for_status()
    return resp.json()


def chat_completion_raw(payload: dict, access_token: str) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Client-ID": "pytest-smoke",
        "X-Request-ID": str(uuid.uuid4()),
    }

    resp = requests.post(
        CHAT_URL, headers=headers, json=payload, timeout=30, verify=False
    )
    return resp
