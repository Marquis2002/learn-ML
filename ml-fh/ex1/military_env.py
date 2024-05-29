from pettingzoo import AECEnv
import gymnasium
import numpy as np
from typing import Dict, Union, Tuple, List, Optional
from parse_game import parse_game_data_from_file


class MilitaryEnv(AECEnv):
    def __init__(self, info_dict: Dict[str, Union[Dict[str, int], Tuple[int, ...], List[int]]]):
        self.red_bases = info_dict['red_bases']
        self.blue_bases = info_dict['blue_bases']
        self.fighters = info_dict['fighters']
        self.map_size = info_dict[]


        pass

    def action_space(self, agent: AgentID) -> gymnasium.spaces.Space:
        pass
    def observation_space(self, agent: AgentID) -> gymnasium.spaces.Space:
        pass

    def observe(self, agent: AgentID) -> ObsType | None:
        pass
    def step(self, action: ActionType) -> None:
        pass
    def render(self) -> None | np.ndarray | str | list:
        pass
    def reset(
        self,
        seed: int | None = None,
        options: dict | None = None,
    ) -> None:
        pass

