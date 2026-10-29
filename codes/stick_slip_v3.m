function [t,x,v] = stick_slip_v3
% Exact segments for m=k=1, belt speed U, static force Fs > Fk > 0.
U=0.3; Fs=0.6; Fk=0.4;
Ts=2*(Fs-Fk)/U;
Tl=2*pi-2*atan((Fs-Fk)/U);
s=linspace(0,Ts,101); q=linspace(0,Tl,301);
tc=[s,Ts+q(2:end)];
xc=[2*Fk-Fs+U*s,Fk+(Fs-Fk)*cos(q(2:end))+U*sin(q(2:end))];
vc=[U*ones(size(s)),-(Fs-Fk)*sin(q(2:end))+U*cos(q(2:end))];
t=[]; x=[]; v=[];
for j=0:2
    t=[t,j*(Ts+Tl)+tc]; x=[x,xc]; v=[v,vc];
end
subplot(2,1,1); plot(t,x); ylabel('x'); grid on
subplot(2,1,2); plot(t,v-U); ylabel('v-U'); xlabel('t'); grid on
fprintf('Stick time=%.6f, slip time=%.6f\n',Ts,Tl);
end
