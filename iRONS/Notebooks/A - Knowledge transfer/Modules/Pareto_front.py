# -*- coding: utf-8 -*-
"""
This module is part of the iRONS toolbox by A. Peñuela and F. Pianosi at 
Bristol University (2021).

Licence: MIT
"""
import numpy as np

def compute_efficient_sol2(Y,e,n_max):

    """
    Find Pareto-efficient solutions of the multi-criteria optimization problem
    
       min y = f(z)
    
    where y = | y_1, y_2,..., y_q | and z belongs to a finite set (size: n).
    Minimization is performend by pairwise comparison.
    If "n" is large, pairwise comparison is computed iteratively within
    subsets that never exceeds the maximum number of elements "n_max".
    --------------------------------------------------------------------------
    
    Input/Output
    
    Y = double array of size (n,q)
      = | y_1(z1) y_2(z1) ... y_q(z1) |
        | y_1(z2) y_2(z2) ... y_q(z2) |
        |                 ...         |
        | y_1(zn) y_2(zn) ... y_q(zn) |
    
    e = double array of size (1,q)
      = | e_1       e_2   ... e_q     |
    epsilon precision for applying dominance criterion
    (if e=zeros(1,q) then Pareto-dominance is applied)
    
    n_max = scalar: maximum number of solutions that can be pairwise
    compared at each iteration.
    
    Y_eff = double array of size (nn,q) with objective values of the
    "nn" efficient solutions (Pareto frontier)
    
    Ieff  = double array of size (nn,1) with row indices of the original data
    matrix Y corresponding to efficient solutions.
    
    Example:
    M = np.random.rand(1000,3)
    d,eff=compute_efficient_sol(M,[0, 0, 0],1000)
    figure; plot3(M(:,1),M(:,2),M(:,3),'xr',M(eff,1),M(eff,2),M(eff,3),'.b')
    grid on; box on
    d,eff2=compute_efficient_sol(M,[0.01, 0.01, 0],1000)
    figure; plot3(M(:,1),M(:,2),M(:,3),'xr',M(eff,1),M(eff,2),M(eff,3),'.b',M(eff2,1),M(eff2,2),M(eff2,3),'.g'); grid on; box on
    """
    
    n,q = np.shape(Y)
    if n<=1 or q<=1:
        raise Exception('input Y must be a matrix')
    if len(e)!=q:
        raise Exception('The length of vector ''e'' must coincide with the number of columns in ''Y''')

    if len(np.unique(Y,axis = 0))<n:    
        raise Exception('all rows of matrix Y must be different')

    Yeff = Y          
    Ieff = np.transpose(range(n))   
    m = np.ceil(n/n_max)
    while m>1:  
        Y_ = Yeff
        I_ = Ieff
        j  = 0   
        for i in range(m):       
            Yi = Y_[n_max*(i):min(n_max*(i+1),n),:]
            Ii = I_[n_max*(i):min(n_max*(i+1),n)]
            di,effi = compute_efficient_sol(Yi,e)
            n_effi = np.sum(effi)
            Yeff[j:j+n_effi,:] = Yi[effi,:]
            Ieff[j:j+n_effi] = Ii[effi]  
            j = j+n_effi        
        end
        n = j # of detected efficient solutions
        Yeff = Yeff[0:n,:] 
        Ieff = Ieff[0:n] 
        m    = np.ceil(n/n_max) 

    d,eff = compute_efficient_sol(Yeff,e)
    Yeff  = Yeff[eff,:]
    Ieff  = Ieff[eff]
    
    return Yeff, Ieff

def compute_efficient_sol(M,e):
  
    n,q=np.shape(M)
    E = np.transpose(np.tile(np.reshape(e,[q,1]),n))
    d = np.zeros([n,n]) + np.nan
    for i in range(n):
        Y=np.transpose(np.tile(np.reshape(M[i,:],[q,1]),n))
        D=(Y+E>=M) * np.ones(np.shape(M))
        d[:,i]=np.sum(D,axis = 1)

    d=(d==q)
    
    # Meaning: if solution "i" dominates solution "j" then d(i,j)=1
    # otherwise d(i,j)=0
    
    eff=np.sum(d,axis=0)==1
    
    #Meaning: if there is only one nonzero element over a column of "d"
    #then it means that the corresponding solution is "dominated" by itself
    #only. In other terms, it is an efficient solution.
    #
    #If Pareto dominance criterion was used so far (i.e. sum(e)=0)
    #then the set of efficient solutions has been found.
    #However, if epsilon dominance was used, it may be that some
    #solutions do not appear in "eff" because epsilon-dominated by other
    #epsilon-dominated solutions but not from efficient solutions. 
    #These solutions should be found and added in the final set of efficient
    #solutions.
    #Example:
    #
    #M = 
    #   0.0046    0.3998   (1)
    #   0.7749    0.2599   (2)
    #   0.9619    0.0844   (3)
    #e =
    #   0.1       0.2
    #
    #(1) is epsilon dominant over (2), and (2) is epsilon dominant over (3).
    #It turns out that only solution (1) falls in "eff"
    #(because it is not epsilon dominated by any other solution), 
    #however we would like solution (3) to be also included in "eff"
    #because it is not epsilon dominated by (1)!

    if sum(e)>0:
        tmp = d*np.tile(np.reshape(eff,[n,1]),n) 
        # Meaning: if solution "i" dominates solution "j" AND
        # solution "i" is efficient, then d(i,j)=1
        # otherwise d(i,j)=0
        eps_eff = np.sum(tmp,axis = 0)==0
        # Meaning: find those solutions that are not epsilon-dominated by efficient
        # solutions...
        eff = eff + np.transpose(eps_eff)
        
    return d,eff

#M = np.random.rand(1000,3)
#Yeff, Ieff=compute_efficient_sol2(M,[0.001, 0.001, 0.001],1000)
#
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#import numpy as np
#
#
#def randrange(n, vmin, vmax):
#    '''
#    Helper function to make an array of random numbers having shape (n, )
#    with each number distributed Uniform(vmin, vmax).
#    '''
#    return (vmax - vmin)*np.random.rand(n) + vmin
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#
#n = 100
#
## For each set of style and range settings, plot n random points in the box
## defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
## for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#
#ax.scatter(M[:,0], M[:,1], M[:,2], c='yellow')
#ax.scatter(Yeff[:,0], Yeff[:,1], Yeff[:,2], c='black')
#
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
#
#plt.show()