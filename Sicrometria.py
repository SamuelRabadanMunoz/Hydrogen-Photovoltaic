# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:28:38 2021

@author: SAMUEL
"""

class Sicro():  # ECUACIÓN ANTONIE

    def __init__(self,T = None, HR = None, W = None, A =8.071, B =1730.63, C = 233.426, Patm_mmHg = 760):
        self.A = A
        self.B = B
        self.C = C
        self.Pt = Patm_mmHg
        self.T = T
        self.HR = HR
        self.W = W
   
    def calculo_W(self):

        Pvs = 10**(self.A - self.B/(self.C+self.T)) # mmHg
        Pv = self.HR*Pvs/100   
        W  =(0.62198*Pv/(self.Pt-Pvs))*1000
        return W
    
    def calculo_T(self):
        import math  
        Pvs = (self.W*self.Pt)/(621.98*self.HR/100 + 1)
        T = -self.B/(math.log10(Pvs)-self.A)-self.C
        return T
   


