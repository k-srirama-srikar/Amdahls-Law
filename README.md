# Ahmdal's Law


## About Ahmdal's Law
Gene Ahmdal, one of the early pioneers of computing made a simple but insightful observation about the effectiveness of improving the performance of one part of a system.

The idea is that we speed up one part of the, the effect on the overall system performance depends on both how significant this part was and how much it sped up.

Consider a system executes an application program in time $T_old$ and a fraction $\alpha$ of this time is required by some part of the system and now we improve it's performance by a factor $k$. Now the overall execution time would be, \
$T_new = (1-\alpha)T_old + (\alpha T_old)/k$ \
$= T_old[(1-\alpha)+\alpha/k]$ 

From this we compute the speed up as $S = T_{old}/T_{new}$ \
$S =  \frac{1, (1-\alpha)+\alpha/k}$
