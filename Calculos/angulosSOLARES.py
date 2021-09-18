# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""
import math
from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()



## -------------CAPÍTULO ÁNGULOS SOLARES---------------

class angulosSOLARES():
    def __init__(self, phi,azimut):
        self.phi = phi
        self.azimut = azimut
    

    def calculo(self):   
        n = 1 # Contador para el día del año
        t = 0 # Valor para controlar la hora
        j = -1  # Iteración de mes
        delta_m = {}  # Diccionario inclinación solar
        omega_ps = {}  # Diccionario ángulo puesta de sol
        theta_z = {} # Diccionario ángulo cenital solar con respecto a la horizontal beta = 0
        alpha_s = {} # Diccionario ángulo altura solar con respecto a la horizontal beta = 0
        omega_s = {} # Diccionario con la hora solar diaria
        gamma_s = {} # Diccionario ángulo acimutal solar
        for i in Meses:
            delta_m[i] = []  # Lista inclinación solar por mes
            omega_ps[i] = []  # Lista ángulo puesta de sol por mes
            theta_z[i] = [] # Lista cenital solar con respecto a la horizontal beta = 0 por mes
            alpha_s[i] = [] # Lista altura solar con respecto a la horizontal beta = 0 por mes
            omega_s[i] = [] # Lista con la hora solar diaria por mes
            gamma_s[i] = [] # Lista el ángulo azimutal solar por mes
            j = j + 1  # Valor iterativo de los meses
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año
                # Lógica de control para añadir los días del año
                t = t + 1        
                if t == 25: # A la iteración 25 se vuelve a 1 (paso al siguiente día)
                    t = 1
                    n = n + 1 # Día del año
                omega_s[i].append(15*((t-1)-12))     # Hora solar
                delta_m[i].append(23.45*math.sin(math.radians(360/365*(284+n))))  #Inclinación solar 
                omega_ps[i].append(math.degrees(math.acos(-math.tan(math.radians(self.phi))*math.tan(math.radians(delta_m[i][k]))))) # Ángulo puesta sol
                if omega_s[i][k] >= 0:
                        s = 1
                if omega_s[i][k] < 0:
                        s = -1
                if omega_ps[i][k] > abs(omega_s[i][k]): # Si el ángulo solar es menor que el ángulo de puesta de sol es de día.
                    theta_z[i].append(math.degrees(math.acos((math.sin(math.radians(delta_m[i][k]))*math.sin(math.radians(self.phi))+math.cos(math.radians(delta_m[i][k]))*math.cos(math.radians(self.phi))*math.cos(math.radians(omega_s[i][k]))))))
                    alpha_s[i].append(90-theta_z[i][k])

                    num = math.cos(math.radians(theta_z[i][k]))*math.sin(math.radians(self.phi))-math.sin(math.radians(delta_m[i][k]))  
                    den = math.sin(math.radians(theta_z[i][k]))*math.cos(math.radians(self.phi))+0.000001
                    cociente = num/den
                    gamma_s[i].append(s*abs(math.degrees(math.acos(cociente))))
                    
                else:
                    theta_z[i].append(None)
                    alpha_s[i].append(None)
                    gamma_s[i].append(None)
        return delta_m, omega_ps, theta_z, alpha_s, omega_s, gamma_s             

