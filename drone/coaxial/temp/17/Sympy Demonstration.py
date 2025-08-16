#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sympy
sympy.init_printing(use_latex=True)


# If you ever don't feel like taking derivatives, you can use a Python library called `sympy` to do the dirty work.
# 
# When we have a $g$ function like this:
# 
# $$
# g = \begin{bmatrix}
# u_{\phi} \\
# \dot{y} - \sin(\phi) \Delta t \\
# y + \dot{y} \Delta t
# \end{bmatrix}
# $$
# 
# and a state vector like this:
# 
# $$
# x = \begin{bmatrix}
# \phi \\
# \dot{y} \\
# y
# \end{bmatrix}
# $$
# 
# (Note that I'm writing $\phi$ here instead of $x_{\phi}$. Like wise with $\dot{y}$ and $y$)
# 
# we can use sympy to calculate $g'$ as follows:

# In[6]:


# 1. define sympy symbols
u_phi, phi, y_dot, y, dt = sympy.symbols(
'u_phi, phi, y_dot, y, dt')

# 2. define the state variable
x = sympy.Matrix([
    phi, 
    y_dot, 
    y])

# 3. define state transition function
g = sympy.Matrix([
    u_phi,
    y_dot - sympy.sin(phi) * dt,
    y + y_dot * dt
])

# 4. take jacobian of g with respect to x
g.jacobian(x)


# You'd still need to implement this matrix in code, but at least the derivatives have been taken care of!
