import engine
import numpy as np
import matplotlib.pyplot as plt

run_1 = engine.Engine()
run_1.initialize()
time_record, cord_record, v_record, acc_record = run_1.main()



## Display functions

def static_displays():

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = run_1.names[name_count])            
        name_count += 1
    plt.title("x")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("y")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("z")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("vx")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("vy")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("vz")
    plt.legend()
    plt.figure()
    
    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("ax")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("ay")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = run_1.names[name_count])
        name_count += 1
    plt.title("az")
    plt.legend()
    plt.show()
        
def active_display_2d():

    n = 0

    while True:
        name_count = 0
        for record in cord_record:
            if n <= len(record):
                plt.plot([record[i][0] for i in range(n)], [record[i][1] for i in range(n)])
                plt.scatter([record[n-1][0]], [record[n-1][1]], label = run_1.names[name_count])
                plt.legend()
                name_count += 1

        plt.gca().set_aspect('equal')
        plt.title(f"Time = {n*run_1.duration/run_1.datapoints/86400:.2f}days")
        plt.pause(0.04)
        plt.clf()
        n += 1
        if n > len(cord_record[0]):
            n = 0

def active_display_3d():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    n = 0
    plt.ion()

    while True:
        name_count = 0
        ax.clear()
        for record in cord_record:
            if n <= len(record):
                ax.plot3D([record[i][0] for i in range(n)], [record[i][1] for i in range(n)], [record[i][2] for i in range(n)])
                ax.scatter3D([record[n-1][0]], [record[n-1][1]], [record[n-1][2]], label = run_1.names[name_count])
                ax.legend()
                name_count += 1

        ax.set_title(f"Time = {n*run_1.duration/run_1.datapoints/86400:.2f}days")
        plt.pause(0.04)
        n += 1
        if n > len(cord_record[0]):
            n = 0
# static_displays()
# active_display_2d()
active_display_3d()