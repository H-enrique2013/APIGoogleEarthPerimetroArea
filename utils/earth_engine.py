import ee

def init_earth_engine():
    credentials = ee.ServiceAccountCredentials(
        email='earthengine-service@proyecto-areaperimetroearth.iam.gserviceaccount.com',
        key_file='service-account.json'
    )
    ee.Initialize(credentials)

