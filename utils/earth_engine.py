import ee
import os
import json


def init_earth_engine():
    creds_json = os.getenv("GEE_CREDENTIALS_JSON")  # Asegúrate que esté bien cargada
    if not creds_json:
        raise ValueError("No se encontró la variable de entorno GEE_CREDENTIALS_JSON")

    # Guardar temporalmente en archivo local
    with open("service_account.json", "w") as f:
        f.write(creds_json)

    # Inicializar Earth Engine con archivo
    service_account = json.loads(creds_json)["client_email"]
    credentials = ee.ServiceAccountCredentials(service_account, "service_account.json")
    ee.Initialize(credentials)
    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''