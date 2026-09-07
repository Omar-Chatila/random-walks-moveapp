import inspect
import json
from pathlib import Path
from unittest.mock import create_autospec, patch

import pytest
from hmmcma import Feature
from randomwalks import AdaptiveKernelMovementPolicy, Animal, BarrierMode, StateAnnotationMethod, StateDependentWalker

from app.app import App
from app.config import ConfigDto
from sdk.moveapps_io import MoveAppsIo


@pytest.mark.parametrize('model', [1, 2, 3])
def test_policy_is_always_adaptive_even_with_legacy_settings(model):
    config = ConfigDto({'walk_model': model, 'movement_policy': 'FIXED_STEPS', 'num_steps': 3})
    assert isinstance(config.movement_policy, AdaptiveKernelMovementPolicy)


def test_correlated_uses_automatic_range_and_ignores_brownian_time_override():
    config = ConfigDto({'walk_model': 2, 'brownian_time_factor': 3, 'rnge': 7})
    assert config.kernel_config.range_m is None
    assert config.kernel_config.time_factor is None


def test_brownian_uses_automatic_range_and_native_interval_divisor():
    config = ConfigDto({'walk_model': 1, 'brownian_time_factor': 3})
    assert config.kernel_config.range_m is None
    assert config.kernel_config.model_timestep_s(900) == 300
    assert config.kernel_config.is_brownian
    assert ConfigDto({'walk_model': 1}).kernel_config.range_m is None


@pytest.mark.parametrize('key,value', [
                                      ('brownian_time_factor', 0),
                                      ('brownian_time_factor', float('nan')), ('hmm_states', 2.5)])
def test_invalid_parameters_are_rejected(key, value):
    with pytest.raises(ValueError):
        ConfigDto({'walk_model': 1, key: value})


def test_barrier_names_match_new_library_and_animal_presets():
    assert ConfigDto({'animal_type': 1, 'barrier_mode': 'FULL_REACHABILITY'}).barrier_mode == BarrierMode.ALLOW
    assert ConfigDto({'animal_type': 0}).animal_type == Animal.AIRBORNE
    assert ConfigDto({'animal_type': 0}).barrier_mode == BarrierMode.ALLOW
    assert ConfigDto({'animal_type': 2}).barriers is None


@pytest.mark.parametrize('model', [1, 2])
def test_app_calls_current_walker_interface_in_order(tmp_path, monkeypatch, model):
    monkeypatch.setenv('APP_ARTIFACTS_DIR', str(tmp_path))
    # Autospec uses the installed library's real signatures, catching API drift.
    walker = create_autospec(StateDependentWalker, instance=True)
    walker.__enter__.return_value = walker
    expected = object()
    walker.generate_walks.return_value = expected
    with patch('app.app.StateDependentWalker', autospec=True) as constructor, \
         patch('app.app.save_trajectory_collection_timed') as save:
        constructor.return_value = walker
        result = App(MoveAppsIo()).execute(object(), {'walk_model': model})
    assert result is expected
    assert isinstance(constructor.call_args.kwargs['movement_policy'], AdaptiveKernelMovementPolicy)
    walker.annotate_behavior.assert_called_once_with(
        method=StateAnnotationMethod.HMM, features=[Feature.TURN_ANGLE, Feature.SPEED], num_states=3)
    kwargs = walker.get_kernels.call_args.kwargs
    assert 'rnge' not in kwargs
    assert 'n_hmm_states' not in kwargs
    assert kwargs['kernel_config'].is_brownian == (model == 1)
    names = [call[0] for call in walker.mock_calls]
    assert names.index('annotate_behavior') < names.index('get_kernels') < names.index('generate_walks')
    save.assert_called_once_with(expected, str(tmp_path / 'animated_trajectories.html'))


def test_appspec_defaults_and_example_config_match():
    root = Path(__file__).resolve().parents[2]
    settings = json.loads((root / 'appspec.json').read_text())['settings']
    defaults = {setting['id']: setting['defaultValue'] for setting in settings}
    example = json.loads((root / 'app-configuration.json').read_text())
    assert set(defaults) == set(example)
    assert not {'movement_policy', 'time_step_seconds', 'num_steps', 'reference_speed', 'rnge',
                'brownian_range_m'} & set(defaults)
 
    assert 'kernel_config' in inspect.signature(StateDependentWalker.get_kernels).parameters
