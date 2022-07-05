# poliastro

## Introduction

[poliastro](https://www.poliastro.space/) is an open source (MIT) pure Python library for interactive Astrodynamics and
Orbital Mechanics, with a focus on ease of use, speed, and quick visualization. It provides a simple and intuitive API,
and handles physical quantities with units.

## Documentation

The poliastro documentation is available [here](https://docs.poliastro.space/en/stable/).

## Installation

ou can create a new dedicated environment called *poliastro-main* and install the latest stable release of poliastro by 
navigating to this directory and running the following command:

```
conda env create -f poliastro.yaml
```

## Output CSV content

The CSV file generated with poliastro contains the following columns:

| Columns |             0              |     1-3      |     4-6      |               7-12                |     13-15     |     16-18     |
|---------|:--------------------------:|:------------:|:------------:|:---------------------------------:|:-------------:|:-------------:|
| Content |           Epoch            | ECI position | ECI velocity | **Osculating** keplerian elements | ECEF position | ECEF velocity |
| Units   | Seconds since initial date |      m       |     m/s      |              m, rad               |       m       |       m       |

The **osculating** keplerian elements are given in the following order:

- semi-major axis
- eccentricity
- inclination
- argument of periapsis 
- longitude of ascending node 
- ⚠ **true** anomaly

