"""
Herramientas Computacionales para la InvestigaciÃ³n - MAE UdeSA 2022
TomÃ¡s Pacheco y Abigail Riquelme
Comentarios sobre el modelo 4a

"""

# Comenzamos importando las librerías que se necesitarán para correrlo los diferentes programas.

from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, 
                       QgsProcessingMultiStepFeedback,QgsProcessingParameterFeatureSin)
import processing

# Ahora vamos a definir el directorio de trabajo y las direcciones a las carpetas dentro

main = "" # Definimos el directorio principal
inputclean = "{}/output/clean.shp".format(main) # Para importar la capa clean
inputcountries = "{}/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(main) # Para importar la capa de paises
outputcsvcountries = "{}/output/languages_by_country.csv".format(main) # Para exportar el csv con la cantidad de idiomas por país


# Definimos la clase para el modelo 4a

class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None): # Con esta primera función lo que se hace es definir los procesos del algoritmo, para este modelo son cuatro. 
        # Aca se agrega la herramienta "fix geometries" 
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aca se agrega la herramienta "fix geometries" (la agregamos nuevamente debido a que la utilizaremos para dos bases de datos distintas)
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aca se agrega la herramienta "intersection" 
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
    # Mediante la siguiente función se procesa el algoritmo. La función tiene como parámetros el nombre del algoritmo, 
    # los parámetros definidos anteriormente, el contexto en el que se ejecutará el algoritmo y feedback del modelo.  
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback) # En el primer argumento de la función escribimos la cantidad de procesos del algoritmo. 
        # Definimos diccionarios en donde se ira guardando el output de los distintos procesos. 
        results = {}
        outputs = {}
        
        #########################################################
        # Fix geometries (primera base: wlds)
        #########################################################
        
        # Necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se superpongan o que haya polígonos no cerrados.
         # Definimos diccionario con el input y output. 
        alg_params = {
            'INPUT': inputclean,
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        # Aplicamos el proceso de corregir las geometrías y las guardamos en los diccionarios creados.
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        #########################################################
        # Fix geometries (segunda base: countries)
        #########################################################
        
        # Tal como se explico anteriormente, necesitamos corregir las geometrías. Esto lo hacemos para evitar que los polígonos se 
        # superpongan o que haya polígonos no cerrados.

        # Definimos diccionario con el input y output. 

        alg_params = {
            'INPUT': inputcountries,
            'OUTPUT': parameters['Fixgeo_countries']
        }
        # Aplicamos el proceso de corregir las geometrías y las guardamos en los diccionarios creados.
        outputs['FixGeometriesContries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesContries']['OUTPUT']
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
        
        #########################################################
        # Calculamos el promedio de la variable ADMIN  
        # por polígogo (statistics by categories) 
        #########################################################
        
        # Definimos los parámetros para poder calcular la media de la variable ADMIN por poligono. 
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersection_7a8169c8_148a_4cd5_892a_d79533348735',
            'OUTPUT': outputcsvcountries,
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        # Aplicamos el proceso para calcular la media y lo guardamos en los diccionarios creados.
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Indicamos que si ocurre algún tipo de error se suspensa el procesamiento del algoritmo y se devuelva un diccionario en blanco. 
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        #########################################################
        # Hacemos la intersección de las capas 'FixGeometriesWlds'
        # y 'FixGeometriesContries' (intersections) 
        #########################################################
        
        # Definimos los parámetros para poder hacer la intersección entre dos capas. 
        alg_params = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['FixGeometriesContries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        # Aplicamos el proceso para intersecar las capas nombradas anteriormente.
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
