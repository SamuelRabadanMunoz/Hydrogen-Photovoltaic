# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""




class balanceCINFERIOR(): ## Balance energético a la cara inferior del módulo fotovoltaico

      def __init__(self,T_i,T_c,h_conv,h_rad_is,U_i,T_ext,T_suelo,alto,ancho):  
        self.h_rad_is = h_rad_is  
        self.h_conv = h_conv
        self.T_c = T_c
        self.T_i = T_i
        self.U_i = U_i
        self.T_ext = T_ext
        self.T_suelo = T_suelo
        self.alto = alto
        self.ancho = ancho

      def calculo(self):
       
        # Transferencia de calor de la cara superior
        Q_cond = self.U_i*(self.T_c-self.T_i) # Conducción cara superior hacia célcula
        Q_conv = self.h_conv*(self.T_ext-self.T_i) # Convección cara superior hacia ambiente
        T_ik = self.T_i + 273  # Temperatura superficie en Kelvin
        T_suelok = self.T_suelo + 273 # Temperatura suelo en Kelvin        
        Q_rad_is = self.h_rad_is*(T_suelok**(4)-T_ik**(4))
        cp_te = 1400 # Capacidad calorífica del tedlar J/kg*ºC 
        e_te = 0.2/1000 # Espesor tedlar m
        rho_te = 1380 # densidad del tedlar kg/m3

        # BALANCE DE ENERGÍA
        gamma = Q_cond+Q_conv+Q_rad_is # J/m2*h gamma positivo aumenta T_s / gamma negativo disminuye T_s
        gamma = gamma*self.alto*self.ancho
        m = e_te*self.alto*self.ancho*rho_te              
        T_i2 = (gamma/(m*cp_te))+self.T_i # Temperatura resultante del balance de energía a la cara superior

        return Q_cond, Q_conv, Q_rad_is, gamma, T_i2    
        
