import requests
from setup.config import Config
from typing import Tuple

class AuthService:
    def login(self, username: str, password: str) -> Tuple[str,str]:
        url = f"{Config.API_URL}/core/auth"
        data = {
            "username": username,
            "password": password
        }

        try:
            req = requests.post(url, data=data)
            response = req.json()
            return response["user_id"], response["access_token"]
        except Exception as error:
            raise error
        