# poliastro (main branch)

## Introduction

[poliastro](https://www.poliastro.space/) is an open source (MIT) pure Python library for interactive Astrodynamics and
Orbital Mechanics, with a focus on ease of use, speed, and quick visualization. It provides a simple and intuitive API,
and handles physical quantities with units.

## Documentation

The poliastro documentation is available [here](https://docs.poliastro.space/en/stable/).

## Installation

You can create a new dedicated environment called *poliastro-main* by navigating to this directory and running
the following command:

```
conda env create -f poliastro-main.yaml
```

Then, activate the environment with the following command:

```
conda activate poliastro-main
```

Finally, you can install the main branch of poliastro in this environment with the following command:

```
pip install git+https://github.com/poliastro/poliastro.git@main
```

Like with the method using a `.yaml` file, the poliastro installation step will automatically install the required
version of python.

## Output CSV content

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

