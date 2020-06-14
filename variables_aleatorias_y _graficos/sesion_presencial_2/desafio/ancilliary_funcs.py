#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import scipy.stats as stats

def calcular_medidas_descriptivas(objeto):
    """
    calcular_medidas_descriptivas:
        Función que permite calcular las medidas descriptivas para los casos contínuos 
        o la frecuencias absolutas para las variables discretas.
    parameters:
        objeto: objeto tipo DataFrame
    returns:
        medidas descriptivas o frecuencias absolutas
    """
    variables_continuas = ['float64', 'int64']
    variables_discretas = ['object']    
    for nombre_columna, serie in objeto.iteritems():
        if isinstance(serie, pd.Series):
            print(nombre_columna, serie.dtypes)
            print('*************************************************************')
            if serie.dtype in variables_continuas:
                # vamos a eliminar los datos perdidos en la columna
                serie = serie.dropna()
                print(round(serie.describe(),2))
            if serie.dtype in variables_discretas:
                print(serie.value_counts())

def observaciones_perdidas(dataframe, var, print_list=False):
    """
    observaciones_perdidas:
        Función que permite listar las observaciones perdidas de una variable
    parameters:
        dataframe: objeto DataFrame.
        var: Variable a inspeccionar.
        print_list : Opción para imprimir la lista de observaciones perdidas en la variable, 
        por defecto es False.
    return:
        cantidad de casos perdidos, porcentaje correspondiente
    """
    # Cuando print_list = True , debe retornar la lista de casos
    if print_list:
        return dataframe[dataframe[var].isna()]
    
    # La función debe retornar la cantidad de casos perdidos y el porcentaje correspondiente
    cantidad = dataframe[var].isnull().sum()
    porcentaje = cantidad / len(dataframe)
    resultado = {"cantidad": cantidad, "porcentaje": round(porcentaje, 2), 'tipo': dataframe[var].dtypes}
    return resultado

def crear_histograma(dataframe, var, sample_mean=False, true_mean=False):
    """
    crear_histograma:
        Función que permite crear un histograma
    parameters:
        dataframe : La base de datos donde se encuentran los datos específicos.
        var : La variable a graficar.
        sample_mean : Booleano. Si es verdadero, debe generar una recta vertical indicando la
        media de la variable en la selección muestral. Por defecto debe ser False.
        true_mean : Booleano. Si es verdadero, debe generar una recta vertical indicando la
        media de variable en la base de datos completa.
    returns:
        histograma
    """
    # Limpiar muestra
    muestra = dataframe[var].dropna()
    # Si es verdadero, debe generar una recta vertical indicando la media de la variable en la sel. muestral
    if sample_mean:
        plt.axvline(muestra.mean(), lw=3, color='tomato', linestyle='--', label=f"Media Sel. Muestral ({round(muestra.mean(), 2)}%)")
        plt.legend()
    # Si es verdadero, debe generar una recta vertical indicando la media de variable en la bd completa
    if true_mean:
        muestra_completa = df[var].dropna()
        plt.axvline(muestra_completa.mean(), lw=3, color='green', linestyle='--', label=f"Media Muestra Global ({round(muestra_completa.mean(), 2)}%)")
        plt.legend()

    plt.hist(muestra, color='lightgrey')
    plt.xlabel(var)
    plt.ylabel('Frecuencia')
    plt.show()

