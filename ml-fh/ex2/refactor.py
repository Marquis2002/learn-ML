import heapq
import random
from sklearn.cluster import KMeans

class Base:
    def __init__(self, x, y, fuel, missile, defense, value):
        self.x = x
        self.y = y
        self.fuel = fuel
        self.missile = missile
        self.defense = defense
        self.value = value
        self.destroyed = False

class Aircraft:
    def __init__(self, id, x, y, fuel_capacity, missile_capacity, blue_bases, red_bases, clusters):
        self.id = id
        self.x = x
        self.y = y
        self.fuel_capacity = fuel_capacity
        self.missile_capacity = missile_capacity
        self.fuel = 0
        self.missile = 0
        self.blue_bases = blue_bases
        self.red_bases = red_bases
        self.clusters = clusters
        self.target_cluster = None
        self.target_base = None
        self.moved_this_frame = False
        self.path = None
        self.path_index = 0

    def is_in_bounds(self, x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def refuel(self, amount):
        if self.fuel + amount <= self.fuel_capacity:
            self.fuel += amount
            return f"fuel {self.id} {amount}"
        return None

    def reload_missile(self, amount):
        if self.missile + amount <= self.missile_capacity:
            self.missile += amount
            return f"missile {self.id} {amount}"
        return None

    def move(self, direction):
        if self.fuel <= 0:
            return None
        if direction == 0 and self.is_in_bounds(self.x - 1, self.y):
            self.x -= 1
        elif direction == 1 and self.is_in_bounds(self.x + 1, self.y):
            self.x += 1
        elif direction == 2 and self.is_in_bounds(self.x, self.y - 1):
            self.y -= 1
        elif direction == 3 and self.is_in_bounds(self.x, self.y + 1):
            self.y += 1
        else:
            return None
        self.fuel -= 1
        return f"move {self.id} {direction}"

    def attack(self, direction, count):
        if count <= 0 or self.missile < count:
            return None

        if direction == 0 and self.is_in_bounds(self.x, self.y - 1):  # Up
            target_x, target_y = self.x, self.y - 1
        elif direction == 1 and self.is_in_bounds(self.x, self.y + 1):  # Down
            target_x, target_y = self.x, self.y + 1
        elif direction == 2 and self.is_in_bounds(self.x - 1, self.y):  # Left
            target_x, target_y = self.x - 1, self.y
        elif direction == 3 and self.is_in_bounds(self.x + 1, self.y):  # Right
            target_x, target_y = self.x + 1, self.y
        else:
            return None

        # Check if target is a valid red base
        for base in self.red_bases:
            if base.x == target_x and base.y == target_y and not base.destroyed:
                base.defense -= count
                self.missile -= count
                if base.defense <= 0:
                    base.destroyed = True
                    global score
                    score += base.value
                return f"attack {self.id} {direction} {count}"

        return None

    def a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for direction, (dx, dy) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0)]):
                neighbor = (current[0] + dx, current[1] + dy)
                tentative_g_score = g_score[current] + 1

                if self.is_in_bounds(neighbor[0], neighbor[1]) and grid[neighbor[0]][neighbor[1]] != '#':
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = (current, direction)
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        total_path = []
        while current in came_from:
            current, direction = came_from[current]
            total_path.append((current, direction))
        total_path.reverse()
        return total_path

    def generate_actions(self):
        actions = []

        # If all red bases are destroyed, no actions needed
        if all(base.destroyed for base in self.red_bases):
            return actions
        else:
            # If path is set, follow it
            if self.path:
                if self.path_index < len(self.path):
                    current, direction = self.path[self.path_index]
                    action = self.move(direction)
                    if action:
                        actions.append(action)
                    self.path_index += 1
                    self.moved_this_frame = True
                    if self.path_index >= len(self.path):
                        self.path = None
                        self.path_index = 0
                return actions

            # Refuel and reload missile if at a blue base
            for base in self.blue_bases:
                if base.x == self.x and base.y == self.y:
                    fuel_needed = self.fuel_capacity - self.fuel
                    if fuel_needed > 0 and base.fuel > 0:
                        fuel_amount = min(fuel_needed, base.fuel)
                        action = self.refuel(fuel_amount)
                        if action:
                            actions.append(action)
                        base.fuel -= fuel_amount  # Update base fuel reserve

                    missile_needed = self.missile_capacity - self.missile
                    if missile_needed > 0 and base.missile > 0:
                        missile_amount = min(missile_needed, base.missile)
                        action = self.reload_missile(missile_amount)
                        if action:
                            actions.append(action)
                        base.missile -= missile_amount  # Update base missile reserve

            # Attack the nearest red base if in range
            if self.missile > 0:
                for direction, (dx, dy) in enumerate([(0, 1), (0, -1), (-1, 0), (1, 0)]):
                    target_x, target_y = self.x + dx, self.y + dy
                    for base in self.red_bases:
                        if base.x == target_x and base.y == target_y and not base.destroyed:
                            count = min(self.missile, base.defense)
                            action = self.attack(direction, count)
                            if action:
                                actions.append(action)
                            break

            # Only allow one move per frame
            if not self.moved_this_frame:
                # Check if fuel is below a threshold and find nearest base with fuel
                if self.fuel <= 10:
                    target_base = min((base for base in self.blue_bases if base.fuel > 0),
                                      key=lambda b: abs(b.x - self.x) + abs(b.y - self.y), default=None)
                    if target_base:
                        path = self.a_star((self.x, self.y), (target_base.x, target_base.y))
                        if path and len(path) > 1:
                            self.path = path
                            self.path_index = 1  # Skip the starting point
                            current, direction = path[1]
                            action = self.move(direction)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True

                # Check if missile count is below a threshold and find nearest base with missiles
                elif self.missile == 0:
                    target_base = min((base for base in self.blue_bases if base.missile > 0),
                                      key=lambda b: abs(b.x - self.x) + abs(b.y - self.y), default=None)
                    if target_base:
                        path = self.a_star((self.x, self.y), (target_base.x, target_base.y))
                        if path and len(path) > 1:
                            self.path = path
                            self.path_index = 1  # Skip the starting point
                            current, direction = path[1]
                            action = self.move(direction)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True

                # Move towards the nearest red base if have missiles
                else:
                    target_base = min(self.red_bases,
                                  key=lambda b: (abs(b.x - self.x) + abs(b.y - self.y)) if not b.destroyed else float('inf'))
                    if not target_base.destroyed:
                        if self.x < target_base.x:
                            if not any(base.x == self.x + 1 and base.y == self.y and not base.destroyed for base in self.red_bases):
                                action = self.move(1)
                                if action:
                                    actions.append(action)
                                self.moved_this_frame = True
                        elif self.x > target_base.x:
                            if not any(base.x == self.x - 1 and base.y == self.y and not base.destroyed for base in self.red_bases):
                                action = self.move(0)
                                if action:
                                    actions.append(action)
                                self.moved_this_frame = True
                        elif self.y < target_base.y:
                            if not any(base.x == self.x and base.y == self.y + 1 and not base.destroyed for base in self.red_bases):
                                action = self.move(3)
                                if action:
                                    actions.append(action)
                                self.moved_this_frame = True
                        elif self.y > target_base.y:
                            if not any(base.x == self.x and base.y == self.y - 1 and not base.destroyed for base in self.red_bases):
                                action = self.move(2)
                                if action:
                                    actions.append(action)
                                self.moved_this_frame = True
                    else:
                        pass

            # If no other actions, set a new target
            if not actions:
                if self.target_cluster is None or all(base.destroyed for base in self.target_cluster):
                    self.assign_new_target_cluster()

                if self.target_base is None or self.target_base.destroyed:
                    self.assign_new_target_base()

                if self.target_base and not self.target_base.destroyed:
                    path = self.a_star((self.x, self.y), (self.target_base.x, self.target_base.y))
                    if path and len(path) > 1:
                        self.path = path
                        self.path_index = 1
                        current, direction = path[1]
                        action = self.move(direction)
                        if action:
                            actions.append(action)
                        self.moved_this_frame = True

            return actions

    def assign_new_target_cluster(self):
        cluster_values = [
            sum(base.value for base in cluster if not base.destroyed)
            for cluster in self.clusters
        ]
        target_cluster_index = max(range(len(cluster_values)), key=lambda i: cluster_values[i])
        self.target_cluster = self.clusters[target_cluster_index]

    def assign_new_target_base(self):
        if self.target_cluster:
            self.target_base = min(
                (base for base in self.target_cluster if not base.destroyed),
                key=lambda b: abs(b.x - self.x) + abs(b.y - self.y),
                default=None
            )

