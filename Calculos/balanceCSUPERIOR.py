# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""


class balanceCSUPERIOR(): ## Balance energético a la cara superior de la placa fotovoltaica   

      def __init__(self,G,rho,tau,alpha,T_cielo,T_suelo,h_conv,h_rad_sc,h_rad_ss,U_c,T_ext,T_c, T_s,alto,ancho):  
        self.G = G
        self.rho = rho # Reflectividad
        self.tau = tau  # Transmisividad
        self.alpha = 1-self.rho-self.tau # Absortividad
        self.T_cielo = T_cielo #ºC
        self.T_suelo = T_suelo #ºC
        self.h_conv = h_conv # W/m2·K
        self.h_rad_sc = h_rad_sc #W/m2·K
        self.h_rad_ss = h_rad_ss #W/m2·K
        self.U_c = U_c #W/m2·K
        self.T_ext = T_ext
        self.T_c = T_c
        self.T_s = T_s
        self.alto = alto
        self.ancho = ancho
        self.T_cielo
        self.T_suelo
        
      def calculo(self):
        # Reparto de radiación
        Q_trans = self.G*self.tau # Radiación transmitida hacia la célula
        Q_refl = self.G*self.rho # Radiación reflejada hacia el cielo
        Q_abs = self.G*self.alpha # Radiació absorbida por la cara superior
        
        # Transferencia de calor de la cara superior
        Q_cond = self.U_c*(self.T_c-self.T_s) # Conducción cara superior hacia célcula
        Q_conv = self.h_conv*(self.T_ext-self.T_s) # Convección cara superior hacia ambiente
        T_sk = self.T_s + 273  # Temperatura superficie en Kelvin
        T_cielok = self.T_cielo + 273  # Temperatura cielo en Kelvin
        T_suelok = self.T_suelo + 273 # Temperatura suelo en Kelvin        
        Q_rad_sc = self.h_rad_sc*(T_cielok**(4)-T_sk**(4))
        Q_rad_ss = self.h_rad_ss*(T_suelok**(4)-T_sk**(4))
        cp_v = 0.779*1000 # Capacidad calorífica del vidro J/kg*ºC
        e_v = 3/1000 # Espesor vidro templado m
        rho_v = 2500 # densidad del vidrio templado kg/m3

        # BALANCE DE ENERGÍA
        gamma = Q_abs+Q_rad_sc+Q_rad_ss+Q_cond+Q_conv # J/m2*h gamma positivo aumenta T_s / gamma negativo disminuye T_s
        gamma = gamma*self.alto*self.ancho
        m = e_v*self.alto*self.ancho*rho_v           
        T_s2 = (gamma/(m*cp_v))+self.T_s # Temperatura resultante del balance de energía a la cara superior

        return Q_trans, Q_refl, Q_abs, Q_cond, Q_conv, Q_rad_sc, Q_rad_ss, gamma, T_s2    
        
