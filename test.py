## Energy for blowing up planets calculator
# m = 2.29E+19
# r = 222000


# E = (3*6.67e-11*m**2)/(5*r)

# print(E)
import numpy as np


data = np.load('saved_data/psyche_position_10years.npz')

cord, velocity = data['cord_record'], data['v_record']

cord_x = [c[-1][0] for c in cord]
cord_y = [c[-1][1] for c in cord]
cord_z = [c[-1][2] for c in cord]
v_x = [v[-1][0] for v in velocity]
v_y = [v[-1][1] for v in velocity]
v_z = [v[-1][2] for v in velocity]
print(cord_x)
print(cord_y)
print(cord_z)
print(v_x)
print(v_y)
print(v_z)
