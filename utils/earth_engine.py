import ee


def init_earth_engine():
    creds_json = os.environ.get("CREDENTIALS_JSON")
    if not creds_json:
        raise Exception("Variable de entorno 'CREDENTIALS_JSON' no definida")

    # Guardar temporalmente el contenido para inicializar EE
    with open("/tmp/credentials.json", "w") as f:
        f.write(creds_json)

    creds_dict = json.loads(creds_json)
    credentials = ee.ServiceAccountCredentials(
        email=creds_dict["client_email"],
        key_file="/tmp/credentials.json"
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