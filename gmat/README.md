# GMAT

## Introduction

The General Mission Analysis Tool ([GMAT](https://sourceforge.net/projects/gmat/))  is an open-source tool for space
mission design and navigation. GMAT is developed by a team of NASA, industry, and public and private
contributors.

## Installation

Simply head over [here](https://sourceforge.net/projects/gmat/files/latest/download) to download and install the latest
version of GMAT.

## Output TXT content

The TXT file generated with GMAT contains the following columns:

| Columns |      0       |     1-3      |     4-6      |             7-12              |     13-15     |     16-18     |
|---------|:------------:|:------------:|:------------:|:-----------------------------:|:-------------:|:-------------:|
| Content | Elapsed time | ECI position | ECI velocity | Osculating keplerian elements | ECEF position | ECEF velocity |
| Units   |      s       |      km      |     km/s     |            km, deg            |      km       |     km/s      |

The osculating keplerian elements are given in the following order:

- semi-major axis
- eccentricity
- inclination
- argument of periapsis
- longitude of ascending node
- true anomaly

