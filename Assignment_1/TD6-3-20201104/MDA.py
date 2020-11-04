# OBJET :   Calcul de la poussee et du GLOW 
#           d'un propulseur a poudre      
#
# USAGE :   [Obj,Cons] = Booster(X_)
#
# ENTREE : 
#  X_(1) : Dc : diametre au col de tuyere (en m) -- normalise 0 < X_(1) < 1 -- denormalise -- 0.05 < Dc < 1
#  X_(2) : Ds : diametre du sortie de tuyere (en m) -- normalise 0 < X_(2) < 1 -- denormalise -- 0.5 < Ds < 1.2
#  X_(3) : Pc : pression de combustion (en bars) -- normalise 0 < X_(3) < 1 -- denormalise -- 1 < Pc < 500
#  X_(4) : mp : masse de poudre embarquée (en kg) -- normalise 0 < X_(4) < 1 -- denormalise -- 10000 < mp < 15000
# 
# SORTIE :  
#  Objs  : Obj1 = - Poussee (N), Obj2 = GLOW (kg)
#  Cons  : vecteur des contraintes (dimension = 8) (G(X,Z)<=0 faisable)
import numpy as np
import Masse
import Propulsion
import Performances
def Booster(X_):
    
    
    lb_bnd = np.array([0.2,0.5,5,10000])
    up_bnd = np.array([1,1.2,100,15000])
    
    X = lb_bnd + (up_bnd - lb_bnd)*X_
    
    Z = np.array([0,0,0]) #Choix des technologies

    # Choix du type de grain
    np_ = Z[0]  #0: Butalite, 1 : Butalane, 2 : Nitramite, 3 : pAIM-120
    # Choix des matériaux
    nm = Z[1]  # 0: Acier, 1: Aluminium
    # Choix du nombre de moteurss
    nmot = Z[2] #0: Moteur 1, 1: Moteur 2, 2: Moteur 3
    
    
    propergols=np.array([[1,2698.,1.22,0.0244,1598.,14.500,5000000.,0.40,1469.69150388984],
    [2,3384.,1.14,0.0276,1766.,14.50,5000000.,0.40,1585.94906686235],
    [3,3160,1.18,0.025,1757.,14.50,5000000.,0.40,1590.28799661913],
    [4,3000.,1.18,0.0265, 1729.98,8.8646,6894760.,0.40,1504.18794586416]])
    
    
    Vref = propergols[np_,5]
    Pref = propergols[np_,6]/100000
    n_ = propergols[np_,7]
    c_etoile = propergols[np_,8]
    ga = propergols[np_,2]
    rhop = propergols[np_,4]
    
    if nm==0: #Acier
        rhom = 7830.
        sigmar = 11000.
        eps = 1.3
    elif nm==1: #Aluminium
        rhom = 2800.
        sigmar = 4000.
        eps = 1.5
        
    if nmot==0: 
        eff = 0.95
        m_penal = 0.90
    elif nmot ==1: 
        eff = 1.0
        m_penal = 1.0
    elif nmot ==2: 
        eff = 1.05
        m_penal = 1.1


    parametres = np.array([Vref,Pref,n_,c_etoile,ga, rhop,rhom,sigmar,eps])
        
    Xp = np.zeros([4]) 
    Xp[0] = X[0]
    Xp[1] = X[1]
    Xp[2] = 0.83
    Xp[3] = X[2]
    S = Propulsion.calcul_poussee(Xp,parametres) 
    
    Xm = np.zeros([5])
    Xm[0] = X[0]
    Xm[1] = X[3]
    Xm[2] = X[2]
    Xm[3] = 11.
    Xm[4] = 1.07
    M = Masse.calcul_masse(Xm,parametres)


    Delta_V = Performances.calcul_perfo(X,M,S,eff)
    
    Obj2 = M[0]
    
    Cons = np.zeros([8])
    Cons[0] = S[1]
    Cons[1] = S[2]
    Cons[2] = S[3]
    Cons[3] = S[4]
    Cons[4] = M[3]
    Cons[5] = M[4]
    Cons[6] = M[5]
    Cons[7] = M[6]
    
    
    Obj1=-Delta_V/1000.
    Obj2=Obj2/1e3
    Cons[0]=Cons[0]*1/120.
    Cons[1]=Cons[1]*1/35.
    Cons[5]=Cons[5]*1/34.
    Cons[6]=Cons[6]*1/20.
    Cons[7]=Cons[7]*1/60.
    return [Obj1,Obj2], Cons