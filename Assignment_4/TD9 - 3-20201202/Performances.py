import numpy as np



def calcul_perfo(X,M,S,eff):
    Isp = eff*S[0]/X[3]*M[7]/9.80665
    mi = M[0]
    mf = M[1]
    Delta_V = 9.80665*Isp*np.log(mi/mf) #Tsiolkovsky formula
    #print(Delta_V,Isp,mi,mf)
    return Delta_V
    