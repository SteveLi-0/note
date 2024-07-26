# multi-agent forward simulation
## 1. EPOSILON
However, afterdecoupling prediction and planning, it is problematic to accountfor the impact of the ego vehicle’s future motion on the otheragents. 
By contrast, our method couples the prediction insidethe behavior planning, where each potential scenario consideredby the planner has its own corresponding future anticipation.
### simple model-based driver model
#### IDM
The Intelligent Driver Model (IDM) is a commonly used car-following model to simulate the behavior of vehicles in traffic flow. The acceleration \( \dot{v} \) of a vehicle is given by:

\[
\dot{v} = a \left[ 1 - \left( \frac{v}{v_0} \right)^\delta - \left( \frac{s^*(v, \Delta v)}{s} \right)^2 \right]
\]

where

\[
s^* = s_0 + max(0, vT + \frac{v \Delta v}{2 \sqrt{ab}})
\]

Here are the parameters and their meanings:



\( v \): The current speed of the vehicle (m/s).
\( v_0 \): The desired speed of the vehicle (m/s).
\( a \): The maximum acceleration (m/s\(^2\)).
\( b \): The comfortable deceleration (m/s\(^2\)).
\( \delta \): The acceleration exponent (typically set to 4).
\( s \): The current gap to the leading vehicle (m).
\( s_0 \): The minimum gap (m), a small constant to prevent division by zero and to ensure a safe distance.
\( T \): The safe time headway (s), representing the desired time gap between vehicles.
\( \Delta v \): The speed difference to the leading vehicle (m/s), defined as \( \Delta v = v - v_{\text{lead}} \).

#### pure pursuit