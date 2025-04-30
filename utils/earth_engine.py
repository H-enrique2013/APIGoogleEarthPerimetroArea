import ee
import os
import json


def init_earth_engine():
    creds_json = os.getenv("GEE_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError("No se encontró la variable de entorno GEE_CREDENTIALS_JSON")

    try:
        # Desescapar texto si viene con \\n
        creds_unescaped = bytes(creds_json, "utf-8").decode("unicode_escape")
        creds_dict = json.loads(creds_unescaped)
    except Exception as e:
        raise ValueError(f"Error procesando GEE_CREDENTIALS_JSON: {e}")

    # Guardar archivo temporal para autenticar
    cred_path = "service_account.json"
    with open(cred_path, "w") as f:
        json.dump(creds_dict, f)

    service_account = creds_dict["client_email"]
    credentials = ee.ServiceAccountCredentials(service_account, cred_path)
    ee.Initialize(credentials)
    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''