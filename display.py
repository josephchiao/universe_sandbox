import engine
import numpy as np
import matplotlib.pyplot as plt

def run_engine():

    run_1 = engine.Engine()
    run_1.initialize()
    time_record, cord_record, v_record, acc_record = run_1.main()
    return time_record, cord_record, v_record, acc_record, run_1.names, run_1.duration, run_1.datapoints

## Storage functions

def data_storage(file):
    time_record, cord_record, v_record, acc_record, names, duration, datapoints = run_engine()
    np.savez(file, time_record = time_record, cord_record = cord_record, v_record = v_record, acc_record = acc_record, names = names, duration = duration, datapoints = datapoints, allow_pickle=True)

def data_retrieval(file):
    
    data = np.load(file, allow_pickle=True)

    return data['time_record'], data['cord_record'], data['v_record'], data['acc_record'], data['names'], data['duration'], data['datapoints']

## Display functions

def static_displays(time_record, cord_record, v_record, acc_record, names):

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])            
        name_count += 1
    plt.title("x")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("y")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("z")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vx")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vy")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vz")
    plt.legend()
    plt.figure()
    
    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("ax")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("ay")
    plt.legend()
    plt.figure()

    name_count = 0
    plt.plot(time_record[0:len(cord_record[3])], [np.sqrt(np.sum(np.array(cord_record[10][i]-np.array(cord_record[3][i])) ** 2)) for i in range(len(cord_record[3]))])
    print('min distance =', min([np.sqrt(np.sum(np.array(cord_record[10][i]-np.array(cord_record[3][i])) ** 2)) for i in range(len(cord_record[3]))]) / 1000, 'km on day',  np.argmin([np.sqrt(np.sum(np.array(cord_record[10][i]-np.array(cord_record[3][i])) ** 2)) for i in range(len(cord_record[3]))]))
    plt.plot(time_record[0:len(cord_record[3])], np.zeros(len(cord_record[3])))
    plt.title('distance between earth and 16 Psyche')
    plt.figure()

    # ax = plt.axes(projection='3d')
    # while True:
    #     plt.cla()

    #     for i in range(3620, 3650):
    #         ax.scatter3D([cord_record[0][i][0]], [cord_record[0][i][1]], [cord_record[0][i][2]], label = f'Sun {i}', c = 'y')
    #         ax.scatter3D([cord_record[3][i][0]], [cord_record[3][i][1]], [cord_record[3][i][2]], label = 'Earth', c = 'b')
    #         ax.scatter3D([cord_record[10][i][0]], [cord_record[10][i][1]], [cord_record[10][i][2]], label = '16 Psyche', c = 'r')
    #         ax.legend()
    #         plt.pause(1)
    
    name_count = 0
    for record in acc_record:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("az")
    plt.legend()
    plt.show()
        
def active_display_2d(cord_record, names, duration, datapoints, leg = 300):

    count = len(cord_record[0])
    replay = True

    while replay:
        for n in range(count):
            name_count = 0
            plt.clf()
            for record in cord_record:
                if n <= len(record):
                    plt.plot([record[i][0] for i in range(max(0, n-leg), n)], [record[i][1] for i in range(max(0, n-leg), n)])
                    plt.scatter([record[n-1][0]], [record[n-1][1]], label = names[name_count], s = 10)
                    plt.legend()
                    name_count += 1

            plt.gca().set_aspect('equal')
            plt.title(f"Time = {n*duration/datapoints/86400:.2f}days")
            plt.pause(0.04)
        replay = input("Replay?") == ''



def active_display_3d(cord_record, names, duration, datapoints, leg = 300):
    ax = plt.axes(projection='3d')
    n = 0
    count = len(cord_record[0])
    plt.ion()
    replay = True

    while replay:
        for n in range(count):
            name_count = 0
            ax.clear()
            ax.set_box_aspect(np.ptp(np.array([record[i][0] for i in range(max(0, n-leg), n)])), np.ptp(np.array([record[i][1] for i in range(max(0, n-leg), n)])), np.ptp([record[i][2] for i in range(max(0, n-leg), n)]))
            for record in cord_record:
                if n <= len(record):
                    ax.plot3D([record[i][0] for i in range(max(0, n-leg), n)], [record[i][1] for i in range(max(0, n-leg), n)], [record[i][2] for i in range(max(0, n-leg), n)])
                    ax.scatter3D([record[n-1][0]], [record[n-1][1]], [record[n-1][2]], label = names[name_count])
                    ax.legend()
                    name_count += 1

            ax.set_title(f"Time = {n*duration/datapoints/86400:.2f}days")
            plt.pause(0.04)
        replay = input("Replay?") == ''

# static_displays()
# active_display_2d()
# active_display_3d()
data_storage("saved_data/psyche_position_10years_2.npz")
time_record, cord_record, v_record, acc_record, names, duration, datapoints = data_retrieval("saved_data/psyche_position_10years_2.npz")
# time_record, cord_record, v_record, acc_record, names, duration, datapoints = run_engine()


# active_display_2d(cord_record, names, duration, datapoints, leg=365)
static_displays(time_record, cord_record, v_record, acc_record, names)
# active_display_3d(cord_record, names, duration, datapoints)
