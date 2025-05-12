from flask import Flask, request, jsonify
from flask_cors import CORS
from model import sectorEstadistico
import json
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
def getMapId():
    data = request.get_json()
    try:
        dep = data.get('departamento')
        prov = data.get('provincia')
        distr = data.get('distrito')
        sector = data.get('sector')
        psatelite = data.get('satelite')
        pfechaInicio = data.get('fechaInicio')
        pfechaFin = data.get('fechaFin')
        index = data.get('indice')
        pnubosidad = float(data.get('porcentajeNubosidad'))

        # Validación de entradas
        if not all([psatelite, pfechaInicio, pfechaFin, index, dep, prov, distr, sector]):
            return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

        # Leer shapefile y filtrar por sector
        gdf_filtrado = sectorEstadistico(dep, prov, distr, sector)
        
        if gdf_filtrado.empty:
            return jsonify({'error': 'No se encontró el polígono para los parámetros proporcionados'}), 400

        poligono_geojson = gdf_filtrado.iloc[0].geometry.__geo_interface__
        roi = ee.Geometry(poligono_geojson)

        # Selección de colección
        def get_collection(sat):
            if sat == 'Sentinel-2':
                return (ee.ImageCollection('COPERNICUS/S2_SR')
                        .filterBounds(roi)
                        .filterDate(pfechaInicio, pfechaFin)
                        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', pnubosidad)))
            elif sat in ['Landsat-8', 'Landsat-9']:
                landsat_id = 'LANDSAT/LC08/C02/T1_L2' if sat == 'Landsat-8' else 'LANDSAT/LC09/C02/T1_L2'
                return (ee.ImageCollection(landsat_id)
                        .filterBounds(roi)
                        .filterDate(pfechaInicio, pfechaFin)
                        .filter(ee.Filter.lt('CLOUD_COVER', pnubosidad)))
            else:
                return None

        collection = get_collection(psatelite)
        if collection is None:
            return jsonify({'error': 'Satélite no válido'}), 400

        if collection.size().getInfo() == 0:
            return jsonify({'error': 'No hay imágenes disponibles para los parámetros seleccionados'}), 400

        #image = collection.sort('system:time_start', False).first().clip(roi)
        image = collection.median().clip(roi)

        # Aplicar escala para Landsat
        if psatelite in ['Landsat-8', 'Landsat-9']:
            image = image.multiply(0.0000275).subtract(0.2)

        # Cálculo de índices
        def calcular_indice(img, idx, sat):
            if idx == 'NDVI':
                return img.normalizedDifference(['B8', 'B4']) if sat == 'Sentinel-2' else \
                       img.normalizedDifference(['SR_B5', 'SR_B4'])
            elif idx == 'NDWI':
                return img.normalizedDifference(['B3', 'B8']) if sat == 'Sentinel-2' else \
                       img.normalizedDifference(['SR_B3', 'SR_B5'])
            elif idx == 'NDBI':
                return img.normalizedDifference(['B11', 'B8']) if sat == 'Sentinel-2' else \
                       img.normalizedDifference(['SR_B6', 'SR_B5'])
            elif idx == 'EVI':
                if sat == 'Sentinel-2':
                    nir = img.select('B8')
                    red = img.select('B4')
                    blue = img.select('B2')
                else:
                    nir = img.select('SR_B5')
                    red = img.select('SR_B4')
                    blue = img.select('SR_B2')
                return img.expression(
                    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                    {'NIR': nir, 'RED': red, 'BLUE': blue}
                )
            elif idx == 'RGB':
                return img.select(['B4', 'B3', 'B2']) if sat == 'Sentinel-2' else \
                       img.select(['SR_B4', 'SR_B3', 'SR_B2'])
            else:
                return None

        index_img = calcular_indice(image, index, psatelite)
        if index_img is None:
            return jsonify({'error': 'Índice no reconocido'}), 400

        if index == 'NDVI':
            vis_params = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
        elif index == 'NDWI':
            vis_params = {'min': -1, 'max': 1, 'palette': ['brown', 'white', 'cyan']}
        elif index == 'NDBI':
            vis_params = {'min': -1, 'max': 1, 'palette': ['purple', 'white', 'orange']}
        elif index == 'EVI':
            vis_params = {'min': -1, 'max': 1, 'palette': ['red', 'white', 'darkgreen']}
        elif index == 'RGB':
            vis_params = {}
        else:
            vis_params = {'min': -1, 'max': 1}

        map_id_dict = ee.Image(index_img).getMapId(vis_params)

        return jsonify({
            'tile_url': map_id_dict['tile_fetcher'].url_format,
            'idindex': index + " (GEE)"
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

@app.route('/SectorEstadistico', methods=['POST'])
def sector_estadistico():
    try:
        data=request.get_json()
        dep=data.get('Departamento')
        prov=data.get('Provincia')
        distr=data.get('Distrito')
        sector=data.get('Sector')
        if not all([dep,prov,distr,sector]):
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        gdf = sectorEstadistico(dep, prov, distr, sector)  # devuelve GeoDataFrame
        solo_geom = gdf[['geometry']]  # <-- solo geometría
        geojson_str = solo_geom.to_json()
        return jsonify(json.loads(geojson_str))

    except Exception as e:
        return jsonify({'error':str(e)}),500


@app.route('/googleearthengineIcon.ico')
def favicon():
    return send_from_directory('static', 'googleearthengineIcon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

