import matplotlib.pyplot as plt


def state_kep_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
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
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["sma"] / 1E3, linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["sma"] / 1E3, linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["sma"] / 1E3, linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["sma"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["sma"], linewidth=line_width)
    plt.title('Semi-major axis', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('sma [km]')

    plt.subplot(2, 3, 2)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["ecc"], linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["ecc"], linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["ecc"], linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["ecc"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["ecc"], linewidth=line_width)
    plt.title('Eccentricity', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('ecc [-]')

    plt.subplot(2, 3, 3)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["inc"], linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["inc"], linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["inc"], linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["inc"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["inc"], linewidth=line_width)
    plt.title('Inclination', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('inc [deg]')

    plt.subplot(2, 3, 4)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["aop"], linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["aop"], linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["aop"], linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["aop"], linewidth=line_width)
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["aop"], linewidth=line_width)
    plt.title('Argument of perigee', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('aop [deg]')

    plt.subplot(2, 3, 5)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["raan"], linewidth=line_width, linestyle='dotted')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["raan"], linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["raan"], linewidth=line_width)
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["raan"], linewidth=line_width, linestyle='dashed')
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["raan"], linewidth=line_width)
    plt.title('RAAN', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('raan [deg]')

    plt.subplot(2, 3, 6)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["tan"], linewidth=line_width, label='poliastro')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["tan"], linewidth=line_width, label='Tudatpy')
    plt.plot(results_celestlab["time"] / tsv, results_celestlab["tan"], linewidth=line_width, label='CelestLab')
    plt.plot(results_gmat_tudatpy["time"] / tsv, results_gmat_tudatpy["tan"], linewidth=line_width,
             label='GMAT (Tudatpy)')
    plt.plot(results_gmat_poliastro["time"] / tsv, results_gmat_poliastro["tan"], linewidth=line_width,
             label='GMAT (poliastro)')
    plt.title('True anomaly', y=1.09)
    plt.xlabel(f'time [{tsn}]')
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('tan [deg]')

    # plt.suptitle(f'{spacecraft} osculating keplerian elements in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.23)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep.pdf')
    fig.show()
