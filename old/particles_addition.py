import odometry
import random

robustness_constant = 0.05 #(5% chance of random sonar values)

# --- per particle ---

def calculate_likelihood(self, sonar_distance):
  #decide wall & distance
  lowestDistance = odometry.walls[0].distanceFrom(self.x, self.y, self.theta)
  closestWall = odometry.walls[0]
  for wall in odometry.walls:
    if wall.validIntersectionExistsFrom(self.x, self.y, self.theta) \
    and wall.distanceFrom(self.x, self.y, self.theta) < lowestDistance:
      closestWall = wall
      lowestDistance = wall.distanceFrom(self.x, self.y, self.theta)

  #actual likelihood calculation
  m = closestWall.distanceFrom(self.x, self.y, self.theta)
  z = sonar_distance
  return math.exp((-(z - m)**2) / (2 * sonar_sigma**2)) + robustness_constant


# --- for all particles ---

def normalise():
  probability_sum = 0
  for p in particles:
    probability_sum += p.weight

  for p in particles:
    p.weight /= probability_sum

def resample():
  #normalise
  normalise()
  #generate cumulative probability list
  cumul_prob_list = []
  cumul_prob = 0
  prev_prob = 0
  for p in particles:
    prev_prob = cumul_prob
    cumul_prob += p.weight
    cumul_prob_list.append((prev_prob, cumul_prob, p)) #triple

  #randomly choose new copied particle
  new_particles = []
  r = 0 #random number
  for i in range(len(particles)):
    r = random.random() #0.0-1.0
    for c in cumul_prob_list:
      if r < c[1] and r >= c[0]: #c[0] = lower bound for this particle, c[1] = upper bound
        new_particles.append(
          Particle(c[2].x, c[2].y, c[2].theta, 1/NUM_PARTICLES)
        ) #c[2] = old particle
        break
    else: #else belonging to for loop - check python documentation if confused
      #if no particle found in cpl, throw error
      print "Error: no particle found for probability ", r

  #overwrite list
  particles = new_particles

def update_probability(sonar_distance):
  for p in particles:
    p.calculate_likelihood(sonar_distance)
  resample()
