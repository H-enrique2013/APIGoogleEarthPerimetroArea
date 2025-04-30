import ee
import os
import json


def init_earth_engine():
    creds_json = os.getenv("GEE_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError("No se encontró la variable de entorno GEE_CREDENTIALS_JSON")

    # Guardar las credenciales como archivo temporal
    cred_path = "service_account.json"
    with open(cred_path, "w") as f:
        f.write(creds_json)

    # Leer el email desde el archivo ya guardado
    with open(cred_path) as f:
        creds_dict = json.load(f)

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