# Optimal Vehicle Trajectory Planning for Static Obstacle Avoidance using Nonlinear Optimization

## problem formulation 

### vehicle kinematic model

control input: linear jerk and curvature change rate 

positional increment functions are difficult to comuppte, so we use Gaussian-Legendra quadrature to approximate the positional increment function.

10th order approximation is adopted in the paper.

### trajectroy planning problem input

vehicle initial state, vehicle parameters and kinematic bounds, vehicle model, reference line and drivable corridor, target speed

### objective formulation

The optimal evaluation of a vehicle trajectory is a weighted summatin of the following terms:
- centripetal acceleration
- centripetal jerk
- curavature change rate
- linear jerk
- distance to RL
- closeness to target speed

The author emphasize the **Huber loss** in distance to RL and the closeness to target speed. 

If a quadratic form of the cost is used, at the beginning of the lane change, this cost factor will become excessively large numerically, which causes other cost factors essentially become ineffective and leads to drastic lateral motions. The same idea applies to the closeness to target speed factor during ego vehicle starts from a static state to avoid drastic longitudinal motions

### Constraints

- Equality coonstraints for trajectory continuty
- Collision avoidance constraints: two disk model
- Kinematic limit and pose constraints:
  - vehicle state constraints
  - heading angle difference: not necessary but helpful on convergence rate in large curvature scenarios

## Implementation

- Initial guess and warm start can reduce the number of interation to 2 or 3
  - P controller 
  - previous cycle 
- The smoothness and density of the drivable corridor boundaries can greatly influence the convergence rate
  - smooth out the sharp corner
  - interpolate the boundaries to a high resoluion 1m to 0.1 m
- The prjection function is one of the bottleneck of the comuputation time.
  - using R tree to index the polyline before the optimaization can reduce the computation time to O(logN)
  
  
