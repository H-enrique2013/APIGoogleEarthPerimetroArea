import ee
import os
import json


import os
import json
import ee

def init_earth_engine():
    # Cargar la variable de entorno como string JSON
    credentials_json = os.environ.get("GEE_CREDENTIALS_JSON")

    if not credentials_json:
        raise ValueError("La variable de entorno GEE_CREDENTIALS_JSON no está definida")

    # Convertir el string JSON a dict
    creds = json.loads(credentials_json)

    # Autenticarse con Earth Engine usando la cuenta de servicio
    credentials = ee.ServiceAccountCredentials(creds["client_email"], key_data=credentials_json)

    # Inicializar Earth Engine con esas credenciales
    ee.Initialize(credentials)

    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''