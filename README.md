# 2022 MULLER Arnaud - Research Internship

## Final Article

The article written as part of this study can be found [here](Final_Article.pdf).


## Table of Contents

<!-- Start TOC (do not remove me) -->

* [Introduction](#introduction)
* [Features](#features)
* [Libraries](#libraries)
* [Validation tools](#validation-tools)
* [Features comparison](#features-comparison)

<!-- End TOC (do not remove me) -->

## Introduction

The goal of this research internship is to compare various python libraries able to perform orbit propagation of
satellites and select the most appropriate one to be implemented in the CREME space mission design workflow based on its
ease of use, feature set, performance and accuracy.

## Features

The following features are investigated:

- Orbit propagation
    - Keplerian
    - With J2, J3, J4+ effects
    - With drag
    - With other perturbations (+ SRP, 3rd body, etc.)
- Eclipses prediction
- Ground station visibility prediction
- Export of ECEF states

## Libraries

The following libraries have been found:

- ~~astropy~~ *not a library for orbit propagation*
- poliastro
- tudatpy
- ~~skyfield~~ *only does SGP4 propagation*
- orbit-predictor *(mostly SGP4 propagation)*
- Orbitdeterminator *(does basic propagation, but no eclipses or communication windows prediction)*
- orbdetpy *(prediction of communication windows but not eclipses)*
- Orekit python wrapper

## Validation tools

Results are to be validated with the following tools:

- Celestlab & CelestlabX on Scilab
- GMAT

## Features comparison

Abbreviations :

- OP : Orbit propagation
- GS : Ground station

| Feature                  | poliastro | Tudatpy | Orbit Predictor  | Orbitdeterminator | orbdetpy | Orekit (py) |
|--------------------------|:---------:|:-------:|------------------|-------------------|:--------:|:-----------:|
| Propagation language     |  Python   |   C++   | Python/C++(SGP4) | Python/C++(SGP4)  |   Java   |    Java     |
| OP - Keplerian           |     ✅     |    ✅    | ✅                | ✅                 |    ✅     |      ✅      |
| OP - J2                  |     ✅     |    ✅    | ✅                | ✅                 |    ✅     |      ✅      |
| OP - J3                  |     ✅     |    ✅    | ❌                | ❌                 |    ✅     |      ✅      |
| OP - J4+                 |     ❌     |    ✅    | ❌                | ❌                 |    ✅     |      ✅      |
| OP - Drag                |     ✅     |    ✅    | ❌                | ✅                 |    ✅     |      ✅      |
| OP - 3rd body            |     ✅     |    ✅    | ❌                | ❌                 |    ✅     |      ✅      |
| OP - SRP                 |     ✅     |    ✅    | ❌                | ❌                 |    ✅     |      ✅      |
| OP - SGP4                |     ❌     |    ❌    | ✅                | ✅                 |    ❌     |      ✅      |
| OP - Other perturbations |     ❌     |    ✅    | ❌                | ❌                 |    ✅     |      ✅      |
| Eclipses                 |     ✅     |    ✅    | ✅                | ❌                 |    ❌     |      ✅      |
| GS visibility            |     ❌     |    ❌    | ❌                | ❌                 |    ✅     |      ✅      |
| ECEF export              |     ❌     |    ✅    | ✅                | ✅                 |    ✅     |      ✅      |

## Validation tools force models

### Celestlab

| Model            |                 Earth gravity                  | Other bodies gravity | Atmospheric drag | Solar radiation pressure |
|------------------|:----------------------------------------------:|:--------------------:|:----------------:|:------------------------:|
| Keplerian        |                   Point mass                   |          ❌           |        ❌         |            ❌             | 
| Secular J2       | Only secular effects of J2 on AOP, RAAN and MA |          ❌           |        ❌         |            ❌             | 
| Eckstein-Hechler |  Zonal harmonics up to J6, no tesseral terms   |          ❌           |        ❌         |            ❌             | 
| Lyddane          |            Zonal harmonics up to J5            |          ❌           |        ❌         |            ❌             |   
| STELA            |           Degree and order up to 15            |      Moon & Sun      |        ✅         |            ✅             |    

### GMAT

| Model        | Earth gravity | Other bodies gravity | Atmospheric drag | Solar radiation pressure |
|--------------|:-------------:|:--------------------:|:----------------:|:------------------------:|
| Customizable |       ✅       |          ✅           |        ✅         |            ✅             | 

## Validation models

Spherical gravity model : "zonal harmonics only" --> order m = 0. Degree up to chosen value.

### Tudatpy

To compare with Celestlab and GMAT

| Orbit        |                  Earth gravity                   | Other bodies gravity  | Atmospheric drag | Solar radiation pressure | Celestlab equivalent |
|--------------|:------------------------------------------------:|:---------------------:|:----------------:|:------------------------:|:--------------------:|
| keplerian    |                    Point mass                    |           ❌           |        ❌         |            ❌             |      Keplerian       | 
| earthZonalJ5 | Zonal harmonics up to J5 (degree l=5, order m=0) |           ❌           |        ❌         |            ❌             |       Lyddane        | 
| complete     |    Spherical harmonics degree and order = 15     | Moon & Sun point mass |        ✅         |            ✅             |        STELA         |  

### Poliastro

To compare with Celestlab (Keplerian only) and GMAT

| Orbit        |                  Earth gravity                   | Other bodies gravity  | Atmospheric drag | Solar radiation pressure | Celestlab equivalent |
|--------------|:------------------------------------------------:|:---------------------:|:----------------:|:------------------------:|:--------------------:|
| keplerian    |                    Point mass                    |           ❌           |        ❌         |            ❌             |      Keplerian       | 
| earthZonalJ3 | Zonal harmonics up to J3 (degree l=3, order m=0) |           ❌           |        ❌         |            ❌             |          ❌           | 
| complete     | Zonal harmonics up to J3 (degree l=3, order m=0) | Moon & Sun point mass |        ✅         |            ✅             |          ❌           |  

## Models used

| Feature                   | poliastro  |   Tudatpy   |  Celestlab  |           GMAT            |
|---------------------------|:----------:|:-----------:|:-----------:|:-------------------------:|
| Atmospheric density model | Jacchia77  | NRLMSISE-00 | NRLMSISE-00 | JacchiaRoberts & MSISE-90 |
| Earth gravity field       | J2/J3 only |   GOCO05c   |    EGM96    |           EGM96           |




