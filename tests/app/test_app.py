import unittest
import os
from tests.config.definitions import ROOT_DIR
from app.app import App
from app.config import *
from sdk.moveapps_io import MoveAppsIo
import pandas as pd
import movingpandas as mpd


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['APP_ARTIFACTS_DIR'] = os.path.join(ROOT_DIR, 'tests/resources/output')
        self.sut = App(moveapps_io=MoveAppsIo())

    def test_bird_run(self):
        # prepare
        data: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/input4_LatLon.pickle'))
        print(data.to_point_gdf().head())
        short_trajs = []

        for traj in data:
            short_df = traj.df.iloc[:20].copy()
            short_traj = mpd.Trajectory(short_df, traj.id)
            short_trajs.append(short_traj)

        data = mpd.TrajectoryCollection(short_trajs)

        config: dict = {
            "animal_type": 0,
            "water_mode": 2,

            "cell_resolution": 50,
            "grid_resolution": 300,

            "movement_policy": "TIME_STEP",
            "time_step_seconds": 300,

            "num_steps": 10,
            "reference_speed": 1.2,

            "dt_tolerance": 4.0,

            "hmm_states": 3,
            "rnge": 700,

            "walk_model": 2,
            }


        # execute
        result = self.sut.execute(data=data, config=config)
        assert result is not None


    def test_terrestrial_run(self):
        # prepare
        data: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/input1_LatLon.pickle'))
        print(data.to_point_gdf().head())
        short_trajs = []

        for traj in data:
            short_df = traj.df.iloc[:20].copy()
            short_traj = mpd.Trajectory(short_df, traj.id)
            short_trajs.append(short_traj)

        data = mpd.TrajectoryCollection(short_trajs)

        config: dict = {
            "animal_type": 1,
            "water_mode": 1,

            "cell_resolution": 50,
            "grid_resolution": 300,

            "movement_policy": "TIME_STEP",
            "time_step_seconds": 300,

            "num_steps": 10,
            "reference_speed": 1.2,

            "dt_tolerance": 4.0,

            "hmm_states": 2,
            "rnge": 200,

            "walk_model": 1,
            }


        # execute
        result = self.sut.execute(data=data, config=config)
        assert result is not None

    def test_terrestrial_run_mollweide(self):
        # prepare
        data: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/input1_Mollweide.pickle'))
        print(data.to_point_gdf().head())
        short_trajs = []

        for traj in data:
            short_df = traj.df.iloc[:20].copy()
            short_traj = mpd.Trajectory(short_df, traj.id)
            short_trajs.append(short_traj)

        data = mpd.TrajectoryCollection(short_trajs)

        config: dict = {
            "animal_type": 1,
            "water_mode": 1,

            "cell_resolution": 50,
            "grid_resolution": 300,

            "movement_policy": "TIME_STEP",
            "time_step_seconds": 300,

            "num_steps": 10,
            "reference_speed": 1.2,

            "dt_tolerance": 4.0,

            "hmm_states": 2,
            "rnge": 200,

            "walk_model": 1,
            }


        # execute
        result = self.sut.execute(data=data, config=config)
        assert result is not None

    def test_app_config(self):
        # prepare
        config: dict = {
            "animal_type": 0,
            "water_mode": 2,

            "cell_resolution": 50,
            "grid_resolution": 300,

            "movement_policy": "TIME_STEP",
            "time_step_seconds": 300,

            "num_steps": 10,
            "reference_speed": 1.2,

            "dt_tolerance": 4.0,

            "hmm_states": 2,
            "rnge": 700,

            "walk_model": 2,
            }

        # execute
        actual = config

        # verify
        self.assertEqual(0, actual["animal_type"])
        self.assertEqual(2, actual["water_mode"])
        self.assertEqual(50, actual["cell_resolution"])
        self.assertEqual("TIME_STEP", actual["movement_policy"])


    
    """
    # Use this test if the App should return the input data
    def test_app_returns_input(self):
        # prepare
        expected: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/input2_LatLon.pickle'))
        config: dict = {}

        # execute
        actual = self.sut.execute(data=expected, config=config)

        # verif
        self.assertEqual(expected, actual)
    """
