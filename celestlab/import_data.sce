// =====================================================
// IMPORT INPUT DATA
// =====================================================
input_path = strsubst(pwd(), 'celestlab', 'input_data');

orbit = read_csv(strcat([input_path,"\orbits\",orbit_name,".csv"]));
semi_major_axis = strtod(orbit(1,2));
eccentricity = strtod(orbit(2,2));
inclination = strtod(orbit(3,2));
argument_of_periapsis = strtod(orbit(4,2));
longitude_of_ascending_node = strtod(orbit(5,2));
true_anomaly = strtod(orbit(6,2));
mean_anomaly = CL_kp_v2M(eccentricity,true_anomaly*%CL_deg2rad)*%CL_rad2deg;

spacecraft = read_csv(strcat([input_path,"\spacecraft\",spacecraft_name,".csv"]));
mass = strtod(spacecraft(1,2));
drag_coefficient = strtod(spacecraft(2,2));
reflectivity_coefficient = strtod(spacecraft(3,2));
drag_area = strtod(spacecraft(4,2));
srp_area = strtod(spacecraft(5,2));

dates = read_csv(strcat([input_path,"\dates\",dates_name,".csv"]));
start_date = dates(1,2);
start_epoch = CL_dat_cal2cjd(strtod(part(start_date,1:4)),strtod(part(start_date,6:7)),strtod(part(start_date,9:10)),strtod(part(start_date,12:13)),strtod(part(start_date,15:16)),strtod(part(start_date,18:19)));
end_date = dates(2,2);
end_epoch = CL_dat_cal2cjd(strtod(part(end_date,1:4)),strtod(part(end_date,6:7)),strtod(part(end_date,9:10)),strtod(part(end_date,12:13)),strtod(part(end_date,15:16)),strtod(part(end_date,18:19)));
step_size =strtod(dates(3,2))/86400; // convert seconds to julian days

groundstation = read_csv(strcat([input_path,"\groundstations\",groundstation_name,".csv"]));
groundstation_longitude = strtod(groundstation(1,2))*%CL_deg2rad;
groundstation_latitude = strtod(groundstation(2,2))*%CL_deg2rad;
groundstation_altitude = strtod(groundstation(3,2));
groundstation_min_elev = strtod(groundstation(4,2))*%CL_deg2rad;
groundstation = [groundstation_longitude;groundstation_latitude;groundstation_altitude];
