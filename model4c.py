"""
Herramientas Computacionales para la Investigación - MAE UdeSA 2022
Tomás Pacheco y Abigail Riquelme
Comentarios sobre el modelo 4c

"""


# Comenzamos importando las librerías que se necesitarán para correr los diferentes programas.
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,  QgsProcessingMultiStepFeedback, 
                       QgsProcessingParameterFeatureSink,  QgsCoordinateReferenceSystem)
import processing


# Definimos directorios para importar y exportar archivos
main = "" # Definimos el directorio principal
inputcountries = "{}/input/counties/ne_10m_admin_0_countries.shp".format(main) # Generamos un string con la direccion del archivo raster de LANGAA??
output = "{}/output".format(main) # Generamos un string con la direcciÃ³n de la carpeta en donde guardaremos todo lo que exportemos


# Definimos la clase 
class Model4c(QgsProcessingAlgorithm):

    # 
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    #
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback) # El proceso tendrá cinco pasos
        # Definimos dos diccionarios para los resultados
        results = {}
        outputs = {}

        #########################################################
        # Reproyectamos la capa
        #########################################################
        
        # Vamos a reproyectar la capa de países. Para esto definimos el input que está en la memoria y el output es una capa llamada 'Countries_reproyected'.
        alg_params = {
            'INPUT': 'Remaining_fields_befb7c77_3d1d_40e5_af83_b3275ab18d38',
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'),
            'OUTPUT': parameters['Countries_reprojected']
        }
        # Aplicamos el proceso
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['ReprojectLayer']['OUTPUT']

        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

       #########################################################
        # Borramos campos
       #########################################################
        
        # Guardamos en este diccionario una serie de variables que queremos eliminar de la capa de país.
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': inputcountries,
            'OUTPUT': parameters['Countries_drop_fields']
        }
        # Aplicamos el proceso
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_drop_fields'] = outputs['DropFields']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}


       #########################################################
       # Calculamos el área en km2 de cada uno de los países 
       #########################################################
       
        # Para hacerlo, usamos la herramienta 'field calculator'. Exportamos un field que se llama 'km2area' que tiene 10 caracteres de largo
        # y se usa como input la capa reproyectada del paso anterior.
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'area($geometry)/1000000',
            'INPUT': 'Reprojected_754e0ec3_4d6b_440c_a901_730b73b87148',
            'OUTPUT': parameters['Areas_out']
        }
        # Se aplica el proceso
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['FieldCalculator']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}


        
        #########################################################
        # Fix geometries 
        #########################################################
        
        # Necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se superpongan o que haya polígonos no cerrados.
        # Definimos el input (capa reproyectada) y el output que es 'countries_fixgeo.

        alg_params = {
            'INPUT': 'Reprojected_754e0ec3_4d6b_440c_a901_730b73b87148',
            'OUTPUT': parameters['Countries_fixgeo']
        }
        # Aplicamos el proceso
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['FixGeometries']['OUTPUT']

        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Guardamos los datos a un csv
        #########################################################

        # Guaramos vector feacture a un archivo. Este se va a llamar 'areas_out21.csv'
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'areas_out [ESRI:54034]',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '{}/areas_out21.csv'.format(output)
        }
        # Exportamos
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        # Indicamos que la función devuelva el diccionario de resultados.
        return results

    def name(self):
        return 'model4c'

    def displayName(self):
        return 'model4c'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4c()
