from parse_game import parse_game_data_from_file
from military_env import MilitaryEnv

def main():
    filename = "../data/testcase1.in"
    info_dict = parse_game_data_from_file(filename)

    env = MilitaryEnv(info_dict)



main()