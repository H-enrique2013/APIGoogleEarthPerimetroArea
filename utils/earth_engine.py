import ee
import os
import json


import os
import json
import ee

def init_earth_engine():
    raw = os.getenv("GEE_CREDENTIALS_JSON")
    if not raw:
        raise ValueError("La variable de entorno GEE_CREDENTIALS_JSON no está definida.")
    
    # Primera carga (para quitar comillas escapadas)
    cleaned = json.loads(raw)

    # Segunda carga (para convertir a dict)
    creds = json.loads(cleaned)

    credentials = ee.ServiceAccountCredentials(creds["client_email"], key_data=creds)
    ee.Initialize(credentials)
    print("✅ Earth Engine inicializado correctamente.")

    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''