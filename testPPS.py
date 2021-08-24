from PPSclass  import PPS
import numpy as np
import time
from matplotlib import pyplot as plt

start = time.perf_counter()

sim = PPS(5, np.pi, 17/180*np.pi, 0.67)
sim.area_init(250,250)
#sim.particle_sys_init(N=12, method="center", a=0.8)
sim.particle_sys_init(density=0.04, method="random", a=20)

#print(X0)

sim.simulate(150)

end = time.perf_counter()
# print("N= ", sim.N)
print("Time elapsed: ", end-start)

# data = sim.get_data()
# X0, Y0, _  = data[0]
# plt.scatter(X0, Y0, color = 'g')
# plt.show()
x1, y1, Phi1 = sim.get_data()


#plot


i=0
alfa_offset = 8
for xt, yt in zip(x1,y1):
    i+=1
    plt.scatter(xt, yt, c='k', alpha=i/len(x1[:])/alfa_offset, marker='.', s=100)
plt.scatter(x1[-1], y1[-1], c='g', marker='.',s=100)
plt.xlim((0,sim.width))
plt.ylim((0,sim.heigth))
plt.show()
#save
sim.save_data("250x250test2")
