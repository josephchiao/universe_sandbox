import numpy as np
import setup
import matplotlib.pyplot as plt
import pandas as pd

class Engine():

    """Runs the similation"""

    def __init__(self):
        ## Set up variables:
        self.dt =  -25  ## Similation resolution, the time step for each physical similation
        self.duration = -3650 * (24 * 60 * 60)   ## in seconds -----> (10 ** 8 / 3) #1 years
        self.datapoints = 3650  ## The number of data points. Not all similation points are recorded. 

        ## automated variables
        self.data_dt = int(self.duration / (self.dt * self.datapoints))


        # Object variables
        self.names =     ["Sun"                 , "Mercury"             , "Venus"               , "16 PSYCHE"           , "Earth"               , "Moon"                , "Mars"                , "Jupiter (Barycenter)", "Saturn (Barycenter)" , "Uranus (Barycenter)" , "Neptune (Barycenter)"]
        self.x =         [-9.345179560723215E+08, -3.066280020399633E+10,  4.241523780615441E+10, 1.332669484217063E+11 , 1.332669484217063E+11 , 1.335115538339742E+11 , 6.747943946041068E+10 , 2.386548507059724E+11 , 1.405290056341902E+12 , 1.696203015169804E+12 , 4.468466449028410E+12 ]
        self.y =         [-6.891997255130514E+08, -6.332461663911606E+10, -1.005141852451964E+11, 6.405022273790847+10  , 6.405722273790847E+10 , 6.432168012177803E+10 , 2.171314908655735E+11 , 7.171570159775424E+11 , -3.250368810142248E+11, 2.384013498889377E+12 , -1.305536792859370E+11]
        self.z =         [2.808020552381236E+07 , -2.363815633173857E+09, -3.844209582780004E+09, 2.340600043957308E+07 , 2.340600043957308E+07 , 4.515263670701534E+07 , 2.914625644065842E+09 , -8.314200237697065E+09, -5.030003745278995E+10, -1.312041863176441E+10, -1.002918467490595E+11]
        self.dx =        [1.171141409503890E+01 , 3.421324448497383E+04 ,  3.189997653124255E+04, -1.340830383006313E+04, -1.340830383006313E+04, -1.418075387469403E+04, -2.218867871956940E+04, -1.254494990218617E+04, 1.639431222382655E+03 , -5.598938405448334E+03, 1.228527312837289E+02 ]
        self.dy =        [-7.773267888831897E+00, -1.852574578279112E+04,  1.382298194466176E+04, 3.540012015024854E+04 , 2.670012015024854E+04 , 2.746602153275207E+04 , 9.312690164420285E+03 , 4.748026448354953E+03 , 9.391318109935765E+03 , 3.630556819941044E+03 , 5.465190553250536E+03 ]
        self.dz =        [-1.770867040567239E-01, -4.650535104571055E+03, -1.650210517407690E+03, -2.553271354706510E+00, -2.553271354706510E+00, 7.521965462881575E+01 , 7.396309725474666E+02 , 2.609964785616201E+02 , -2.285802336714240E+02, 8.601588286213824E+01 , -1.153768490097717E+02]
        self.mass =      [1988500E+24           , 3.302E+23             , 48.685E+23            , 2.29E+19              , 5.97219E+24           , 7.349E+22             , 6.4171E+23            , 1.89818722E+27        , 5.6834E+26            , 86.813E+24            , 102.409E+24           ]
        self.size =      [695700000             , 2439340               , 6051840               , 111000                , 6371010               , 1737530               , 3389920               , 69911000              , 58232000              , 25362000              , 24624000              ]    ## Radius in meters
        self.E_d =       [float('inf')          , 1.7887880495543877e+30, 1.5674005523031013e+32, 9.453553243243244e+22 , 2.2404539891036462e+32, 1.2439452533308777e+29, 4.861443573441852e+30 , 2.0625745759794106e+36, 2.2198918860956182e+35, 1.1892224930974686e+34, 1.7044910790514136e+34]    ## 1 kg tnt = 4184 kJ
        self.elaticity = [0                     , 0                     , 0                     , 0                     , 0                     , 0                     , 0                     , 0                     , 0                     , 0                     , 0                     ] 
        self.grav_sig =  [True                  ,True                   ,True                   , False                 ,True                   ,True                   ,True                   ,True                   ,True                   ,True                   ,True                   ]



    def initialize(self):
        self.space = setup.Space()
        self.objects = {self.names[i] : setup.Object(self.names[i], self.x[i], self.y[i], self.z[i], 
                                self.dx[i], self.dy[i], self.dz[i], 
                                self.mass[i], self.size[i], self.E_d[i], self.elaticity[i], self.grav_sig[i]) 
                                for i in range(len(self.x))}

    def main(self):

        cord_record = [[] for i in range(len(self.objects))]
        v_record = [[] for i in range(len(self.objects))]
        acc_record = [[] for i in range(len(self.objects))]
        time_record = []
        data_t = 0
        pop_pending = []
        stop = False

        while self.space.time > self.duration:  ## < in normal time, > in reverse time. 
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
            
