# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""
import math
from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()


class radiacionTotal(): ## Modelo de Liu y Jordan (1963). La radiación en una superficie inclinada es la suma de la componente directa, difusa y el reflejo de los cuerpos adyacentes.   
    def __init__(self,I_bt,G_d,beta,rho_g):
        self.I_bt = I_bt
        self.G_d = G_d
        self.beta = beta
        self.rho_g = rho_g
    def calculo(self):
        j = -1  # Iteración de mes
        I_t = {} # Radiación total sobre superficie inclinada     J/m2    
        G_t = {} # Radiación total sobre superficie inclinada     W/m2   
        for i in Meses:
            j = j + 1  # Valor iterativo de los meses
            I_t[i] = []
            G_t[i] = []
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año  
                t_1 = self.I_bt[i][k]
                t_2 = self.G_d[i][k]*3600*(1+(math.cos(math.radians(self.beta))))/2
                t_3 = (self.I_bt[i][k]+self.G_d[i][k]*3600)*self.rho_g*(1-(math.cos(math.radians(self.beta))))/2
                I_t[i].append((t_1+t_2+t_3)) 
                G_t[i].append(I_t[i][k]/3600)
        return I_t, G_t        
                
                