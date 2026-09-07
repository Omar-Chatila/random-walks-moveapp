import logging
import tempfile

from sdk.moveapps_spec import hook_impl
from movingpandas import TrajectoryCollection
from hmmcma import Feature
from randomwalks import StateDependentWalker, StateAnnotationMethod
from randomwalks.bindings.walk_visualization import save_trajectory_collection_timed

from app.config import ConfigDto

class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        config: ConfigDto = ConfigDto(config)
        logging.info('Starting state-dependent walks with adaptive kernel movement policy')

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
                    walker.annotate_behavior(
                        method=StateAnnotationMethod.HMM,
                        features=[Feature.TURN_ANGLE, Feature.SPEED],
                        num_states=config.hmm_states,
                    )
                    walker.get_kernels(
                        kernel_config=config.kernel_config,
                        plot_dir=kernels_dir,
                    )
                    result = walker.generate_walks(
                        max_cell_size=config.cell_resolution,
                        barrier_mode=config.barrier_mode,
                    )

                # save artifact: animated trajectories
                save_trajectory_collection_timed(result, visualization_dir)
            except Exception:
                logging.exception("Random-walk generation failed")
                logging.info("Execution failed, returning input\n")
            else:
                logging.info("Successful execution\n")

        # return the resulting data for next Apps in the Workflow
        return result
