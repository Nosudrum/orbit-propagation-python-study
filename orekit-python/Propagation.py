# get_ipython().run_line_magic('matplotlib', 'inline')

from math import radians

import orekit
from orekit import JArray_double
from orekit.pyhelpers import setup_orekit_curdir
from org.hipparchus.ode.nonstiff import DormandPrince853Integrator
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FramesFactory
from org.orekit.orbits import KeplerianOrbit, OrbitType, PositionAngle
from org.orekit.propagation import SpacecraftState
from org.orekit.propagation.analytical import EcksteinHechlerPropagator, KeplerianPropagator
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import Constants, IERSConventions

vm = orekit.initVM()

setup_orekit_curdir()

utc = TimeScalesFactory.getUTC()

ra = 500 * 1000  # Apogee
rp = 400 * 1000  # Perigee
i = radians(87.0)  # inclination
omega = radians(20.0)  # perigee argument
raan = radians(10.0)  # right ascension of ascending node
lv = radians(0.0)  # True anomaly

epochDate = AbsoluteDate(2020, 1, 1, 0, 0, 00.000, utc)
initialDate = epochDate

a = (rp + ra + 2 * Constants.WGS84_EARTH_EQUATORIAL_RADIUS) / 2.0
e = 1.0 - (rp + Constants.WGS84_EARTH_EQUATORIAL_RADIUS) / a

# Inertial frame where the satellite is defined
inertialFrame = FramesFactory.getEME2000()

# Orbit construction as Keplerian
initialOrbit = KeplerianOrbit(a, e, i, omega, raan, lv,
                              PositionAngle.TRUE,
                              inertialFrame, epochDate, Constants.WGS84_EARTH_MU)

propagator = KeplerianPropagator(initialOrbit)

propagator.getInitialState()

propagator.propagate(initialDate, initialDate.shiftedBy(3600.0 * 48))

propagator_eh = EcksteinHechlerPropagator(initialOrbit,
                                          Constants.EIGEN5C_EARTH_EQUATORIAL_RADIUS,
                                          Constants.EIGEN5C_EARTH_MU, Constants.EIGEN5C_EARTH_C20,
                                          Constants.EIGEN5C_EARTH_C30, Constants.EIGEN5C_EARTH_C40,
                                          Constants.EIGEN5C_EARTH_C50, Constants.EIGEN5C_EARTH_C60)

propagator_eh.getInitialState()

end_state = propagator_eh.propagate(initialDate, initialDate.shiftedBy(3600.0 * 48))

OrbitType.KEPLERIAN.convertType(end_state.getOrbit())

minStep = 0.001
maxStep = 1000.0
initStep = 60.0

positionTolerance = 1.0

tolerances = NumericalPropagator.tolerances(positionTolerance,
                                            initialOrbit,
                                            initialOrbit.getType())

integrator = DormandPrince853Integrator(minStep, maxStep,
                                        JArray_double.cast_(tolerances[0]),
                                        # Double array of doubles needs to be cast in Python
                                        JArray_double.cast_(tolerances[1]))
integrator.setInitialStepSize(initStep)

satellite_mass = 100.0  # The models need a spacecraft mass, unit kg.
initialState = SpacecraftState(initialOrbit, satellite_mass)

propagator_num = NumericalPropagator(integrator)
propagator_num.setOrbitType(OrbitType.CARTESIAN)
propagator_num.setInitialState(initialState)

gravityProvider = GravityFieldFactory.getNormalizedProvider(10, 10)
propagator_num.addForceModel(
    HolmesFeatherstoneAttractionModel(FramesFactory.getITRF(IERSConventions.IERS_2010, True), gravityProvider))

OrbitType.KEPLERIAN.convertType(propagator_num.getInitialState().getOrbit())

end_state = propagator_num.propagate(initialDate, initialDate.shiftedBy(3600.0 * 48))

OrbitType.KEPLERIAN.convertType(end_state.getOrbit())  # Note that this is the Osculating orbit!
