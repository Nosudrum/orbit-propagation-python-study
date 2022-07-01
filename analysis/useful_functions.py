import csv
from datetime import datetime, timedelta
from os import makedirs
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import pandas as pd

main_path = str(Path(__file__).parents[1])
input_data_path = str(Path(__file__).parents[1].joinpath('input_data'))


def plot_sphere(ax, center, radius):
    """
    Plot a sphere in 3D using matplotlib.
    :param ax: figures axes to plot in.
    :param center: center of the sphere.
    :param radius: radius of the sphere.
    """
    u, v = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j]
    x = radius * np.cos(u) * np.sin(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(v)
    ax.plot_surface(x - center[0], y - center[1], z - center[2], color='cyan', alpha=0.5)


def plotly_sphere(center, radius):
    """
    Plot a sphere in 3D using plotly.
    :param center: center of the sphere.
    :param radius: radius of the sphere.
    :return: cartesian coordinates of the sphere surface.
    """
    nb_points = 50
    x = np.zeros(nb_points ** 2) * np.NaN
    y = np.zeros(nb_points ** 2) * np.NaN
    z = np.zeros(nb_points ** 2) * np.NaN
    ii = 0
    for theta in np.linspace(0, 2 * np.pi, nb_points):
        for phi in np.linspace(0, np.pi, nb_points):
            x[ii] = radius * np.cos(theta) * np.sin(phi)
            y[ii] = radius * np.sin(theta) * np.sin(phi)
            z[ii] = radius * np.cos(phi)
            ii += 1
    return x - center[0], y - center[1], z - center[2]


def plotly_trajectory(states_array):
    """
    Plot the trajectory in 3D using plotly.
    :param states_array: array with ECI positions in columns 1,2,3 and time in column 0.
    :return: plotly figure.
    """
    fig = go.Figure(data=go.Scatter3d(
        x=states_array[:, 1] / 1E3, y=states_array[:, 2] / 1E3, z=states_array[:, 3] / 1E3,
        marker=dict(
            size=2,
            color=states_array[:, 0]
        )
    ))
    [earth_x, earth_y, earth_z] = plotly_sphere([0, 0, 0], 6371008.366666666)
    fig.add_mesh3d(
        x=earth_x / 1E3, y=earth_y / 1E3, z=earth_z / 1E3,
        alphahull=0,
        color='darkblue',
        opacity=0.5,
        hoverinfo='skip'
    )
    fig.update_layout(template='plotly_dark',
                      scene=dict(
                          xaxis_title='x [km]',
                          yaxis_title='y [km]',
                          zaxis_title='z [km]'))
    return fig


def get_spacecraft(filename):
    """
    Import spacecraft data from a CSV file.
    :param filename: name of spacecraft file.
    :return: spacecraft dictionary.
    """
    with open(input_data_path + '/spacecraft/' + filename + '.csv', mode='r', encoding='utf_8_sig') as inp:
        reader = csv.reader(inp)
        spacecraft = {rows[0]: float(rows[1]) for rows in reader}
    return spacecraft


def get_station(filename):
    """
    Import station data from a CSV file.
    :param filename: name of station file.
    :return: station dictionary.
    """
    with open(input_data_path + '/groundstations/' + filename + '.csv', mode='r', encoding='utf_8_sig') as inp:
        reader = csv.reader(inp)
        station = {rows[0]: float(rows[1]) for rows in reader}
    return station


def get_orbit(filename):
    """
    Import orbit data from a CSV file.
    :param filename: name of orbit file.
    :return: orbit dictionary.
    """
    with open(input_data_path + '/orbits/' + filename + '.csv', mode='r', encoding='utf_8_sig') as inp:
        reader = csv.reader(inp)
        orbit = {rows[0]: float(rows[1]) for rows in reader}
    return orbit


def get_dates(filename):
    """
    Import dates from a CSV file.
    :param filename: name of dates file.
    :return: dates dictionary.
    """
    with open(input_data_path + '/dates/' + filename + '.csv', mode='r', encoding='utf_8_sig') as inp:
        reader = csv.reader(inp)
        dates = {}
        for row in reader:
            if row[0] == 'step_size':
                info = timedelta(seconds=int(row[1]))
            else:
                info = datetime.strptime(row[1], '%Y-%m-%d-%H:%M:%S')
            dates[row[0]] = info
    return dates


def get_results(library, propagation, spacecraft, orbit, dates):
    """
    Import results from a CSV file.
    :param library: orbit propagation library used (tudatpy, poliastro, celestlab, gmat-poliastro, gmat-tudatpy).
    :param propagation: propagation mode used (keplerian, EarthZonalJ5, complete)
    :param spacecraft: name of the spacecraft file.
    :param orbit: name of the orbit file.
    :param dates: name of the dates file.
    :return: pandas dataframe with results.
    """
    match library:
        case 'celestlab':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'tudatpy':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'tudatpy-dev':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'poliastro':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'poliastro-main':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'gmat-tudatpy':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case 'gmat-poliastro':
            columns = ["time", "x_eci", "y_eci", "z_eci", "vx_eci", "vy_eci", "vz_eci", "sma", "ecc", "inc", "aop",
                       "raan", "tan", "x_ecef", "y_ecef", "z_ecef", "vx_ecef", "vy_ecef", "vz_ecef"]
        case _:
            raise ValueError('Unknown library.')
    if library == 'gmat-tudatpy' and propagation == 'complete':
        results = pd.read_csv(f'{main_path}/gmat/results/complete_tudatpy/{spacecraft}_{orbit}_{dates}.txt',
                              names=columns, na_values=['Nan'], delim_whitespace=True)
    elif library == 'gmat-poliastro' and propagation == 'complete':
        results = pd.read_csv(f'{main_path}/gmat/results/complete_poliastro/{spacecraft}_{orbit}_{dates}.txt',
                              names=columns, na_values=['Nan'], delim_whitespace=True)
    elif library == 'gmat-tudatpy' and propagation == 'keplerian':
        results = pd.read_csv(f'{main_path}/gmat/results/keplerian_tudatpy/{spacecraft}_{orbit}_{dates}.txt',
                              names=columns, na_values=['Nan'], delim_whitespace=True)
    elif library == 'gmat-poliastro' and propagation == 'keplerian':
        results = pd.read_csv(f'{main_path}/gmat/results/keplerian_poliastro/{spacecraft}_{orbit}_{dates}.txt',
                              names=columns, na_values=['Nan'], delim_whitespace=True)
    elif library == 'gmat-tudatpy' or library == 'gmat-poliastro':
        results = pd.read_csv(f'{main_path}/gmat/results/{propagation}/{spacecraft}_{orbit}_{dates}.txt',
                              names=columns, na_values=['Nan'], delim_whitespace=True)
    elif (library == 'poliastro' or library == 'poliastro-main') and propagation == 'earthZonalJ5':
        results = pd.read_csv(f'{main_path}/{library}/results/earthZonalJ3/{spacecraft}_{orbit}_{dates}.csv',
                              names=columns, na_values=['Nan'])
    else:
        results = pd.read_csv(f'{main_path}/{library}/results/{propagation}/{spacecraft}_{orbit}_{dates}.csv',
                              names=columns, na_values=['Nan'])
    return results


def write_results(propagation_name, spacecraft_name, orbit_name, dates_name, array):
    """
    Write results to a CSV file.
    :param propagation_name: force model name.
    :param spacecraft_name: name of spacecraft file.
    :param orbit_name: name of orbit file.
    :param dates_name: name of dates file.
    :param array: array to save.
    """
    makedirs('results/' + propagation_name, exist_ok=True)
    np.savetxt(f'results/{propagation_name}/{spacecraft_name}_{orbit_name}_{dates_name}.csv', array, delimiter=",")


def get_timescale(dates):
    """
    Get timescale from dates.
    :param dates: dates dictionary imported from a CSV file.
    :return: timescale dictionary to divide the elapsed time columns and name legend.
    """
    duration = dates["end_date"] - dates["start_date"]
    timescale = {"duration": duration.total_seconds(), }
    if duration.total_seconds() < 0:
        raise ValueError("End date is before start date!")
    elif duration.total_seconds() == 0:
        raise ValueError("Duration is zero!")
    elif duration.total_seconds() <= 60:  # 1 minute --> seconds
        timescale["value"] = 1
        timescale["name"] = "s"
    elif duration.total_seconds() <= 3600:  # 1 hour --> minutes
        timescale["value"] = 60
        timescale["name"] = "min"
    elif duration.total_seconds() <= 3 * 86400:  # 3 days --> hours
        timescale["value"] = 3600
        timescale["name"] = "hrs"
    else:  # more than 3 days --> days
        timescale["value"] = 86400
        timescale["name"] = "days"
    return timescale
