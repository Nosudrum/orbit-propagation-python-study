import matplotlib.pyplot as plt


def state_ecef_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
                    results_gmat_poliastro):
    tsv = plot_settings["timescale"]["value"]
    tsn = plot_settings["timescale"]["name"]
    tsd = plot_settings["timescale"]["duration"] / tsv
    spacecraft = plot_settings["spacecraft"]["name"]
    orbit = plot_settings["orbit"]["name"]
    dates = plot_settings["dates"]["name"]
    propagation = plot_settings["propagation"]

    line_width = 1

    fig = plt.figure(figsize=(8, 5))

    plt.subplot(2, 3, 1)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["x_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["x_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["x_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["x_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["x_ecef"] / 1E3, linewidth=line_width)
    plt.title('X (ECEF)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('x [Mm]')

    plt.subplot(2, 3, 2)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["y_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["y_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["y_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["y_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["y_ecef"] / 1E3, linewidth=line_width)
    plt.title('Y (ECEF)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('y [Mm]')

    plt.subplot(2, 3, 3)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["z_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["z_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["z_ecef"] / 1E6, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["z_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["z_ecef"] / 1E3, linewidth=line_width)
    plt.title('Z (ECEF)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('z [Mm]')

    plt.subplot(2, 3, 4)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vx_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vx_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["vx_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["vx_ecef"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["vx_ecef"], linewidth=line_width)
    plt.title('VX (ECEF)', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('vx [km/s]')

    plt.subplot(2, 3, 5)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vy_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vy_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["vy_ecef"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["vy_ecef"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["vy_ecef"], linewidth=line_width)
    plt.title('VY (ECEF)', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('vy [km/s]')

    plt.subplot(2, 3, 6)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vz_ecef"] / 1E3, linewidth=line_width,
             label='poliastro')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vz_ecef"] / 1E3, linewidth=line_width, label='Tudatpy')
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["vz_ecef"] / 1E3, linewidth=line_width,
             label='CelestLab')
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["vz_ecef"], linewidth=line_width,
             label='GMAT (Tudatpy)')
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["vz_ecef"], linewidth=line_width,
             label='GMAT (poliastro)')
    plt.title('VZ (ECEF)', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('vz [km/s]')

    # plt.suptitle(f'{spacecraft} ECEF state in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.23)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_ecef.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_ecef.pdf')
    fig.show()
