# Changelog SDK

## 2026-03-09 `v1.1.0`

- improve robustness for heterogeneous input trajectories
- enhance HMM model fitting, state prediction and model selection
- fix column order issue in HMM feature processing and state assignment
- improve HMM preprocessing and subsequence generation
- add trajectory segmentation based on radius criterion
- refactor UTM transformations to use segment-consistent projections
- fix UTM/grid projection issues in segment-based walk generation
- refine `S`/`T` calculation in movement policies
- add fixed-step movement policy
- improve handling of lower and upper bounds for spatial and temporal walk parameters
- improve kernel clipping, resampling and grid-based kernel generation
- add debug export of resampled kernels as PNG