# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()


class balanceCELULA(): ## Balance energético a la célula de silicio  

      def __init__(self, G_trans, Q_ele, Q_cond_s, Q_cond_i, T_c, alto, ancho):  
        self.G_trans = G_trans
        self.Q_ele = Q_ele
        self.Q_cond_s = Q_cond_s
        self.Q_cond_i =Q_cond_i
        self.T_c = T_c
        self.alto = alto
        self.ancho = ancho
        
      def calculo(self):          
        e_c = 0.000275 #Espersor de la célcula de silicio EN m
        cp_c = 713 # Capacidad calorífica de la célcula de silicio J/kg*ºC 
        rho_c = 2330 # Densidad de la célcula de silicio kg/m3
        # BALANCE DE ENERGÍA
        gamma = (self.G_trans)+self.Q_ele+self.Q_cond_s+self.Q_cond_i # J/m2*h gamma positivo aumenta T_s / gamma negativo disminuye T_s
        gamma = gamma*self.alto*self.ancho
        m = e_c*self.alto*self.ancho*rho_c
        T_c2 = (gamma/(m*cp_c))+self.T_c # Temperatura resultante del balance de energía de la celula
        return T_c2, gamma    
        
