import numpy as np

class Space:

    """Mainly for storing global variable such as time"""

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
        self.destroyed = False
    
    def time_step(self, time_size, objects):
        self.cord += self.velocity * time_size
        self.velocity += self.gravity(self.cord, objects) * time_size
        collision = self.collision_check(objects)
        return collision

    def collision_check(self, objects):
        collisions = []
        for body in objects:
            abs_dis = np.sqrt(np.sum((self.cord - objects[body].cord) ** 2))
            if abs_dis < objects[body].size + self.size:
                collisions.append(Collision(self, objects[body]))

        return collisions
    
    def collision_step(self, time_size, collision):
    
        if not collision.evaluated:
            stop = collision.collision()

        if stop:
            return True

        while collision.collision_check_bool():
            collision.object_1.cord += collision.object_1.velocity * time_size
            collision.object_2.cord += collision.object_2.velocity * time_size

        return False

class Collision():

    """Computes the collision mechenism between two objects"""

    def __init__(self, object_1 = None, object_2 = None):
        
        self.object_1 = object_1
        self.object_2 = object_2
        self.evaluated = False

    def collision(self):
        
        self.evaluated = True
        print("Collision between", self.object_1.name, "and", self.object_2.name)

        comb_elaticity = (self.object_1.elaticity +self.object_2.elaticity) / 2
        e_i_1 = 0.5 * self.object_1.mass * (np.sum(self.object_1.velocity ** 2))
        e_i_2 = 0.5 * self.object_2.mass * (np.sum(self.object_2.velocity ** 2))
        e_i_comb = e_i_1 + e_i_2
        
        v_ela_1 = ((self.object_1.mass - self.object_2.mass) * self.object_1.velocity + 2 * self.object_2.mass * self.object_2.velocity)/(self.object_1.mass + self.object_2.mass)
        v_inela = (self.object_1.mass * self.object_1.velocity + self.object_2.mass * self.object_2.velocity)/(self.object_1.mass + self.object_2.mass)

        impulse_ela_1 = (v_ela_1 - self.object_1.velocity) * self.object_1.mass
        impulse_inela_1 = (v_inela - self.object_1.velocity) * self.object_1.mass
        true_impulse_1 = (impulse_ela_1 - impulse_inela_1) * comb_elaticity + impulse_inela_1
        true_impulse_2 = -true_impulse_1

        v_f_1 = self.object_1.velocity + true_impulse_1 / self.object_1.mass
        v_f_2 = self.object_2.velocity + true_impulse_2 / self.object_2.mass

        e_f_1 = 0.5 * self.object_1.mass * (np.sum(v_f_1 ** 2))
        e_f_2 = 0.5 * self.object_2.mass * (np.sum(v_f_2 ** 2))
        e_f_comb = e_f_1 + e_f_2
        e_residule = e_i_comb - e_f_comb

        if (self.object_1.elaticity + self.object_2.elaticity) == 0:
            e_share_1 = 0.5
            e_share_2 = 0.5
        else:
            e_share_1 = self.object_2.elaticity / (self.object_1.elaticity + self.object_2.elaticity)
            e_share_2 = self.object_1.elaticity / (self.object_1.elaticity + self.object_2.elaticity)
        e_residule_1 = e_residule * e_share_1
        e_residule_2 = e_residule * e_share_2

        if e_residule_1 > self.object_1.break_energy and e_residule_2 > self.object_2.break_energy:
            self.object_1.destroyed, self.object_2.destroyed = True, True
            return True
        
        elif e_residule_1 > self.object_1.break_energy:

            self.object_2.velocity = v_inela
            self.object_2.mass += self.object_1.mass
            self.object_2.break_energy -= e_residule_2
            self.object_1.destroyed, self.object_2.destroyed = True, False
            return False

        elif e_residule_2 > self.object_2.break_energy:
            self.object_1.velocity = v_inela
            self.object_1.mass += self.object_2.mass
            self.object_1.break_energy -= e_residule_1
            self.object_1.destroyed, self.object_2.destroyed = False, True
            return False

        else:
            self.object_1.velocity = v_f_1
            self.object_1.break_energy -= e_residule_1
            self.object_2.velocity = v_f_2
            self.object_2.break_energy -= e_residule_2
            return False

    
    def collision_check_bool(self):
        abs_dis = np.sqrt(np.sum((self.object_1.cord - self.object_2.cord) ** 2))
        return (abs_dis < self.object_2.size + self.object_1.size)
    