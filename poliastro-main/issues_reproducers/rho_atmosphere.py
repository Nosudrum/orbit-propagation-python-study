from astropy import units as u
from poliastro.earth.atmosphere import jacchia

atm_jacchia = jacchia.Jacchia77(2400 * u.K)
alt = 500 * u.km
R_jacchia = jacchia.R
rho_jacchia = atm_jacchia.density(alt)
P_jacchia = atm_jacchia.pressure(alt)
[z, T, N2, O2, O, Ar, He, H, total_number_density, mean_molecular_weight] = atm_jacchia.altitude_profile(alt)

print(f'P (pressure) = {P_jacchia}')
print(f'WM (mean molecular weight) = {mean_molecular_weight}')
print(f'R (gas constant) = {R_jacchia}')
print(f'T (temperature) = {T}')
print(f'rho (density) = {rho_jacchia}')
