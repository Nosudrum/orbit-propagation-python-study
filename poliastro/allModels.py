from math import ceil

import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import CartesianDifferential, CartesianRepresentation, GCRS, ITRS
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth, Moon, Sun
from poliastro.core.elements import rv2coe
from poliastro.core.events import eclipse_function
from poliastro.core.perturbations import *
from poliastro.core.propagation import func_twobody
from poliastro.earth.atmosphere import jacchia
from poliastro.ephem import build_ephem_interpolant
from poliastro.spheroid_location import SpheroidLocation
from poliastro.twobody import Orbit
from poliastro.twobody.events import AltitudeCrossEvent
from poliastro.twobody.propagation import cowell

from useful_functions import *

# Initial settings (independent of poliastro)
propagation_name = 'complete'  # 'keplerian', 'earthZonalJ3' or 'complete'
orbit_name = 'leo1'
dates_name = '1day'
spacecraft_name = 'Sunjammer'
groundstation_name = 'test_station'

# Set simulation start and end epochs (in seconds since J2000 = January 1, 2000 at 00:00:00)
dates = get_dates(dates_name)
simulation_start_epoch = dates["start_date"]
simulation_end_epoch = dates["end_date"]

# Define initial state
orbit = get_orbit(orbit_name)
semi_major_axis = orbit["semi_major_axis"] * u.m
eccentricity = orbit["eccentricity"] * u.one
inclination = orbit["inclination"] * u.deg
argument_of_periapsis = orbit["argument_of_periapsis"] * u.deg
longitude_of_ascending_node = orbit["longitude_of_ascending_node"] * u.deg
true_anomaly = orbit["true_anomaly"] * u.deg

# Define spacecraft
mass = get_spacecraft(spacecraft_name)["mass"] * u.kg
drag_coefficient = get_spacecraft(spacecraft_name)["drag_coefficient"] * u.one
reflectivity_coefficient = get_spacecraft(spacecraft_name)["reflectivity_coefficient"] * u.one
drag_area = get_spacecraft(spacecraft_name)["drag_area"] * u.m ** 2
srp_area = get_spacecraft(spacecraft_name)["srp_area"] * u.m ** 2

# Setup atmosphere
"""
Exosphere temperature set to 1050 K as an average value.
In reality, it ranges between 700 K and 1400 K at sunspot minimum and maximum respectively.
https://www.sciencedirect.com/topics/earth-and-planetary-sciences/exosphere
"""
atmosphere = jacchia.Jacchia77(1050 * u.K)

# Setup epochs
epoch_start = Time(dates["start_date"], scale='utc')
epoch_end = Time(dates["end_date"], scale='utc')
step_size = dates["step_size"]
epochs = np.arange(dates["start_date"], dates["end_date"], dates["step_size"])
epochs_timedelta = TimeDelta(np.linspace(0, (dates["end_date"] - dates["start_date"]).total_seconds(),
                                         num=ceil((dates["end_date"] - dates["start_date"]) / dates["step_size"])),
                             format='sec')

# Setup initial orbit
orbit_init = Orbit.from_classical(Earth, semi_major_axis, eccentricity, inclination, longitude_of_ascending_node,
                                  argument_of_periapsis, true_anomaly, epoch=epoch_start)

# Get  3rd body coordinates (calling in on every iteration will be just too slow)
"""
This function generates a 3rd body ephemeris interpolant. The x value is the time in seconds since the start 
epoch, while the y value is the cartesian position of the 3rd body in the ECI (GCRS) frame.
From this, we can calculate the position of the 3rd body in the ECI frame at any time using 
interpolant(time in seconds since start epoch).
"""
print("Generating 3rd body ephemeris interpolant...")
Sun_r = build_ephem_interpolant(Sun, step_size.total_seconds() * u.s,
                                (epoch_start.to_value("jd") << u.d, epoch_end.to_value("jd") << u.d),
                                rtol=1)
Moon_r = build_ephem_interpolant(Moon, step_size.total_seconds() * u.s,
                                 (epoch_start.to_value("jd") << u.d, epoch_end.to_value("jd") << u.d),
                                 rtol=1)
print("Done!")


