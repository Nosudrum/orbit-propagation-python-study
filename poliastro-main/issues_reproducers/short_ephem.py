from datetime import datetime

from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Moon, Sun
from poliastro.ephem import build_ephem_interpolant

# Setup start/end epochs
start_epoch = datetime(2020, 1, 1, 0, 0, 0)
end_epoch = datetime(2020, 1, 2, 0, 0, 0)

# Create Time objects
start_epoch_Time_obj = Time(start_epoch, scale='utc')
end_epoch_Time_obj = Time(end_epoch, scale='utc')

# Build the Sun ephemeris interpolant
"""
This line throws the following error:
ValueError: cannot reshape array of size 0 into shape (0,newaxis)
"""
Sun_r = build_ephem_interpolant(Sun, 1 * u.year,
                                (start_epoch_Time_obj.to_value("jd") << u.d, end_epoch_Time_obj.to_value("jd") << u.d),
                                rtol=1e-2)

# Build the Moon ephemeris interpolant
"""
This line throws the following error:
ValueError: The number of derivatives at boundaries does not match: expected 1, got 0+0
"""
Moon_r = build_ephem_interpolant(Moon, 28 * u.day,
                                 (start_epoch_Time_obj.to_value("jd") << u.d, end_epoch_Time_obj.to_value("jd") << u.d),
                                 rtol=1e-2)
