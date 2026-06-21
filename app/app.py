import logging
import tempfile

from sdk.moveapps_spec import hook_impl
from movingpandas import TrajectoryCollection
from randomwalks import StateDependentWalker
from randomwalks.bindings.walk_visualization import save_trajectory_collection_timed

from app.config import ConfigDto

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config: ConfigDto = ConfigDto(config)
        logging.info(f'Welcome to the {config}')

        kernels_dir = self.moveapps_io.create_artifacts_file("kernels.png")
        visualization_dir = self.moveapps_io.create_artifacts_file("animated_trajectories.html")

        result = data
        with tempfile.TemporaryDirectory(dir=".") as tmp_dir:
            try:
                with StateDependentWalker(
                    data=data,
                    animal_type=config.animal_type,
                    resolution=config.grid_resolution,
                    out_directory=str(tmp_dir),
                    movement_policy=config.movement_policy,
                    barriers=config.barriers,
                ) as walker:
                    walker.get_kernels(
                        n_hmm_states=config.hmm_states,
                        dt_tolerance=config.dt_tolerance,
                        rnge=config.rnge,
                        is_brownian=config.is_brownian,
                        plot_dir=kernels_dir,
                    )
                    result = walker.generate_walks(
                        max_cell_size=config.cell_resolution,
                        barrier_mode=config.barrier_mode,
                    )

                # save artifact: animated trajectories
                save_trajectory_collection_timed(result, visualization_dir)
            except Exception as e:
                logging.info(str(e))
                logging.info("Execution failed, returning input\n")
            else:
                logging.info("Successful execution\n")

        # return the resulting data for next Apps in the Workflow
        return result
