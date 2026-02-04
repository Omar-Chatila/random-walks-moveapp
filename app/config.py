from optparse import Option
from typing import Optional
from enum import Enum


from pydantic import BaseModel, Field

class AnimalType(int, Enum):
    AIRBORNE = 0
    TERRESTRIAL = 1
    MARINE = 2

class WaterMode(int, Enum):
    FORBID = 0
    AVOID = 1
    ALLOW = 2

class MovementPolicy(str, Enum):
    TIME_STEP = "TIME_STEP"
    FIXED_STEPS = "FIXED_STEPS"
    AUTO_SPEED = "AUTO_SPEED"



class ConfigDto(BaseModel):
    def __init__(self, config: dict):
        super().__init__()
        self.__config = config
        self.__animal_type: AnimalType = config.get("animal_type", AnimalType.AIRBORNE)
        self.__water_mode: WaterMode = config.get("water_mode", WaterMode.FORBID)
        self.__grid_resolution: int = config.get("grid_resolution", 350)
        self.__movement_policy: MovementPolicy = config.get("movement_policy", MovementPolicy.TIME_STEP)
        self.__time_step_seconds:Optional[int] = config.get("time_step_seconds", 180)
        self.__num_steps:Optional[int] = config.get("num_steps", 10)
        self.__reference_speed: Optional[float] = config.get("reference_speed", 1.0)
        self.__dt_tolerance: Optional[float] = config.get("dt_tolerance", 2.0)
        self.__year = config.get("year", 2014)

    @property
    def animal_type(self) -> AnimalType:
        return self.__animal_type

    @property
    def water_mode(self) -> WaterMode:
        return self.__water_mode

    @property
    def grid_resolution(self) -> int:
        return self.__grid_resolution

    @property
    def movement_policy(self) -> MovementPolicy:
        return self.__movement_policy

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
    def year(self) -> int:
        return self.__year

