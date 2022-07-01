import numpy as np
from astropy import units as u
from numpy.linalg import norm
from poliastro.bodies import Earth
from poliastro.core.perturbations import atmospheric_drag
from poliastro.earth.atmosphere import jacchia

atm_jacchia = jacchia.Jacchia77(1050 * u.K)
alt = 500 * u.km
rho = atm_jacchia.density(alt)

t0 = 0 * u.s
state = np.array([7200, 0, 0, 0, -1.03551869, 7.36809836])  # in km and km/s
k = Earth.k.to(u.km ** 3 / u.s ** 2)  # does not matter here
C_D = 1.2 * u.one
A = 20 * u.m ** 2
m = 2000 * u.kg
A_over_m = (A / m).to(u.km ** 2 / u.kg)  # conversion to km2/kg as per documentation

# Compute the drag acceleration using the poliastro function
acc_drag = atmospheric_drag(t0, state, k, C_D, A_over_m, rho)
print(f'Drag acceleration (poliastro): {acc_drag}')

# Compute the drag acceleration using the same code as the poliastro function
v_vec = state[3:]
v = norm(v_vec)
B = C_D * A_over_m

acc_drag_manual = -(1.0 / 2.0) * rho * B * v * v_vec
print(f'Drag acceleration (manual): {acc_drag_manual}')

