import matplotlib.pyplot as plt
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.constants.general import R_mean_earth
from poliastro.plotting import static
from poliastro.twobody import Orbit

# Create an orbit
a = R_mean_earth + 10000 * u.km
ecc = 0.4 * u.one
inc = 55 * u.deg
raan = 56 * u.deg
argp = 278 * u.deg
nu = 50 * u.deg
epoch = Time("2010-01-01 00:00:00", scale='utc')

# Propagate the orbit
orb_0 = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, epoch=epoch)
orb_1 = orb_0.propagate(30 * u.hour)

# Plot results
orbit_plot = static.StaticOrbitPlotter()
orbit_plot.plot(orb_0, label="Initial orbit")
orbit_plot.plot(orb_1, label="Final orbit")
plt.show()
