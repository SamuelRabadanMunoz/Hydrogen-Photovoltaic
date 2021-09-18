# -*- coding: utf-8 -*-
"""
Trabajo fin de máster - Samuel Rabadán Muñoz - Simulación energética de producción de hidrógeno mediante pila PEM alimentada por energía fotovoltaica
"""

from Calculos.calculoPOTENCIA import calculoPOTENCIA # Cálculo del coeficiente de transferencia por conducción para la cara superior y la cara inferior de la placa fotovoltaica
from Calculos.balanceCSUPERIOR import balanceCSUPERIOR # Cálculo del coeficiente de transferencia por conducción para la cara superior y la cara inferior de la placa fotovoltaica
from Calculos.balanceCINFERIOR import balanceCINFERIOR # Cálculo del coeficiente de transferencia por conducción para la cara superior y la cara inferior de la placa fotovoltaica
from Calculos.balanceCELULA import balanceCELULA # Cálculo del coeficiente de transferencia por conducción para la cara superior y la cara inferior de la placa fotovoltaica
from Calculos.Datos import Datos
T_ext, HR_ext, G_bn, G_d, v_viento, Meses = Datos.horario_palma()

class balanceGLOBAL(): ## Balance energético a la placa fotovoltaica   

      def __init__(self,G,Ns,Voc_ref,Isc_ref,Vmpp_ref,Impp_ref,eta_Voc,eta_Isc,T_c,rho,tau,alpha,T_cielo,T_suelo,h_conv,h_rad_sc,h_rad_ss,h_rad_is,U_c,U_i,T_i,T_s,alto, ancho):  
          self.G = G
          self.Ns = Ns
          self.Voc_ref = Voc_ref
          self.Isc_ref = Isc_ref
          self.Vmpp_ref = Vmpp_ref
          self.Impp_ref = Impp_ref
          self.eta_Voc = eta_Voc
          self.eta_Isc = eta_Isc
          self.T_c = T_c
          self.rho = rho
          self.tau = tau
          self.alpha = alpha
          self.T_cielo = T_cielo
          self.T_suelo = T_suelo
          self.h_conv = h_conv
          self.h_rad_sc = h_rad_sc
          self.h_rad_ss = h_rad_ss
          self.h_rad_is = h_rad_is
          self.U_c = U_c
          self.U_i = U_i
          self.T_i = T_i
          self.T_s = T_s
          self.alto = alto
          self.ancho = ancho
        
      def calculo(self):
          j = -1    
          # Diccionarios de datos
          P = {}  # Potencia eléctrica resultante
          I = {}  # Intensidad eléctrica producida
          V = {}  # Tensión eléctrica producida
          Q_trans_s = {}  # Radiación transmitida del vidrio hacia la célula
          Q_refl_s = {}   # Radiación reflejada por el vidrio superior
          Q_abs_s = {}    # Radiación absorbida por el vidrio superior
          Q_cond_s = {}   # Calor por conducción cara superior - célula
          Q_conv_s = {}   # Calor por convección cara superior al ambiente
          Q_rad_sc_s = {}  # Calor por radiación de la cara superior al cielo
          Q_rad_ss_s = {}  # Calor por radiación de la cara superior al suelo
          gamma_s = {}  # Resultante del balance de energía cara superior
          T_s2 = {}     # Temperatura de la cara superior
          Q_cond_i = {}  #  Calor por conducción cara inferior - célula
          Q_conv_i = {} # Calor por convección cara inferior al ambiente
          Q_rad_is = {} # Calor por radiación de la cara inferior al suelo
          gamma_i = {}  # Resultante del balance de energía cara inferior
          T_i2 = {} # Temperatura de la cara inferior
          T_c2 = {} # Temperatura de la célula
          gamma_c = {}   # Resultante del balance de energía célula
          for i in Meses:
              j = j + 1  # Valor iterativo de los meses       
              P[i] = []
              I[i] = []
              V[i] = []
              Q_trans_s[i] = []
              Q_refl_s[i] = []
              Q_abs_s[i] = []
              Q_cond_s[i] = []
              Q_conv_s[i] = []
              Q_rad_sc_s[i] = []
              Q_rad_ss_s[i] = []
              gamma_s[i] = []
              T_s2[i] = []
              Q_cond_i[i] = []
              Q_conv_i[i] = []
              Q_rad_is[i] = []
              gamma_i[i] = []                
              T_i2[i] = []
              T_c2[i] = []   
              gamma_c[i] = []
              if j == 0: # Valores inciales de la cara inferior/superior y de la célula de la placa fotovoltaica.
                  T_i2[i].append(self.T_i)
                  T_c2[i].append(self.T_c)
                  T_s2[i].append(self.T_s) 
              if j != 0:  # Resultado del último día de cada mes, se pasa al primer día del mes siguiente
                  T_i2[i].append(T_i2_aux)
                  T_c2[i].append(T_c2_aux)
                  T_s2[i].append(T_s2_aux)
              for k in range(0,len(T_ext[Meses[j]])): # Bucle tipo para recorrer todos los días del año          
                  
                  # Componente eléctrica
                  P_aux, I_aux, V_aux = calculoPOTENCIA(self.G[i][k],self.Ns,self.Voc_ref, self.Isc_ref, self.Vmpp_ref, self.Impp_ref, self.eta_Voc, self.eta_Isc, T_c2[i][k]).calculo()
                  if P_aux > self.Vmpp_ref*self.Impp_ref:
                      P_aux = self.Vmpp_ref*self.Impp_ref
                  P[i].append(P_aux)
                  I[i].append(I_aux)
                  V[i].append(V_aux)
                  
                  
                  # Balance energético a la cara superior
                  Q_trans_s_aux, Q_refl_s_aux, Q_abs_s_aux, Q_cond_s_aux, Q_conv_s_aux, Q_rad_sc_s_aux, Q_rad_ss_s_aux, gamma_s_aux, T_s2_aux = balanceCSUPERIOR(self.G[i][k],self.rho,self.tau,self.alpha,self.T_cielo[i][k],self.T_suelo,self.h_conv[i][k],self.h_rad_sc,self.h_rad_ss,self.U_c,T_ext[i][k],T_c2[i][k],T_s2[i][k],self.alto,self.ancho).calculo()  
                  Q_trans_s[i].append(Q_trans_s_aux)
                  Q_refl_s[i].append(Q_refl_s_aux)
                  Q_abs_s[i].append(Q_abs_s_aux)
                  Q_cond_s[i].append(Q_cond_s_aux)
                  Q_conv_s[i].append(Q_conv_s_aux)
                  Q_rad_sc_s[i].append(Q_rad_sc_s_aux)
                  Q_rad_ss_s[i].append(Q_rad_ss_s_aux)
                  gamma_s[i].append(gamma_s_aux)
                  T_s2[i].append(T_s2_aux)           
                                                  
                  # Balance energética a la cara inferior                
                  Q_cond_i_aux, Q_conv_i_aux, Q_rad_is_i_aux, gamma_i_aux, T_i2_aux = balanceCINFERIOR(T_i2[i][k],T_c2[i][k],self.h_conv[i][k],self.h_rad_is,self.U_i,T_ext[i][k],self.T_suelo,self.alto,self.ancho).calculo()              
                  Q_cond_i[i].append(Q_cond_i_aux)
                  Q_conv_i[i].append(Q_conv_i_aux)
                  Q_rad_is[i].append(Q_rad_is_i_aux)
                  gamma_i[i].append(gamma_i_aux)
                  T_i2[i].append(T_i2_aux)
                  
                  # Balance energético a la célula
                  T_c2_aux, gamma_c_aux = balanceCELULA(Q_trans_s_aux,P_aux,-Q_cond_s_aux, -Q_cond_i_aux, T_c2[i][k],self.alto,self.ancho).calculo()    
                  gamma_c[i].append(gamma_c_aux)
                  T_c2[i].append(T_c2_aux)
              T_c2[i].pop() 
              T_i2[i].pop()
              T_s2[i].pop()
          return P, I, V, Q_trans_s, Q_refl_s, Q_abs_s, Q_cond_s, Q_conv_s, Q_rad_sc_s, Q_rad_ss_s, gamma_s, T_s2, Q_cond_i, Q_conv_i, Q_rad_is, gamma_i, T_i2, T_c2  , gamma_c     
    