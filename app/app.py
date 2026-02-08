from sdk.moveapps_spec import hook_impl
from sdk.moveapps_io import MoveAppsIo
from movingpandas import TrajectoryCollection
import logging
import matplotlib.pyplot as plt

from random_walk_package import StateDependentWalker

# showcase for importing functions from another .py file (in this case from "./app/getGeoDataFrame.py")

from app.config import ConfigDto

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config:ConfigDto = ConfigDto(config)
        logging.info(f'Welcome to the {config}')

        output_dir = self.moveapps_io.get_artifacts_dir()

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
                                      is_brownian=config.walk_model)
        

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
