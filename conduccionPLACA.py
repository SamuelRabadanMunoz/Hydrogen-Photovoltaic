# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()

class conduccionPLACA(): ## Conducción placa solar fotovoltaica
    def calculo(self):
        
        ## Constantes composición placa fotovoltaica -> Vidro/EVA/Célula/EVA/Tedlar
        k_v = 1.1  # Conductividad térmica vidrio templado W/m·k
        k_eva = 0.3 # Conductividad térmica etil-vinil-acetato (EVA) W/m·k
        k_ted = 0.2 # Conductividad térmica Tedlar W/m·K
        ## Espesores típicos de placa fotovoltaica
        e_v = 4/1000 # Espesor vidro templado m
        e_eva1 = 1/1000 # Espesor EVA cara frontal m
        e_eva2 = 0.5/1000 # Espesor EVA cara posterior m
        e_ted = 0.2/1000 # Espesor tedlar m
        ## Números característicos
        R_aux = (e_v/k_v)+(e_eva1/k_eva) 
        U_s = 1/R_aux  # Resistencia total por la cara superior W/m2·K
        R_aux = (e_eva2/k_eva)+(e_ted/k_ted)
        U_i = 1/R_aux  # Resistencia total por la cara inferior W/m2·K
        return U_s, U_i

