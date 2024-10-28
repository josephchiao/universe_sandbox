## Energy for blowing up planets calculator
# m = 2.29E+19
# r = 222000


# E = (3*6.67e-11*m**2)/(5*r)

# print(E)
import numpy as np


data = np.load('saved_data/impact_stats_prediction.npz')

cord, velocity = data['cord_record'], data['v_record']

cord_x = [c[9][0] for c in cord]
cord_y = [c[9][1] for c in cord]
cord_z = [c[9][2] for c in cord]
v_x = [v[9][0] for v in velocity]
v_y = [v[9][1] for v in velocity]
v_z = [v[9][2] for v in velocity]
print(cord_x)
print(cord_y)
print(cord_z)
print(v_x)
print(v_y)
print(v_z)
