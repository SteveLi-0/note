# ALM ilqr
## scope
This document describes the implementation of an al_ilqr algorithm for trajectory tracking problem with state-input constraints and obstacle avoidance constraints. To simplify the problem, we assume that the vehicle and obstacle is a mass point and the distance between the vehicle and obstacle should not be less than a constant.

## problem formulation
### vehicle model
...
### constraints
#### state/input constraints

state constraints:
$$
\begin{bmatrix}
    x_{min} \\ y_{min} \\ \phi_{min} \\ u_{min} \\ v_{min} \\ \omega_{min}
\end{bmatrix}
\leq
\begin{bmatrix}
    x \\ y \\ \phi \\ u \\ v \\ \omega
\end{bmatrix}
\leq
\begin{bmatrix}
    x_{max} \\ y_{max} \\ \phi_{max} \\ u_{max} \\ v_{max} \\ \omega_{max}
\end{bmatrix}
$$
input constraints:
$$
\begin{bmatrix}
    a_{min} \\ \delta_{min}
\end{bmatrix}
\leq 
\begin{bmatrix}
    a \\ \delta
\end{bmatrix}
\leq
\begin{bmatrix}
    a_{max} \\ \delta_{max}
\end{bmatrix}
$$

#### obstacle constraints
The core of the collision avoidance constraints is the distance from ego vehicleto the polygon.
The distance is Eucledian distance.


