import numpy as np
import matplotlib.pyplot as plt


def parse_game_data_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n')
        n, m = map(int, lines[0].split())  # Map size
        map_layout = lines[1:n + 1]  # Map layout

        offset = n + 1
        blue_base_count = int(lines[offset])  # Number of blue bases
        blue_bases = []
        for i in range(offset + 1, offset + 1 + 2 * blue_base_count, 2):
            if i + 1 >= len(lines):  # Check for out-of-bounds
                print("Error: Incomplete base information.")
                return None
            position = tuple(map(int, lines[i].split()))  # Base position
            attributes = list(map(int, lines[i + 1].split()))  # Base attributes
            blue_bases.append({'position': position, 'attributes': attributes})

        offset += 2 * blue_base_count + 1
        red_base_count = int(lines[offset])  # Number of red bases
        red_bases = []
        for i in range(offset + 1, offset + 1 + 2 * red_base_count, 2):
            if i + 1 >= len(lines):  # Check for out-of-bounds
                print("Error: Incomplete base information.")
                return None
            position = tuple(map(int, lines[i].split()))  # Base position
            attributes = list(map(int, lines[i + 1].split()))  # Base attributes
            red_bases.append({'position': position, 'attributes': attributes})

        offset += 2 * red_base_count + 1
        if offset >= len(lines):  # Check for fighter count line
            print("Error: Missing fighter count information.")
            return None
        fighter_count = int(lines[offset])  # Number of fighters
        fighters = []
        for i in range(offset + 1, offset + 1 + fighter_count):
            if i >= len(lines):  # Check for out-of-bounds
                print("Error: Incomplete fighter information.")
                return None
            fighters.append(list(map(int, lines[i].split())))  # Fighter attributes

        # Create a numpy array for map layout
        map_observation = np.zeros((len(map_layout), len(map_layout[0])), dtype=np.uint8)
        for i, row in enumerate(map_layout):
            for j, cell in enumerate(row):
                if cell == '.':
                    map_observation[i, j] = 0  # Neutral area
                elif cell == '#':
                    map_observation[i, j] = 2  # Red base
                elif cell == '*':
                    map_observation[i, j] = 1  # Blue base

        return {
            'map_size': (n, m),
            'map_layout': map_observation,
            'blue_bases': blue_bases,
            'red_bases': red_bases,
            'fighters': fighters
        }


def display_game_data(game_data):
    n, m = game_data['map_size']
    map_layout = game_data['map_layout']
    blue_bases = game_data['blue_bases']
    red_bases = game_data['red_bases']
    fighters = game_data['fighters']

    fig, ax = plt.subplots(figsize=(m, n))
    plt.xlim(-0.5, m - 0.5)
    plt.ylim(-0.5, n - 0.5)

    # Draw the map layout
    for y, row in enumerate(map_layout):
        for x, cell in enumerate(row):
            plot_y = n - 1 - y
            if cell == 0:
                ax.plot(x, plot_y, marker='s', color='white', markersize=30)
            elif cell == 1:
                ax.plot(x, plot_y, marker='*', color='blue', markersize=20)
            elif cell == 2:
                ax.plot(x, plot_y, marker='p', color='red', markersize=20)

    # Mark fighters
    for fighter in fighters:
        x, y = fighter[1], fighter[0]
        plot_y = n - 1 - y
        ax.plot(x, plot_y, marker='^', color='green', markersize=10)

    plt.gca().invert_yaxis()  # Ensure correct y-axis orientation
    plt.axis('on')
    ax.set_xticks(range(m))
    ax.set_yticks(range(n))
    ax.grid(which='both')

    plt.savefig('test1.png')

    # plt.show()


if __name__ == '__main__':
    filename = "../data/testcase1.in"  # Update this to the correct path if necessary
    info_dict = parse_game_data_from_file(filename)
    # if info_dict:
    #     display_game_data(info_dict)
