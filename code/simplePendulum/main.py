from animator import Animator
from pendulum import Pendulum
from timing import Timing
import numpy as np
from rk4 import RK4

timing = Timing(0, 5, 60)

# State
pendulum = Pendulum()
state0 = np.array([np.deg2rad(30), 0])
rk = RK4(pendulum.ode, timing, state0)

# Animation
animator = Animator(rk, pendulum, timing.nInstances)
animator.animate()

# import numpy as np
# theta = [0, 60, 90, 120, 180, 360]

# for i in range(len(theta)):
#   thetaRad = np.deg2rad(theta[i])
#   x, y = pendulum.getPos(thetaRad)
#   print(f"{theta[i]} {x}, {y}, {np.sqrt(x**2 + y**2)}")

#   y = pendulum.ode(np.array((thetaRad, 0)))
#   print(f"{y[1]}")

