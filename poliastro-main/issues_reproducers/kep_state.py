from datetime import datetime, timedelta

import astropy.units as u
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.core.elements import rv2coe
import numpy as np
from poliastro.twobody.propagation import cowell

semi_major_axis = 7272000 * u.m
eccentricity = 0.002 * u.one
inclination = 99.0 * u.deg
argument_of_periapsis = 90 * u.deg
longitude_of_ascending_node = 0 * u.deg
true_anomaly = 0 * u.deg

start = datetime(2020, 1, 1, 0, 0)
step_size = timedelta(seconds=10)
end = start + step_size

epoch_start = Time(start, scale='utc')
epoch_end = Time(end, scale='utc')
epochs = np.arange(start, end + step_size, step_size)
epochs_sec = np.arange(0, (end + step_size - start).total_seconds(), step_size.total_seconds())
epochs_timedelta = TimeDelta(epochs_sec, format='sec')

orbit = Orbit.from_classical(Earth, semi_major_axis, eccentricity, inclination, longitude_of_ascending_node,
                             argument_of_periapsis, true_anomaly, epoch=epoch_start)

[r_vec, v_vec] = cowell(k=Earth.k.to(u.km ** 3 / (u.s ** 2)),
                        r=orbit.r.to(u.km),
                        v=orbit.v.to(u.km / u.s),
                        tofs=epochs_timedelta
                        )

keplerian_state = np.array(rv2coe(k=Earth.k.to(u.km ** 3 / (u.s ** 2)), r=r_vec[0], v=v_vec[0], tol=1e-08))

keplerian_state[0] = keplerian_state[0] / (1 - keplerian_state[1] ** 2)
raan = keplerian_state[3]
aop = keplerian_state[4]
keplerian_state[3] = aop
keplerian_state[4] = raan
keplerian_state[2:6] = keplerian_state[2:6] * 180 / np.pi % 360

states_array = np.empty((len(r_vec), 7))
states_array[:, 0] = epochs_timedelta[:len(r_vec)].to_value(u.s)
states_array[:, 1:4] = r_vec.to_value(u.m)
states_array[:, 4:7] = v_vec.to_value(u.m / u.s)
keplerian_states = np.array(
    [rv2coe(k=Earth.k.to_value(u.km ** 3 / (u.s ** 2)), r=r_vec[ii].to_value(u.km), v=v_vec[ii].to_value(u.km / u.s), tol=1e-08) for
     ii in range(len(r_vec))])
