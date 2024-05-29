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

        if direction == 0 and self.is_in_bounds(self.x, self.y - 1):  # Up
            target_x, target_y = self.x - 1, self.y
        elif direction == 1 and self.is_in_bounds(self.x, self.y + 1):  # Down
            target_x, target_y = self.x + 1, self.y
        elif direction == 2 and self.is_in_bounds(self.x - 1, self.y):  # Left
            target_x, target_y = self.x, self.y - 1
        elif direction == 3 and self.is_in_bounds(self.x + 1, self.y):  # Right
            target_x, target_y = self.x, self.y + 1
        else:
            return None

        # Check if target is a valid red base
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

        # If all red bases are destroyed, no actions needed
        if all(base.destroyed for base in self.red_bases):
            return actions
        else:
            # # If path is set, follow it
            # if self.path:
            #     if self.path_index < len(self.path):
            #         current, direction = self.path[self.path_index]
            #         action = self.move(direction)
            #         if action:
            #             actions.append(action)
            #         self.path_index += 1
            #         self.moved_this_frame = True
            #         if self.path_index >= len(self.path):
            #             self.path = None
            #             self.path_index = 0
            #     return actions
            # Refuel and reload missile if at a blue base
            # 1. fuel here
            for base in self.blue_bases:
                if base.x == self.x and base.y == self.y:
                    fuel_needed = self.fuel_capacity - self.current_fuel
                    if fuel_needed > 0 and base.fuel > 0:
                        fuel_amount = min(fuel_needed, base.fuel)
                        action = self.refuel(fuel_amount)
                        if action:
                            actions.append(action)
                        base.fuel -= fuel_amount  # Update base fuel reserve

                    missile_needed = self.missile_capacity - self.current_missiles
                    if missile_needed > 0 and base.missile > 0:
                        missile_amount = min(missile_needed, base.missile)
                        action = self.reload(missile_amount)
                        if action:
                            actions.append(action)
                        base.missile -= missile_amount  # Update base missile reserve

            # Attack the nearest red base if in range
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
                                  key=lambda b: (abs(b.x - self.x) + abs(b.y - self.y)) if not b.destroyed else float(
                                      'inf'))
                if not target_base.destroyed:
                    if self.x < target_base.x:
                        if not any(base.x == self.x + 1 and base.y == self.y and not base.destroyed for base in
                                   self.red_bases):
                            action = self.move(1)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True
                    elif self.x > target_base.x:
                        if not any(base.x == self.x - 1 and base.y == self.y and not base.destroyed for base in
                                   self.red_bases):
                            action = self.move(0)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True
                    elif self.y < target_base.y:
                        if not any(base.x == self.x and base.y == self.y + 1 and not base.destroyed for base in
                                   self.red_bases):
                            action = self.move(3)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True
                    elif self.y > target_base.y:
                        if not any(base.x == self.x and base.y == self.y - 1 and not base.destroyed for base in
                                   self.red_bases):
                            action = self.move(2)
                            if action:
                                actions.append(action)
                            self.moved_this_frame = True

                else:
                    print("Error!")
            return actions


# def parse_input():
#     import sys
#     input = sys.stdin.read
#     data = input().split()
#
#     index = 0
#
#     # Read map size
#     n = int(data[index])
#     m = int(data[index + 1])
#     index += 2
#
#     # Read map
#     map_data = []
#     for i in range(n):
#         map_data.append(data[index])
#         index += 1
#
#     # Read blue bases
#     blue_base_count = int(data[index])
#     index += 1
#     blue_bases = []
#     for _ in range(blue_base_count):
#         x = int(data[index])
#         y = int(data[index + 1])
#         fuel_supply = int(data[index + 2])
#         missile_supply = int(data[index + 3])
#         defense_value = int(data[index + 4])
#         military_value = int(data[index + 5])
#         blue_bases.append((x, y, fuel_supply, missile_supply, defense_value, military_value))
#         index += 6
#
#     # Read red bases
#     red_base_count = int(data[index])
#     index += 1
#     red_bases = []
#     for _ in range(red_base_count):
#         x = int(data[index])
#         y = int(data[index + 1])
#         fuel_supply = int(data[index + 2])
#         missile_supply = int(data[index + 3])
#         defense_value = int(data[index + 4])
#         military_value = int(data[index + 5])
#         red_bases.append((x, y, fuel_supply, missile_supply, defense_value, military_value))
#         index += 6
#
#     # Read fighters
#     fighter_count = int(data[index])
#     index += 1
#     fighters = []
#     for _ in range(fighter_count):
#         id = int(data[index])
#         x = int(data[index + 1])
#         y = int(data[index + 2])
#         fuel_capacity = int(data[index + 3])
#         missile_capacity = int(data[index + 4])
#         fighters.append(Fighter(id, x, y, fuel_capacity, missile_capacity))
#         index += 5
#
#     return n, m, map_data, blue_bases, red_bases, fighters


