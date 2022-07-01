from time import time

import matplotlib.pyplot as plt
from astropy.coordinates import CartesianDifferential, CartesianRepresentation, GCRS, ITRS
from astropy.time import TimeDelta
from poliastro.bodies import Earth, Moon, Sun
from poliastro.constants import Wdivc_sun
from poliastro.core.elements import rv2coe
from poliastro.core.events import eclipse_function
from poliastro.core.perturbations import *
from poliastro.core.propagation import func_twobody
from poliastro.earth.atmosphere import jacchia
from poliastro.spheroid_location import SpheroidLocation
from poliastro.twobody import Orbit
from poliastro.twobody.events import AltitudeCrossEvent
from poliastro.twobody.propagation import cowell

from useful_functions import *

# Initial settings (independent of poliastro)
propagation_name = 'complete'  # 'keplerian', 'earthZonalJ3' or 'complete'
orbit_name = 'sso600'
dates_name = '1hour'
spacecraft_name = 'CREME'
groundstation_name = 'toulouse'

print(f"poliastro propagation started with following settings :")
print(f"Force model = {propagation_name}\nOrbit = {orbit_name}\nDate = {dates_name}")
print(f"Spacecraft = {spacecraft_name}\nGround Station = {groundstation_name}")
print("-------------------------------------------------------------------------\n")

# Set simulation start and end epochs (in seconds since J2000 = January 1, 2000 at 00:00:00)
print("Setting simulation start and end epochs...")
dates = get_dates(dates_name)
simulation_start_epoch = dates["start_date"]
simulation_end_epoch = dates["end_date"]

# Define initial state
print("Setting initial conditions...")
orbit = get_orbit(orbit_name)
semi_major_axis = orbit["semi_major_axis"] * u.m
eccentricity = orbit["eccentricity"] * u.one
inclination = orbit["inclination"] * u.deg
argument_of_periapsis = orbit["argument_of_periapsis"] * u.deg
longitude_of_ascending_node = orbit["longitude_of_ascending_node"] * u.deg
true_anomaly = orbit["true_anomaly"] * u.deg

# Define spacecraft
print("Creating spacecraft...")
mass = get_spacecraft(spacecraft_name)["mass"] * u.kg
drag_coefficient = get_spacecraft(spacecraft_name)["drag_coefficient"] * u.one
reflectivity_coefficient = get_spacecraft(spacecraft_name)["reflectivity_coefficient"] * u.one
drag_area = get_spacecraft(spacecraft_name)["drag_area"] * u.m ** 2
srp_area = get_spacecraft(spacecraft_name)["srp_area"] * u.m ** 2

# Setup atmosphere
print("Setting up atmosphere...")
"""
Exosphere temperature set to 1050 K as an average value.
In reality, it ranges between 700 K and 1400 K at sunspot minimum and maximum respectively.
https://www.sciencedirect.com/topics/earth-and-planetary-sciences/exosphere
"""
atmosphere = jacchia.Jacchia77(1050 * u.K)

# Setup epochs
print("Setting up epochs...")
start = dates["start_date"]
end = dates["end_date"]
step_size = dates["step_size"]
epoch_start = Time(start, scale='utc')
epoch_end = Time(end, scale='utc')
epochs = np.arange(start, end + step_size, step_size)
epochs_sec = np.arange(0, (end + step_size - start).total_seconds(), step_size.total_seconds())
epochs_timedelta = TimeDelta(epochs_sec, format='sec')

# Setup initial orbit
print("Setting up initial orbit...")
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
Sun_r = custom_ephem_interpolant(epochs, epochs_sec, Sun, Earth)
Moon_r = custom_ephem_interpolant(epochs, epochs_sec, Moon, Earth)
print("Done!")


# Setup force model


def f(t0, state, k):
    # Keplerian acceleration (J1)
    du_kep = func_twobody(t0, state, k)

    du_total = du_kep
    if propagation_name == 'earthZonalJ3' or propagation_name == 'complete':
        # J2 perturbation acceleration
        acc_x, acc_y, acc_z = J2_perturbation(
            t0, state, k, J2=Earth.J2.value, R=Earth.R.to(u.km)
        )
        du_j2 = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        # J3 perturbation acceleration
        acc_x, acc_y, acc_z = J3_perturbation(
            t0, state, k, J3=Earth.J3.value, R=Earth.R.to(u.km)
        )
        du_j3 = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        du_total = du_total + du_j2 + du_j3
    if propagation_name == 'complete':
        # Drag perturbation acceleration
        alt = (np.linalg.norm(state[0:3]) - Earth.R_mean.to_value(u.km)) * u.km
        """
        Jacchia77 only implemented in the range 90 km - 2500 km.
        """

        if alt <= 2500 * u.km:
            rho = atmosphere.density(alt)  # en kg/km3
            acc_x, acc_y, acc_z = atmospheric_drag(
                t0,
                state,
                k,
                C_D=drag_coefficient.value,
                A_over_m=(drag_area / mass).to_value(u.km ** 2 / u.kg),
                rho=rho.to_value(u.kg / (u.km ** 3)))
            du_drag = np.array([0, 0, 0, acc_x, acc_y, acc_z])
        else:
            du_drag = np.array([0, 0, 0, 0, 0, 0])

        # Moon perturbation acceleration
        acc_x, acc_y, acc_z = third_body(
            t0,
            state,
            k,
            k_third=Moon.k.to_value(u.km ** 3 / (u.s ** 2)),
            perturbation_body=Moon_r,
        )
        du_moon = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        # Sun perturbation acceleration
        acc_x, acc_y, acc_z = third_body(
            t0,
            state,
            k,
            k_third=Sun.k.to_value(u.km ** 3 / (u.s ** 2)),
            perturbation_body=Sun_r,
        )
        du_sun = np.array([0, 0, 0, acc_x, acc_y, acc_z])

        # Solar radiation pressure
        acc_x, acc_y, acc_z = radiation_pressure(
            t0,
            state,
            k,
            R=Earth.R.to(u.km),
            C_R=reflectivity_coefficient,
            A_over_m=(srp_area / mass).to_value(u.km ** 2 / u.kg),
            Wdivc_s=Wdivc_sun.to_value(u.kg * u.km / u.s ** 2),
            star=Sun_r)
        du_srp = np.array([0, 0, 0, acc_x, acc_y, acc_z])
        du_total = du_total + du_drag + du_moon + du_sun + du_srp
    return du_total


