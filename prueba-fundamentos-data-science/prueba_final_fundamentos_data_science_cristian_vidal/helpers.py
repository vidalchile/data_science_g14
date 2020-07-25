#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Archivo: helpers.py
Autor: Cristian Vidal Muñoz
Descripción: Funciones auxiliares utilizadas en la prueba final modulo Fundamentos de data science (Desafio Latam)
"""

import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
            
def explorar_variables(df):
    """
    explorar_variables:
        Función que permite visualizar gráficamente las variables de un DataFrame
    parameters:
        df: objeto tipo DataFrame
    returns:
        Información visual de la variable (Grafico)
    """
    for n, i in enumerate(df):
        plt.subplot((len(list(df.columns))/2)+1, 2, n+1)
        if df[i].dtypes == float:
            sns.distplot(df[i])
            plt.title(i)
            plt.xlabel("")
        elif df[i].dtypes == "object":
            sns.countplot(df[i])
            plt.title(i)
            plt.xlabel("")
        else:
            sns.distplot(df[i], kde=False)
            plt.title(i)
            plt.xlabel("")
        plt.tight_layout()
        
def get_var_categoricas_numericas(df):
    """
    get_var_categoricas_numericas:
        Función que permite obtener las varibles categóricas y numericas de un DataFrame
    parameters:
        df: objeto tipo DataFrame
    returns:
        vector con el nombre de las variables categóricas
        vector con el nombre de las variables numericas
    """
    categorica=[]
    numerica=[]
    
    for n, i in enumerate(df):
        if (df[i].dtypes =="object"):
            categorica.append(i)
        else:
            numerica.append(i)
    return numerica, categorica

def inspeccionar_vector_objetivo(df, variables, vector_objetivo, tipo='countplot'):
    """
    inspeccionar_vector_objetivo:
        Función que permite visualizar gráficamente las variables con el vector objetivo
    parameters:
        df: objeto tipo DataFrame
        variables: vector con el nombre de las variables
        var_objetivo: nombre del vector objetivo
        tipo: tipo de grafico (countplot o boxplot)
    returns:
        Información visual de las variables con el vector objetivo
    """
    cant_variables = len(variables)
    columnas = 2
    contador = 1
    for variable in variables:
        if variable != vector_objetivo:
            plt.subplot((cant_variables/2) + 1, columnas, contador)
            if tipo == 'boxplot':
                sns.boxplot(y=variable,x=vector_objetivo, data=df)
            if tipo == 'countplot':
                sns.countplot(variable, hue=vector_objetivo, data=df)
            contador = contador + 1
    plt.tight_layout()
    
def fetch_features(dataframe, vector_objetivo="medv"):
    # extraemos los nombres de las columnas en la base de datos
    columns = dataframe.columns
    # generamos 3 arrays vacíos para guardar los valores
    # nombre de la variable
    attr_name = []
    # correlación de pearson
    pearson_r = []
    # valor absoluto de la correlación
    abs_pearson_r = []
    # para cada columna en el array de columnas
    for col in columns:
        # si la columna no es la dependiente
        if col != vector_objetivo:
            # adjuntar el nombre de la variable en attr_name
            attr_name.append(col)
            # adjuntar la correlación de pearson
            pearson_r.append(dataframe[col].corr(dataframe[vector_objetivo]))
            # adjuntar el absoluto de la correlación de pearson
            abs_pearson_r.append(abs(dataframe[col].corr(dataframe[vector_objetivo])))
    # transformamos los arrays en un DataFrame
    features = pd.DataFrame({
        'attribute': attr_name,
        'corr':pearson_r,
        'abs_corr':abs_pearson_r
    })
    # generamos el index con los nombres de las variables
    features = features.set_index('attribute')
    # ordenamos los valores de forma descendiente
    return features.sort_values(by=['abs_corr'], ascending=False)