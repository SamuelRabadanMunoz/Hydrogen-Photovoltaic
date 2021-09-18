# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

import math
from Calculos.Datos import Datos
from Calculos.Sicrometria import Sicro

T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()

class radiacionPLACA(): ## Radiación placa solar fotovoltaica
    def __init__(self,beta):
        self.beta = beta
    def calculo(self):
        j = -1    
        epsilon = 0.9 # Emisividad del vidro y el tedlar
        sigma = 5.67*10**(-8) # Constante de Stefan-Boltzmann
        T_cielo = {} #Diccionario para la temperatura cielo  Faustino Chenlo Romero CIEMAT
        FF_p = (1+math.cos(math.radians(self.beta)))/2 # Factor de forma cara superior panel/cielo y cara inferior panel/suelo
        FF_n = (1-math.cos(math.radians(self.beta)))/2 # Factor de forma cara superior panel/suelo
        h_rad_sc = FF_p*sigma*epsilon  # Radiación cara superior hacia el cielo
        h_rad_ss = FF_n*sigma*epsilon  # Radiación cara superior hacia el suelo
        h_rad_is = FF_p*sigma*epsilon  # Radiación cara inferior hacia el suelo
        for i in Meses:
            j = j + 1  # Valor iterativo de los meses       
            T_cielo[i] = []
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año
                T_dp = Sicro(W = Sicro(T = T_ext[i][k], HR = HR_ext[i][k]).calculo_W(),HR = 99).calculo_T() # Temperatura rocio                               
                T_cielo[i].append(((T_ext[i][k]+273)*(0.8+(T_dp)/250)**(1/4))-273)# Temperatura del cielo, ecuación de Bliss
        return T_cielo, h_rad_sc, h_rad_ss, h_rad_is 
