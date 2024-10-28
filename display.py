import engine
import numpy as np
import matplotlib.pyplot as plt

def run_engine():

    run_1 = engine.Engine()
    run_1.initialize()
    time_record, cord_record, v_record, acc_record, collision_record = run_1.main()
    return time_record, cord_record, v_record, acc_record, run_1.names, run_1.duration, run_1.datapoints, collision_record

## Storage functions

def data_storage(file):
    time_record, cord_record, v_record, acc_record, names, duration, datapoints, collision_record = run_engine()
    np.savez(file, time_record = time_record, cord_record = cord_record, v_record = v_record, acc_record = acc_record, names = names, duration = duration, datapoints = datapoints, collision_record = collision_record, allow_pickle=True)

def data_retrieval(file):
    
    data = np.load(file, allow_pickle=True)

    return data['time_record'], data['cord_record'], data['v_record'], data['acc_record'], data['names'], data['duration'], data['datapoints'], data['collision_record']

## Display functions

def static_displays(time_record, cord_record, v_record, acc_record, names, items = 0):

    if items == 0:
        items = len(cord_record)

    name_count = 0
    for record in cord_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])            
        name_count += 1
    plt.title("x")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("y")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in cord_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("z")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vx")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vy")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in v_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("vz")
    plt.legend()
    plt.figure()
    
    name_count = 0
    for record in acc_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][0] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("ax")
    plt.legend()
    plt.figure()

    name_count = 0
    for record in acc_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][1] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("ay")
    plt.legend()
    plt.figure()

    # name_count = 0
    # plt.plot(time_record[0:len(cord_record[4])], [np.sqrt(np.sum(np.array(cord_record[5][i]-np.array(cord_record[4][i])) ** 2)) for i in range(len(cord_record[4]))])
    # print('min distance =', min([np.sqrt(np.sum(np.array(cord_record[5][i]-np.array(cord_record[4][i])) ** 2)) for i in range(len(cord_record[4]))]) / 1000, 'km on day',  np.argmin([np.sqrt(np.sum(np.array(cord_record[5][i]-np.array(cord_record[4][i])) ** 2)) for i in range(len(cord_record[4]))]))
    # plt.plot(time_record[0:len(cord_record[4])], np.zeros(len(cord_record[4])))
    # plt.title('distance between earth and astroid')
    # plt.figure()

    # ax = plt.axes(projection='3d')
    # while True:
    #     plt.cla()

    #     for i in range(1800, 1850):
    #         ax.scatter3D([cord_record[-1][i][0]], [cord_record[-1][i][1]], [cord_record[-1][i][2]], label = f'Sun {i}', c = 'y')
    #         ax.scatter3D([cord_record[-4][i][0]], [cord_record[-4][i][1]], [cord_record[-4][i][2]], label = 'Earth', c = 'b')
    #         ax.scatter3D([cord_record[-5][i][0]], [cord_record[-5][i][1]], [cord_record[-5][i][2]], label = '16 Psyche', c = 'r')
    #         ax.scatter3D([cord_record[-6][i][0]], [cord_record[-6][i][1]], [cord_record[-6][i][2]], label = 'moon', c = 'w')
    #         ax.legend()
    #         plt.pause(0.1)
    
    name_count = 0
    for record in acc_record[0:items]:
        plt.plot(time_record[0:len(record)], [record[i][2] for i in range(len(record))], label = names[name_count])
        name_count += 1
    plt.title("az")
    plt.legend()
    plt.show()
        
def collision_stats(stats):

    for collision in stats:
        if collision[0] == "mutual":
            print(f"Collision between {collision[2]}, and {collision[3]} at t = {collision[1]} --- Both objects destroyed.")
            print(f'Total impulse = {collision[4]:.4e} Ns, collision time span = {collision[5]:.2f} s, average force = {collision[4]/collision[5]:.4e} N, collision energy = {collision[6]/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((collision[7]-collision[8]) ** 2)):.0f} m/s')
        elif collision[0] == "object_1_destroyed":
            print(f"Collision between {collision[2]}, and {collision[3]} at t = {collision[1]} --- {collision[2]} destroyed.")
            print(f'Total impulse = {collision[4]:.4e} Ns, collision time span = {collision[5]:.2f} s, average force = {collision[4]/collision[5]:.4e} N, collision energy = {collision[6]/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((collision[7]-collision[8]) ** 2)):.0f} m/s')
        elif collision[0] == "object_2_destroyed":
            print(f"Collision between {collision[2]}, and {collision[3]} at t = {collision[1]} --- {collision[3]} destroyed.")
            print(f'Total impulse = {collision[4]:.4e} Ns, collision time span = {collision[5]:.2f} s, average force = {collision[4]/collision[5]:.4e} N, collision energy = {collision[6]/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((collision[7]-collision[8]) ** 2)):.0f} m/s')
        elif collision[0] == "bounce":
            print(f"Collision between {collision[2]}, and {collision[3]} at t = {collision[1]} --- Both objects survived.")
            print(f'Total impulse = {collision[4]:.4e} Ns, collision time span = {collision[5]:.2f} s, average force = {collision[4]/collision[5]:.4e} N, energy obsorbed by {collision[2]} = {collision[6]/10**12:.4e} TJ, , energy obsorbed by {collision[3]} = {collision[7]/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((collision[8]-collision[9]) ** 2)):.0f} m/s')


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

def static_display_2d(cord_record, names, duration, datapoints, index = 0, leg = 300, items = 0):

    if items == 0: 
        items = len(cord_record)

    name_count = 0
    for record in cord_record[0:items]:
        if index <= len(record):
            plt.plot([record[i][0] for i in range(max(0, index-leg), index)], [record[i][1] for i in range(max(0, index-leg), index)])
            plt.scatter([record[index-1][0]], [record[index-1][1]], label = names[name_count], s = 10)
            plt.legend()
            name_count += 1

    plt.gca().set_aspect('equal')
    plt.title(f"Time = {index*duration/datapoints/86400:.2f}days")
    plt.show()

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


# data_storage("saved_data/inelastic_collision_demo.npz")
# time_record, cord_record, v_record, acc_record, names, duration, datapoints, collision_record = data_retrieval("saved_data/earth_destruction.npz")
# time_record, cord_record, v_record, acc_record, names, duration, datapoints = run_engine()


# active_display_2d(cord_record, names, duration, datapoints, leg=365)
# collision_stats(collision_record)
# static_displays(time_record, cord_record, v_record, acc_record, names)
# active_display_3d(cord_record, names, duration, datapoints)
