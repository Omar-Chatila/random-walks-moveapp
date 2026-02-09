import os
import logging

from sdk.moveapps_spec import hook_impl
from movingpandas import TrajectoryCollection

from random_walk_package import StateDependentWalker, save_trajectory_collection_timed

# showcase for importing functions from another .py file (in this case from "./app/getGeoDataFrame.py")

from app.config import ConfigDto

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config:ConfigDto = ConfigDto(config)
        logging.info(f'Welcome to the {config}')
        
        output_dir = os.environ.get('APP_ARTIFACTS_DIR', './resources/output')
        try:
            walker = StateDependentWalker(data=data,
                                        animal_type=config.animal_type, 
                                        resolution=config.grid_resolution,
                                        out_directory=output_dir, 
                                        n_hmm_states=config.hmm_states)

            result = walker.generate_walks(out_dir=output_dir,
                                        dt_tolerance=config.dt_tolerance, 
                                        rnge=config.rnge, 
                                        movement_policy=config.movement_policy, 
                                        max_cell_size=config.cell_resolution, 
                                        water_mode=config.water_mode,
                                        is_brownian=config.walk_model == 1)
            
            save_trajectory_collection_timed(result, output_dir)
        except Exception as e:
            logging.info(str(e))
            return data
        

        #logging.info(f'Subsetting data for {config.year}')
        #plot_file = self.moveapps_io.create_artifacts_file("plot.png")

        # return the resulting data for next Apps in the Workflow
        return result
