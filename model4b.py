"""
Herramientas Computacionales para la Investigación - MAE UdeSA 2022
Tomás Pacheco y Abigail Riquelme
Comentarios sobre el modelo 4b
"""

# Comenzamos importando las librerías que se necesitarán para correrlo los diferentes programas.

from qgis.core import (QgsProcessing,QgsProcessingAlgorithm,QgsProcessingMultiStepFeedback,QgsProcessingParameterVectorDestination,QgsProcessingParameterFeatureSink)
import processing

# Ahora vamos a definir el directorio de trabajo y las direcciones a las carpetas dentro

main = ""
inputs = "{}/input".format(main)
output = "{}/output".format(main) 

# Definimos la clase para el modelo 4b

class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None): # Con esta primera función lo que se hace es definir los procesos del algoritmo, para este modelo son veintidos. 
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroid_nearest_coast_joined', 'centroid_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coord', 'centroids_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
    # Mediante la siguiente función se procesa el algoritmo. La función tiene como parámetros el nombre del algoritmo, 
    # los parámetros definidos anteriormente, el contexto en el que se ejecutará el algoritmo y feedback del modelo. 
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(22, model_feedback) # En el primer argumento de la función escribimos la cantidad de procesos del algoritmo. 
        # Definimos diccionarios en donde se ira guardando el output de los distintos procesos. 
        results = {}
        outputs = {}
        
        #########################################################
        # Unimos dos capas: "centroidsout" y "Nearest_cat_adjust" 
        # (join attributes by field value)
        #########################################################
        
        # Definimos los parámetros para poder unir las dos capas nombradas anteriormente. 
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': 'output_01aea043_d084_4fe1_9369_1dd1fbaec6e6',
            'INPUT_2': 'Remaining_fields_1f8c1a97_3f52_4089_ad1a_f921b07f30dd',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        # Aplicamos el proceso para así poder unir las dos capas, guardamos esto en los diccionarios creados. 
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_joined'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Eliminamos algunas variables de la base 
        # "Nearest_cat_adjust" (drop fields)
        #########################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  
        
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_0ceb76a4_3337_49c4_b49f_15bd60354bc3',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 91-95. 
        outputs['DropFieldsCat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsCat_adjust']['OUTPUT']
        
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Fix geometries para la base "countries"
        #########################################################
        
        # Necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se superpongan o que haya polígonos no cerrados.

        # Definimos diccionario con el input y output. 
        alg_params = {
            'INPUT': '{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp'.format(inputs),
            'OUTPUT': parameters['Fixgeo_countries']
        }
        
        # Aplicamos el proceso de corregir las geometrías y las guardamos en los diccionarios creados.
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Corregimos la variable "cat" (field calculator)
        #########################################################


        # Definimos el siguiente diccionario. 
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature,'cat')-1",
            'INPUT': 'from_output_98cdf641_8493_4249_80af_31033f187d00',
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        # Ahora aplicamos el proceso para calcular la cantidad de letras del nombre de cada idioma. Utilizamos como parámetro el diccionario definido 
        # anteriomente en las lineas 132-140. 
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Añadimos atributos geométricos a la capa "centroids" 
        # (add geometry attributes)
        #########################################################
        
        # Para usar esta herramienta tenemos que definir los parámetros, esto es lo que hacemos mediante el siguiente diccionario: 
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': 'Centroids_9d86384d_dcd8_4dad_a8eb_03c0471fd55f',
            'OUTPUT': parameters['Centroids_w_coord']
        }
        # Aplicamos el proceso y guardamos los outputs
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Añadimos atributos geométricos a la capa "geo coast" 
        # (add geometry attributes)
        #########################################################
        
        # Para usar esta herramienta tenemos que definir los parámetros, esto es lo que hacemos mediante el siguiente diccionario: 
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': 'Remaining_fields_9696b96a_c75c_4c94_a218_5873cd1792c3',
            'OUTPUT': parameters['Add_geo_coast']
        }
        # Aplicamos el proceso utilizando como componente el diccionario definido en las lineas 175-179 y guardamos los outputs.
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributes']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
       
        ##################################################################
        # Eliminamos algunas variables de la capa "centroids_coast_joined" 
        # (drop fields)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Joined_layer_657def29_79eb_47f5_acf7_dfb2e822e86a',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 196-200. 
        outputs['DropFieldsCentroids_coast_joined'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroids_coast_joined']['OUTPUT']
        
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
        
        ##################################################################
        # Eliminamos algunas variables de la capa "coast_lon" 
        # (drop fields)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_fd6de8a8_4baf_4c07_88a1_920472db8d05',
            'OUTPUT': '{}/csvout21.csv'.format(output),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 56-59. 
        outputs['DropFieldsCoast_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}
        
        ##################################################################
        # Eliminamos algunas variables de la capa "fixgeo_coast" 
        # (drop fields)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  

        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Fixed_geometries_fed85ab2_2d33_4700_9a59_b62765ea7fe3',
            'OUTPUT': parameters['Coastout']
        }
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 241-245. 
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']
        
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Fix geometries (capa "coast")
        #########################################################
        
        # Necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se superpongan o que haya polígonos no cerrados.

        # Definimos diccionario con el input y output. 

        alg_params = {
            'INPUT': '{}/ne_10m_coastline/ne_10m_coastline.shp'.format(inputs),
            'OUTPUT': parameters['Fixgeo_coast']
        }
        
        # Aplicamos el proceso de corregir las geometrías y las guardamos en los diccionarios creados.
        outputs['FixGeometriesCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['FixGeometriesCoast']['OUTPUT']
        
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Generamos una variable que contiene los centroides para 
        # cada uno de los países 
        #########################################################
        
        # Definimos el siguiente diccionario con los parámetros para poder generar los centroides de cada país. 
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'],
            'OUTPUT': parameters['Country_centroids']
        }
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']
        
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Generamos una variable igual a la coordenada "y"
        # de la capa "coast_land" (field calculator)
        #########################################################
        
        # Definimos el siguiente diccionario con los parámetros para poder duplicar la variable especificada anteriormente. 
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': 'Added_geom_info_d9997a05_e0bf_4ee5_b2d5_eb39a0cad0b7',
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['FieldCalculatorCoast_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorCoast_lat']['OUTPUT']
        
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Generamos una variable igual a la coordendana "x" 
        # de la capa "cent_lon" (field calculator)
        #########################################################

        # Definimos el siguiente diccionario con los parámetros para poder duplicar la variable especificada anteriormente. 
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cant_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': 'Calculated_95939d88_bbae_4878_bb41_bcf23527dd3d',
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}
 
        #########################################################
        # Extracción por atributo (nos quedamos con las 
        # observaciones para las cuales la distancia es 
        # estrictamente positiva)
        #########################################################

        # Definimos el siguiente diccionario con los parámetros para poder aplicar la herramienta.
        
        alg_params = {
            'FIELD': 'distance',
            'INPUT': 'Vertices_cd575656_1d01_4550_8cb8_6b46dfcd2ece',
            'OPERATOR': 2,  # >
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']
        
        # Indicamos que si ocurre algún tipo de error se suspenda el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}
        
        ##################################################################
        # Eliminamos algunas variables de la capa "centroids_w_coord"
        # (drop fields)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Added_geom_info_8c204278_878a_45f4_a90f_6ead7343aaf4',
            'OUTPUT': parameters['Centroidsout']
        }
        
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 56-59. 
        outputs['DropFieldsCentroids_w_coord'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coord']['OUTPUT']

        # A continuación indicamos que si ocurre algún tipo de error se suspenda el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        ##################################################################
        # Calculo de la distiancia del centroide al punto 
        # costero más cercado (v.distance)
        ##################################################################
        
        # Definimos el siguiente diccionario para así poder aplicar la herramiento que nos permita realizar el 
        # cálculo de la distancia del centroide al punto costero más cercano. 
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': 'Added_geom_info_8c204278_878a_45f4_a90f_6ead7343aaf4',
            'from_type': [0,1,3],  # point,line,area
            'to': 'Remaining_fields_8925a6b4_3b3e_44d1_b35f_83f3af2bdb12',
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.     
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        # Indicamos que si ocurre algún tipo de error se suspenda el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        #########################################################
        # Generamos una variable igual a la coordendana "x" 
        # de la capa "coast_lon" (field calculator)
        #########################################################

        # Definimos el siguiente diccionario con los parámetros para poder duplicar la variable especificada anteriormente. 
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': 'Calculated_48d195d8_aa09_4a18_921b_ba770264156c',
            'OUTPUT': parameters['Added_field_coast_lon']
        }
       
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']
        
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        ##################################################################
        # Eliminamos algunas variables de la capa "cent_lan_lon"
        # (drop fields)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  

        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculated_5f70e3b8_4982_44e5_aa03_7b5a8ce34931',
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['DropFieldsCen_lat_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['DropFieldsCen_lat_lon']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}
        
        
        ##################################################################
        # Realizamos el merge entre las capas ccentroids y coast 
        # según la variable "ISO_A3" (join attributes by field value)
        ##################################################################

        # Definimos el siguiente diccionario con los parámetros para mergear las capas nombradas anteriormente. 
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': 'Remaining_fields_4ba1f6a0_5ed5_4590_816a_433eeabef278',
            'INPUT_2': 'Remaining_fields_be6f30df_2db0_4ee2_8f69_b34cc58f6b3e',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroid_nearest_coast_joined']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['JoinAttributesByFieldValueCcentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroid_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCcentroidsYCoast']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        #########################################################
        # Extraemos los vertices
        #########################################################
        
        # Definimos el input y output
        alg_params = {
            'INPUT': 'Joined_layer_4fd3c2ad_817f_443e_bba8_b0fd49c1bd99',
            'OUTPUT': parameters['Extract_vertices']
        }
        
        # Aplicamos el proceso anteriormente especificado y las guardamos en los diccionarios creados.
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        #########################################################
        # Generamos una variable igual a la coordendana "y" 
        # de la capa "cant_lat" (field calculator)
        #########################################################

        # Definimos el siguiente diccionario con los parámetros para poder duplicar la variable especificada anteriormente. 
        
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cant_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': 'Extracted__attribute__c4325664_7467_41af_83aa_d3080e0b4a62',
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCant_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCant_lat']['OUTPUT']

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Extract vertices
        alg_params = {
            'INPUT': 'Remaining_fields_1f8c1a97_3f52_4089_ad1a_f921b07f30dd',
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']
        return results

    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
