from random import uniform
import numpy as np


class PPS:
    def __init__(self, r, alpha, beta, v):
        """
        Based on article:
        "Schmickl, T., Stefanec, M. & Crailsheim, K.
        How a life-like system emerges from a simplistic particle motion law.
        Sci Rep 6, 37969 (2016). https://doi.org/10.1038/srep37969"

        :param r: radius at which particles react to each other
        :param alpha: fixed rotation angle
        :param beta: rotation angle proportional to local neighbourhood size
        :param v: constant velocity at which particles move
        """
        self.r = r
        self.alpha = alpha
        self.beta = beta
        self.v = v
        self.X = []
        self.Y = []
        self.Phi = []
        #self.Pos = (self.X, self.Y)
        self.Data = []
        self.XT = []
        self.YT = []
        self.PhiT = []

        self.progress = 0

    def area_init(self, width, heigth):
        self.width = width
        self.heigth = heigth

    def particle_sys_init(self, N=None, density=None, method = "random", a=None):

        if N:
            self.N = N
            if method=="random":
                for i in range(N):
                    self.X.append(uniform(0,self.width))
                    self.Y.append(uniform(0,self.heigth))
                    self.Phi.append(uniform(-np.pi, np.pi))
            elif method=="center" and a:
                for i in range(N):
                    self.X.append(uniform(self.width/2 - a,self.width/2 + a))
                    self.Y.append(uniform(self.heigth/2 - a,self.heigth/2 + a))
                    self.Phi.append(uniform(-np.pi, np.pi))
            else: print("Wrong initialization method given! System not initialized!")
        elif density:
            Nt = int(density*self.width*self.heigth)
            self.N = Nt
            if method == "random":
                for i in range(Nt):
                    self.X.append(uniform(0,self.width))
                    self.Y.append(uniform(0,self.heigth))
                    self.Phi.append(uniform(-np.pi, np.pi))
            elif method == "center" and a:
                for i in range(N):
                    self.X.append(uniform(self.width / 2 - a, self.width / 2 + a))
                    self.Y.append(uniform(self.heigth / 2 - a, self.heigth / 2 + a))
                    self.Phi.append(uniform(-np.pi, np.pi))
            else:
                print("Wrong initialization method given! System not initialized!")

        else:
            print("Please input one of the parameters! System not initialized!" )
        print("Number of particles: ", self.N)
        #conversion to np array
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
        self.Phi = np.array(self.Phi)


    def move_particle(self,index):
        temp_x = self.X[index] + np.cos(self.Phi[index]) * self.v
        temp_y = self.Y[index] + np.sin(self.Phi[index]) * self.v

        if temp_x < 0: temp_x += self.width
        elif temp_x > self.width: temp_x -= self.width

        if temp_y < 0:  temp_y += self.heigth
        elif temp_y > self.heigth:  temp_y-= self.heigth

        self.X[index] = temp_x
        self.Y[index] = temp_y

    def circle_check(self,xr,yr,x,y, r):
        if (x-xr)**2 + (y-yr)**2 < r**2: return True
        else: return False

    def check_neighbours_r(self,r, index, t):
        """
        Searches for neighbours in given radius r, for particle of given index and time step t.
        :param r: radius of search
        :param index: particle index
        :param t: time step
        :return: number N of neighbours in radius r
        """
        x_indices = np.where((self.XT[t] < self.XT[t][index] + self.r) & (self.XT[t] > self.XT[t][index] - self.r))
        y_indices = np.where(
            (self.YT[t][x_indices] < self.YT[t][index] + self.r) & (self.YT[t][x_indices] > self.YT[t][index] - self.r))
        neighbours = x_indices[0][y_indices]

        neighbours = np.setdiff1d(neighbours, index, True)

        N = 0
        for i in neighbours:
            if self.circle_check(self.XT[t][index], self.YT[t][index], self.XT[t][i], self.YT[t][i], r):
                N += 1
        return N

    def check_neighbours(self, index, t = -1):
        x_indices = np.where((self.XT[t] < self.XT[t][index] + self.r) & (self.XT[t] > self.XT[t][index] - self.r) )
        y_indices = np.where((self.YT[t][x_indices] < self.YT[t][index] + self.r) & (self.YT[t][x_indices] > self.YT[t][index] - self.r) )
        neighbours = x_indices[0][y_indices]

        neighbours = np.setdiff1d(neighbours, index, True)

        N = 0
        L = 0
        R = 0
        angle = self.PhiT[t][index]
        for i in neighbours:
            if self.circle_check(self.XT[t][index], self.YT[t][index], self.XT[t][i], self.YT[t][i], self.r):
                #x_new = np.cos(angle)*self.X[i] - np.sin(angle)*self.Y[i]
                y_new = -np.sin(angle) * (self.XT[t][i] - self.XT[t][index]) + np.cos(angle) * (self.YT[t][i] - self.YT[t][index])
                if y_new > 0: L += 1
                else: R +=1
                N +=1
        return N, R, L, neighbours

    def evolve_particle(self, index):
        #main part of the code

        x_indices = np.where((self.X < self.X[index] + self.r) & (self.X > self.X[index] - self.r) )
        y_indices = np.where((self.Y[x_indices] < self.Y[index] + self.r) & (self.Y[x_indices] > self.Y[index] - self.r) )
        neighbours = x_indices[0][y_indices]

        neighbours = np.setdiff1d(neighbours, index, True)

        N = 0
        L = 0
        R = 0
        angle = self.Phi[index]
        for i in neighbours:
            if self.circle_check(self.X[index], self.Y[index], self.X[i], self.Y[i], self.r):

                #x_new = np.cos(angle)*self.X[i] - np.sin(angle)*self.Y[i]
                y_new = -np.sin(angle) * (self.X[i] - self.X[index])+ np.cos(angle) * (self.Y[i] - self.Y[index])
                if y_new > 0: L += 1
                else: R +=1
                N +=1

        #N -= 1
        #L -= 1
        #print("N=",N,"L=",L, "R=",R, "Phi=", self.Phi[index])
        delta_phi = self.alpha + self.beta * N * np.sign(R - L) #dać minus
        self.Phi[index] -= delta_phi

        self.move_particle(index)

    def simulate(self, T):
        """
        Runs full simulation of system set by __init__, area_init and particle_sys_init
        :param T: max time steps in simulation
         Saves data in XT, YT and PhiT in format: XT[t][i], where t - time step no, i - particle index
        """
        self.XT = np.zeros((T,self.N))
        self.YT = np.zeros((T,self.N))
        self.PhiT = np.zeros((T,self.N))

        self.XT[0][:] = self.X
        self.YT[0][:] = self.Y
        self.PhiT[0][:] = self.Phi



        order_list = np.arange(self.N)
        for t in range(T):
            np.random.shuffle(order_list)
            for i in order_list:
                #print("Particle ", i)
                self.evolve_particle(i)

            self.XT[t][:] = self.X
            self.YT[t][:] = self.Y
            self.PhiT[t][:] = self.Phi
            #self.Data = np.append(self.Data, [self.X, self.Y, self.Phi])
            print("Time:", t)
            self.progress = (t+1)/T
        self.save_data("tmp/last")

    def save_data(self, filename):
        settings = {"r":self.r,
                    "alpha": self.alpha,
                    "beta": self.beta,
                    "v": self.v,
                    "width": self.width,
                    "height": self.heigth,
                    "N": self.N}
        with open("data/"+filename, 'wb') as file:
            np.savez_compressed(file, self.XT, self.YT, self.PhiT, settings)


    def get_data(self):
        #return self.Data, self.XT, self.YT, self.PhiT
        return self.XT, self.YT, self.PhiT

    def get_progress(self):
        """
        Returns number of time steps 't' divided by maximum time specified in simulate function
        :return: float from 0 to 1 : (t+1)/T_max
        """
        return self.progress

    def get_color_indices(self, t, colors=["green","brown", "blue", "yellow", "magenta"]):
        """
        User inputs time step number and (optionally) five colors in string list.
        The "colors" parameter corresponds to 5 conditions that define how particles are colored, depending on
        number of neighbours(N) and radius (r), namely: (N_r)
        N_5 < 13 - first color, 13<=N_5<=15 - second, 15< N_5  <= 35 - third, N_5>35 - fourth and N_1.3 > 15 - fifth

        :param t: time/frame index from which color indices will be returned
        :param colors: (optional) list of 5 string, valid color names; if less than 5 given, warning raised and
        proceeds with default
        :return: dictionary in format: {"color_name": [list_of_indices]}, so that to each key (color) is assigned
        corresponding particle indices
        """

        ranges = [(0,12), (13,15), (16, 35), (36,np.inf), (16, np.inf)]
        if len(colors) != 5:
            colors=["green","brown", "blue", "yellow", "magenta"]
            raise Warning("Invalid number of color names, should be 5. Proceeding with standard colors.")
        r_list = [5,5,5,5,1.3]
        n_list5 = []
        for i in range(self.N):
            n= self.check_neighbours_r(5,i,t)
            n_list5.append(n)
        n_list13 = []
        for i in range(self.N):
            n= self.check_neighbours_r(1.3,i,t)
            n_list13.append(n)

        n_list5 = np.array(n_list5)
        n_list13 = np.array(n_list13)
        dict = {}
        for color, range_ in zip(colors[:-1], ranges[:-1]):
            temp_list = np.where( (n_list5 > range_[0]) & (n_list5 < range_[1] ) )
            dict.update( {color: temp_list} )
        temp_list = np.where( (n_list13 > ranges[-1][0]) & (n_list13 < ranges[-1][1] ) )
        dict.update({colors[-1]: temp_list})

        return dict



