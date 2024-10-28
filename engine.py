import numpy as np
import setup

class Engine():

    """Runs the similation"""

    def __init__(self):

        ## Set up variables:
        self.dt =  1  ## Similation resolution, the time step for each physical similation
        self.duration = 30 * (24 * 60 * 60)   ## total duration of the similation in seconds
        self.datapoints = 300  ## The number of data points. Not all similation points are recorded. 

        ## automated variables
        self.data_dt = int(self.duration / (self.dt * self.datapoints))

### Collision test system (Throw the moon at Earth)
        self.names = ["Earth", "Moon"]
        self.x = [0, 384400000]
        self.y = [0, 300000000]
        self.z = [0, 0]  
        self.dx = [0, 0] 
        self.dy = [0, 0]
        self.dz = [0, 0] 
        self.mass = [5.972 * (10 ** 24), 7.34 * (10 ** 22)]
        self.size = [6371010, 1737530]
        self.E_d = [2.2404539891036462e+32, 1.2439452533308777e+29]   ## 1 kg tnt = 4184 kJ
        self.elaticity = [0, 0]        
        self.grav_sig =  [True ,True ]


    def initialize(self):

        ## To properly setup the engine, 
        ## Initiating a space class for all the objects to share.
        ## Initiating a dictionary of objects

        self.space = setup.Space()
        self.objects = {self.names[i] : setup.Object(self.names[i], self.x[i], self.y[i], self.z[i], 
                                self.dx[i], self.dy[i], self.dz[i], 
                                self.mass[i], self.size[i], self.E_d[i], self.elaticity[i], self.grav_sig[i]) 
                                for i in range(len(self.x))}

    def main(self):
        
        ## Where everything happens

        ## Local variables
        cord_record = [[] for i in range(len(self.objects))]
        v_record = [[] for i in range(len(self.objects))]
        acc_record = [[] for i in range(len(self.objects))]
        time_record = []
        collision_record = []
        data_t = 0
        pop_pending = []
        stop = False

        ## Time step while similation duration is not reached
        while self.space.time < self.duration:  ## < in normal time, > in reverse time. 
            i = 0
            for body in self.objects:  ## Cycle through each objects in space
                if not self.objects[body].destroyed:
                    
                    collision = self.objects[body].time_step(self.dt, {self.objects[x].name:self.objects[x] for x in self.objects if x != body and not self.objects[x].destroyed})
                    
                    if collision:
                        for c in collision:
                            
                            ## Execute collision
                            stop, stats = self.objects[body].collision_step(self.dt, c, self.objects)
                            stats.insert(1, self.space.time)
                            collision_record.append(stats)

                            ## If both objects are destroyed, stop similation.
                            if stop:
                                break  
                            
                            ## If an object is destroyed, mark its destruction. 
                            if self.objects[body].destroyed:
                                pop_pending.append(self.objects[body].name)
                            elif c.object_2.destroyed:
                                pop_pending.append(c.object_2.name)
                
                if not data_t:  ## Data recording interval
                    cord_record[i].append(np.array(self.objects[body].cord))
                    v_record[i].append(np.array(self.objects[body].velocity))
                    acc_record[i].append(np.array(self.space.gravity(self.objects[body].cord, {self.objects[x].name:self.objects[x] for x in self.objects if x != body and not self.objects[x].destroyed})))
                
                i += 1

            ## Record timestamp
            if not data_t:
                time_record.append(self.space.time)
                print("Running", len(cord_record[0]), "/", self.datapoints)           
                data_t = self.data_dt

            ## Remove bodies that have been destroyed
            for body in pop_pending:
                self.objects[body].cord = [None, None, None]
                self.objects[body].velocity = [None, None, None]
            pop_pending = []

            ## Progress time
            self.space.time += self.dt
            data_t -= 1

            ## Check for stop condition
            if stop:
                print("Two body annihilation event. Engine stopped")
                break

        return time_record, cord_record, v_record, acc_record, collision_record
            
