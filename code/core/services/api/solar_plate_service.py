import requests
from setup.config import Config
from typing import Tuple, Dict

class SolarPlateService:
    def getData(self, user_id: str) -> Dict:
        url = f"{Config.API_URL}/core/user/{id}"
    
        try:
            req = requests.get(url)
            response = req.json()
            
            return response
        except Exception as error:
            raise error
        