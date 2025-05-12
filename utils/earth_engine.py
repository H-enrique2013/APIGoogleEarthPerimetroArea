import ee
import os
import json


def init_earth_engine():
    credentials_json = os.environ.get("GEE_CREDENTIALS_JSON")

    if not credentials_json:
        raise ValueError("Falta GEE_CREDENTIALS_JSON")

    # Primer loads convierte el string escapado a un JSON real
    try:
        actual_json = json.loads(credentials_json)
    except Exception as e:
        raise ValueError("JSON de GEE_CREDENTIALS_JSON malformado") from e

    credentials = ee.ServiceAccountCredentials(
        actual_json["client_email"],
        key_data=json.dumps(actual_json)  # ahora el dict se vuelve a convertir a string para key_data
    )

    ee.Initialize(credentials)
    
''' 
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
''' 