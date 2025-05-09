import geopandas as gpd
import os

def RutaShape(dep):
    
    dicdep={
          
            "APURIMAC":['shapefiles/03_APURIMAC_SectoresEstadisticos.shp',
                        'shapefiles/03_APURIMAC_SuperficieAgricola.shp',
                        'shapefiles/Centros Poblados Apurimac.shp',
                        'shapefiles/Curvas de Nivel Apurimac.shp',
                        'shapefiles/Dep Apurimac.shp',
                        'shapefiles/Rios Apurimac.shp',
                        'shapefiles/Trocha y Camino Apurimac.shp'],
            
            "AYACUCHO":['shapefiles/05_AYACUCHO_SectoresEstadisticos.shp',
                        'shapefiles/05_AYACUCHO_SuperficieAgricola.shp',
                        'shapefiles/Centros Poblados Ayacucho.shp',
                        'shapefiles/Curvas de Nivel Ayacucho.shp',
                        'shapefiles/Dep Ayacucho.shp',
                        'shapefiles/Rios Ayacucho.shp',
                        'shapefiles/Trocha y Camino Ayacucho.shp'
                        ],
            
            "HUANCAVELICA":['shapefiles/09_HUANCAVELICA_SectoresEstadisticos.shp',
                            'shapefiles/09_HUANCAVELICA_SuperficieAgricola.shp',
                            'shapefiles/Centros Poblados Huancavelica.shp',
                            'shapefiles/Curvas de Nivel Huancavelica.shp',
                            'shapefiles/Dep Huancavelica.shp',
                            'shapefiles/Rios Huancavelica.shp',
                            'shapefiles/Trocha y Camino Huancavelica.shp'
                            ],
            
            "MADRE DE DIOS":['shapefiles/17_MADRE_DE_DIOS_SectoresEstadisticos.shp',
                             'shapefiles/17_MADRE_DE_DIOS_SuperficieAgricola.shp',
                             'shapefiles/Centros Poblados Madre de Dios.shp',
                             'shapefiles/Curvas de Nivel Madre de Dios.shp',
                             'shapefiles/Dep Madre de Dios.shp',
                             'shapefiles/Rios Madre de Dios.shp',
                             'shapefiles/Trocha y Camino Madre de Dios.shp'
                             ],
            
            "MOQUEGUA":['shapefiles/18_MOQUEGUA_SectoresEstadisticos.shp',
                        'shapefiles/18_MOQUEGUA_SuperficieAgricola.shp',
                        'shapefiles/Centros Poblados Moquegua.shp',
                        'shapefiles/Curvas de Nivel Moquegua.shp',
                        'shapefiles/Dep Moquegua.shp',
                        'shapefiles/Rios Moquegua.shp',
                        'shapefiles/Trocha y Camino Moquegua.shp'
                        ],

            "PUNO":['shapefiles/21_PUNO_SectoresEstadisticos.shp',
                    'shapefiles/21_PUNO_SuperficieAgricola.shp',
                    'shapefiles/Centros Poblados Puno.shp',
                    'shapefiles/Curvas de Nivel Puno.shp',
                    'shapefiles/Dep Puno.shp',
                    'shapefiles/Rios Puno.shp',
                    'shapefiles/Trocha y Camino Puno.shp'
                    ],

            "TACNA":['shapefiles/23_TACNA_SectoresEstadisticos.shp',
                     'shapefiles/23_TACNA_SuperficieAgricola.shp',
                     'shapefiles/Centros Poblados Tacna.shp',
                     'shapefiles/Curvas de Nivel Tacna.shp',
                     'shapefiles/Dep Tacna.shp',
                     'shapefiles/Rios Tacna.shp',
                     'shapefiles/Trocha y Camino Tacna.shp'
                     ],

            "TUMBES":['shapefiles/24_TUMBES_SectoresEstadisticos.shp',
                      'shapefiles/24_TUMBES_SuperficieAgricola.shp',
                      'shapefiles/Centros Poblados Tumbes.shp',
                      'shapefiles/Curvas de Nivel Tumbes.shp',
                      'shapefiles/Dep Tumbes.shp',
                      'shapefiles/Rios Tumbes.shp',
                      'shapefiles/Trocha y Camino Tumbes.shp'
                      ],

            "CUSCO":['shapefiles/08_CUSCO_SectoresEstadisticos.shp',
                      'shapefiles/08_CUSCO_SuperficieAgricola.shp',
                      'shapefiles/Centros Poblados Cusco.shp',
                      'shapefiles/Curvas de Nivel Cusco.shp',
                      'shapefiles/Dep Cusco.shp',
                      'shapefiles/Rios Cusco.shp',
                      'shapefiles/Trocha y Camino Cusco.shp'
                     ],

             "LORETO":['shapefiles/16_LORETO_SectoresEstadisticos.shp',
                      'shapefiles/16_LORETO_SuperficieAgricola.shp',
                      'shapefiles/Centros Poblados Loreto.shp',
                      'shapefiles/Curvas de Nivel Loreto.shp',
                      'shapefiles/Dep Loreto.shp',
                      'shapefiles/Rios Loreto.shp',
                      'shapefiles/Trocha y Camino Loreto.shp'
                      ],

             "PASCO":['shapefiles/19_PASCO_SectoresEstadisticos.shp',
                      'shapefiles/19_PASCO_SuperficieAgricola.shp',
                      'shapefiles/Centros Poblados Pasco.shp',
                      'shapefiles/Curvas de Nivel Pasco.shp',
                      'shapefiles/Dep Pasco.shp',
                      'shapefiles/Rios Pasco.shp',
                      'shapefiles/Trocha y Camino Pasco.shp'
                      ]
                      
        }
    
    return dicdep[dep]


def sectorEstadistico(dep,prov,distr,sector):
        dic_url=RutaShape(dep)
        url=dic_url[0]
        path_map=os.path.join(url)
        if not os.path.exists(path_map):
                print("Contenido de la carpeta 'shape':", os.listdir('shape'))
                raise ValueError(f"No se encontraron archivos en la ruta '{path_map}'")
        
        shape_sector=gpd.read_file(path_map)
        sect_estadistico = shape_sector[
        (shape_sector['NOMBDEP'] == dep) &
        (shape_sector['NOMBPROV'] == prov) &
        (shape_sector['NOMBDIST'] == distr) &
        (shape_sector['NOM_SE'] == sector)
        ]
        return sect_estadistico

#valor=sectorEstadistico('PUNO','LAMPA','PALCA','CHULLUNQUIANI')

#print(valor)
#print('-------------------------')
#print(type(valor[['geometry']]))

