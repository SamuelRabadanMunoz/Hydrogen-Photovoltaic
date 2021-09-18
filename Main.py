# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación de una planta fotovoltaica para producir hidrógeno aplicado a usos ferroviarios y marítimos: Caso de estudio en la isla de Mallorca
"""

from Calculos.Datos import Datos
from Calculos.angulosSOLARES import angulosSOLARES # Cálculos sobre ángulos solares
from Calculos.radiacionSInclinada import radiacionSInclinada # Cálculo ángulo de indicendia entre la normal de la superficie inclinada y el rayo de sol // Cálculo radiación directa en superficie inclinada
from Calculos.radiacionTotal import radiacionTotal # Cálculo de la radiación total sobre superficie inclinada mediante el modelo de Liu y Jordan (1963)
from Calculos.conveccionFORZADA import conveccionFORZADA # Cálculo de la convección por la velocidad del viento en una superficie plana
from Calculos.conduccionPLACA import conduccionPLACA # Cálculo del coeficiente de transferencia por conducción para la cara superior y la cara inferior de la placa fotovoltaica
from Calculos.radiacionPLACA import radiacionPLACA # Cálculo del coeficiente de transferencia por radiación para la cara superior y la cara inferior de la placa fotovoltaica. Cálculo de la temperatura del media del cielo
from Calculos.balanceGLOBAL import balanceGLOBAL #  Balance de energía al módulo fotovoltaico
from Calculos.produccionHidrogeno import produccionHidrogeno # Cálculo de producción de hidrógeno


T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma() # Obtenición de datos
dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # Número de días por mes


azimut = 0 # Orientación 0 Sur
beta = 20 # Inclinación de la superficie de captación
rho_g = 0.2 # Albedo correspondiente al suelo
L = 1 # Longitud característica del módulo


# >>>>> Simulación con  JA Solar JAM72S20-455/MR Lloseta <<<<<<

phi = 39.718 # Latitud Lloseta
N_m = 18816  # Número de módulos de Lloseta
Ns = 144
Voc_ref = 49.85
Isc_ref = 11.41
Vmpp_ref = 41.82
Impp_ref = 10.88
eta_Voc = -0.00272*Voc_ref
eta_Isc = 0.00044*Isc_ref
alto = 2.2 # Altura placa fotovoltaica
ancho = 1.1  # Ancho placa fotovoltaica


# >>>>> Simulación con  JAM72S10-405/MR Petra <<<<<<
# phi = 39.609 # Latitud Petra
# N_m = 18648  # Número de módulos de Petra
# Ns = 144
# Voc_ref = 49.82
# Isc_ref = 10.32
# Vmpp_ref = 41.46
# Impp_ref =9.77
# eta_Voc = -0.00289*Voc_ref
# eta_Isc = 0.00051*Isc_ref
# alto = 2.015 # Altura placa fotovoltaica
# ancho = 0.996  # ANcho placa fotovoltaica

# Vidrio de la cara superior
rho_v = 0.04
tau_v = 0.95
alpha_v = 1-rho_v-tau_v
T_suelo = 15
T_s = 15
T_i = 15
T_c = 15



## >>>>>>>>>>>>> CAPÍTULO RADIACIÓN SOLAR <<<<<<<<<<<<<<<



## -------------SUBCAPÍTULO ÁNGULOS SOLARES---------------


delta_m, omega_ps, theta_z, alpha_s, omega_s, gamma_s = angulosSOLARES(phi,azimut).calculo()


## -------------SUBCAPÍTULO RADIACIÓN EN SUPERFICIE INCLINADA --------------- 

theta, R_b, I_bt = radiacionSInclinada(theta_z,beta,gamma_s,azimut,phi,delta_m,omega_s, G_bn).calculo() ## Radiación directa en superficie inclinada
I_t, G_t = radiacionTotal(I_bt,G_d,beta,rho_g).calculo() ## Modelo de Liu y Jordan (1963) para la radiación total sobre superficie inclinada

## >>>>>>>>>>>>> CAPÍTULO BALANCE PLACA FOTOVOLTAICA <<<<<<<<<<<<<<<



## -------------SUBCAPÍTULO COEFICIENTES DE TRANSFERENCIA DE CALOR-------------


h_conv, Re, Nu = conveccionFORZADA(v_viento,L).calculo() #Convección en la cara frontal y trasera según la velocidad viento
T_cielo, h_rad_sc, h_rad_ss, h_rad_is  = radiacionPLACA(beta).calculo() #Radiación SC (superior-cielo) SS (superior-suelo) IS (inferior-suelo)
U_s, U_i = conduccionPLACA().calculo() #Conducción



## -------------SUBCAPÍTULO CÁLCULO DEL BALANCE ENERGÉTICO TRANSFERENCIA DE CALOR-------------



P, I, V, Q_trans_s, Q_refl_s, Q_abs_s, Q_cond_s, Q_conv_s, Q_rad_sc_s, Q_rad_ss_s, gamma_cs, T_s2, Q_cond_i, Q_conv_i, Q_rad_is, gamma_ci, T_i2, T_c2, gamma_c = balanceGLOBAL(G_t,Ns,Voc_ref,Isc_ref,Vmpp_ref,Impp_ref,eta_Voc,eta_Isc,T_c,rho_v,tau_v,alpha_v,T_cielo,T_suelo,h_conv,h_rad_sc,h_rad_ss,h_rad_is,U_s,U_i,T_i,T_s,alto,ancho).calculo()      



## >>>>>>>>>>>>> CAPÍTULO CÁLCULO HIDRÓGENO <<<<<<<<<<<<<<<


## -------------SUBCAPÍTULO INYECCCIÓN A RED MEDIANTE HIDRÓGENO -------------

Vn_H2, m_H2 , Q_pila, Q_out, P_pila, P_out  = produccionHidrogeno(P,N_m).calculo()  #Producción de hidrógeno y energía disponible en pila PEM para uso

















    
    