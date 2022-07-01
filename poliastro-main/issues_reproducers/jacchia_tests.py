import numpy as np
from astropy import units as u
from poliastro.earth.atmosphere.jacchia import Jacchia77

wmN2 = 28.0134 * u.g / u.mol
wmO2 = 31.9988 * u.g / u.mol
wmO = 15.9994 * u.g / u.mol
wmAr = 39.948 * u.g / u.mol
wmHe = 4.0026 * u.g / u.mol
wmH = 1.0079 * u.g / u.mol

Na = 6.02217e23 * 1 / u.mol  # from Jacchia PDF page 51

jacchia77_solutions = {
    90 * u.km: -5.465,
    100 * u.km: -6.247,
    120 * u.km: -7.646,
    150 * u.km: -8.701,
    200 * u.km: -9.566,
    300 * u.km: -10.667,
    400 * u.km: -11.507,
    500 * u.km: -12.246,
    560 * u.km: -12.659,
    800 * u.km: -13.991,
    1000 * u.km: -14.547,
    1500 * u.km: -15.260,
    2000 * u.km: -15.780,
    2400 * u.km: -16.085
}

for z in jacchia77_solutions:
    expected_rho_log = jacchia77_solutions[z]

    atmosphere = Jacchia77(1000 * u.K)

    properties = atmosphere.altitude_profile(z)
    for i in range(2, len(properties) - 1):
        if properties[i].value <= 1.26e-10:
            properties[i] = -9.9 * properties[i].unit
    Z, T, CN2, CO2, CO, CAr, CHe, CH, CM, WM = properties

    density = ((wmN2 * CN2 + wmO2 * CO2 + wmO * CO + wmAr * CAr + wmHe * CHe + wmH * CH) / Na).to(u.kg / u.m ** 3)
    rho_log = np.log10(density.value)

    print(
        f'altitude: {z}, expected log density: {expected_rho_log}, computed log density: {rho_log}, log difference: {(rho_log - expected_rho_log):e}')
