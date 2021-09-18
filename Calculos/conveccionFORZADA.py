# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()

class conveccionFORZADA(): ## Convección forzada entre la placa fotovoltaica y el viento
    def __init__(self,v_viento,L):
        self.v_viento = v_viento
        self.L = L
    def calculo(self):
        j = -1  # Iteración de mes
        ## Constantes del aire
        rho = 1.184 # Densidad del aire kg/m3
        nu_v =  0.000018 # Viscosidad dinámica del aire Pa·s
        Cp = 1007 # Calor específico del aire J/kg·K
        k_c = 0.025 # Conductividad del aire  W/m·K
        ## Números característicos
        Re = {} # Diccinario número de Reynolds
        Pr = (Cp*nu_v)/k_c # Número de Prandtl para el aire
        Nu = {} # Diccionario número de Nusselt
        # Coeficiente de convección W/m2·K
        h_conv = {}
        for i in Meses:
            j = j + 1  # Valor iterativo de los meses
            Re[i] = []  # Lista número Reynolds
            Nu[i] = []  # Lista número Nusselt 
            h_conv[i] =[] # Lista coeficiente convectivo
            for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año  
                t_RE = (rho*self.v_viento[i][k]*self.L)/nu_v                
                Re[i].append(t_RE)
                # Correlación para el número de Nusselt de Churchill and Ozoe (1973) obtenida en la sección 4.9.2 of Nellis and Klein ecuación (4-59.1)
                if Re[i][k] < 2300: # Flujo laminar
                    t_1 = 0.3387*Pr**(1/3)*Re[i][k]**(1/2) 
                    t_2 = (1+(0.0468/Pr)**(2/3))**(1/4)
                    Nu[i].append(t_1/t_2)
                if Re[i][k] >= 2300: # Flujo turbulento
                    # Re_c = Re[i][k]
                    # t_1 = 0.6774*Pr**(1/3)*Re_c**(1/2) 
                    # t_2 = (1+(0.0468/Pr)**(2/3))**(1/4)
                    # t_3 = 0.037*Pr**(1/3)*(Re[i][k]**(0.8)-Re_c**(0.8))
                    # Nu[i].append((t_1/t_2)+t_3)
                    Nu[i].append(0.0296*Re[i][k]**(4/5)*Pr**(1/3))
                h_conv[i].append(Nu[i][k]*k_c/self.L)    
        return h_conv , Re, Nu       
                    