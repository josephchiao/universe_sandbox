import engine
import setup
import numpy as np
import matplotlib.pyplot as plt

space, objects = engine.initialize()
cord_record, v_record, acc_record, time_record = engine.main(space, objects)



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

n = 0

while True:
    for record in cord_record:
        plt.plot([record[i][0] for i in range(n)], [record[i][1] for i in range(n)])
        plt.scatter([record[n-1][0]], [record[n-1][1]])

    plt.gca().set_aspect('equal')
    plt.title(f"Time = {n*duration/datapoints/86400:.2f}days")
    plt.draw()
    plt.pause(0.04)
    plt.clf()
    n += 1
    if n > len(cord_record[0]):
        n = 0



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

# plt.show()