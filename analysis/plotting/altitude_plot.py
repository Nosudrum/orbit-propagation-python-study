import matplotlib.pyplot as plt
import numpy as np


def altitude_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
                  results_gmat_poliastro):
    tsv = plot_settings["timescale"]["value"]
    tsn = plot_settings["timescale"]["name"]
    tsd = plot_settings["timescale"]["duration"] / tsv
    spacecraft = plot_settings["spacecraft"]["name"]
    orbit = plot_settings["orbit"]["name"]
    dates = plot_settings["dates"]["name"]
    propagation = plot_settings["propagation"]

    line_width = 1

    norm_celestlab = np.linalg.norm(results_celestlab[["x_eci", "y_eci", "z_eci"]], axis=1)
    norm_tudatpy = np.linalg.norm(results_tudatpy[["x_eci", "y_eci", "z_eci"]], axis=1)
    norm_poliastro = np.linalg.norm(results_poliastro[["x_eci", "y_eci", "z_eci"]], axis=1)
    norm_gmat_tudatpy = np.linalg.norm(results_gmat_tudatpy[["x_eci", "y_eci", "z_eci"]], axis=1)
    norm_gmat_poliastro = np.linalg.norm(results_gmat_poliastro[["x_eci", "y_eci", "z_eci"]], axis=1)

    norm_poliastro = (norm_poliastro - 6378136.3) / 1E3
    norm_tudatpy = (norm_tudatpy - 6378136.3) / 1E3
    norm_celestlab = (norm_celestlab - 6378136.3) / 1E3
    norm_gmat_tudatpy = (norm_gmat_tudatpy - 6378.1363)
    norm_gmat_poliastro = (norm_gmat_poliastro - 6378.1363)

    y_min = min(min(norm_celestlab), min(norm_tudatpy), min(norm_poliastro), min(norm_gmat_tudatpy),
                min(norm_gmat_poliastro))
    y_max = max(max(norm_celestlab), max(norm_tudatpy), max(norm_poliastro), max(norm_gmat_tudatpy),
                max(norm_gmat_poliastro))
    y_min = y_min - (y_max - y_min) * 0.1
    y_max = y_max + (y_max - y_min) * 0.1

    plt.figure(figsize=(8, 5))
    plt.subplot(2, 2, 1)
    plt.plot(results_poliastro["time"] / tsv, norm_poliastro, linewidth=line_width, label='poliastro', color='black')
    plt.title('CelestLab', y=1.09)
    plt.ylim([y_min, y_max])
    plt.xlim([0, tsd])
    plt.ylabel('altitude [km]')

    plt.subplot(2, 2, 2)
    plt.plot(results_tudatpy["time"] / tsv, norm_tudatpy, linewidth=line_width, label='tudatpy', color='black')
    plt.title('Tudatpy', y=1.09)
    plt.xlim([0, tsd])
    plt.ylim([y_min, y_max])
    plt.ylabel('altitude [km]')

    plt.subplot(2, 2, 3)
    plt.plot(results_celestlab["time"] / tsv, norm_celestlab, linewidth=line_width, label='celestlab', color='black')
    plt.title('poliastro', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylim([y_min, y_max])
    plt.ylabel('altitude [km]')

    plt.subplot(2, 2, 4)
    plt.plot(results_gmat_tudatpy["time"] / tsv, norm_gmat_tudatpy, linewidth=line_width, label='GMAT (Tudatpy)',
             color='black')
    plt.plot(results_gmat_poliastro["time"] / tsv, norm_gmat_poliastro, linewidth=line_width, label='GMAT (poliastro)',
             linestyle='dashed',
             color='black')
    plt.title('GMAT', y=1.09)
    plt.legend()
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylim([y_min, y_max])
    plt.ylabel('altitude [km]')

    # plt.suptitle(f'{spacecraft} altitude in {orbit} orbit')

    plt.tight_layout()

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_altitude.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_altitude.pdf')
    plt.show()
