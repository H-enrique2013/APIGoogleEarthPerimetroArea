from flask import Flask, request, jsonify
from utils.earth_engine import init_earth_engine
import ee

app = Flask(__name__)

# Inicializar Earth Engine al arrancar la app
init_earth_engine()

@app.route('/area', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
