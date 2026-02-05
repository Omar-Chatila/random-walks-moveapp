from sdk.moveapps_spec import hook_impl
from sdk.moveapps_io import MoveAppsIo
from movingpandas import TrajectoryCollection
import logging
import matplotlib.pyplot as plt

from random_walk_package import StateDependentWalker, TimeStepPolicy, SpeedBasedPolicy
# showcase for importing functions from another .py file (in this case from "./app/getGeoDataFrame.py")
from app.getGeoDataFrame import get_GDF

from app.config import ConfigDto, MovementPolicy

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config = ConfigDto(config)
        logging.info(f'Welcome to the {config}')

        walker = StateDependentWalker(data=data,
                                      animal_type=config.animal_type,
                                      resolution=config.grid_resolution,
                                      out_directory="resources")

        mvm_pol = TimeStepPolicy(config.time_step_seconds)
        if config.movement_policy == MovementPolicy.TIME_STEP:
            mvm_pol = TimeStepPolicy(config.time_step_seconds)
        elif config.movement_policy == MovementPolicy.FIXED_STEPS:
            mvm_pol = TimeStepPolicy(config.num_steps)
        else:
            mvm_pol = SpeedBasedPolicy(config.time_step_seconds,
                                       config.reference_speed,
                                       config.grid_resolution)

        result = walker.generate_walks(dt_tolerance=config.dt_tolerance, rnge=1000, movement_policy=mvm_pol)


        #logging.info(f'Subsetting data for {config.year}')

        # showcase creating an artifact
        if result is not None:
            result.plot(column=data.get_traj_id_col(), alpha=0.5)
            plot_file = self.moveapps_io.create_artifacts_file("plot.png")
            plt.savefig(plot_file)
            logging.info(f'saved plot to {plot_file}')
        else:
            logging.warning("Nothing to plot")

        # showcase accessing auxiliary files
        auxiliary_file_a = MoveAppsIo.get_auxiliary_file_path("auxiliary-file-a")
        with open(auxiliary_file_a, 'r') as f:
            logging.info(f.read())

        # Translate the result back to a TrajectoryCollection
        if result is not None:
            result = TrajectoryCollection(
                result,
                traj_id_col=data.get_traj_id_col(),
                t=data.to_point_gdf().index.name,
                crs=data.get_crs()
            )

        # return the resulting data for next Apps in the Workflow
        return result
