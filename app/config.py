from optparse import Option
from typing import Optional
from enum import Enum

from random_walk_package import Animal, MovementPolicyCfg, SpeedBasedPolicy, TimeStepPolicy, WaterMode, MovementPolicy


from pydantic import BaseModel


class ConfigDto(BaseModel):
    def __init__(self, config: dict):
        super().__init__()
        self.__animal_type: int = int(config.get("animal_type", Animal.AIRBORNE))
        self.__water_mode: WaterMode = config.get("water_mode", WaterMode.FORBID)

        self.__cell_resolution: int = config.get("cell_resolution", 50)
        self.__grid_resolution: int = config.get("grid_resolution", 350)

        self.__movement_policy: MovementPolicyCfg = config.get("movement_policy", MovementPolicyCfg.TIME_STEP)
        self.__time_step_seconds:Optional[int] = config.get("time_step_seconds", 180)
        self.__num_steps:Optional[int] = config.get("num_steps", 10)
        self.__reference_speed: Optional[float] = config.get("reference_speed", 1.0)

        self.__dt_tolerance: Optional[float] = config.get("dt_tolerance", 2.0)

        self.__hmm_states: Optional[int] = config.get("hmm_states", 3)
        self.__rnge: Optional[int] = config.get("rnge", 500)

        self.__walk_model: Optional[int] = config.get("walk_model", 1) 
        self.__year = config.get("year", 2014)

    @property
    def animal_type(self) -> int:
        return self.__animal_type

    @property
    def water_mode(self) -> WaterMode:
        return self.__water_mode

    @property
    def cell_resolution(self) -> int:
        return self.__cell_resolution

    @property
    def grid_resolution(self) -> int:
        return self.__grid_resolution

    @property
    def movement_policy(self) -> MovementPolicy:
        mvm_pol = TimeStepPolicy(self.time_step_seconds)
        if self.__movement_policy == MovementPolicyCfg.TIME_STEP:
            mvm_pol = TimeStepPolicy(self.time_step_seconds)
        elif self.__movement_policy == MovementPolicyCfg.FIXED_STEPS:
            mvm_pol = TimeStepPolicy(self.num_steps)
        else:
            mvm_pol = SpeedBasedPolicy(self.time_step_seconds,
                                       self.reference_speed,
                                       self.grid_resolution)
        return mvm_pol

    @property
    def time_step_seconds(self) -> Optional[int]:
        return self.__time_step_seconds

    @property
    def num_steps(self) -> Optional[int]:
        return self.__num_steps

    @property
    def reference_speed(self) -> Optional[float]:
        return self.__reference_speed

    @property
    def dt_tolerance(self) -> Optional[float]:
        return self.__dt_tolerance
    
    @property
    def hmm_states(self) -> Optional[int]:
        return self.__hmm_states
    
    @property
    def rnge(self) -> Optional[int]:
        return self.__rnge
    
    @property
    def walk_model(self) -> Optional[int]:
        return self.__walk_model

    @property
    def year(self) -> int:
        return self.__year

