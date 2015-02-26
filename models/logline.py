from mongokit import Document
from datetime import datetime

class Logline(Document):
    __collection__ = 'logdata'
    __database__ = 'weather'
    structure = {
        'logtime': datetime,
        'inT1': float,
        'inT2': float,
        'inT3': float,
        'outT': float,
        'pressure': float,
        'humidity': float,
        'light': int
    }
    required_fields = ['logtime']
    default_values = {
        'logtime': datetime.utcnow
    }

class Temp(Document):
    __collection__ = 'logdata'
    __database__ = 'weather'
    structure = {'temp': float,
                 'logtime': datetime
                 }
    required_fields = ['logtime', 'temp']

