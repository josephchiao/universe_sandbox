import numpy as np
import setup
import matplotlib.pyplot as plt

class Engine():

    """Runs the similation"""

    def __init__(self):
        ## Set up variables:
        self.dt = 10  ## Similation resolution, the time step for each physical similation
        self.duration = 3600000   ## in seconds -----> (10 ** 8 / 3) #1 years
        self.datapoints = 300  ## The number of data points. Not all similation points are recorded. 

        ## automated variables
        self.data_dt = int(self.duration / (self.dt * self.datapoints))


        ## Object variables
        self.names = ["Earth", "Moon", "Moon2"]
        self.x = [0, 384400000, -384400000]
        self.y = [0, 0, 0]
        self.z = [0, 0, 0]  
        self.dx = [0, 0, 0] 
        self.dy = [0, 1022, -1022]
        self.dz = [0, 0, 0] 
        self.mass = [5.972 * (10 ** 24), 7.34 * (10 ** 22), 7.34 * (10 ** 21)]
        self.size = [6371000, 1737400, 1737400]
        self.E_d = [2.25 * (10 ** 32), 1.2 * (10 ** 29), 1.2 * (10 ** 29)]   ## 1 kg tnt = 4184 kJ
        self.elaticity = [0.9, 0.9, 0.9]

    def initialize(self):
        self.space = setup.Space()
        self.objects = {self.names[i] : setup.Object(self.names[i], self.x[i], self.y[i], self.z[i], 
                                self.dx[i], self.dy[i], self.dz[i], 
                                self.mass[i], self.size[i], self.E_d[i], self.elaticity[i]) 
                                for i in range(len(self.x))}

    def main(self):

        cord_record = [[] for i in range(len(self.objects))]
        v_record = [[] for i in range(len(self.objects))]
        acc_record = [[] for i in range(len(self.objects))]
        time_record = []
        data_t = 0
        pop_pending = []
        stop = False

        while self.space.time < self.duration:
            i = 0
            for body in self.objects:
                collision = self.objects[body].time_step(self.dt, {self.objects[x].name:self.objects[x] for x in self.objects if x != body})
                
                if collision:
                    for c in collision:
                        stop = self.objects[body].collision_step(self.dt, c)
                        if stop:
                            break                
                if not data_t:
                    cord_record[i].append(np.array(self.objects[body].cord))
                    v_record[i].append(np.array(self.objects[body].velocity))
                    acc_record[i].append(np.array(self.space.gravity(self.objects[body].cord, {self.objects[x].name:self.objects[x] for x in self.objects if x != body})))
                i += 1

                if self.objects[body].destroyed:
                    pop_pending.append(self.objects[body].name)

            if not data_t:
                time_record.append(self.space.time)
                print("Running", len(cord_record[0]), "/", self.datapoints)           
                data_t = self.data_dt
        
            for body in pop_pending:
                self.objects.pop(body)
            pop_pending = []

            self.space.time += self.dt
            data_t -= 1
            if stop:
                print("Two body annihilation event. Engine stopped")
                break

        return time_record, cord_record, v_record, acc_record
            
