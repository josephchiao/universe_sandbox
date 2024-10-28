import numpy as np
import copy 

class Space:

    """Mainly for storing global variable such as time"""

    def __init__(self):

        self.time = 0  ## Overall time
    
    def gravity(self, cord, objects):
        
        ## For discriminating destroyed objects.
        if all(v is None for v in cord):
            return [None, None, None]
        
        ## Consider gravitational pull from all gravitationally significant objects in the space.
        accs = []
        acc = np.zeros(3, dtype="float64") 
        gravitational_constant = 6.67 * (10 ** -11)

        ## Cycle through all other objects in space (not including self)
        for body in objects:
            if objects[body].grav_significance:  ## Reject bodies that are marked gravitationally insignificant. 

                abs_distance = np.sqrt(np.sum((objects[body].cord - cord) ** 2))
                accs.append(np.array(gravitational_constant * objects[body].mass / (abs_distance ** 2) * ((objects[body].cord - cord) / abs_distance)))

        for i in accs:  ## Sum the pull from all bodies. 
            acc += i

        return acc

class Object(Space):

    """What an object is and what it does"""

    def __init__(self, 
                 name = "",
                 x = 0, y = 0, z = 0, 
                 dx = 0, dy = 0, dz = 0, 
                 mass = 0, size = 1, f = float("inf"), elaticity = 0, grav_sig = True):
        
        self.name = name
        self.cord = np.array([x, y, z], dtype='float64')  ## Cordinate system using Solar System Barycenter as center. In meters. 
        self.velocity = np.array([dx, dy, dz], dtype='float64')  ## In m/s
        self.mass = mass  ## In kg
        self.size = size  ## Radius in m
        self.break_energy = f  ## Total energy required to destroy a body, in J
        self.elaticity = elaticity  ## An arbitrary coeficient for determining elaticity. Two bodies with combined elaticity of zero would be completely inelastic, while combined elaticity of 2 would be completely elastic. 
        self.grav_significance = grav_sig  ## Boolean value for marking the gravitational significance of a body. The gravitational pull will not be considered if value == False. 
        self.destroyed = False  ## Boolean value for marking the state of a body. 
    
    def time_step(self, time_size, objects):

        ## Generic time step. 
        ## Evaluates velocity and acceleration
        ## Also detects collision, but does not compute the outcome. 
        
        delta_cord = self.velocity * time_size
        delta_v = self.gravity(self.cord, objects) * time_size
        self.cord += delta_cord
        self.velocity += delta_v
        collision = self.collision_check(objects)

        return collision

    def collision_check(self, objects):

        ## To check for collision between two bodies. 
        ## Can support a body simultaniously colliding with multiple objects. 

        collisions = []
        for body in objects:
            abs_dis = np.sqrt(np.sum((self.cord - objects[body].cord) ** 2))
            if abs_dis < objects[body].size + self.size:
                collisions.append(Collision(self, objects[body]))

        return collisions
    
    def collision_step(self, time_size, collision, objects):
        

        if not collision.evaluated:
            stop, stats = collision.collision()

        if stop:
            return True, stats

        ## Clipping rejection
        while collision.collision_check_bool() and not collision.object_1.destroyed and not collision.object_2.destroyed:
            collision.object_1.time_step(time_size, {objects[x].name:objects[x] for x in objects if x != collision.object_1.name})
            collision.object_2.time_step(time_size, {objects[x].name:objects[x] for x in objects if x != collision.object_2.name})
            print('escaping')
        
        return False, stats

