import csv
from datetime import datetime, timedelta
from os import makedirs
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from astropy import units as u
from astropy.time import Time
from poliastro.ephem import Ephem
from scipy.interpolate import interp1d

input_data_path = str(Path(__file__).parents[1].joinpath('input_data'))


def plot_sphere(ax, center, radius):
    """
    Plot a sphere in 3D using matplotlib.
    :param ax: figures axes to plot in.
    :param center: center of the sphere.
    :param radius: radius of the sphere.
    """
    uu, vv = np.mgrid[0:2 * np.pi:50j, 0:np.pi:50j]
    x = radius * np.cos(uu) * np.sin(vv)
    y = radius * np.sin(uu) * np.sin(vv)
    z = radius * np.cos(vv)
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


def compute_visibility(pos_ecf, station, min_elev):
    """
    Compute visibility of a spacecraft from a given station.
    :param pos_ecf: position of the spacecraft in ECEF coordinates.
    :param station: ground station - poliastro SpheroidLocation object.
    :param min_elev: minimum elevation angle.
    :return: visibility bool vector and elevation angle vector.
    """

    station_ecf = station.cartesian_cords.to_value()
    station_sat_vector = pos_ecf - station_ecf
    station_normal_vector = station.N
    station_sat_vector_unit = station_sat_vector.T / np.apply_along_axis(np.linalg.norm, 1, station_sat_vector)
    dot_product = np.dot(station_normal_vector, station_sat_vector_unit)
    elevation = 90 - np.arccos(dot_product) * 180 / np.pi
    visibility = elevation >= min_elev
    return visibility, elevation


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


def custom_ephem_interpolant(epochs, epochs_timedelta, body, attractor):
    """
    Create a custom interpolant for ephemeris data.
    :param epochs: epochs in datetime format.
    :param epochs_timedelta: epochs in seconds since start array.
    :param body: celestial body requested.
    :param attractor: central body.
    """
    epochs_jd = Time(Time(epochs, scale='utc').to_value("jd"), format="jd", scale="tdb")

    ephem = Ephem.from_body(body, epochs_jd, attractor=attractor)

    interpolant = interp1d(
        epochs_timedelta,
        ephem.sample(epochs_jd).xyz.to_value(u.km)
    )
    return interpolant
