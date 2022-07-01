# Tudatpy

## Introduction

TU Delft Astrodynamics Toolbox in Python, or tudatpy, is a python library that primarily exposes the powerful set
of [Tudat](https://tudat.tudelft.nl/) C++ libraries.

## Documentation

The Tudat documentation, including tudatpy installation instructions and other links, is
available [here](https://docs.tudat.space/en/stable/). The tudatpy API reference is
available [here](https://py.api.tudat.space/en/latest/).

## Installation

You can install tudatpy in a new dedicated environment called *tudat-space* by navigating to this directory and running
the following command :

```
conda env create -f environment.yaml
```

## Output CSV content

### Main states file

The states CSV file generated with Tudatpy contain the following columns:

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

