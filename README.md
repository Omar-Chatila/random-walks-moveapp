# Random Walks MoveApp

This MoveApp provides a ready-to-use application of the
**state-dependent random walk model** for animal movement simulation
as described in the reference paper below.

---

## Example Outputs

Tiger Shark around Hawaii   |  Wild Boar in Austria
:-------------------------:|:-------------------------:
<img width="1191" height="682" src="https://github.com/user-attachments/assets/e0817c58-500f-4b40-bc9c-4a1d1c140843" /> | <img width="756" height="617" src="https://github.com/user-attachments/assets/bc4370fa-c5a1-48da-822a-47d1c7d604d9" />

---

## Scientific Background

This app is based on the following publication:

> **State-Dependent Random Walks for Realistic Animal Movement Simulation**  
> *ACM SIGSPATIAL 2024*  
> https://dl.acm.org/doi/10.1145/3678717.3691231

---

## Base Implementation (Algorithm Package)

The core algorithm and model implementation is provided by the
**Random Walks Python package**, which implements the methods described
in the paper:

🔗 **Random Walks – Core Python Implementation (Backend in C)**  
https://github.com/ls11ae/random-walks-python/tree/state-walks

This MoveApp acts as a **wrapper and integration layer** for MoveApps,
handling input/output, configuration, and execution within the
MoveApps ecosystem.

---

## MoveApp Repository

The MoveApps-specific implementation (this repository):

🔗 https://github.com/Omar-Chatila/random-walks-moveapp

---

## Description

This App generates realistic, state-dependent random walk trajectories between observed animal locations. Movement kernels are learned directly from the input trajectories using Gaussian mixture models and Hidden Markov Models (HMMs), enabling behaviour-specific movement simulation. The generated walks interpolate between observed fixes and produce temporally continuous trajectories that respect movement behaviour, terrain context, and timing constraints.

## Documentation

This App creates state-dependent random walks between consecutive observed animal locations. It uses Hidden Markov Models (HMMs) to infer behavioural states (e.g. resting, foraging, travelling) from movement features and builds movement kernels for each detected state. These kernels are then used to simulate realistic paths between observations while respecting spatial and temporal constraints.

For each trajectory:

1. Movement features such as speed, turning angle, distance, and terrain are computed.
2. A Hidden Markov Model is fitted to infer behavioural states.
3. Behaviour-specific movement kernels are constructed using Gaussian-based correlated and Brownian walk models.
4. Random walks are generated between consecutive observed locations using these kernels and a configurable movement policy.
5. Interpolated paths are merged with original observations into a continuous trajectory output.

Generated trajectories preserve timestamps and produce temporally consistent paths that reflect inferred behaviour and environmental context.

### Application scope

#### Generality of App usability

This App was developed for animal movement data and is applicable to most taxonomic groups (terrestrial, airborne, and marine animals). Behavioural interpretation of inferred HMM states depends on species and sampling resolution.

The App is particularly suited for:

* movement ecology research
* trajectory interpolation between sparse fixes
* simulation of realistic animal paths
* state-dependent movement modelling

The App assumes movement follows continuous trajectories between recorded locations and may produce unrealistic results for highly discontinuous or erroneous tracking data.

#### Required data properties

* Input must be a `MovingPandas.TrajectoryCollection`
* Each trajectory must contain:

  * timestamps
  * geographic coordinates
  * individual identifier
* Data must be temporally ordered
* CRS must be defined 
* Fix rate should be reasonably consistent (large gaps allowed but influence results)
* Very large spatial jumps may lead to coarse interpolation unless grid settings are adjusted

Optional but beneficial:

* Moderate sampling frequency (15 min to 24h recommended)
* Moderate number of locations (500 to 5000 recommended)
* Continuous tracking without long missing intervals

### Input type

`MovingPandas.TrajectoryCollection`

### Output type

`MovingPandas.TrajectoryCollection`

The output contains the original points plus interpolated random-walk points between them.

### Artefacts

`trajectories_timed.html`
Leaflet visualization showing animated, time-aware random walk trajectories for each individual.

### Settings

**Animal Type (`animal_type`)**
Primary movement mode of the animal. Influences terrain and water handling.
Options: Airborne, Terrestrial, Marine.

**Behaviour Towards Water (Terrestrial) (`water_mode`)**
Defines how terrestrial animals interact with water bodies. Ignored for airborne and marine animals.

**Upper Bound for Walk Unit Length (metres) (`cell_resolution`)**
Maximum spatial unit length of individual walk steps. Controls spatial discretization.

**Number of Grid-Cells Along the Longer Axis (`grid_resolution`)**
Fallback grid resolution when two points are very far apart. Limits memory and runtime.

**Movement Policy (`movement_policy`)**
Defines how number of steps and step sizes are determined:

* **Fixed time step**: step sizes are calculated using distance and calculated number of steps
* **Fixed number of** steps: step sizes are calculated using distance and fixed number of steps
* **Automatic based on** reference speed: Uses reference speed and Euclidean Distance to calculate step sizes and number of steps 

**Time Step (seconds) (`time_step_seconds`)**
Used when movement policy = fixed time step.

**Number of Steps (`num_steps`)**
Used when movement policy = fixed number of steps.

**Reference Speed (m/s) (`reference_speed`)**
Used for automatic step calculation when policy = auto speed.

**Delta-T Tolerance Factor (`dt_tolerance`)**
Controls grouping of observations into continuous trajectory segments for kernel estimation.

**Maximal Number of HMM States (`hmm_states`)**
Number of behavioural states used in HMM. Should be lower for few locations. Values: 2–4.

**HMM-Kernels Range (`rnge`)**
Spatial kernel radius (m) used for transition matrices.

**Random Walk Motion Model (`walk_model`)**
Choice of motion model:

* Brownian
* Correlated
* Animal-type dependent default 

### Changes in output data

The output trajectory collection:

* contains all original points
* adds interpolated points between observations
* includes inferred behavioural state per original observation
* preserves timestamps and trajectory structure

Original input data is not modified.

### Most common errors

**No CRS defined**
Input trajectories must contain a valid coordinate reference system.

**Very sparse data**
Extremely large time gaps may lead to unrealistic interpolation or very coarse paths.

**Large spatial jumps**
If two consecutive points are extremely far apart, grid fallback resolution may produce simplified paths.

**Too few data for HMM**
Short trajectories may not contain enough information to estimate set number of behavioural states reliably. Re-run with lower `hmm_states`.

### Null or error handling

**Missing timestamps:**
Trajectory is skipped or returned unchanged.

**Missing CRS:**
Processing stops with error.

**HMM cannot be fitted:**
If insufficient data is available, kernel estimation falls back to simpler movement assumptions or skips trajectory.


If severe errors occur, the App returns the original trajectory collection unchanged and logs a warning.
