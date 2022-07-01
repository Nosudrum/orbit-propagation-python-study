# Celestlab

## Introduction

[CelestLab](https://logiciels.cnes.fr/fr/content/celestlab) is a Scilab toolbox for Space Flight Dynamics. It has been
developed by CNES (Centre National d'Études
Spatiales - French Space Agency) for mission analysis purposes.

[CelestlabX](https://logiciels.cnes.fr/fr/content/celestlabx) is CelestLab's extension module. It contains low level
functions that are called by CelestLab. Included features are related in particular to STELA (CNES software for orbit
long-term propagation), Two-Line Elements and MSIS2000 atmospheric model.

## Scilab installation

[Scilab](https://www.scilab.org/) is a free and open-source software that can be used for scientific programming. It is
very similar to Matlab. To install it, simply download the installer for your operating system and run it.

## Celestlab & CelestlabX installation

The installation of Celestlab and CelestlabX is easy : simply run the following commands in Scilab :
```
atomsInstall("celestlab")
```
```
atomsInstall("celestlabx")
```

## Output CSV content

### Main states file

The states CSV file generated with Scilab contain the following columns:

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

