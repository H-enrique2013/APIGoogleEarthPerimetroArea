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


@app.route('/googleearthengineIcon.ico')
def favicon():
    return send_from_directory('static', 'googleearthengineIcon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

