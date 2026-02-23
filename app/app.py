import os
import logging

from sdk.moveapps_spec import hook_impl
from movingpandas import TrajectoryCollection
from random_walk_package import StateDependentWalker, save_trajectory_collection_timed

from app.config import ConfigDto

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config:ConfigDto = ConfigDto(config)
        logging.info(f'Welcome to the {config}')

        successful = True

        kernels_dir = self.moveapps_io.create_artifacts_file("kernels2.png");
        visualization_dir = self.moveapps_io.create_artifacts_file("");

        tmp_dir = os.environ.get('APP_ARTIFACTS_DIR', './resources/auxiliary')
        try:
            walker = StateDependentWalker(data=data,
                                        animal_type=config.animal_type, 
                                        resolution=config.grid_resolution,
                                        out_directory=tmp_dir,
                                        n_hmm_states=config.hmm_states)

            result = walker.generate_walks(out_dir=kernels_dir,
                                        dt_tolerance=config.dt_tolerance, 
                                        rnge=config.rnge, 
                                        movement_policy=config.movement_policy, 
                                        max_cell_size=config.cell_resolution, 
                                        water_mode=config.water_mode,
                                        is_brownian=config.walk_model == 1)

            # save artifact: animated trajectories
            save_trajectory_collection_timed(result, visualization_dir)
        except Exception as e:
            successful = False
            logging.info(str(e))
            return data
        logging.info(f"Successful execution\n")
        # return the resulting data for next Apps in the Workflow
        return result
