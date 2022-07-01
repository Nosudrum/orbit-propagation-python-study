# Import statements
import numpy as np
from tudatpy.kernel import numerical_simulation
from tudatpy.kernel.astro import element_conversion
from tudatpy.kernel.interface import spice
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup

# Load spice kernels
spice.load_standard_kernels([])

# Set simulation start and end epochs (in seconds since J2000 = January 1, 2000 at 00:00:00)
simulation_start_epoch = 0
simulation_end_epoch = 86400

# Create default body settings and bodies system
bodies_to_create = ["Earth", "Sun"]
global_frame_origin = "Earth"
global_frame_orientation = "J2000"
body_settings = environment_setup.get_default_body_settings(
    bodies_to_create, global_frame_origin, global_frame_orientation)
bodies = environment_setup.create_system_of_bodies(body_settings)

# Add vehicle object to system of bodies
bodies.create_empty_body("Spacecraft")

# Define bodies that are propagated and their respective central bodies
bodies_to_propagate = ["Spacecraft"]
central_bodies = ["Earth"]

# Define accelerations acting on the spacecraft

acceleration_settings_spacecraft = dict(
    Earth=[propagation_setup.acceleration.spherical_harmonic_gravity(5, 0)]
)

acceleration_settings = {"Spacecraft": acceleration_settings_spacecraft}

# Create acceleration models
acceleration_models = propagation_setup.create_acceleration_models(
    bodies, acceleration_settings, bodies_to_propagate, central_bodies
)

# Set initial conditions for the satellite
earth_gravitational_parameter = bodies.get("Earth").gravitational_parameter
initial_state = element_conversion.keplerian_to_cartesian_elementwise(
    gravitational_parameter=earth_gravitational_parameter,
    semi_major_axis=7200000,
    eccentricity=0,
    inclination=np.deg2rad(98),
    argument_of_periapsis=np.deg2rad(0),
    longitude_of_ascending_node=np.deg2rad(0),
    true_anomaly=np.deg2rad(0),
)

# Setup dependent variables to be save
ecef_vel_dep_var = propagation_setup.dependent_variable.body_fixed_groundspeed_velocity("Spacecraft", "Earth")
dependent_variables_to_save = [ecef_vel_dep_var]

# Create termination settings
termination_time = propagation_setup.propagator.time_termination(simulation_end_epoch)

# Create propagation settings
propagator_settings = propagation_setup.propagator.translational(
    central_bodies,
    acceleration_models,
    bodies_to_propagate,
    initial_state,
    termination_time,
    output_variables=dependent_variables_to_save
)

# Create numerical integrator settings
fixed_step_size = 10
integrator_settings = propagation_setup.integrator.runge_kutta_4(
    simulation_start_epoch, fixed_step_size
)

# Create simulation object and propagate the dynamics
dynamics_simulator = numerical_simulation.SingleArcSimulator(
    bodies, integrator_settings, propagator_settings
)

print('OK')
