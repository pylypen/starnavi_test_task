import os
import requests


class EmailHunter:
    """
    Email Hunter Class for Verifying email
    """
    _key = None
    _valid_status = (
        'valid',
        'accept_all',
        'webmail'
    )
    _type_request = 'email-verifier?email='
    _url = 'https://api.hunter.io/v2/'

    def __init__(self, email):
        self._email = email
        self._set_key()

    def _set_key(self):
        # Getting key from .env
        self._key = os.getenv('EMAIL_HUNTER_KEY', None)

    def _generate_url(self):
        return f'{self._url}{self._type_request}{self._email}&api_key={self._key}'

    def is_available(self):
        # Checking Key
        return True if self._key is not None else False

    def email_verifier(self):
        # Getting url and response
        url = self._generate_url()
        response = requests.get(url).json()

        if response is None:
            return False

        # Catching errors
        # TODO add this info to logs
        if "errors" in response.keys():
            return True

        # Checking valid status
        if response['data']['status'] in self._valid_status:
            return True

        return False
