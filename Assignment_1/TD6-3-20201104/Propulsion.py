from scipy.optimize import fsolve
import numpy as np



def calcul_poussee(X,parametres):
    
    # ENTREE :
    #  Dc : diamètre au col de tuyère (en m)
    #  Ds : diamètre du sortie de tuyère (en m)
    #  Pc : pression de combustion (en bars)
    #  Pa : pression ambiante de dimensionnement (en bars)
    #  

    # SORTIE :  
    #  S(1)       : Poussée (N)
    #  S(2)       : Indicateur Pc/Pa
    #  S(3)       : Indicateur As/Ac
    #  S(4)       : Indicateur Ps/Pc
    #  S(5)       : Indicateur Cf 
    
    
    Dc = X[0]
    Ds = X[1]
    Pa = X[2]
    Pc = X[3]
    
    Vref = parametres[0]
    Pref = parametres[1]
    n_ = parametres[2]
    c_etoile = parametres[3]
    ga = parametres[4]
    rhop = parametres[5]
    
    Ac = np.pi*Dc**2./4.
    As = np.pi*Ds**2./4.
    epsilon = As/Ac
    
    a_ = Vref*Pref**(-n_)
    exposant1 = 1./(1.-n_)
    a2 = (a_*(10.**(-5.))**n_)/1000.
    Kn = (Pc*100000.)**(1./exposant1)/(rhop*a2*c_etoile)
    
    Cf = 0.
    if (Pc > 1.1*Pa):
        if(As/Ac < 1.1):
            Ps = 1.01*Pc
        else:
            Ps = Pc/nari(ga,As/Ac)    
    
        if (Ps > 0.9*Pc):
            F = 0.
        else:
            Cf = cf(1,ga,Pc/Ps,Pc/Pa,As/Ac)
        
            if (Cf > 0.):
                F = 0.98*Cf*Pc*Ac*100000.
            else:
                F = 0.
    
    else:
        F = 0.
        Ps = Pa
#    Ps = Pc/nari(ga,As/Ac)
#    Cf = cf(1,ga,Pc/Ps,Pc/Pa,As/Ac)
#    F = 0.98*Cf*Pc*Ac*100000.
#    
#    if (Pc > 1.1*Pa):
#            if(As/Ac < 1.1):
#                Ps = 1.01*Pc 
    dc1 = (1.1*Pa - Pc)/Pa
    dc2 = 1.1 - As/Ac
    dc3 = (Ps - 0.9*Pc)/Pc
    dc4 = -Cf/2.
    
    S = np.zeros([5])
    S[0] = F
    S[1] = dc1
    S[2] = dc2
    S[3] = dc3
    S[4] = dc4
    
    return S


    
def nari(Gama,Ae_At):
    
    lb = 1.8
    up = 10000000
    x0 = 2.
    f = lambda x : fuser(x,Gama,Ae_At)
    Pc_Pe = fsolve(f,x0)

    return Pc_Pe

def fuser(Pc_Pe,Gama,Ae_At):
    
    y = nar(Gama,Pc_Pe)-Ae_At
    
    return y


def nar(Gama, Pc_Pe):
    k1 = 1./(Gama - 1.)
    k2 = 1./Gama
    k3 = (Gama- 1.)/Gama
    Ae_At = ((2./(Gama + 1.))**k1 * Pc_Pe**k2)/np.sqrt(((Gama + 1.)/(Gama-1.))*(1.-(1./Pc_Pe)**k3))

    return Ae_At

    
def cf(Lambda,Gama,Pc_Pe,Pc_Pa,Ae_At):
    
    pe_pc = 1. / Pc_Pe
    pa_pc = 1. / Pc_Pa

    k1 = (Gama - 1.) / Gama
    k2 = (Gama + 1.) / 2. / (Gama - 1.)
    Ct = Lambda * Gama * np.sqrt( (2. / (Gama - 1.)) * (1. - pe_pc ** k1)) /((Gama + 1.) / 2.) ** k2 + Ae_At * (pe_pc - pa_pc)
    
    return Ct
