import ee
import os
import json


def init_earth_engine():
    credentials_json = os.environ.get("GEE_CREDENTIALS_JSON")

    if not credentials_json:
        raise ValueError("La variable de entorno GEE_CREDENTIALS_JSON no está definida.")

    try:
        creds_dict = json.loads(credentials_json)
    except json.JSONDecodeError as e:
        raise ValueError("Error al parsear las credenciales JSON") from e

    credentials = ee.ServiceAccountCredentials(
        creds_dict["client_email"],
        key_data=credentials_json  # Aquí sí debe ser el string original
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