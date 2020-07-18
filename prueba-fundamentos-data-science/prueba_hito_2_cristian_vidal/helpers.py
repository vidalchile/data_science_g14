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

def obtener_porcentaje_datos_perdidos(df, variables):
    """
    obtener_porcentaje_datos_perdidos:
        función que permite obtener el porcentaje de valores perdidos de una variable
    parameters:
        df: objeto tipo DataFrame
        variables: vector con los nombre de las variables a examinar
    returns:
        nombre de la variable y su porcentaje de valores vacios
    """
    for colname, serie in df.iteritems():
         if colname in variables:
            print(colname, serie.isna().value_counts('%')[1].round(3))
            
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

def get_var_categoricas_vector_objetivo(df, var_categoricas, vector_objetivo):
    """
    get_var_categoricas_vector_objetivo:
        Función que permite visualizar gráficamente las variables categóricas con el vector objetivo
    parameters:
        df: objeto tipo DataFrame
        var_categoricas: vector con el nombre de las variables categóricas
        var_objetivo: nombre del vector objetivo
    returns:
        Información visual de las variables categóricas con el vector objetivo (Grafico)
    """
    cant_var_categoricas = len(var_categoricas)
    columnas = 2
    contador = 1
    for variable in var_categoricas:
        plt.subplot((cant_var_categoricas/2) + 1, columnas, contador)
        sns.countplot(variable, hue=vector_objetivo, data=df)
        contador = contador + 1
    plt.tight_layout()

