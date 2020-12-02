
import numpy as np

def calcul_masse(X,parametres):
    
    # ENTREE :
    #  Dc : diamètre au col de tuyère (en m)
    #  mp : masse du bloc de poudre (en kg)
    #  Pc : pression de combustion (en bars)
    #  L0 : Longueur utile du bloc (en m)
    #  D0 : Diamètre hors tout du propulseur (en m)
    #
    # SORTIE :  
    #  M(1)       : Masse totale (kg)
    #  M(2)       : Masse sèche case (kg)
    #  M(3)       : Masses annexes (tuyère + allumeur) (kg)
    #  M(4)       : Contrainte de remplissage
    #  M(5)       : Contrainte de serrage
    #  M(6)      : Contrainte encombrement 1
    #  M(7)      : Contrainte encombrement 2
    #  M(8)      : Durée de combustion (en s)
    
    Dc = X[0]
    mp = X[1]
    Pc = X[2]
    L0 = X[3]
    D0 = X[4]
    
    m_payload = 500.
    
    Vref = parametres[0]
    Pref = parametres[1]
    n_ = parametres[2]
    c_etoile = parametres[3]
    ga = parametres[4]
    rhop = parametres[5]
    rhom = parametres[6]
    sigmar = parametres[7]
    eps = parametres[8]
    
    Crlim = 0.87
    rhopt = 1445.7
    Ac = np.pi*Dc**2./4.
    deb = Pc*100000.*Ac/c_etoile
    tc = mp/deb
    
    
    e = Pc*D0*eps/2./sigmar
    ept = 1.11/1000.


    Vp = mp/rhop
    Aport = np.pi*(D0-2.*(e+ept))**2./4. - Vp/L0
    Dport = np.sqrt(4.*Aport/np.pi)
    Scombeff = np.pi*Dport*L0
    a = Vref*Pref**(-n_)
    exposant1 = 1./(1.-n_)
    a2 = (a*(10**(-5))**n_)/1000.
    Kn = (Pc*100000.)**(1./exposant1)/(rhop*a2*c_etoile)
    Scomb = Kn*Ac
    Cr = mp/rhop/(L0*np.pi*(D0 - 2.*e - 2.*ept)**2.)*4.
    if (Scombeff <= 0):
        g1 = (Scomb - Scombeff)/Scomb
        g2 = (3.*Scombeff - Scomb)/Scomb
    else:
        g1 = (Scombeff - Scomb)/Scomb
        g2 = (Scomb - 3.*Scombeff)/Scomb

    M = np.zeros([8])
    M[0] = mp +1.05*( (rhom*e+rhopt*ept)*D0*np.pi*L0 + 2.*np.pi*D0**2./4.*e*rhom)+m_payload
    M[1] = 1.05*( (rhom*e+rhopt*ept)*D0*np.pi*L0 + 2.*np.pi*D0**2./4.*e*rhom)+m_payload
    M[2] = 0.05*(mp + (rhom*e+rhopt*ept)*D0*np.pi*L0+ 2.*np.pi*D0**2./4.*e*rhom)
    M[3] = (Cr-Crlim)/Crlim
    if Aport==0.:
        M[4] = Ac*1.3
    else:    
        M[4] = (Ac*1.3-Aport)/Aport 
    M[5] = g1
    M[6] = g2
    M[7] = tc
    
    return M