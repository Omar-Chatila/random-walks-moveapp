from typing import Optional

from randomwalks.bindings.data_structures.Terrain import Animal, BarrierMode, MesaLandcover, MovementPolicyCfg
from randomwalks.core.MovementPolicy import FixedStepsPolicy, MovementPolicy, SpeedBasedPolicy, TimeStepPolicy

from pydantic import BaseModel

class ConfigDto(BaseModel):
    def __init__(self, config: dict):
        super().__init__()

        self.__animal_type: int = int(config.get("animal_type", 0))

        self.__water_barrier: bool = bool(config.get("water_barrier", False))
        self.__builtup_barrier: bool = bool(config.get("builtup_barrier", False))

        try:
            self.__barrier_mode: BarrierMode = BarrierMode(
                config.get("barrier_mode", BarrierMode.AVOID)
            )
        except ValueError:
            self.__barrier_mode = BarrierMode.AVOID

        self.__cell_resolution: int = int(config.get("cell_resolution", 50))
        self.__grid_resolution: int = int(config.get("grid_resolution", 350))

        self.__movement_policy: MovementPolicyCfg = self.__coerce_movement_policy(
            config.get("movement_policy", MovementPolicyCfg.TIME_STEP)
        )

        self.__time_step_seconds: Optional[int] = config.get("time_step_seconds", 180)
        self.__num_steps: Optional[int] = config.get("num_steps", 10)
        self.__reference_speed: Optional[float] = config.get("reference_speed", 1.0)

        self.__dt_tolerance: Optional[float] = config.get("dt_tolerance", 2.0)

        self.__hmm_states: Optional[int] = config.get("hmm_states", 3)
        self.__rnge: Optional[int] = config.get("rnge", 500)

        self.__walk_model: Optional[int] = int(config.get("walk_model", 1))

    @staticmethod
    def __coerce_movement_policy(value) -> MovementPolicyCfg:
        if isinstance(value, MovementPolicyCfg):
            return value
        try:
            return MovementPolicyCfg(value)
        except ValueError:
            return MovementPolicyCfg[str(value).upper()]

    @property
    def animal_type(self) -> Animal:
        if self.__animal_type == 0:
            return Animal.AIRBORNE
        elif self.__animal_type == 1:
            return Animal.TERRESTRIAL
        else:
            return Animal.MARINE

    @property
    def barrier_mode(self) -> BarrierMode:
        return self.__barrier_mode

    @property
    def water_mode(self) -> BarrierMode:
        return self.barrier_mode

    @property
    def barriers(self) -> list[MesaLandcover]:
        if self.animal_type == Animal.AIRBORNE:
            return []
        if self.animal_type == Animal.MARINE:
            return []
        barriers = []
        if self.__builtup_barrier:
            barriers.append(MesaLandcover.BUILT_UP)
        if self.__water_barrier:
            barriers.append(MesaLandcover.PERMANENT_WATER)
        return barriers

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
            mvm_pol = FixedStepsPolicy(self.num_steps)
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
    def is_brownian(self) -> bool:
        if self.__walk_model == 1:
            return True
        if self.__walk_model == 2:
            return False
        return self.animal_type == Animal.TERRESTRIAL
