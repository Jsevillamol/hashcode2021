# Hashcode 2021
# Dedekind's Army RULES

import networkx as nx
from queue import Queue

# Input processing

INPUT = 'a'
path = ''

with open(path + INPUT + '.txt') as fp:
  # Read first line
  simulation_length, n_intersections, n_streets, n_cars, car_points = map(int,fp.readline().split())

  # Read street map
  street_map = nx.DiGraph()
  street_directory = {}
  
  incoming = [[] for it in range(n_intersections)]
  for street in range(n_streets):
    start, end, name, length = fp.readline().split()
    start, end, length = map(int, (start, end, length))
    street_map.add_edge(start, end)
    street_map[start][end]["name"] = name
    street_map[start][end]["length"] = length
    street_directory[name] = (start,end)
    incoming[end].append(name)

  # Read car paths   
  car_paths = []
  for car in range(n_cars):
    car_path = fp.readline().rstrip('\n').split(" ")[1:]
    car_paths.append(car_path)
    
 even_schedule = []
import random
for node in range(n_intersections):
  clone = [el for el in incoming[node]]
  random.shuffle(clone)
  even_schedule.append(clone)
  
  
def run(schedule):
  # Initialize streets
  for start,end in street_map.edges():
    street_map[start][end]["car_queue"] = []
    
  # initialize cars 
  for car in car_paths:
    car = car.copy()
    initial_street = car.pop()
    start, end = street_directory[initial_street]
    street_length = street_map[start][end]["length"]
    # The cars enter at negative length time to simulate them entering at the end of the street
    street_map[start][end]["car_queue"].append((-length,car))

  total_score = 0
  for time in range(simulation_length):
    step_score = step(schedule, time)
    total_score += step_score

  return total_score

def step(schedule, time):
  step_score = 0

  # Check streets for cars arriving at their destination
  for start,end in street_map.edges():
    # If the street is empty we do nothing
    if len(street_map[start][end]["car_queue"]) == 0:
      continue

    # We retrieve the first car of the street
    entry_time, car = street_map[start][end]["car_queue"][0]
    
    # If the car has not had enough time to cross the street nothing happens 
    if time - entry_time < street_map[start][end]["length"]:
      break
    
    # If it is the last destination of the car it vanishes and we get points
    if len(car) == 0:
      print(f"Car has arrived to its destination at {street_map[start][end]['name']}!")
      street_map[start][end]["car_queue"] = street_map[start][end]["car_queue"][1:]
      step_score += car_points + simulation_length - time

  # We advance cars in each intersection
  for intersection in street_map:
    # Check which street has a green light
    intersection_schedule = schedule[intersection]
    open_street = intersection_schedule[time % len(intersection_schedule)]
    start,end = street_directory[open_street]
    
    # If the open street is empty continue
    if len(street_map[start][end]["car_queue"]) == 0:
      continue

    # Check the first car from the open street
    entry_time, car = street_map[start][end]["car_queue"][0]

    # If the car has not had enough time to cross the street nothing happens 
    if time - entry_time <  street_map[start][end]["length"]:
      continue 

    # Move the car to the next street in its path
    street_map[start][end]["car_queue"] = street_map[start][end]["car_queue"][1:]
    next_street = car.pop()
    start,end = street_directory[next_street]
    street_map[start][end]["car_queue"].append((time, car))

  return step_score

run(even_schedule)

def schedule_to_txt(schedule, filename):
  f = open(filename+'.txt', 'w')
  f.write(str(len(schedule))+'\n')
  for ii in range(len(schedule)):
    f.write(str(ii)+'\n'+str(len(schedule[ii]))+'\n')
    for street in schedule[ii]:
      jj = 1
      while True:
        if ii+1 == len(schedule):
          f.write(street+' '+str(jj))
          break
        if schedule[ii+1] == street:
          ii += 1
          jj += 1
        else:
          f.write(street+' '+str(jj)+'\n')
          break
  f.close()

schedule_to_txt(even_schedule, 'submission'+INPUT)