class Collision():

    """Computes the collision mechenism between two objects"""

    def __init__(self, object_1 = None, object_2 = None):
        
        ## Import both objects, and store universal information about the collision
        self.object_1 = object_1
        self.object_2 = object_2
        self.evaluated = False
        self.collision_time = 0

    def collision(self):
        
        self.evaluated = True

        v_i_1 = copy.deepcopy(self.object_1.velocity)
        v_i_2 = copy.deepcopy(self.object_2.velocity)

        ## Compute the correct elaticity for the collision
        comb_elaticity = (self.object_1.elaticity + self.object_2.elaticity) / 2
        
        ## Compute the collision result with assumption of elastic and inelastic 
        v_ela_1 = -self.object_1.velocity
        v_inela = (self.object_1.mass * self.object_1.velocity + self.object_2.mass * self.object_2.velocity)/(self.object_1.mass + self.object_2.mass)

        ## Compute the impulse of the collision
        impulse_ela_1 = (v_ela_1 - self.object_1.velocity) * self.object_1.mass
        impulse_inela_1 = (v_inela - self.object_1.velocity) * self.object_1.mass
        true_impulse_1 = (impulse_ela_1 - impulse_inela_1) * comb_elaticity + impulse_inela_1
        true_impulse_2 = -true_impulse_1
        comb_impulse = np.sqrt(np.sum(true_impulse_1 ** 2))

        ## Assume all objects survive, compute the true resultant speed of the collision
        v_f_1 = self.object_1.velocity + true_impulse_1 / self.object_1.mass
        v_f_2 = self.object_2.velocity + true_impulse_2 / self.object_2.mass

        if (self.object_1.elaticity + self.object_2.elaticity) == 2:
            v_f_1 = -self.object_1.velocity
            v_f_2 = -self.object_2.velocity

        if (self.object_1.elaticity + self.object_2.elaticity) == 0:
            e_share_1 = 0.5
            e_share_2 = 0.5

        else:
            e_share_1 = self.object_2.elaticity / (self.object_1.elaticity + self.object_2.elaticity)
            e_share_2 = self.object_1.elaticity / (self.object_1.elaticity + self.object_2.elaticity)

        ## Compute the energy of the collision
        e_i_1 = 0.5 * self.object_1.mass * (np.sum(self.object_1.velocity ** 2))
        e_i_2 = 0.5 * self.object_2.mass * (np.sum(self.object_2.velocity ** 2))
        e_i_comb = e_i_1 + e_i_2
        e_f_1 = 0.5 * self.object_1.mass * (np.sum(v_f_1 ** 2))
        e_f_2 = 0.5 * self.object_2.mass * (np.sum(v_f_2 ** 2))
        e_f_comb = e_f_1 + e_f_2
        e_residule = e_i_comb - e_f_comb
        
        ## Energy passed onto each body
        e_residule_1 = e_residule * e_share_1
        e_residule_2 = e_residule * e_share_2
        
        ## If both objects are destroyed: 
        if e_residule_1 > self.object_1.break_energy and e_residule_2 > self.object_2.break_energy:

            self.collision_time = min(self.object_1.size, self.object_2.size) / np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2))

            print("Collision between", self.object_1.name, "and", self.object_2.name, "--- Both objects destroyed. Simulation stoped.")
            print(f'Total impulse = {comb_impulse:.4e} Ns, collision time span = {self.collision_time:.2f} s, average force = {comb_impulse/self.collision_time:.4e} N, collision energy = {e_f_comb/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)):.0f} m/s')

            self.object_1.destroyed, self.object_2.destroyed = True, True
            
            return True, ["mutual", self.object_1.name, self.object_2.name, comb_impulse, self.collision_time, e_f_comb, v_i_1, v_i_2, self.object_1.cord, self.object_2.cord]
        
        ## If one of the two objects is destroyed: 
        elif e_residule_1 > self.object_1.break_energy or (comb_elaticity == 0 and self.object_1.mass < self.object_2.mass):

            self.collision_time = self.object_1.size / np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2))

            print("Collision between", self.object_1.name, "and", self.object_2.name, "---", self.object_1.name, "destroyed.")
            print(f'Total impulse = {comb_impulse:.4e} Ns, collision time span = {self.collision_time:.2f} s, average force = {comb_impulse/self.collision_time:.4e} N, energy obsorbed by {self.object_2.name} = {e_residule_2/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)):.0f} m/s')

            self.object_2.velocity = v_inela
            self.object_2.mass += self.object_1.mass
            self.object_2.break_energy -= e_residule_2
            self.object_1.destroyed, self.object_2.destroyed = True, False

            return False, ["object_1_destroyed", self.object_1.name, self.object_2.name, comb_impulse, self.collision_time, e_residule_2, v_i_1, v_i_2, self.object_1.cord, self.object_2.cord]

        elif e_residule_2 > self.object_2.break_energy or (comb_elaticity == 0 and self.object_1.mass >= self.object_2.mass):

            self.collision_time = (self.object_1.size + self.object_2.size) * 0.02 / np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)) * 2

            print("Collision between", self.object_1.name, "and", self.object_2.name, "---", self.object_2.name, "destroyed.")
            print(f'Total impulse = {comb_impulse:.4e} Ns, collision time span = {self.collision_time:.2f} s, average force = {comb_impulse/self.collision_time:.4e} N, energy obsorbed by {self.object_1.name} = {e_residule_1/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)):.0f} m/s')

            self.object_1.velocity = v_inela
            self.object_1.mass += self.object_2.mass
            self.object_1.break_energy -= e_residule_1
            self.object_1.destroyed, self.object_2.destroyed = False, True
            self.collision_time = self.object_2.size / np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2))
            return False, ["object_2_destroyed", self.object_1.name, self.object_2.name, comb_impulse, self.collision_time, e_residule_1, v_i_1, v_i_2, self.object_1.cord, self.object_2.cord]

        ## If neither objects are destroyed
        else:
            self.collision_time = (self.object_1.size + self.object_2.size) * 0.02 / np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)) * 2

            print("Collision between", self.object_1.name, "and", self.object_2.name, "--- Both objects survived.")
            print(f'Total impulse = {comb_impulse:.4e} Ns, collision time span = {self.collision_time:.2f} s, average force = {comb_impulse/self.collision_time:.4e} N, energy obsorbed by {self.object_1.name} = {e_residule_1/10**12:.4e} TJ, , energy obsorbed by {self.object_2.name} = {e_residule_2/10**12:.4e} TJ, relative speed when collided = {np.sqrt(np.sum((self.object_1.velocity-self.object_2.velocity) ** 2)):.0f} m/s')

            self.object_1.velocity = v_f_1
            self.object_1.break_energy -= e_residule_1
            self.object_2.velocity = v_f_2
            self.object_2.break_energy -= e_residule_2

            return False, ["bounce", self.object_1.name, self.object_2.name, comb_impulse, self.collision_time, e_residule_1, e_residule_2, v_i_1, v_i_2, self.object_1.cord, self.object_2.cord]

    def collision_check_bool(self):

        ## Check if a collision is underway(an object clipping abother). 

        abs_dis = np.sqrt(np.sum((self.object_1.cord - self.object_2.cord) ** 2))
        return (abs_dis < self.object_2.size + self.object_1.size)
    