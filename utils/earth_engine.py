import ee
import os
import json


def init_earth_engine():
    creds_json = os.getenv("GEE_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError("No se encontró la variable de entorno GEE_CREDENTIALS_JSON")

    try:
        # Esto es suficiente si ya pegaste el JSON con comillas escapadas desde Render
        creds_dict = json.loads(creds_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decodificando el JSON de GEE_CREDENTIALS_JSON: {e}")

    cred_path = "service_account.json"
    with open(cred_path, "w") as f:
        json.dump(creds_dict, f)

    service_account = creds_dict["client_email"]
    credentials = ee.ServiceAccountCredentials(service_account, cred_path)
    ee.Initialize(credentials)

    # Opcional: borrar el archivo
    # os.remove(cred_path)
    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''