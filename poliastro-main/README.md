# poliastro-main



## Introduction

[poliastro](https://www.poliastro.space/) is an open source (MIT) pure Python library for interactive Astrodynamics and
Orbital Mechanics, with a focus on ease of use, speed, and quick visualization. It provides a simple and intuitive API,
and handles physical quantities with units.

## Documentation

The poliastro documentation is available [here](https://docs.poliastro.space/en/stable/).

## Installation

Start by creating a new conda environment:
```
conda create --name poliastro-main
```
Activate it with
```
conda activate poliastro-main
```
Then, install `pip` and `git` with
```
conda install pip git
```
Finally, you can install the main branch of poliastro in this environment with the following command:
```
pip install git+https://github.com/poliastro/poliastro.git@main
```

## Output CSV content

### Main states file

The states CSV file generated with poliastro contains the following columns:

| Columns |      0       |     1-3      |     4-6      |             7-12              |     13-15     |     16-18     |
|---------|:------------:|:------------:|:------------:|:-----------------------------:|:-------------:|:-------------:|
| Content | Elapsed time | ECI position | ECI velocity | Osculating keplerian elements | ECEF position | ECEF velocity |
| Units   |      s       |      m       |     m/s      |            m, rad             |       m       |      m/s      |

The osculating keplerian elements are given in the following order:

- semi-major axis
- eccentricity
- inclination
- argument of periapsis
- longitude of ascending node
- true anomaly

