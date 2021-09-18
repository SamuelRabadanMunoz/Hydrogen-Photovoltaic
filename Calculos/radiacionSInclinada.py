# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

import math
from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()

class radiacionSInclinada():
    def __init__(self,theta_z,beta,gamma_s,azimut,phi,delta_m,omega_s, G_bn):
        self.theta_z =theta_z
        self.beta = beta
        self.gamma_s = gamma_s
        self.gamma= azimut
        self.phi = phi
        self.delta_m = delta_m
        self.omega = omega_s
        self.G_bn = G_bn
    def calculo(self):
        j = -1
        theta = {} #Ángulo de incidencia entre la normal a una superficie inclinada y la incidencia del rayo solar   
        R_b = {} #Factor geométrico en función del ángulo theta_z y theta         
        I_bt = {} #Radiación sobre superficie inclinada
        for i in Meses:
            j = j + 1  # Valor iterativo de los meses
            theta[i] = [] # Lista ángulo de incidencia entre la normal a una superficie inclinada y la incidencia del rayo solar                
            R_b[i] = [] # Lista factor geométrico en función del ángulo theta_z y theta 
            I_bt[i] = [] # Lista de radiación sobre superficie inclinada
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año  
                if self.theta_z[i][k] == None:    
                    theta[i].append(None)
                    R_b[i].append(0)
                    I_bt[i].append(0)
                else:       
                    # theta[i].append(math.degrees(math.acos((math.cos(math.radians(self.theta_z[i][k]))*math.cos(math.radians(self.beta))+math.sin(math.radians(self.theta_z[i][k]))*math.sin(math.radians(self.beta))*math.cos(math.radians(self.gamma_s[i][k]-self.gamma))))))
                    t_1 = math.sin(math.radians(self.delta_m[i][k]))*math.sin(math.radians(self.phi))*math.cos(math.radians(self.beta))
                    t_2 = math.sin(math.radians(self.delta_m[i][k]))*math.cos(math.radians(self.phi))*math.sin(math.radians(self.beta))*math.cos(math.radians(self.gamma))
                    t_3 = math.cos(math.radians(self.delta_m[i][k]))*math.cos(math.radians(self.phi))*math.cos(math.radians(self.beta))*math.cos(math.radians(self.omega[i][k]))
                    t_4 = math.cos(math.radians(self.delta_m[i][k]))*math.sin(math.radians(self.phi))*math.sin(math.radians(self.beta))*math.cos(math.radians(self.gamma))*math.cos(math.radians(self.omega[i][k]))
                    t_5 = math.cos(math.radians(self.delta_m[i][k]))*math.sin(math.radians(self.beta))*math.sin(math.radians(self.gamma))*math.sin(math.radians(self.omega[i][k]))
                    theta[i].append(math.degrees(math.acos(t_1-t_2+t_3+t_4+t_5)))
                    R_b[i].append((math.cos(math.radians(self.theta_z[i][k])))/(math.cos(math.radians(theta[i][k]))))
                    if R_b[i][k] < 0:
                        R_b[i][k] = 0
                    if R_b[i][k] > 5: # Filtro para evitar picos en primeras horas o últimas
                        R_b[i][k] = 5
                    
                    I_bt[i].append(self.G_bn[i][k]*R_b[i][k]*3600)
                                
        return theta, R_b , I_bt  


            