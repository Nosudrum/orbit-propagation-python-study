from astropy import units as u
from poliastro.earth.atmosphere import coesa62, coesa76, jacchia

# Create atmospheres
atm_coesa62 = coesa62.COESA62()
atm_coesa76 = coesa76.COESA76()
atm_jacchia = jacchia.Jacchia77(1050 * u.K)

# Get densities
alt = 500 * u.km
rho_coesa62 = atm_coesa62.density(alt)
rho_coesa76 = atm_coesa76.density(alt)
rho_jacchia = atm_jacchia.density(alt)
print(f'rho_coesa62 = {rho_coesa62}, rho_coesa76 = {rho_coesa76}, rho_jacchia = {rho_jacchia}')
