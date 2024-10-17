import numpy as np

class Space:
    def __init__(self):
        self.time = 0  ## Overall time
    
    def gravity(self, cord, objects):
        accs = []
        acc = np.zeros(3, dtype="float64") 
        gravitational_constant = 6.67 * (10 ** -11)
        for body in objects:
            abs_distance = np.sqrt(np.sum((objects[body].cord - cord) ** 2))
            accs.append(np.array(gravitational_constant * objects[body].mass / (abs_distance ** 2) * ((objects[body].cord - cord) / abs_distance)))
        for i in accs:
            acc += i
        return acc

class Object(Space):

    """What an object is and what it does"""

    def __init__(self, 
                 name = "",
                 x = 0, y = 0, z = 0, 
                 dx = 0, dy = 0, dz = 0, 
                 mass = 0, size = 1, f = float("inf"), elaticity = 0):
        
        self.name = name
        self.cord = np.array([x, y, z], dtype='float64')
        self.velocity = np.array([dx, dy, dz], dtype='float64')
        self.mass = mass
        self.size = size
        self.break_energy = f
        self.elaticity = elaticity
    
    def time_step(self, time_size, objects):
        self.cord += self.velocity * time_size
        self.velocity += self.gravity(self.cord, objects) * time_size
        # collided, object = self.collision_check(objects)
        # if collided:
        #     print("collision with", object.name)
        #     # output_1, output_2 = self.collision(object)
        
        # return False, None, None, None

    def collision_check(self, objects):
        for object in objects:
            abs_dis = np.sqrt(np.sum((self.cord - object.cord) ** 2))
            if abs_dis < object.size + self.size:
                return True, object
        return False, None


    def collision(self, object):
        
        comb_elaticity = (self.elaticity + object.elaticity) / 2
        e_i_self = 0.5 * self.mass * (np.sum(self.velocity ** 2))
        e_i_other = 0.5 * object.mass * (np.sum(object.velocity ** 2))
        e_i_comb = e_i_self + e_i_other
        e_f_comb = e_i_comb * comb_elaticity
        e_residule = e_i_comb - e_f_comb

        p_i_self = self.mass * self.velocity
        p_i_other = object.mass * object.velocity
        p_comb = p_i_self + p_i_other

        if e_self_residule > self.break_energy and e_other_residule > object.break_energy:

            return None, None
        
        elif e_self_residule > self.break_energy or e_other_residule > object.break_energy:
            ## Combine two object

            remaining_object = None
            return remaining_object


        f_vector_self = self.cord - object.cord
        f_vector_other = -f_vector_self

        e_self_share = object.elaticity / (self.elaticity + object.elaticity)
        e_other_share = self.elaticity / (self.elaticity + object.elaticity)
        e_self_residule = e_residule * e_self_share
        e_other_residule = e_residule * e_other_share

        return 