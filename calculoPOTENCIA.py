# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 08:47:18 2021

@author: SAMUEL
"""


import math
from scipy.optimize import fsolve, root




class calculoPOTENCIA(): ## Cálulo de la potencia, intensidad y tensión de cada placa fotovoltaica por el método de las 4 variables. Resolución mediante Levenberg-Marquardt 
    def __init__(self,G,Ns, Voc_ref, Isc_ref, Vmpp_ref, Impp_ref, eta_Voc, eta_Isc, T_c):
        self.Ns =  Ns
        self.G = G
        self.Voc_ref = Voc_ref
        self.Isc_ref = Isc_ref
        self.Vmpp_ref = Vmpp_ref
        self.Impp_ref = Impp_ref
        self.eta_Voc = eta_Voc
        self.eta_Isc = eta_Isc
        self.T_c = T_c
        
    def calculo(self):
        # Constantes
        e = 1.6*10**(-19)
        k = 1.381*10**(-23)
        G_ref = 1000
        Eq = 1.12 # Banda prohibida del Silicio
        Tc_ref = 25+273 # Temperatura de los valores de referencia        
        n = 1  # Factor idealidad del diodo
        tau = 0.23 # Transmisividad del silicio
        rho = 0.075 # Reflectividad del silicio    
        alpha = 1 - tau - rho # Absortividad del silicio
        self.G = self.G*alpha  # Radiación absorbida por el silicio
        
        # Temperatura        
        T_c = self.T_c+273
        # Placa fotovoltaica       
       
        V = self.Vmpp_ref+self.eta_Voc*(T_c-Tc_ref) # Tensión en función de la temperatura
        V_t = k*T_c/e  # Voltaje térmico
        
        
        # >> Valores de referencia según ficha técnica <<
        
        a_ref = 1.5
        t_1 = self.Isc_ref
        t_2 = math.exp(self.Voc_ref/a_ref)-1
        I0_ref = t_1/t_2
        
        t_1 = (a_ref*math.log(1-(self.Impp_ref/self.Isc_ref)))-self.Vmpp_ref+self.Voc_ref
        t_2 = self.Impp_ref
        Rs_ref = t_1/t_2
        Rs = Rs_ref
        def f(s):
            # 
            I_L = s[0]
            I_0 = s[1]
            a = s[2]
            f1 = ((self.G/G_ref)*(self.Isc_ref+self.eta_Isc*(T_c-Tc_ref)))-I_L
            
            f2 = (I0_ref*((T_c/Tc_ref)**3)*math.exp(((Eq*self.Ns)/a)*(1-(Tc_ref/T_c))))-I_0
            f3 = (a_ref*(T_c/Tc_ref))-a
            return f1, f2, f3
      
        semilla = [7.7,1*10**(-5),1.5]
        sol = root(f,semilla, method = 'lm')             
        I_L = sol.x[0]
        I_0 = sol.x[1]
        a = sol.x[2]     
        def f_I(y):
            I = y[0]            
            f6 = I_L-I_0*(math.exp((V+I*Rs)/(self.Ns*n*V_t+0.1))-1)-I
            return f6
        semilla = self.Impp_ref
        sol_2 = root(f_I,semilla, method = 'lm')
        I = sol_2.x[0]
        P = I*V
        if self.G == 0:
            P = 0
            I = 0
            V = 0
        if P <= 0:
            P = 0
            I = 0
            V = 0            
        return P, I , V
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# Impp = self.Impp_ref*(I_sc/self.Isc_ref)
# Vmpp = self.Voc_ref

# I_sc = (self.Isc_ref*(G/G_ref))+self.eta_Isc*(T_c-Tc_ref)

# def f(s):  
#     I_L = s[0]
#     I_0 = s[1]
#     R_s = s[2]
#     m = s[3]
#     V_oc = s[4]
#     f1 = (I_sc*(1+(R_s/R_sh))+I_0*(math.exp((I_sc*R_s)/(m*V_t))-1))-I_L
#     f2 = ((I_sc-(V_oc/R_sh))*math.exp(-(V_oc/(m*V_t))))-I_0
#     f3 = (R_so-(((m*V_t)/I_0)*math.exp(-(V_oc/(m*V_t)))))-R_s
#     f4 =((Vmpp+(Impp*R_so)-V_oc)/(V_t*(math.log(I_sc-(Vmpp/R_sh)-Impp)-math.log(I_sc-(V_oc/R_sh))+(Impp/(I_sc-(V_oc/R_sh))))))-m
#     f5 = (self.Voc_ref+(m*V_t*math.log(G/G_ref))+self.eta_Voc*(T_c-Tc_ref))-V_oc
#     return f1, f2, f3, f4, f5



# def f_I(y):
#     I = y[0]
#     V = y[1]
#     f6 = I_L-I_0*(math.exp((V+I*R_s)/(self.Ns*n*V_t))-1)-((V+I*R_s)/R_sh)-I
#     return f6
# # I = []
# # V = []


















#### FICHA
# e = 1.6*10**(-19)
# k = 1.381*10**(-23)
# m = 1
# Eq = 1.12



# >> Cálculo depediendo de G y de T

# a = a_ref*(T_c/Tc_ref)

# I_L = (G/G_ref)*(self.Isc_ref+self.eta_Isc*(T_c-Tc_ref))

# t_1 = I0_ref
# t_2 = (T_c/Tc_ref)**3
# t_3 = math.exp((Eq*self.Ns/a)*(1-(Tc_ref/T_c)))
# I_0 = t_1*t_2*t_3



# intesidad = solve(I_L-(I_0*(math.exp((e*(V+I*Rs_ref))/(k*T_c))-1))-I,I)
# V_oc, Rs, m, I_L, I_0 = var('V_oc Rs m I_L I_0')


















