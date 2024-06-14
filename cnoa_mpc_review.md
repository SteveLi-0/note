## 0. Overall

```
lat_mpc_controller.cc
lat_mpc_controller.h
```

- variables
  - control conf & vehicle param
  - matched point & predict point
  - interpolation
    - lateral error vs. velocity
    - lateral error vs. curvature
    - heading error vs.  velocity
  - matrix
    - continuous
      - ABE
    - discreted
      - Ad Bd Ed
    - Q & R
    - state
  - matrix vector
    - reference
    - reference point
    - disturbance effect ( desired curvature)
    - control command
    - control command list
    - mpc state
    - error state
  - conf & parm
  - enable flag
    - incremental mpc
    - rk4
- methods
  - **GetSysTimeInNanos()**
    - get nanoseconds
  - **Init()**
    - input:
      - control conf
      - vehicle param
    - call **LoadMPCConf()**
    - call **LoadSchedulers()**
    - initialize matrix
      - A Ad B E
      - reference, disturbance, control cmd, cmd list, mpc state
  - **LoadMPCConf()**
    - enable: incremental mpc, rk4
    - dim: np, nc, state num, 
    - other conf: control period, eps, max iteration
    - matrix QR & QR update
    - mpc vehicle param 
  - **LoadSchedulers()**
    - lat_error_v, lat_error_curvature, heading_error_v
  - **Reset()**
    - set first frame
  - **Control()**
    - inputs
      - steer rate input, traj, curr_veh_state, predict_veh_state
    - current state error for debug
    - predict state error / point for mpc
    - call **OCPSettingAndSolve()**
    - set steer request
  - **OCPSettingAndSolve()**
    - inputs
      - steer rate limit
      - error
    - set upper&lower bounds
      - control bounds: max steer or steer rate
      -  state bounds: for incre-mpc-steer -> max steer, others -> max
    - initial mpc state: predict point error

## 1. controller

CnoaLatController 类继承于 Controller 类

#### Base Controller

- constructor & virtual destructor
  - destructor / constructor = default C++11/20 新特性
- virtual = 0 
  - Status Init()
    - inputs: control_conf & injector (control input message)
  - Status ComputeControlCommand()
    - inputs: planning message, control command & control debug
  - Status Reset()
    - reset controller
  - Status ResetControlStatus()
    - reset controller status
  - Status Name()
    - string: controller name

#### CnoaLatontroller : Controller

- variables
  - 
  - 

