"""
Herramientas Computacionales para la InvestigaciÃ³n - MAE UdeSA 2022Name : model1
TomÃ¡s Pacheco y Abigail Riquelme
Comentarios sobre el modelo 3

"""

from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, 
                       QgsProcessingMultiStepFeedback, QgsProcessingParameterFeatureSink)
import processing

# Definimos la clase para este modelo 3. 

class Model3(QgsProcessingAlgorithm):
    # Tal como hicimos antes, definimos los parámetros que vamos a usar. Este modelo solo va tener 5 parámetros. 
    def initAlgorithm(self, config=None):
        # Aqui se agrega un campo para eliminar algunas variables
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aqui agregamos se agrega la herramienta "fix geometries#"
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo_3', 'fix_geo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Agregamos el parámetro para luego poder calcular el promedio de 1800
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Agregamos el parámetro para luego poder calcular el promedio de 1900
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Agregamos el parámetro para luego poder calcular el promedio del año 2000
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    # Mediante la siguiente función se procesa el algoritmo, La función tiene como parámetros el nombre del algoritmo, 
    # los parámetros definidos anteriormente, el contexto en el que se ejecutará el algoritmo y el feedback del modelo. 
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback) # En el primer argumento de la función escribimos 
        # la cantidad de parámetros del modelo.
        # Definimos diccionarios en donde se ira guardando el output de los distintos procesos. 
        results = {}
        outputs = {}
        
        ##################################################################
        # Calculamos el promedio para el año 1900 (zonal statistics)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder calcular el promedio de la población en el año 1900
        # El segundo y tercer elemento del diccionario indican los archivos que utilizaremos como inputs, 
        # el quinto elemento indica que calcularemos la media y el último elemento aplica el método para 
        # exportar la capa modificada. 
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Zonal_Statistics_9c198540_2075_41fd_a3c8_773968728c29',
            'INPUT_RASTER': 'popd_1900AD_f1103fc8_70fd_453c_8de3_ff4fd09cf421',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  
            'OUTPUT': parameters['Pop1900']
        }
        # A continuacion aplicamos el proceso para poder calcular la media de la población para el año 1900, se utiliza 
        # como parametro el definido en las lineas 46-52. 
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['ZonalStatistics']['OUTPUT']
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        ##################################################################
        # Eliminamos algunas variables (drop fields)
        ##################################################################
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene la capa que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar la capa modificado.  
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Fixed_geometries_05cd4438_63ce_4bb6_8b02_1a7a5ff364bf',
            'OUTPUT': parameters['Drop_fields_3']
        }
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 68-72. 
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['DropFields']['OUTPUT']
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        ##################################################################
        # Calculamos el promedio para el año 2000 (zonal statistics)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder calcular el promedio de la población en el año 2000
        # El segundo y tercer elemento del diccionario indican los archivos que utilizaremos como inputs, 
        # el quinto elemento indica que calcularemos la media y el último elemento aplica el método para 
        # exportar la capa modificada. 
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Zonal_Statistics_9c198540_2075_41fd_a3c8_773968728c29',
            'INPUT_RASTER': 'popd_2000AD_e287c674_7a5c_4e12_bb11_8dc8ced1c95a',
            'RASTER_BAND': 1,
            'STATISTICS': [0,1,2],  # Count,Sum,Mean
            'OUTPUT': parameters['Pop2000']
        }
        # A continuacion aplicamos el proceso para poder calcular la media de la población para el año 1900, se utiliza 
        # como parametro el definido en las lineas 90-96.
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['ZonalStatistics']['OUTPUT']
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        ##################################################################
        # Calculamos el promedio para el año 1800 (zonal statistics)
        ##################################################################
        
        # Definimos el siguiente diccionario para poder calcular el promedio de la población en el año 1800
        # El segundo y tercer elemento del diccionario indican los archivos que utilizaremos como inputs, 
        # el quinto elemento indica que calcularemos la media y el último elemento aplica el método para 
        # exportar la capa modificada. 
        
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Zonal_Statistics_9c198540_2075_41fd_a3c8_773968728c29',
            'INPUT_RASTER': 'popd_1800AD_93636370_5d26_458a_87e4_57826ef34ca2',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1800']
        }
        # A continuacion aplicamos el proceso para poder calcular la media de la población para el año 1900, se utiliza 
        # como parametro el definido en las lineas 115-122.
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['ZonalStatistics']['OUTPUT']
        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

         #########################################################
        # Fix geometries 
        #########################################################
        
        # Necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se superpongan o que haya polígonos no cerrados.
        alg_params = {
            'INPUT': 'C:/Users/Abi/Desktop/herramientasC5/input/counties/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fix_geo_3']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo_3'] = outputs['FixGeometries']['OUTPUT']
        return results

    def name(self):
        return 'model3'

    def displayName(self):
        return 'model3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()
