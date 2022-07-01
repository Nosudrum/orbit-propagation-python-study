from datetime import datetime

import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth, Moon
from poliastro.core.perturbations import third_body
from poliastro.ephem import build_ephem_interpolant

# Setup start/end epochs
start_epoch = datetime(2020, 1, 1, 0, 0, 0)
end_epoch = datetime(2020, 1, 30, 0, 0, 0)

# Create Time objects
start_epoch_Time_obj = Time(start_epoch, scale='utc')
end_epoch_Time_obj = Time(end_epoch, scale='utc')

# Build the Moon ephemeris interpolant
Moon_r = build_ephem_interpolant(Moon, 28 * u.day,
                                 (start_epoch_Time_obj.to_value("jd") << u.d, end_epoch_Time_obj.to_value("jd") << u.d),
                                 rtol=1e-2)

t0 = 0 * u.s
state = np.array([7200, 0, 0, 0, -2, 7])
k = Earth.k.to(u.km ** 3 / (u.s ** 2))
k_third = Moon.k.to(u.km ** 3 / (u.s ** 2))

acc_x, acc_y, acc_z = third_body(
    t0.to_value(u.s),
    state,
    k.to_value(u.km ** 3 / u.s ** 2),
    k_third.to_value(u.km ** 3 / u.s ** 2),
    perturbation_body=Moon_r,
)
print(f'acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
