// =====================================================
// CREATE DIRECTORIES IF MISSING
// =====================================================
results_path = strcat([pwd(),"\results"]);
if ~isdir(results_path) then
    mkdir(pwd(), "results");
end
results_model_path = strcat([results_path,"\",propagation_name]);
if ~isdir(results_model_path) then
    mkdir(results_path, propagation_name);
end
results_partial_name=strcat([results_model_path,"\",spacecraft_name,"_",orbit_name,"_",dates_name]);

// =====================================================
// SAVE STATES TO CSV
// =====================================================
kep_osc_results(6,:) = CL_kp_M2v(kep_osc_results(2,:), kep_osc_results(6,:));
kep_osc_results(3:6,:) = pmodulo(kep_osc_results(3:6,:)*%CL_rad2deg,360);

csvWrite([states_array,kep_osc_results',pos_ecf',vel_ecf'],strcat([results_partial_name,'.csv']));

// =====================================================
// CREATE PLOTTABLE ECLIPSE POINTS
// =====================================================
eclipse_pen_plot=%nan*zeros(4*length(eclipse_pen)/2,1);
for ii=1:length(eclipse_pen)/2
    tmp=4*(ii-1)+1;
    eclipse_pen_plot(tmp,1)=eclipse_pen(1,ii);
    eclipse_pen_plot(tmp,2)=0;
    eclipse_pen_plot(tmp+1,1)=eclipse_pen(1,ii);
    eclipse_pen_plot(tmp+1,2)=1;
    eclipse_pen_plot(tmp+2,1)=eclipse_pen(2,ii);
    eclipse_pen_plot(tmp+2,2)=1;
    eclipse_pen_plot(tmp+3,1)=eclipse_pen(2,ii);
    eclipse_pen_plot(tmp+3,2)=0;
end
if length(eclipse_pen_plot)>0 then
    eclipse_pen_plot(:,1)=(eclipse_pen_plot(:,1)-epochs(1))*24;
    eclipse_pen_plot=[0,0;eclipse_pen_plot;ceil((end_epoch-start_epoch)*24),0];
else
    eclipse_pen_plot=[0,0;ceil((end_epoch-start_epoch)*24),0];
end

eclipse_umb_plot=%nan*zeros(4*length(eclipse_umb)/2,1);
for ii=1:length(eclipse_umb)/2
    tmp=4*(ii-1)+1;
    eclipse_umb_plot(tmp,1)=eclipse_umb(1,ii);
    eclipse_umb_plot(tmp,2)=0;
    eclipse_umb_plot(tmp+1,1)=eclipse_umb(1,ii);
    eclipse_umb_plot(tmp+1,2)=1;
    eclipse_umb_plot(tmp+2,1)=eclipse_umb(2,ii);
    eclipse_umb_plot(tmp+2,2)=1;
    eclipse_umb_plot(tmp+3,1)=eclipse_umb(2,ii);
    eclipse_umb_plot(tmp+3,2)=0;
end
if length(eclipse_umb_plot)>0 then
    eclipse_umb_plot(:,1)=(eclipse_umb_plot(:,1)-epochs(1))*24;
    eclipse_umb_plot=[0,0;eclipse_umb_plot;ceil((end_epoch-start_epoch)*24),0];
else
    eclipse_umb_plot=[0,0;ceil((end_epoch-start_epoch)*24),0];
end

// =====================================================
// CREATE PLOTTABLE COMMUNICATION WINDOWS POINTS
// =====================================================
comm_win_plot=%nan*zeros(4*length(comm_windows)/2,1);
for ii=1:length(comm_windows)/2
    tmp=4*(ii-1)+1;
    comm_win_plot(tmp,1)=comm_windows(1,ii);
    comm_win_plot(tmp,2)=0;
    comm_win_plot(tmp+1,1)=comm_windows(1,ii);
    comm_win_plot(tmp+1,2)=1;
    comm_win_plot(tmp+2,1)=comm_windows(2,ii);
    comm_win_plot(tmp+2,2)=1;
    comm_win_plot(tmp+3,1)=comm_windows(2,ii);
    comm_win_plot(tmp+3,2)=0;
end
if length(comm_win_plot)>0 then
    comm_win_plot(:,1)=(comm_win_plot(:,1)-epochs(1))*24;
    comm_win_plot=[0,0;comm_win_plot;ceil((end_epoch-start_epoch)*24),0];
else
    comm_win_plot=[0,0;ceil((end_epoch-start_epoch)*24),0];
end

// =====================================================
// CREATE PLOTS
// =====================================================
scf(1);
param3d(sat_pos(1,:)/1e3, sat_pos(2,:)/1e3, sat_pos(3,:)/1e3);
title('Spacecraft trajectory around the Earth');
xlabel('x [km]');
ylabel('y [km]');
zlabel('z [km]');
deff("[x,y,z]=sph(alp,tet)",["x=r*cos(alp).*cos(tet)+orig(1)*ones(tet)";..
     "y=r*cos(alp).*sin(tet)+orig(2)*ones(tet)";..
     "z=r*sin(alp)+orig(3)*ones(tet)"]);
r=%CL_eqRad/1e3; orig=[0 0 0];
set(gca(),"auto_clear","off");
[xx,yy,zz]=eval3dp(sph,linspace(-%pi/2,%pi/2,40),linspace(0,%pi*2,20));
plot3d(xx,yy,zz,,theta=70,alpha=80);
h=gca();
h.box="back_half";
xs2png(1,strcat([results_partial_name,".png"]));

scf(2);
plot(eclipse_pen_plot(:,1),1-eclipse_pen_plot(:,2),'Color','blue');
// plot(eclipse_umb_plot(:,1),1-eclipse_umb_plot(:,2),'Color','red');
ax=gca();
ax.data_bounds=[0 -0.01;ceil((end_epoch-start_epoch)*24) 1.01];
xlabel("Time [h]");
ylabel("Shadow function");
title("Spacecraft shadow function");
// legend(['Penumbra','Umbra']);
xs2png(2,strcat([results_partial_name,"_shadow_function.png"]));

scf(3);
plot(comm_win_plot(:,1),comm_win_plot(:,2),'Color','blue');
ax=gca();
ax.data_bounds=[0 -0.01;ceil((end_epoch-start_epoch)*24) 1.01];
xlabel("Time [h]");
ylabel("Visibility function");
title("Spacecraft ground station visibility function");
xs2png(3,strcat([results_partial_name,"_visibility_function.png"]));
