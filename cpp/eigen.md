# Eigen 笔记
### 
```cpp
    ConstraintVector computeConstraints() const {
        ConstraintVector constraints;
        
        // State constraints
        constraints.template segment<STATE_DIM>(0) = state_ - state_max_;
        constraints.template segment<STATE_DIM>(STATE_DIM) = state_min_ - state_;
        
        // Control constraints
        constexpr int control_start = 2 * STATE_DIM;
        constraints.template segment<CONTROL_DIM>(control_start) = control_ - control_max_;
        constraints.template segment<CONTROL_DIM>(control_start + CONTROL_DIM) = 
            control_min_ - control_;
        
        return constraints;
    }
```

```python
    def constraints(self):
        self.normalize_state()
        # Define constraints as g(state, control) <= 0
        state_constraints = np.hstack((self.state - self.state_max, self.state_min - self.state))
        control_constraints = np.hstack((self.control - self.control_max, self.control_min - self.control))

        return np.hstack((state_constraints, control_constraints))
```

```
            // Clip control inputs
            u[t] = u[t].cwiseMin(node->getControlMax()).cwiseMax(node->getControlMin());
```