"""Exercise the installed native backend without external trajectory data."""
import numpy as np

from randomwalks.bindings.data_structures.KernelContext import KernelContextHandle
from randomwalks.bindings.data_structures.KernelMapping import KernelMapping
from randomwalks.bindings.data_structures.Terrain import MesaLandcover, TerrainMapHandle
from randomwalks.bindings.data_structures.types import Reachability
from randomwalks.bindings.mixed_walk import MixedWalkBinding


def test_full_reachability_and_streaming_ud_match_full_result():
    terrain = TerrainMapHandle.single_value(MesaLandcover.GRASSLAND, 7, 7)
    mapping = KernelMapping.from_state_kernel(terrain, np.ones((3, 3)), directions=8)
    context = None
    forward = None
    try:
        context = KernelContextHandle.pool(terrain, mapping, Reachability.FULL)
        forward = MixedWalkBinding.walk(context, 4, 1, 2)
        path = MixedWalkBinding.backtrace(forward, context, 5, 4)
        assert len(path) == 5
        np.testing.assert_array_equal(path[0], [1, 2])
        np.testing.assert_array_equal(path[-1], [5, 4])
        direct = MixedWalkBinding.single_state_walk(context, 4, 1, 2, 5, 4)
        assert len(direct) == 5
        np.testing.assert_array_equal(direct[0], [1, 2])
        np.testing.assert_array_equal(direct[-1], [5, 4])
        full_handle = MixedWalkBinding.utilization_distribution(forward, context, 5, 4)
        reduced_handle = MixedWalkBinding.utilization_distribution_sum(forward, context, 5, 4)
        try:
            full = full_handle.to_numpy_sum(7, 7, average=True)
            reduced = reduced_handle.to_numpy()
            assert np.isfinite(reduced).all()
            assert reduced.sum() > 0
            np.testing.assert_allclose(reduced, full, rtol=1e-12, atol=1e-12)
        finally:
            full_handle.free()
            reduced_handle.free()
    finally:
        if forward is not None:
            forward.free()
        if context is not None:
            context.free()
        mapping.free()
        terrain.free()
