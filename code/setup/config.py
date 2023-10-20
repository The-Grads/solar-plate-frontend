from decouple import config


class Config(object):
    API_URL = config('API_URL', default="http://app:5000")