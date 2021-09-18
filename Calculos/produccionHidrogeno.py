# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""
from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()


class produccionHidrogeno(): # Electrolizador escogido marca H2B2 EL600N
    def __init__(self,P, N_m):
        self.P = P
        self.N_m = N_m

        
    def calculo(self):
        P_cons = (5.1+0.178)*1000  # Consumo Wh eléctrico / Nm3 H2 producido, incluye Balance of Plant (BoP) y el trabajo de compresión
        j = -1  # Iteración de mes
        eta_pila = 0.52  # Eficiencia pila de combustible
        F = 96485.33  #  Constante de Faraday C/mol        
        PCS_H2 = 141.86*1000000 # Poder calorífico superior del hidrógeno J/kg
        Vn_H2 = {}  # Producción de hidrógeno en m3/h en condiciones normales
        m_H2 = {}  # Producción de hidrógeno en kg/h
        Q_pila = {} # Enegía eléctrica disponible depsués de la pila PEM
        Q_out = {}  # Calor producido por la reacción química en la pila PEM
        P_pila= {}  # Potencia eléctrica producida por la pila en W
        P_out = {} # Potencia calorífica producida por la pila en W   
        for i in Meses:
            Vn_H2[i] = []  # Lista Producción de hidrógeno en m3/h en condiciones estandar
            m_H2[i] = []  # Lista Producción de hidrógeno en kg/h                   
            Q_pila[i] = [] # Lista Enegía eléctrica disponible depsués de la pila PEM
            Q_out[i] = [] # Lista  Calor producido por la reacción química en la pila PEM
            P_pila[i] = [] # Lista Potencia eléctrica producida por la pila en W
            P_out[i] = [] # Lista Potencia calorífica producida por la pila en W
            j = j + 1  # Valor iterativo de los meses
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año    
                Vn_H2[i].append(self.P[i][k]/(P_cons))  # Volumen de hidrógeno producido por unidad de placa
                m_H2[i].append(0.089*Vn_H2[i][k])  # Masa de hidrógeno producido por unidad de placa
                Q_pila[i].append(m_H2[i][k]*PCS_H2*eta_pila)  # Energía producida por la pila en J/h por unidad de placa
                Q_out[i].append((m_H2[i][k]*PCS_H2)-Q_pila[i][k]) # Calor producido por la pila en J/h por unidad de placa
                P_pila[i].append(Q_pila[i][k]/3600)  # Potencia eléctrica producida por la pila en W por unidad de placa
                P_out[i].append(Q_out[i][k]/3600)  # Potencia calorífica producida por la pila en W por unidad de placa 
        return Vn_H2, m_H2 , Q_pila, Q_out, P_pila, P_out
    
    
                  
    