def main():
    # n, m, map_data, blue_bases, red_bases, fighters = parse_input()
    filename = "../data/testcase2.in"
    info_dict = parse_game_data_from_file(filename)

    # get the info-dict from file
    map_size_info = info_dict['map_size']
    map_layout_info = info_dict['map_layout']
    blue_bases_info = info_dict['blue_bases']
    red_bases_info = info_dict['red_bases']
    fighters_info = info_dict['fighters']

    # 1.map_size
    n = map_size_info[0]
    m = map_size_info[1]

    # 2.map_layout
    global map_layout
    map_layout = map_layout_info

    # 3.blue_bases
    blue_bases = []
    for blue_base_id in range(len(blue_bases_info)):
        blue_base_info = blue_bases_info[blue_base_id]
        info_part_first = blue_base_info['position']
        info_part_second = blue_base_info['attributes']
        blue_base = Base(info_part_first[0], info_part_first[1], info_part_second[0], info_part_second[1],
                         info_part_second[2], info_part_second[3])
        blue_bases.append(blue_base)

    # 4.red_bases
    red_bases = []
    for red_base_id in range(len(red_bases_info)):
        red_base_info = red_bases_info[red_base_id]
        info_part_first = red_base_info['position']
        info_part_second = red_base_info['attributes']
        red_base = Base(info_part_first[0], info_part_first[1], info_part_second[0], info_part_second[1],
                        info_part_second[2], info_part_second[3])
        red_bases.append(red_base)

    # 5.fighters
    fighters = []
    for fighter_id in range(len(fighters_info)):
        fighter_info = fighters_info[fighter_id]
        fighter = Fighter(fighter_id, fighter_info[0], fighter_info[1], fighter_info[2], fighter_info[3], blue_bases,
                          red_bases)
        fighters.append(fighter)

    # Implement greedy strategy here
    # Example of simple strategy: Move all fighters towards the nearest red base
    # for fighter in fighters:
    #     while True:
    #         print(f"The {fighter.id}, has fuel {fighter.current_fuel}, and missiles {fighter.current_missiles}")
    #         # Find the nearest red base
    #         nearest_red_base = None
    #         min_distance = float('inf')
    #         for red_base in red_bases:
    #             distance = abs(fighter.x - red_base.x) + abs(fighter.y - red_base.y)
    #             if distance < min_distance:
    #                 min_distance = distance
    #                 nearest_red_base = red_base
    #
    #         if nearest_red_base is None:
    #             break
    #
    #         red_x = nearest_red_base.x
    #         red_y = nearest_red_base.y
    #         if fighter.x < red_x:
    #             fighter.move(1)
    #         elif fighter.x > red_x:
    #             fighter.move(0)
    #         elif fighter.y < red_y:
    #             fighter.move(3)
    #         elif fighter.y > red_y:
    #             fighter.move(2)
    #         else:
    #             # At the red base, attack it
    #             fighter.attack(1, min(fighter.current_missiles, nearest_red_base.defense))
    #             if nearest_red_base.defense <= 0:
    #                 red_bases.remove(nearest_red_base)
    #             break
    #
    #     print("OK")

    # frame
    frame_count = 0
    while frame_count < 15000:
        frame_count += 1
        actions = []

        for fighter in fighters:
            fighter.moved_this_frame = False
            fighter_actions = fighter.generate_actions()
            actions.extend(fighter_actions)

        # Print actions for this Frame
        for action in actions:
            print(action)

        # # Print debug information for each aircraft
        # for aircraft in aircrafts:
        #     print(f"[DEBUG] Aircraft {aircraft.id}: Fuel {aircraft.fuel}, Missile {aircraft.missile}")

        # Print "OK" to indicate the end of this frame
        print("OK")

if __name__ == "__main__":
    main()
