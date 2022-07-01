from useful_functions import *
from plotting import *

# Initial settings (to select results)
propagation_name = 'keplerian'  # 'keplerian','earthZonalJ5' or 'complete'
orbit_name = 'sso600'
dates_name = '1day'
spacecraft_name = 'CREME'
# groundstation_name = 'toulouse'

# Import data
spacecraft = get_spacecraft(spacecraft_name)
spacecraft["name"] = spacecraft_name
orbit = get_orbit(orbit_name)
orbit["name"] = orbit_name
dates = get_dates(dates_name)
dates["name"] = dates_name
timescale = get_timescale(dates)

# Setup dictionary for plot functions
plot_settings = {"propagation": propagation_name, "spacecraft": spacecraft, "orbit": orbit, "dates": dates,
                 "timescale": timescale}

# Import results
results_celestlab = get_results('celestlab', propagation_name, spacecraft_name, orbit_name, dates_name)
results_tudatpy = get_results('tudatpy-dev', propagation_name, spacecraft_name, orbit_name, dates_name)
results_poliastro = get_results('poliastro-main', propagation_name, spacecraft_name, orbit_name, dates_name)
results_gmat_tudatpy = get_results('gmat-tudatpy', propagation_name, spacecraft_name, orbit_name, dates_name)
results_gmat_poliastro = get_results('gmat-poliastro', propagation_name, spacecraft_name, orbit_name, dates_name)

# altitude_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
#               results_gmat_poliastro)
# state_kep_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
#                results_gmat_poliastro)
# state_eci_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
#                results_gmat_poliastro)
# state_ecef_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
#                 results_gmat_poliastro)
state_eci_diff_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
                    results_gmat_poliastro)
state_kep_diff_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
                    results_gmat_poliastro)
