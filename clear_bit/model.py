import os
from urllib.error import HTTPError
import clearbit
from .serializers import PersonSerializer


class ClearBit:
    clearbit = None
    _key = None

    def __init__(self):
        self._set_key()

        # Checking availability
        if self.is_available():
            self.clearbit = clearbit
            self.clearbit.key = self._key

    def _set_key(self):
        # Getting key from .env
        self._key = os.getenv('CLEAR_BIT_KEY', None)

    def is_available(self):
        return True if self._key is not None else False

    def get_person_enrichment(self, email):
        if self.is_available() is False:
            return False

        # Catching problem for clearbit lib
        try:
            response = self.clearbit.Enrichment.find(email=email, stream=True)
        except HTTPError:
            return False
        except:
            return False

        if response['person'] is None:
            return False

        # Serializing data
        serializer = PersonSerializer(data=response['person'])
        serializer.is_valid(raise_exception=True)

        return serializer.data
