"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32209
"""

# Comenzamos importando las librerías que se necesitarán para correrlo los diferentes programas.

from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback, QgsProcessingParameterFeatureSink)
import processing
import os

# Ahora vamos a definir el directorio de trabajo y las direcciones a las carpetas dentro

main = "" # Definimos el directorio principal
wldsin = "{}/langa.shp".format(main) # Generamos un string con la direccion del archivo raster de LANGAA??
output = "{}/output".format(main) # Generamos un string con la dirección de la carpeta en donde guardaremos todo lo que exportemos
wldsout = "{}/wlds_cleaned.shp".format(output) # Generamos un string con la dirección y nombre del archivo en el que exportaremos los datos una vez limpiados




class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None): # Con esta primera función lo que se hace es definir un parámetro al algoritmo.
        # Aquí se agrega un campo autoincremental (autoincremental field)
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aquí se agrega  el parámetro para exportar el archivo modificado
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aquí agrega el parámetro para calcular la cantidad de letras que tiene cada idioma
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aquí se agrega la herramienta "field calculator"
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        # Aquí se agrega el parámetro para filtrar los países cuyos idiomas tienen como máximo 10 letras
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        # Aquí se agrega la herramienta "fix geometries"
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None)
    
    # Mediante la siguiente función se procesa el algoritmo. La función tiene como parámetros el nombre del algoritmo, 
    # los parámetros definidos anteriormente, el contexto en el que se ejecutará el algoritmo y feedback del modelo.           
    def processAlgorithm(self, parameters, context, model_feedback): 
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback) # En el primer argumento de la función escribimos la cantidad de procesos del algoritmo. 
        # Definimos diccionarios en donde se ira guardando el output de los distintos procesos. 
        results = {}
        outputs = {}

        ##################################################################
        # Eliminamos algunas variables (drop fields)
        ##################################################################
        # Definimos el siguiente diccionario para poder eliminar las variables que no son de interés. El primer elemento del diccionario 
        # contiene una lista con los nombres de las variables a eliminar, el segundo elemento tiene el archivo que utilizaremos como input, 
        # el tercer elemento del diccionario aplica el parámetro para exportar el archivo modificado.  
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculated_924c8208_b57a_4493_86bb_f6c8c68d63c7',
            'OUTPUT': parameters['Wldsout']
        }
        # Ahora se aplica el proceso para eliminar las columnas, se utiliza como parámetro el diccionario definido en las lineas 56-59. 
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Se exporta el archivo modificado 
        results['Wldsout'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Field calculator clone
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': '"NAME_PROP"',
            'INPUT': 'menor_a_11_e34436c1_4efe_47fa_8c35_5556f2cbdd3a',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['FieldCalculatorClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculatorClone']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Feature filter
        alg_params = {
            'INPUT': 'Calculated_728a2172_2bdc_4c50_a929_c5e1f25acd77',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FeatureFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incremented_34cdcbc1_c08e_4290_b018_61e3c96f080c',
            'OUTPUT': parameters['Length']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': 'C:/Users/Abi/Desktop/herramientasC5/input/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['FixGeometries']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Add autoincremental field
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'MODULUS': None,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AddAutoincrementalField']['OUTPUT']
        return results

    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