def crear_dotplot(dataframe, plot_var, plot_by, global_stat=False, statistic='mean'):
    """
    crear_dotplot:
        Función que permite crear un dotplot
    parameters:
        submuestra: objeto DataFrame (tiene menos datos).
        dataframe : objeto DataFrame (tiene todos los datos).
        plot_var : La variable a analizar y extraer las medias.
        plot_by : La variable agrupadora.
        global_stat : Booleano. Si es True debe graficar la media global de la variable. Por
        defecto debe ser False .
        statistic: Debe presentar dos opciones. mean para la media y median para la mediana.
        Por defecto debe ser mean .
    returns:
        dotplot
    """
    # Datos dataframe agrupados
    dataframe_agrupado = dataframe.groupby(plot_by)[plot_var]

    # mean para la media
    if statistic == 'mean':
        media_muestra = round(dataframe[plot_var].mean(),2)
        promedios_continentes = round(dataframe_agrupado.mean(),2)
        label_muestra = f"Media Sel. Muestral ({round(media_muestra, 2)}%)"
        plt.axvline(media_muestra, lw=3, color='tomato',  linestyle='--',  label=label_muestra)
    
    # median para la mediana
    if statistic == 'median':
        mediana_muestra = round(dataframe[plot_var].median(),2)
        datos_linea_vertical = mediana_muestra;
        promedios_continentes = round(dataframe_agrupado.median(),2)
        label_muestra = f"Mediana Sel. Muestral ({round(mediana_muestra, 2)}%)"
        plt.axvline(mediana_muestra, lw=3, color='tomato',  linestyle='--',  label=label_muestra)
    
    # zscore para puntaje z
    if statistic == 'zscore':
        puntaje_z_muestra = round(dataframe[plot_var + '_z'].median(),2)
        dataframe_agrupado_z = dataframe.groupby(plot_by)[plot_var + '_z']
        promedios_continentes = round(dataframe_agrupado_z.median(),2)
        label_muestra = f"Puntaje z Sel. Muestral ({round(puntaje_z_muestra, 2)}%)"
        plt.axvline(puntaje_z_muestra, lw=3, color='tomato',  linestyle='--',  label=label_muestra)
    
    # Si es True debe graficar la media global de la variable
    if global_stat and  statistic is 'mean':
        media_global = round(df[plot_var].mean(),2);
        label_muestra = f"Media Muestra Global ({round(media_global, 2)}%)"
        plt.axvline(media_global, lw=3, color='green', linestyle='--', label=label_muestra)
        plt.legend()
    
    # Si es True debe graficar la mediana global de la variable
    if global_stat and  statistic is 'median':
        mediana_global = round(df[plot_var].median(),2)
        label_muestra = f"Mediana Muestra Global ({round(mediana_global, 2)}%)"
        plt.axvline(mediana_global, lw=3, color='green', linestyle='--', label=label_muestra)
        plt.legend()
    
    # Crear dotplot
    plt.title('Dotplot variable {}'.format(plot_var))
    plt.plot(promedios_continentes.values, promedios_continentes.index, 's', color='#0066FF') 
    plt.legend()
    plt.show()
    
def  generar_curvas_de_densidad(df1, df2, variable, log=False):
    """
    generar_curvas_de_densidad:
        Función que permite generar un gráfico comparando dos curvas de densidad
    parameters:
        df1 : Tabla de datos 1.
        df2 : Tabla de datos 2.
        variable : Variable a contrastar.
        log : Booleano. Si es True transformar la variable al logaritmo. Por defecto debe ser False
    returns:
    """
    variable_df1 = df1[variable].dropna()
    variable_df2 = df2[variable].dropna()
    titulo = 'Variable ({})'.format(variable)

    # Si es True transformar la variable al logaritmo. Por defecto debe ser False
    if log:
        variable_df1 = np.log(variable_df1)
        variable_df2 = np.log(variable_df2)
        titulo = "Variable log({})".format(variable)

    x_axis = np.linspace(variable_df1.min(), variable_df1.max(), 1000)
    plt.plot(x_axis, stats.norm.pdf(x_axis, variable_df1.mean(), variable_df1.std()), color='blue', lw=3)

    x_axis = np.linspace(variable_df2.min(), variable_df2.max(), 1000)
    plt.plot(x_axis, stats.norm.pdf(x_axis, variable_df2.mean(), variable_df2.std()), color='tomato', lw=3)

    plt.title(titulo)
    plt.show()
