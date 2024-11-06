from flask import Flask, render_template, request
import random
import time

# --- Union-Find and Kruskal's Algorithm (for MST) ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1


def kruskal(n, edges):
    uf = UnionFind(n)
    mst = []
    edges.sort(key=lambda x: x[2])  # Sort edges by weight (cost/distance)

    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, weight))

    return mst

# --- Crop Class and Irrigation Scheduling ---
class Crop:
    def __init__(self, name, water_requirement):
        self.name = name
        self.water_requirement = water_requirement  # Amount of water needed (in liters)

class IrrigationSchedule:
    def __init__(self, crops):
        self.crops = crops
        self.schedule = {}

    def generate_schedule(self):
        for crop in self.crops:
            irrigation_time = random.randint(1, 3)  # Random irrigation times between 1 to 3 hours
            self.schedule[crop.name] = {
                'water_needed': crop.water_requirement,
                'irrigation_time': irrigation_time
            }

# --- Pump Placement Optimization ---
class Pump:
    def __init__(self, location, capacity):
        self.location = location  # e.g., (x, y) coordinates
        self.capacity = capacity  # Maximum capacity of the pump (liters per hour)

    def __repr__(self):
        return f"Pump at {self.location} with capacity {self.capacity}L/h"

def optimize_pump_placement(farm_layout, num_pumps):
    # Example: farm_layout is a grid of size (x, y), num_pumps is the number of pumps to place
    pumps = []
    for _ in range(num_pumps):
        x = random.randint(0, farm_layout[0] - 1)
        y = random.randint(0, farm_layout[1] - 1)
        capacity = random.randint(100, 500)  # Random pump capacity
        pumps.append(Pump((x, y), capacity))
    return pumps

# --- Flask Routes ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input from the user (number of crops, number of pumps, etc.)
        num_crops = int(request.form['num_crops'])
        num_pumps = int(request.form['num_pumps'])
        
        # Simulate delay for loading results (to enhance user experience)
        time.sleep(2)  # Delay for 2 seconds to simulate processing time

        # 1. Example irrigation network graph (MST)
        edges = [
            (0, 1, 10),  # From source 0 to field 1 with cost 10
            (0, 2, 15),  # From source 0 to field 2 with cost 15
            (1, 2, 5),   # From field 1 to field 2 with cost 5
            (1, 3, 20),  # From field 1 to field 3 with cost 20
            (2, 3, 10)   # From field 2 to field 3 with cost 10
        ]
        n = 4  # Number of nodes (sources, fields)

        # Run Kruskal's Algorithm for Minimum Spanning Tree (MST)
        mst = kruskal(n, edges)

        # 2. Example crop scheduling
        crops = [
            Crop("Wheat", random.randint(150, 300)),
            Crop("Corn", random.randint(200, 350)),
            Crop("Rice", random.randint(250, 400)),
            Crop("Tomatoes", random.randint(100, 200))
        ][:num_crops]  # Limit the number of crops based on input
        schedule = IrrigationSchedule(crops)
        schedule.generate_schedule()

        # 3. Optimize infrastructure placement (Pump placement)
        farm_layout = (10, 10)  # 10x10 grid representing the farm
        pumps = optimize_pump_placement(farm_layout, num_pumps)

        # Render the results in an HTML page
        return render_template('index.html', mst=mst, schedule=schedule.schedule, pumps=pumps)

    return render_template('index.html', mst=None, schedule=None, pumps=None)


if __name__ == '__main__':
    app.run(debug=True)
