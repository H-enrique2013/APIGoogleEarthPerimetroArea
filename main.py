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
    data = request.get_json()
    start = data.get('startDate')
    end = data.get('endDate')
    index = data.get('index')

    collection = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterDate(start, end) \
        .median()

    if index == 'NDVI':
        ndvi = collection.normalizedDifference(['B8', 'B4']).rename('NDVI')
        image = ndvi.visualize(min=0, max=1, palette=['white', 'green'])
    else:
        image = collection.visualize(min=0, max=3000, bands=['B4', 'B3', 'B2'])

    map_id_dict = image.getMapId()
    return jsonify(map_id_dict)

'''   
@app.route('/CalculoAreaGEE', methods=['POST'])
def calcular_area():
    try:
        geojson = request.get_json()
        if not geojson:
            return jsonify({"error": "GeoJSON no proporcionado"}), 400

        geometry = ee.Geometry(geojson["features"][0]["geometry"])
        area_m2 = geometry.area().getInfo()
        area_ha = area_m2 / 10000

        return jsonify({
            "area_m2": round(area_m2, 2),
            "area_ha": round(area_ha, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

@app.route('/CalculoAreaNDVIPerimetro', methods=['POST'])
def calcular_ndvi_area_perimetro():
    try:
        geojson = request.get_json()
        if not geojson:
            return jsonify({"error": "GeoJSON no proporcionado"}), 400
            
        geometry = ee.Geometry(feature['geometry'])
        geometry = ee.Geometry(geojson["features"][0]["geometry"])

        # Cálculo área y perímetro
        area_ha = geometry.area().divide(10000)
        perimetro_m = geometry.perimeter()

        # NDVI promedio
        imagen = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(geometry) \
            .filterDate('2024-01-01', '2024-03-01') \
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
            'ndvi_promedio': ndvi_prom
        }).getInfo()

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/googleearthengineIcon.ico')
def favicon():
    return send_from_directory('static', 'googleearthengineIcon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

