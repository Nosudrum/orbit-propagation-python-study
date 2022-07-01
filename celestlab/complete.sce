close(winsid())
clear
CL_init()

// =====================================================
// INITIAL SETTINGS (INDEPENDENT OF CELESTLAB)
// =====================================================
propagation_name = 'complete'
orbit_name = 'test_orbit2'
dates_name = '5days_1min'
spacecraft_name = 'Sunjammer'

// =====================================================
// IMPORT INPUT DATA
// =====================================================
exec('import_data.sce');

// =====================================================
// SETUP INITIAL STATE AND PROPAGATION EPOCHS
// =====================================================
kep_mean_ini = [semi_major_axis;..
                eccentricity;..
                inclination*%CL_deg2rad;..
                argument_of_periapsis*%CL_deg2rad;..
                longitude_of_ascending_node*%CL_deg2rad;..
                mean_anomaly*%CL_deg2rad]

epochs = start_epoch:step_size:end_epoch;

// =====================================================
// NUMERICAL PROPAGATION WITH STELA
// =====================================================
// Initialisation of STELA parameters
disp("Setting up STELA parameters");
params_stela =  CL_stela_params();

// Definition of spacecraft characteristics
params_stela.mass = mass;
params_stela.drag_coef = drag_coefficient;
params_stela.drag_area = drag_area;
params_stela.srp_area = srp_area;
params_stela.srp_coef = reflectivity_coefficient;

// Setup of the force model
params_stela.zonal_maxDeg = 15;
params_stela.tesseral_maxDeg = 15;
params_stela.solidTides_enabled = %f;
params_stela.appAcc_enabled = %f;

// Setup of the integrator step size (duration of an orbit in seconds)
params_stela.integrator_step = step_size*86400;
//params_stela.integrator_step = 2*%pi*sqrt(semi_major_axis^3/%CL_mu);
//epochs = start_epoch:(params_stela.integrator_step/86400):end_epoch;

//Propagation with default solar activity
disp("Beginning STELA propagation");
kep_mean_results = CL_stela_extrap("kep", start_epoch, kep_mean_ini, epochs, params_stela, 'm');
disp("Completed STELA propagation");

// =====================================================
// CONVERT TO CARTESIAN COORDINATES
// =====================================================
[sat_pos,sat_vel] = CL_oe_kep2car(kep_mean_results);

states_array = [epochs',sat_pos',sat_vel'];

// =====================================================
// COMPUTE ECLIPSES
// =====================================================

sun_pos = CL_eph_sun(epochs);
eclipse_umb = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='umb');
eclipse_umbc = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='umbc');
eclipse_pen = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='pen');

// =====================================================
// PLOT AND EXPORT RESULTS
// =====================================================
exec('process_results.sce');


