from datetime import datetime

from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Sun
from poliastro.ephem import build_ephem_interpolant

# Setup start/end epochs
start_epoch = datetime(2020, 1, 1, 0, 0, 0)
end_epoch = datetime(2020, 1, 2, 0, 0, 0)

# Create Time objects
start_epoch_Time_obj = Time(start_epoch, scale='utc')
end_epoch_Time_obj = Time(end_epoch, scale='utc')

# Build the Sun ephemeris interpolant
"""This line throws the following error: TypeError: Frame data has no associated differentials (i.e. the frame has no 
velocity data) - represent_as() only accepts a new representation. """
Sun_r = build_ephem_interpolant(Sun, 50 * u.day,
                                (start_epoch_Time_obj.to_value("jd") << u.d, end_epoch_Time_obj.to_value("jd") << u.d),
                                rtol=1e-2)
