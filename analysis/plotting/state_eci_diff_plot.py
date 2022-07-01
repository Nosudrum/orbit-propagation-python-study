import matplotlib.pyplot as plt


def state_eci_diff_plot(plot_settings, results_celestlab, results_tudatpy, results_poliastro, results_gmat_tudatpy,
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
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["x_eci"] - results_gmat_poliastro["x_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["x_eci"] - results_gmat_tudatpy["x_eci"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔX (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δx [m]')

    plt.subplot(2, 3, 2)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["y_eci"] - results_gmat_poliastro["y_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["y_eci"] - results_gmat_tudatpy["y_eci"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔY (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δy [m]')

    plt.subplot(2, 3, 3)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["z_eci"] - results_gmat_poliastro["z_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["z_eci"] - results_gmat_tudatpy["z_eci"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔZ (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δz [m]')

    plt.subplot(2, 3, 4)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vx_eci"] - results_gmat_poliastro["vx_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vx_eci"] - results_gmat_tudatpy["vx_eci"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔVX (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δvx [m/s]')
    plt.xlabel(f'time [{tsn}]')

    plt.subplot(2, 3, 5)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vy_eci"] - results_gmat_poliastro["vy_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vy_eci"] - results_gmat_tudatpy["vy_eci"] * 1E3,
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔVY (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δvy [m/s]')
    plt.xlabel(f'time [{tsn}]')

    plt.subplot(2, 3, 6)
    plt.plot(results_poliastro["time"] / tsv, results_poliastro["vz_eci"] - results_gmat_poliastro["vz_eci"] * 1E3,
             color='black', linewidth=line_width, linestyle='dashed', label="poliastro-GMAT")
    plt.plot(results_tudatpy["time"] / tsv, results_tudatpy["vz_eci"] - results_gmat_tudatpy["vz_eci"] * 1E3,
             color='black', linewidth=line_width, label="Tudatpy-GMAT")
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.title('ΔVZ (ECI)', y=1.09)
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δvz [m/s]')
    plt.xlabel(f'time [{tsn}]')

    # plt.suptitle(f'{spacecraft} ECI state deltas wrt GMAT in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.18)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_eci_diff_gmat.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_eci_diff_gmat.pdf')
    fig.show()

    fig = plt.figure(figsize=(8, 5))

    plt.subplot(2, 3, 1)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["x_eci"] - results_celestlab["x_eci"],
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["x_eci"] - results_celestlab["x_eci"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δx [m]')
    plt.title('ΔX (ECI)', y=1.09)

    plt.subplot(2, 3, 2)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["y_eci"] - results_celestlab["y_eci"],
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["y_eci"] - results_celestlab["y_eci"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δy [m]')
    plt.title('ΔY (ECI)', y=1.09)

    plt.subplot(2, 3, 3)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["z_eci"] - results_celestlab["z_eci"],
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["z_eci"] - results_celestlab["z_eci"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlim([0, tsd])
    plt.ylabel('Δz [m]')
    plt.title('ΔZ (ECI)', y=1.09)

    plt.subplot(2, 3, 4)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["vx_eci"] - results_celestlab["vx_eci"],
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["vx_eci"] - results_celestlab["vx_eci"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δvx [m/s]')
    plt.title('ΔVX (ECI)', y=1.09)

    plt.subplot(2, 3, 5)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["vy_eci"] - results_celestlab["vy_eci"],
             color='black', linewidth=line_width, linestyle='dashed')
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["vy_eci"] - results_celestlab["vy_eci"],
             color='black', linewidth=line_width)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δvy [m/s]')
    plt.title('ΔVY (ECI)', y=1.09)

    plt.subplot(2, 3, 6)
    plt.plot(results_celestlab["time"] / tsv, results_poliastro["vz_eci"] - results_celestlab["vz_eci"],
             color='black', linewidth=line_width, linestyle='dashed', label="poliastro-CelestLab")
    plt.plot(results_celestlab["time"] / tsv, results_tudatpy["vz_eci"] - results_celestlab["vz_eci"],
             color='black', linewidth=line_width, label="Tudatpy-CelestLab")
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.xticks([0, tsd / 2, tsd])
    plt.xlabel(f'time [{tsn}]')
    plt.xlim([0, tsd])
    plt.ylabel('Δvz [m/s]')
    plt.title('ΔVZ (ECI)', y=1.09)

    # plt.suptitle(f'{spacecraft} ECI state deltas wrt CelestLab in {orbit} orbit')

    fig.tight_layout()

    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0))
    fig.subplots_adjust(bottom=0.18)

    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_eci_diff_celestlab.png')
    plt.savefig(f'plots/{spacecraft}_{orbit}_{dates}_{propagation}_state_eci_diff_celestlab.pdf')
    fig.show()
