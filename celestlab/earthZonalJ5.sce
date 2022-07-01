close(winsid())
clear
CL_init()

// =====================================================
// INITIAL SETTINGS (INDEPENDENT OF CELESTLAB)
// =====================================================
propagation_name = 'earthZonalJ5'
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
// ANALYTICAL PROPAGATION WITH LYDANE
// =====================================================
kep_mean_results = CL_ex_propagate("lydlp","kep",start_epoch,kep_mean_ini,epochs,'m');

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


