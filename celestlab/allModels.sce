close(winsid())
clear
CL_init()

// =====================================================
// INITIAL SETTINGS (INDEPENDENT OF CELESTLAB)
// =====================================================
propagation_name = 'complete'
// keplerian, earthZonalJ5 or complete
orbit_name = 'sso600'
dates_name = '1day'
spacecraft_name = 'CREME'
groundstation_name = 'toulouse'

// =====================================================
// IMPORT INPUT DATA
// =====================================================
exec('import_data.sce');

// =====================================================
// SETUP INITIAL STATE AND PROPAGATION EPOCHS
// =====================================================
kep_osc_ini = [semi_major_axis;..
                eccentricity;..
                inclination*%CL_deg2rad;..
                argument_of_periapsis*%CL_deg2rad;..
                longitude_of_ascending_node*%CL_deg2rad;..
                mean_anomaly*%CL_deg2rad]

epochs = start_epoch:step_size:end_epoch;

// =====================================================
// PROPAGATION WITH CHOSEN MODEL
// =====================================================
if propagation_name == 'keplerian' then
    // =====================================================
    // KEPLERIAN PROPAGATION
    // =====================================================
    kep_mean_ini = CL_ex_osc2mean("central","kep",kep_osc_ini);
    tic
    kep_mean_results = CL_ex_kepler(start_epoch,kep_mean_ini,epochs);
    time = toc()
    disp(time)
    kep_osc_results = CL_ex_mean2osc("central","kep",kep_mean_results);
elseif propagation_name == 'earthZonalJ5' then
    // =====================================================
    // ANALYTICAL PROPAGATION WITH LYDANE
    // =====================================================
    kep_mean_ini = CL_ex_osc2mean("lydlp","kep",kep_osc_ini);
    tic
    kep_mean_results = CL_ex_propagate("lydlp","kep",start_epoch,kep_mean_ini,epochs,'m');
    time = toc()
    disp(time)
    kep_osc_results = CL_ex_mean2osc("lydlp","kep",kep_mean_results);
elseif propagation_name == 'complete' then
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
    kep_mean_ini = CL_stela_convert("osc2mean", "kep", epochs(1), kep_osc_ini, params_stela);
    disp("Beginning STELA propagation");
    tic
    kep_mean_results = CL_stela_extrap("kep", start_epoch, kep_mean_ini, epochs, params_stela, 'm');
    time = toc()
    disp(time)
    disp("Completed STELA propagation");
    nb_non_nan = sum(~isnan(kep_mean_results(1,:)));
    epochs = epochs(1:nb_non_nan);
    kep_mean_results = kep_mean_results(:,1:nb_non_nan);
    kep_osc_results = CL_stela_convert("mean2osc", "kep", epochs, kep_mean_results, params_stela);
else
    disp("Error - invalid propgator name")
end

elapsed_seconds = (epochs-epochs(1))*86400;

// =====================================================
// CONVERT TO CARTESIAN COORDINATES
// =====================================================
[sat_pos,sat_vel] = CL_oe_kep2car(kep_osc_results);

states_array = [elapsed_seconds',sat_pos',sat_vel'];

// =====================================================
// COMPUTE ECLIPSES
// =====================================================

sun_pos = CL_eph_sun(epochs);
eclipse_umb = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='umb');
eclipse_umbc = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='umbc');
eclipse_pen = CL_ev_eclipse(epochs,sat_pos,sun_pos,typ='pen');

// =====================================================
// COMPUTE COMMUNICATION WINDOWS
// =====================================================
[pos_ecf,vel_ecf] = CL_fr_convert("ECI", "ECF", epochs, sat_pos,sat_vel);
comm_windows = CL_ev_stationVisibility(epochs, pos_ecf, groundstation, groundstation_min_elev);

// =====================================================
// PLOT AND EXPORT RESULTS
// =====================================================
exec('process_results.sce');


