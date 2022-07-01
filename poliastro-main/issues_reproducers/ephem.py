from datetime import datetime, timedelta

import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth, Sun
from poliastro.ephem import Ephem, build_ephem_interpolant
from scipy.interpolate import interp1d

step_size = timedelta(seconds=10)
start = datetime(2020, 1, 1, 0, 0, 0)
end = datetime(2020, 1, 1, 0, 1, 0)
epoch_start = Time(start, scale='utc')
epoch_end = Time(end, scale='utc')

Sun_r_poliastro = build_ephem_interpolant(Sun, 8 * u.s,
                                          (epoch_start.to_value("jd") << u.d, epoch_end.to_value("jd") << u.d),
                                          rtol=1)


def custom_ephem_interpolant(start, end, step_size, body):
    epochs = np.arange(start, end + step_size, step_size)
    epochs_jd = Time(Time(epochs, scale='utc').to_value("jd"), format="jd", scale="tdb")
    epochs_sec = np.arange(0, (end + step_size - start).total_seconds(), step_size.total_seconds())

    ephem = Ephem.from_body(body, epochs_jd, attractor=Earth)

    interpolant = interp1d(
        epochs_sec << u.s,
        ephem.sample(epochs_jd).xyz.to_value(u.km)
    )
    return interpolant


Sun_r_custom = custom_ephem_interpolant(start, end, step_size, Sun)

print(Sun_r_poliastro.x)
print(Sun_r_custom.x)