# Setup force model
def f(t0, state, k):
    print(f't0: {t0}')
    # Keplerian acceleration (J1)
    du_kep = func_twobody(t0, state, k)
    print(f'KEP du: {du_kep}')

    du_total = du_kep
    if propagation_name == 'earthZonalJ3' or propagation_name == 'complete':
        # J2 perturbation acceleration
        acc_x, acc_y, acc_z = J2_perturbation(
            t0.to_value(u.s), state, k.to_value(u.km ** 3 / u.s ** 2), J2=Earth.J2.value, R=Earth.R.to(u.km)
        )
        print(f'J2 acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
        du_j2 = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        # J3 perturbation acceleration
        acc_x, acc_y, acc_z = J3_perturbation(
            t0.to_value(u.s), state, k.to_value(u.km ** 3 / u.s ** 2), J3=Earth.J3.value, R=Earth.R.to(u.km)
        )
        print(f'J3 acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
        du_j3 = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        du_total = du_total + du_j2 + du_j3
    if propagation_name == 'complete':
        # Drag perturbation acceleration
        alt = (np.linalg.norm(state[0:3]) - Earth.R_mean.to_value(u.km)) * u.km
        """
        Jacchia77 only implemented in the range 90 km - 2500 km.
        """

        if alt <= 2500 * u.km:
            rho = atmosphere.density(alt) * jacchia.R / jacchia.k  # kg2 mol/K m3 à changer en kg/km3
            acc_x, acc_y, acc_z = atmospheric_drag(
                t0.to_value(u.s),
                state,
                k.to_value(u.km ** 3 / u.s ** 2),
                C_D=drag_coefficient.value,
                A_over_m=(drag_area / mass).to_value(u.km ** 2 / u.kg),  # WATCH OUT UNIT HERE MIGHT BE WRONG
                rho=rho.to_value(u.kg / (u.m ** 3)))  # WATCH OUT UNIT HERE MIGHT BE WRONG
            print(f'DRAG acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
            du_drag = np.array([0, 0, 0, acc_x, acc_y, acc_z])
        else:
            du_drag = np.array([0, 0, 0, 0, 0, 0])

        # Moon perturbation acceleration
        acc_x, acc_y, acc_z = third_body(
            t0.to_value(u.s),
            state,
            k.to_value(u.km ** 3 / u.s ** 2),
            k_third=Moon.k.to(u.km ** 3 / (u.s ** 2)),
            perturbation_body=Moon_r,
        )
        print(f'MOON acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
        du_moon = np.array([0, 0, 0, acc_x.to_value(u.km / (u.s ** 2)), acc_y.to_value(u.km / (u.s ** 2)),
                            acc_z.to_value(u.km / (u.s ** 2))])

        # Sun perturbation acceleration
        acc_x, acc_y, acc_z = third_body(
            t0.to_value(u.s),
            state,
            k.to_value(u.km ** 3 / u.s ** 2),
            k_third=Sun.k.to(u.km ** 3 / (u.s ** 2)),
            perturbation_body=Sun_r,
        )
        print(f'SUN acc_x: {acc_x}, acc_y: {acc_y}, acc_z: {acc_z}')
        du_sun = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        du_total = du_total + du_drag + du_moon + du_sun

    return du_total


# Define a threshold altitude for crossing.
thresh_alt = 100  # in km
altitude_cross_event = AltitudeCrossEvent(thresh_alt, Earth.R.to_value(u.km))  # Set up the event.
events = [altitude_cross_event]

# Propagate the orbit with Cowell’s formulation
print('Propagating with Cowell’s formulation...')
[r_vec, v_vec] = cowell(k=Earth.k.to(u.km ** 3 / u.s ** 2),
                        r=orbit_init.r,
                        v=orbit_init.v,
                        tofs=epochs_timedelta,
                        f=f,
                        events=events
                        )
print("Done!")

# Build states array
states_array = np.empty((len(epochs_timedelta), 7))
states_array[:, 0] = epochs_timedelta.to_value(u.s)
states_array[:, 1:4] = r_vec.to_value(u.m)
states_array[:, 4:7] = v_vec.to_value(u.m / u.s)

# Compute keplerian elements
"""
The 1st column of keplerian elements is converted from semi-latus rectum to semi-major axis with a=p/(1-e^2). The 
4th and 5th columns (longitude of the ascending node, argument of periapsis) are permuted to match the usual format 
of the orbital elements (argument of periapsis, longitude of the ascending node).
"""
keplerian_states = np.array([rv2coe(k=Earth.k, r=states_array[ii, 1:4], v=states_array[ii, 4:7], tol=1e-08) for ii in
                             range(len(epochs_timedelta))])
keplerian_states[:, 0] = keplerian_states[:, 0] / (1 - keplerian_states[:, 1] ** 2)
raan = keplerian_states[:, 3]
aop = keplerian_states[:, 4]
keplerian_states[:, 3] = aop
keplerian_states[:, 4] = raan

# Compute ECEF coordinates
# These are state vectors in Earth Center Earth Fixed (ECEF reference frame)
gcrs = GCRS(x=states_array[:, 1] * u.m, y=states_array[:, 2] * u.m, z=states_array[:, 3] * u.m,
            v_x=states_array[:, 4] * u.m / u.s, v_y=states_array[:, 5] * u.m / u.s, v_z=states_array[:, 6] * u.m / u.s,
            representation_type=CartesianRepresentation, differential_type=CartesianDifferential, obstime=epochs)
itrs = gcrs.transform_to(ITRS(obstime=epochs))

ecef_states = np.array([itrs.x.to_value(u.m), itrs.y.to_value(u.m), itrs.z.to_value(u.m), itrs.v_x.to_value(u.m / u.s),
                        itrs.v_y.to_value(u.m / u.s), itrs.v_z.to_value(u.m / u.s)]).transpose()

# Compute eclipses
"""
The eclipse function is taken from Escobal, P. Methods of orbit determination (1965). This book is difficult to 
find online, pictures of the relevant section from two different sources are available in the Escobal1965 folder.
The implementation of the function in poliastro 0.16.3 assumes circular bodies and does not account for flattening.
"""
eclipses_umb = np.array(
    [eclipse_function(Earth.k, states_array[ii, 1:7], Sun_r(epochs_timedelta.value[ii]), Sun.R, Earth.R_mean,
                      umbra=True) for ii
     in range(len(epochs_timedelta))]) > 0
eclipses_pen = np.array(
    [eclipse_function(Earth.k, states_array[ii, 1:7], Sun_r(epochs_timedelta.value[ii]), Sun.R, Earth.R_mean,
                      umbra=False) for ii
     in range(len(epochs_timedelta))]) > 0

groundstation = get_station(groundstation_name)
station = SpheroidLocation(groundstation["longitude"] * u.deg, groundstation["latitude"] * u.deg,
                           groundstation["altitude"] * u.m, Earth)
visibility, elevation = compute_visibility(ecef_states[:, 0:3], station, groundstation["minimum_elevation"])

# Export results to a CSV file
write_results(propagation_name, spacecraft_name, orbit_name, dates_name,
              np.concatenate((states_array, keplerian_states, ecef_states), axis=1))

# Create a static 3D figure of the trajectory
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111, projection='3d')
ax.set_title(f'Spacecraft trajectory around the Earth')
ax.plot(states_array[:, 1] / 1E3, states_array[:, 2] / 1E3, states_array[:, 3] / 1E3,
        linestyle='-.')
plot_sphere(ax, [0, 0, 0], Earth.R_mean.to_value(u.km))

# Add the legend and labels, then show the plot
ax.set_xlabel('x [km]')
ax.set_ylabel('y [km]')
ax.set_zlabel('z [km]')
plt.savefig(f'results/{propagation_name}/{spacecraft_name}_{orbit_name}_{dates_name}.png')
plt.show()

# Plot the shadow function
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111)
ax.set_title(f'Spacecraft shadow function')
ax.plot((states_array[:, 0] - states_array[0, 0]) / 3600, 1 - eclipses_pen, linestyle='-')
ax.set(xlabel='Time [h]', ylabel='Shadow function')
plt.savefig(f'results/{propagation_name}/{spacecraft_name}_{orbit_name}_{dates_name}_shadow_function.png')
plt.show()

# Plot the visibility function
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111)
ax.set_title(f'Spacecraft ground station visibility function')
ax.plot((states_array[:, 0] - states_array[0, 0]) / 3600, visibility, linestyle='-')
ax.set(xlabel='Time [h]', ylabel='Visibility function')
plt.savefig(f'results/{propagation_name}/{spacecraft_name}_{orbit_name}_{dates_name}_visibility_function.png')
plt.show()

# Write an interactive HTML visualization of the trajectory
fig = plotly_trajectory(states_array)
fig.write_html(f'results/{propagation_name}/{spacecraft_name}_{orbit_name}_{dates_name}.html')