# Define a threshold altitude for crossing.
print("Setting up threshold altitude...")
thresh_alt = 100  # in km
altitude_cross_event = AltitudeCrossEvent(thresh_alt, Earth.R.to_value(u.km))  # Set up the event.
events = [altitude_cross_event]

# Propagate the orbit with Cowell’s formulation
print('Propagating with Cowell’s formulation...')
start_time = time()

[r_vec, v_vec] = cowell(k=Earth.k.to(u.km ** 3 / (u.s ** 2)),
                        r=orbit_init.r.to(u.km),
                        v=orbit_init.v.to(u.km / u.s),
                        tofs=epochs_timedelta,
                        f=f,
                        events=events
                        )
end_time = time()
print("Propagation complete! Time elapsed: {} seconds".format(end_time - start_time))

# Build states array
print("Building states array...")
states_array = np.empty((len(r_vec), 7))
states_array[:, 0] = epochs_timedelta[:len(r_vec)].to_value(u.s)
states_array[:, 1:4] = r_vec.to_value(u.m)
states_array[:, 4:7] = v_vec.to_value(u.m / u.s)

# Compute keplerian elements
print("Computing Keplerian elements...")
"""
The 1st column of keplerian elements is converted from semi-latus rectum to semi-major axis with a=p/(1-e^2). The 
4th and 5th columns (longitude of the ascending node, argument of periapsis) are permuted to match the usual format 
of the orbital elements (argument of periapsis, longitude of the ascending node).
"""
keplerian_states = np.array(
    [rv2coe(k=Earth.k.to_value(u.km ** 3 / (u.s ** 2)), r=r_vec[ii].to_value(u.km), v=v_vec[ii].to_value(u.km / u.s),
            tol=1e-08) for ii in range(len(r_vec))])
keplerian_states[:, 0] = keplerian_states[:, 0] / (1 - keplerian_states[:, 1] ** 2) * 1E3
raan = keplerian_states[:, 3].copy()
aop = keplerian_states[:, 4].copy()
keplerian_states[:, 3] = aop
keplerian_states[:, 4] = raan
keplerian_states[:, 2:6] = keplerian_states[:, 2:6] * 180 / np.pi % 360

# Compute ECEF coordinates
print("Computing ECEF states")
# These are state vectors in Earth Center Earth Fixed (ECEF reference frame)
gcrs = GCRS(x=states_array[:, 1] * u.m, y=states_array[:, 2] * u.m, z=states_array[:, 3] * u.m,
            v_x=states_array[:, 4] * u.m / u.s, v_y=states_array[:, 5] * u.m / u.s, v_z=states_array[:, 6] * u.m / u.s,
            representation_type=CartesianRepresentation, differential_type=CartesianDifferential,
            obstime=epochs[:len(r_vec)])
itrs = gcrs.transform_to(ITRS(obstime=epochs[:len(r_vec)]))

ecef_states = np.array([itrs.x.to_value(u.m), itrs.y.to_value(u.m), itrs.z.to_value(u.m), itrs.v_x.to_value(u.m / u.s),
                        itrs.v_y.to_value(u.m / u.s), itrs.v_z.to_value(u.m / u.s)]).transpose()

# Compute eclipses
print("Computing eclipses...")
"""
The eclipse function is taken from Escobal, P. Methods of orbit determination (1965). This book is difficult to 
find online, pictures of the relevant section from two different sources are available in the Escobal1965 folder.
The implementation of the function in poliastro 0.16.3 assumes circular bodies and does not account for flattening.
"""
eclipses_umb = np.array(
    [eclipse_function(Earth.k, states_array[ii, 1:7], Sun_r(epochs_timedelta.value[ii]), Sun.R, Earth.R_mean,
                      umbra=True) for ii
     in range(len(r_vec))]) > 0
eclipses_pen = np.array(
    [eclipse_function(Earth.k, states_array[ii, 1:7], Sun_r(epochs_timedelta.value[ii]), Sun.R, Earth.R_mean,
                      umbra=False) for ii
     in range(len(r_vec))]) > 0

# Compute visibility windows
print("Computing visibility windows...")
groundstation = get_station(groundstation_name)
station = SpheroidLocation(groundstation["longitude"] * u.deg, groundstation["latitude"] * u.deg,
                           groundstation["altitude"] * u.m, Earth)
visibility, elevation = compute_visibility(ecef_states[:, 0:3], station, groundstation["minimum_elevation"])

# Export results to a CSV file
print("Exporting results to a CSV file...")
write_results(propagation_name, spacecraft_name, orbit_name, dates_name,
              np.concatenate((states_array, keplerian_states, ecef_states), axis=1))

print("Plotting results...")
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

print("Done!")
