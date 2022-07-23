"""
Herramientas Computacionales para la Investigación - MAE UdeSA 2022
Tomás Pacheco y Abigail Riquelme
Comentarios sobre el modelo 2

"""
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterRasterDestination,QgsCoordinateReferenceSystem)
import processing


# Ahora vamos a definir el directorio de trabajo y las direcciones a las carpetas dentro

main = "" # Definimos el directorio principal
inputhdr = "{}/input/suit/hdr.adf".format(main) # Generamos un string con la direccion del archivo hdr.adf
output = "{}/output".format(main) # Generamos un string con la dirección de la carpeta en donde guardaremos todo lo que exportemos


# Definimos la clase para este modelo 2.
class Model2(QgsProcessingAlgorithm):
    
    # Tal como hicimos antes, definimos los parámetros que vamos a usar. Este modelo solo va a tener
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    # Definimos el algoritmo para procesar las capas.
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        # Definimos dos diccionarios en los que se irá guardando el output
        results = {}
        outputs = {}

        
        #########################################################
        # Vamos a usar la función para reproyectar la capa
        #########################################################

        # Lo que hacemos es definir los parámetros, como el input del archivo.
        # Además, indicamos que queremos reproyectar a WGS84 con el sistema de coordenadas 'EPSG:4326'.
        # Finalmente, indicamos el output.
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': inputhdr,
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        
        # Aplicamos el proceso y guardamos en los diccionarios de output.
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['WarpReproject']['OUTPUT']

        # A continuación indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        #########################################################
        # Extraemos la proyección
        #########################################################
        
        # Tenemos que extraer la proyección. Definimos los parámetros: el input es la capa exportada en el proceso anterior.
        alg_params = {
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        
        # Definimos que el output de la extracción de la proyección se guarde en el diccionario 'output'
        outputs['ExtractProjection'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
       
       # La función devuelve al diccionario llamado 'results' 
       
       return results


    def name(self):
        return 'model2'

    def displayName(self):
        return 'model2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
