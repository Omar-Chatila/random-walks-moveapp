from math import isfinite

from kernelcma import KernelConfig, KernelKind
from randomwalks import AdaptiveKernelMovementPolicy, Animal, BarrierMode, MesaLandcover


class ConfigDto:
    """MoveApps settings mapped to the current state-dependent walker API."""

    def __init__(self, config: dict):
        self.animal_type = {0: Animal.AIRBORNE, 1: Animal.TERRESTRIAL, 2: Animal.MARINE}[
            int(config.get("animal_type", 1))
        ]
        mode = config.get("barrier_mode", "AVOID")
        # MoveApps keeps its existing setting value; the library calls it ALLOW.
        self.barrier_mode = (
            BarrierMode.ALLOW if mode == "FULL_REACHABILITY"
            else BarrierMode[mode] if isinstance(mode, str)
            else BarrierMode(mode)
        )
        self.barriers = []
        if self.animal_type == Animal.TERRESTRIAL:
            if config.get("water_barrier", False):
                self.barriers.append(MesaLandcover.PERMANENT_WATER)
            if config.get("builtup_barrier", False):
                self.barriers.append(MesaLandcover.BUILT_UP)
        elif self.animal_type == Animal.MARINE:
            # Let the walker select its marine land barrier and default mode.
            self.barriers = None
            self.barrier_mode = None
        else:
            self.barrier_mode = BarrierMode.ALLOW

        self.cell_resolution = self._positive(config.get("cell_resolution", 50), "cell_resolution")
        self.grid_resolution = self._integer(config.get("grid_resolution", 500), "grid_resolution")
        self.hmm_states = self._integer(config.get("hmm_states", 3), "hmm_states")
        self.dt_tolerance = self._positive(config.get("dt_tolerance", 2.0), "dt_tolerance")
        self.walk_model = int(config.get("walk_model", 1))
        if self.walk_model not in (1, 2, 3):
            raise ValueError("walk_model must be 1, 2, or 3.")
        self.is_brownian = self.walk_model == 1 or (
            self.walk_model == 3 and self.animal_type == Animal.TERRESTRIAL
        )
        kernel_options = {
            "kind": KernelKind.BROWNIAN if self.is_brownian else KernelKind.CORRELATED,
            "dt_tolerance": self.dt_tolerance,
            "range_m": None,
            "mass_percentile": 99,
        }
        if self.is_brownian:
            kernel_options["time_factor"] = self._positive(
                config.get("brownian_time_factor", 1), "brownian_time_factor"
            )
        self.kernel_config = KernelConfig(**kernel_options)

    @property
    def movement_policy(self):
        return AdaptiveKernelMovementPolicy()

    @staticmethod
    def _positive(value, name):
        number = float(value)
        if not isfinite(number) or number <= 0:
            raise ValueError(f"{name} must be finite and positive.")
        return number

    @classmethod
    def _integer(cls, value, name):
        number = cls._positive(value, name)
        if not number.is_integer():
            raise ValueError(f"{name} must be an integer.")
        return int(number)

    @staticmethod
    def _probability(value, name):
        number = float(value)
        if not isfinite(number) or not 0 < number < 1:
            raise ValueError(f"{name} must be between 0 and 1 (exclusive).")
        return number
