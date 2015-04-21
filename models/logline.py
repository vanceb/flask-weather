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
        'light': int,
        'battery': int,
        'solar': int
    }
    display_fields = ['logtime', 'inT1', 'inT2', 'inT3', 'outT', 'pressure', 'humidity', 'light', 'battery', 'solar']
    field_names = ['Time', "Internal Temp 1 (C)", "Internal Temp 2 (C)", "Internal Temp 3 (C)", "External Temp (C)", "Atmospheric Pressure (mb)", "Humidity (%)", "Ambient Light", "Battery Voltage", "Solar Voltage"]
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

