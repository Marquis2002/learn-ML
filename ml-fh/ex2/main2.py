import base64
from parse_game import parse_game_data_from_file

score = 0

class Base:
    def __init__(self, x, y, fuel, missile, defense, value):
        self.x = x
        self.y = y
        self.fuel = fuel
        self.missile = missile
        self.defense = defense
        self.value = value
        self.destroyed = False


class Fighter:
    def __init__(self, id, x, y, fuel_capacity, missile_capacity, blue_bases, red_bases):
        self.id = id
        self.x = x
        self.y = y
        self.fuel_capacity = fuel_capacity
        self.missile_capacity = missile_capacity
        self.current_fuel = 0
        self.current_missiles = 0
        self.blue_bases = blue_bases
        self.red_bases = red_bases
        self.moved_this_frame = False

    def is_in_bounds(self, x, y):
        n, m = map_layout.shape
        return 0 <= x < n and 0 <= y < m

    def move(self, direction):
        if self.current_fuel <= 0:
            return None
        elif direction == 0 and self.is_in_bounds(self.x - 1, self.y):
            self.x -= 1
        elif direction == 1 and self.is_in_bounds(self.x + 1, self.y):
            self.x += 1
        elif direction == 2 and self.is_in_bounds(self.x, self.y - 1):
            self.y -= 1
        elif direction == 3 and self.is_in_bounds(self.x, self.y + 1):
            self.y += 1
        else:
            return None
        self.current_fuel -= 1
        return f"move {self.id} {direction}"

    def attack(self, direction, count):
        if count <= 0 or self.current_missiles < count:
            return None

        if direction == 0 and self.is_in_bounds(self.x - 1, self.y):  # Up
            target_x, target_y = self.x - 1, self.y
        elif direction == 1 and self.is_in_bounds(self.x + 1, self.y):  # Down
            target_x, target_y = self.x + 1, self.y
        elif direction == 2 and self.is_in_bounds(self.x, self.y - 1):  # Left
            target_x, target_y = self.x, self.y - 1
        elif direction == 3 and self.is_in_bounds(self.x, self.y + 1):  # Right
            target_x, target_y = self.x, self.y + 1
        else:
            return None

        for base in self.red_bases:
            if base.x == target_x and base.y == target_y and not base.destroyed:
                base.defense -= count
                self.current_missiles -= count
                if base.defense <= 0:
                    base.destroyed = True
                    global score
                    score += base.value
                return f"attack {self.id} {direction} {count}"

        return None

    def refuel(self, count):
        if self.current_fuel + count <= self.fuel_capacity:
            self.current_fuel += count
            return f"fuel {self.id} {count}"
        return None

    def reload(self, count):
        if self.current_missiles + count <= self.missile_capacity:
            self.current_missiles += count
            return f"missile {self.id} {count}"
        return None

    def generate_actions(self):
        actions = []

        if all(base.destroyed for base in self.red_bases):
            return actions

        for base in self.blue_bases:
            if base.x == self.x and base.y == self.y:
                fuel_needed = self.fuel_capacity - self.current_fuel
                if fuel_needed > 0 and base.fuel > 0:
                    fuel_amount = min(fuel_needed, base.fuel)
                    action = self.refuel(fuel_amount)
                    if action:
                        actions.append(action)
                    base.fuel -= fuel_amount

                missile_needed = self.missile_capacity - self.current_missiles
                if missile_needed > 0 and base.missile > 0:
                    missile_amount = min(missile_needed, base.missile)
                    action = self.reload(missile_amount)
                    if action:
                        actions.append(action)
                    base.missile -= missile_amount

        if self.current_missiles > 0:
            for direction, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                target_x, target_y = self.x + dx, self.y + dy
                for base in self.red_bases:
                    if base.x == target_x and base.y == target_y and not base.destroyed:
                        count = min(self.current_missiles, base.defense)
                        action = self.attack(direction, count)
                        if action:
                            actions.append(action)
                        break

        if not self.moved_this_frame:
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
                print("Error!")

        return actions


def main():
    filename = "../data/testcase2.in"
    info_dict = parse_game_data_from_file(filename)

    map_size_info = info_dict['map_size']
    map_layout_info = info_dict['map_layout']
    blue_bases_info = info_dict['blue_bases']
    red_bases_info = info_dict['red_bases']
    fighters_info = info_dict['fighters']

    n = map_size_info[0]
    m = map_size_info[1]

    global map_layout
    map_layout = map_layout_info

    blue_bases = []
    for blue_base_info in blue_bases_info:
        position = blue_base_info['position']
        attributes = blue_base_info['attributes']
        blue_base = Base(position[0], position[1], attributes[0], attributes[1], attributes[2], attributes[3])
        blue_bases.append(blue_base)

    red_bases = []
    for red_base_info in red_bases_info:
        position = red_base_info['position']
        attributes = red_base_info['attributes']
        red_base = Base(position[0], position[1], attributes[0], attributes[1], attributes[2], attributes[3])
        red_bases.append(red_base)

    fighters = []
    for fighter_id in range(len(fighters_info)):
        fighter_info = fighters_info[fighter_id]
        fighter = Fighter(fighter_id, fighter_info[0], fighter_info[1], fighter_info[2], fighter_info[3], blue_bases, red_bases)
        fighters.append(fighter)

    frame_count = 0
    while frame_count < 15000:
        frame_count += 1
        actions = []

        for fighter in fighters:
            fighter.moved_this_frame = False
            fighter_actions = fighter.generate_actions()
            actions.extend(fighter_actions)

        for action in actions:
            print(action)

        print("OK")

if __name__ == "__main__":
    main()
