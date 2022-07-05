# Input Data

Subfolders of the `input_data` directory contain all the input data for the python codes.

## Dates

The dates CSV files contain the following data (without table headers):

| Field name   |                     Value example and unit                     |
|--------------|:--------------------------------------------------------------:|
| `start_date` | `2022-12-31-24:59:59` (parsed into a python `datetime` object) | 
| `end_date`   | `2022-12-31-24:59:59` (parsed into a python `datetime` object) |
| `step_size`  |                      `10`    (in seconds)                      |

## Ground stations

| Field name          |  Value example and unit  |
|---------------------|:------------------------:|
| `longitude`         | `1.444209` (in degrees)  | 
| `latitude`          | `43.604652` (in degrees) |
| `altitude`          |   `200`    (in meters)   |
| `minimum_elevation` |   `5`    (in degrees)    |


## Orbits

| Field name                    | Value example and unit |
|-------------------------------|:----------------------:|
| `semi_major_axis`             | `6978140` (in meters)  | 
| `eccentricity`                |   `1e-3` (unitless)    |
| `inclination`                 | `97.8`    (in degrees) |
| `argument_of_periapsis`       |  `15`    (in degrees)  |
| `longitude_of_ascending_node` | `190`    (in degrees)  |
| `true_anomaly`                | `0.1`    (in degrees)  |

## Spacecraft

| Field name                 | Value example and unit |
|----------------------------|:----------------------:|
| `mass`                     |      `4` (in kg)       | 
| `drag_coefficient`         |    `2.2` (unitless)    |
| `reflectivity_coefficient` |  `1.5`    (unitless)   |
| `drag_area`                |   `0.033`    (in m²)   |
| `srp_area`                 |   `0.033`    (in m²)   |

