from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.earth_engine import init_earth_engine
import ee

app = Flask(__name__)
CORS(app)  # Permite a todos los orígenes
# Inicializar Earth Engine al arrancar la app
init_earth_engine()
@app.route("/")
def hello():
    return "API Flask con Earth Engine"


@app.route('/getMapId', methods=['POST'])
def get_map_id():
    try:
        data = request.get_json()
        start = data.get('startDate')
        end = data.get('endDate')
        index = data.get('index')

        collection = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(start, end).median()

        if index == 'NDVI':
            ndvi = collection.normalizedDifference(['B8', 'B4']).rename('NDVI')
            vis_params = {'min': 0, 'max': 1, 'palette': ['white', 'green']}
            image = ndvi.visualize(**vis_params)
        else:
            vis_params = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}
            image = collection.visualize(**vis_params)

        map_id = ee.data.getMapId({'image': image})

        # Extraer solo los datos serializables
        return jsonify({
            'mapid': map_id['mapid'],
            'token': map_id['token']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/CalculoAreaNDVIPerimetro', methods=['POST'])
def calcular_ndvi_area_perimetro():
    try:
        geojson = request.get_json()
        if not geojson or "features" not in geojson or len(geojson["features"]) == 0:
            return jsonify({"error": "GeoJSON no proporcionado o inválido"}), 400

        geometry = ee.Geometry(geojson["features"][0]["geometry"])

        # Cálculo área y perímetro
        area_ha = geometry.area().divide(10000)
        perimetro_m = geometry.perimeter()
        # Cálculo del centroide
        centroide = geometry.centroid()
        centroide_coords = centroide.coordinates().getInfo()
        centroide_text = f"{centroide_coords[1]},{centroide_coords[0]}"  # Lat,Lon

        # NDVI promedio
        imagen = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(geometry) \
            .filterDate('2024-01-01', '2024-03-01') \
            .select(['B4', 'B8']) \
            .median()

     
        ndvi = imagen.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndvi_prom = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10,
            maxPixels=1e9
        ).get('NDVI')

        resultado = ee.Dictionary({
            'area_ha': area_ha,
            'perimetro_m': perimetro_m,
            'ndvi_promedio': ndvi_prom,
            'centroide_text':centroide_text
        }).getInfo()

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/googleearthengineIcon.ico')
def favicon():
    return send_from_directory('static', 'googleearthengineIcon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

