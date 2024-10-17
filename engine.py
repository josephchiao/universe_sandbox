import numpy as np
import setup
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

## Set up variables:
dt = 100
duration = 3600000   ## in seconds -----> (10 ** 8 / 3) #1 years
datapoints = 300

## automated variables
data_dt = int(duration / (dt * datapoints))
cord_record = []
v_record = []
time_record = [data_dt * i for i in range(datapoints)]

## Objects
names = ["Earth", "Moon", "Space station"]
x = [0, 384400000, 384400000]
y = [0, 0, 50000000]
z = [0, 0, 0]  
dx = [0, 0, 312.9] ##312.9
dy = [0, 1022, 1022]
dz = [0, 0, 0] 
mass = [5.972 * (10 ** 24), 7.34 * (10 ** 22), 50]
size = [6371000, 1737000, 100]
E_d = [2.25 * (10 ** 32), 1.2 * (10 ** 29), 418400]   ## 1 kg tnt = 4184 kJ
elaticity = [0, 0, 0]

def initialize():
    space = setup.Space()
    objects = [setup.Object(names[i], x[i], y[i], z[i], 
                            dx[i], dy[i], dz[i], 
                            mass[i], size[i], E_d[i], elaticity[i]) 
                            for i in range(len(x))]
    return space, objects

def main(space, objects):
    cord_record = [[] for i in range(len(objects))]
    v_record = [[] for i in range(len(objects))]
    acc_record = [[] for i in range(len(objects))]
    data_t = 0
    while space.time < duration:
        i = 0
        for object in objects:
            object.time_step(dt, [x for x in objects if x != object])
            # collided, target, output_1, output_2 = object.time_step(dt, [x for x in objects if x != object])
            # if collided:
            #     objects.remove(object)
            #     objects.remove(target)
            #     if output_1 is not None:
            #         objects.append(output_1)
            #     if output_2 is not None:
            #         objects.append(output_2)
                
            if not data_t:
                cord_record[i].append(np.array(object.cord))
                v_record[i].append(np.array(object.velocity))
                # acc_record[i].append(np.array(space.gravity(object.cord, [x for x in objects if x != object])))
            i += 1
        if not data_t:
            print("Running", len(cord_record[0]), "/", datapoints)           
            data_t = data_dt

        space.time += dt
        data_t -= 1
    
    return cord_record, v_record, acc_record
        
space, objects = initialize()
cord_record, v_record, acc_record = main(space, objects)



## Display function

for record in cord_record:
    plt.plot(time_record, [record[i][0] for i in range(len(record))])
plt.title("x")
plt.legend([f"Object {i + 1}" for i in range(len(x))])
plt.figure()

# for record in cord_record:
#     plt.plot(time_record, [record[i][1] for i in range(len(record))])
# plt.title("y")
# plt.legend([f"Object {i + 1}" for i in range(len(x))])
# plt.figure()

# for record in cord_record:
#     plt.plot(time_record, [record[i][2] for i in range(len(record))])
# plt.title("z")
# plt.legend([f"Object {i + 1}" for i in range(len(x))])
# plt.figure()

# for record in v_record:
#     plt.plot(time_record, [record[i][0] for i in range(len(record))])
# plt.title("dx")
# plt.legend([f"Object {i + 1}" for i in range(len(x))])
# plt.figure()

# for record in cord_record:
#     plt.plot([record[i][0] for i in range(len(record))], [record[i][1] for i in range(len(record))])
#     plt.scatter([record[-1][0]], [record[-1][1]])
# plt.figure()

# for record in cord_record:
#     plt.plot([record[i][0] for i in range(len(record))], [record[i][1] for i in range(len(record))])
#     plt.scatter([record[-1][0]], [record[-1][1]])
# plt.figure()

# n = 0

# while True:
#     for record in cord_record:
#         plt.plot([record[i][0] for i in range(n)], [record[i][1] for i in range(n)])
#         plt.scatter([record[n-1][0]], [record[n-1][1]])

#     plt.gca().set_aspect('equal')
#     plt.title(f"Time = years")
#     plt.draw()
#     plt.pause(0.04)
#     plt.clf()
#     n += 1
#     if n > len(cord_record[0]):
#         n = 0



# for record in v_record:
#     plt.plot(time_record, [record[i][1] for i in range(len(record))])
# plt.title("dy")
# plt.legend([f"Object {i + 1}" for i in range(len(x))])
# plt.figure()

# for record in v_record:
#     plt.plot(time_record, [record[i][2] for i in range(len(record))])
# plt.title("dz")
# plt.legend([f"Object {i + 1}" for i in range(len(x))])
# plt.figure()

# plt.plot(time_record, [cord_record[2][i][0]-cord_record[1][i][0] for i in range(len(cord_record[2]))])
# plt.plot(time_record, [cord_record[2][i][1]-cord_record[1][i][1] for i in range(len(cord_record[2]))])
# plt.plot(time_record, [0 for i in range(300)])
# plt.figure()

# plt.plot(time_record, np.sqrt(np.array([cord_record[2][i][0]-cord_record[1][i][0] for i in range(len(cord_record[2]))]) ** 2
#          + np.array([cord_record[2][i][1]-cord_record[1][i][1] for i in range(len(cord_record[2]))]) ** 2) )

plt.show()

