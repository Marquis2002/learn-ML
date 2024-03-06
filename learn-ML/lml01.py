import numpy as np
x = [1.7, 1.75, 1.65, 1.80, 1.78] # height data
su = np.sum(x)
m = np.mean(x)
vr = np.var(x) # variance
sd = np.std(x)  # standard deviation
print('su=',su, '\nnm=',m, '\nvar=',vr, '\nsd=',sd)

# nothing happened