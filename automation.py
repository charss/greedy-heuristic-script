import json, requests, csv, pprint, copy
import sys
import numpy as np
from matplotlib import pyplot as plt

# Gets the file name for the terminal
filename = sys.argv[1]
rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file) # Reads the file and its content
    header = next(csvreader)

    # Adds each row to the list
    for row in csvreader:
        rows.append(row)

pasig_ch_coord = ["Pasig City Hall", '14.5595', '121.08129'] # Pasig Coordinates


coordinates = ''
poi_coord = []
for x in rows: 
  coordinates += f'{x[2]},{x[1]};'
  poi_coord.append([float(x[2]), float(x[1])])

URL = f"http://router.project-osrm.org/trip/v1/driving/121.081286,14.559503;{coordinates}121.081286,14.559503?overview=full&geometries=geojson"
# Stores the data returned by the API
r = requests.get(URL)

print('Distance', r.json()['trips'][0]['distance'] / 1000, 'km')

# Gets the POI sequence created by the API's algorithm
waypoints = r.json()['waypoints']
temp_rows = copy.deepcopy(rows)

temp_rows.insert(0, pasig_ch_coord)
temp_rows.append(pasig_ch_coord)

arrangement = [''] * len(temp_rows)
for index, x in enumerate(waypoints):
  arrangement[x['waypoint_index']] = temp_rows[index][0]
  
print('\nOrder:')
for x in arrangement:
	print(f'-{x}')
print()

# Creates a visual representation of the optimal route
data = np.array(r.json()['trips'][0]['geometry']['coordinates'])
poi_data = np.array(poi_coord)
pasig_np = np.array([14.5595, 121.08129])

x, y = data.T
poi_x, poi_y = poi_data.T
pasig_x, pasig_y = pasig_np.T 
plt.plot(121.08129,14.5595,'ro') 
plt.plot(poi_x, poi_y, 'bo',  color='g')
plt.plot(x, y)
plt.show()


