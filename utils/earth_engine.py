import ee
import os
import json


import os
import json
import ee

def init_earth_engine():
    # Obtener el JSON en texto
    credentials_json = os.environ.get("GEE_CREDENTIALS_JSON")

    if not credentials_json:
        raise ValueError("La variable GEE_CREDENTIALS_JSON no está definida")

    # Convertir el texto a diccionario
    creds_dict = json.loads(credentials_json)

    # Usar el texto como key_data y el email del dict
    credentials = ee.ServiceAccountCredentials(creds_dict["client_email"], key_data=credentials_json)

    # Inicializar EE con las credenciales
    ee.Initialize(credentials)

    
'''
def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)
'''