import sys

def parse_bases(num_bases):
    bases = []
    for _ in range(num_bases):
        x, y = map(int, input().split())
        fuel, missile, defense, value = map(int, input().split())
        bases.append(Base(x, y, fuel, missile, defense, value))
    return bases

def parse_input():
    n, m = map(int, input().split())
    global grid
    grid = [input().strip() for _ in range(n)]

    num_blue_bases = int(input())
    blue_bases = parse_bases(num_blue_bases)

    num_red_bases = int(input())
    red_bases = parse_bases(num_red_bases)

    num_aircrafts = int(input())
    aircrafts = []
    for i in range(num_aircrafts):
        x, y, fuel_capacity, missile_capacity = map(int, input().split())
        aircrafts.append((i, x, y, fuel_capacity, missile_capacity))

    return aircrafts, blue_bases, red_bases

def main():
    global score
    score = 0
    aircrafts_info, blue_bases, red_bases = parse_input()

    # K-means clustering for red bases
    kmeans = KMeans(n_clusters=3, random_state=0).fit([(base.x, base.y) for base in red_bases])
    clusters = [[] for _ in range(3)]
    for base, label in zip(red_bases, kmeans.labels_):
        clusters[label].append(base)

    # Assign clusters to aircrafts
    aircrafts = []
    for info in aircrafts_info:
        i, x, y, fuel_capacity, missile_capacity = info
        aircraft = Aircraft(i, x, y, fuel_capacity, missile_capacity, blue_bases, red_bases, clusters)
        aircrafts.append(aircraft)

    frame_count = 0
    while frame_count < 15000:
        frame_count += 1
        actions = []

        for aircraft in aircrafts:
            aircraft.moved_this_frame = False  # Reset the moved flag
            aircraft_actions = aircraft.generate_actions()
            actions.extend(aircraft_actions)

        # Print actions for this frame
        for action in actions:
            print(action)

        # Print debug information for each aircraft
        for aircraft in aircrafts:
            print(f"[DEBUG] Aircraft {aircraft.id}: Fuel {aircraft.fuel}, Missile {aircraft.missile}")

        # Print "OK" to indicate the end of this frame
        print("OK")

if __name__ == "__main__":
    main()
