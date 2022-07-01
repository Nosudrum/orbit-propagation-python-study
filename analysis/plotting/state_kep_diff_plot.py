import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def state_kep_diff_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
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
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["sma"] - results_gmat_poliastro["sma"] * 1E3,
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["sma"] - results_gmat_tudatpy["sma"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ Semi-major axis)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δsma [m]')

    plt.subplot(2, 3, 2)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["ecc"] - results_gmat_poliastro["ecc"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["ecc"] - results_gmat_tudatpy["ecc"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ Eccentricity', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δecc [-]')

    plt.subplot(2, 3, 3)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["inc"] - results_gmat_poliastro["inc"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["inc"] - results_gmat_tudatpy["inc"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ Inclination', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δinc [deg]')

    plt.subplot(2, 3, 4)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["aop"] - results_gmat_poliastro["aop"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["aop"] - results_gmat_tudatpy["aop"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ Argument of perigee', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δaop [deg]')
    plt.xlabel(f'time [{tsn}]')

    plt.subplot(2, 3, 5)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["raan"] - results_gmat_poliastro["raan"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["raan"] - results_gmat_tudatpy["raan"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ RAAN', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δraan [deg]')
    plt.xlabel(f'time [{tsn}]')

    plt.subplot(2, 3, 6)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["tan"] - results_gmat_poliastro["tan"],
             color='black', linewidth=line_width, linestyle='dashed', label="poliastro-GMAT")
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["tan"] - results_gmat_tudatpy["tan"],
             color='black', linewidth=line_width, label="Tudatpy-GMAT")
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('Δ True anomaly', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δta [deg]')
    plt.xlabel(f'time [{tsn}]')

    # plt.suptitle(f'{spacecraft} ECI state deltas wrt GMAT in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.18)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep_diff_gmat.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep_diff_gmat.pdf')
    fig.show()

    fig = plt.figure(figsize=(8, 5))

    plt.subplot(2, 3, 1)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["sma"] - results_celestlab["sma"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["sma"] - results_celestlab["sma"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δsma [m]')
    plt.title('Δ Semi-major axis', y=1.09)

    plt.subplot(2, 3, 2)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["ecc"] - results_celestlab["ecc"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["ecc"] - results_celestlab["ecc"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δecc [-]')
    plt.title('Δ Eccentricity', y=1.09)

    plt.subplot(2, 3, 3)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["inc"] - results_celestlab["inc"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["inc"] - results_celestlab["inc"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δinc [deg]')
    plt.title('Δ Inclination', y=1.09)

    plt.subplot(2, 3, 4)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["aop"] - results_celestlab["aop"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["aop"] - results_celestlab["aop"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δaop [deg]')
    plt.title('Δ Argument of perigee', y=1.09)

    plt.subplot(2, 3, 5)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["raan"] - results_celestlab["raan"],
             color='black', linestyle='dashed', linewidth=line_width)
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["raan"] - results_celestlab["raan"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δraan [deg]')
    plt.title('Δ RAAN', y=1.09)

    plt.subplot(2, 3, 6)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["tan"] - results_celestlab["tan"],
             color='black', linestyle='dashed', linewidth=line_width, label="poliastro-CelestLab")
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["tan"] - results_celestlab["tan"],
             color='black', linewidth=line_width, label="Tudatpy-CelestLab")
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δtan [deg]')
    plt.title('Δ True anomaly', y=1.09)

    # plt.suptitle(f'{spacecraft} ECI state deltas wrt CelestLab in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.18)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep_diff_celestlab.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_kep_diff_celestlab.pdf')
    fig.show()
