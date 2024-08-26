import numpy as np

safety1 = np.array([1,1,1,1])
bio = np.array([False,False,True,False])
inside = np.array([False,True,True,True])
#bio = np.array([0,0,1,0])
#inside = np.array([0,1,1,1])

mod1 = ~inside + ~bio
#with np.errstate(divide='ignore', invalid='ignore'):
#    mod2 = mod1/mod1
#mod3 = mod2.copy()
#mod3[np.isnan(mod3)] = 0
#safety2 = safety1 * mod3
safety2 = safety1 * mod1

