function [T,sol] = apex_bvp_v3
% Find launch speed and time to reach height h with zero velocity.
g=9.81; h=1;
rhs=@(~,y,T) T*[y(2);-g];
bcs=@(a,b,~) [a(1);b(1)-h;b(2)];
guess=@(s) [h*s;4*(1-s)];
init=bvpinit(linspace(0,1,11),guess,0.5);
sol=bvp5c(rhs,bcs,init);
T=sol.parameters;
s=linspace(0,1,101); y=deval(sol,s);
fprintf('T=%.6f s, v0=%.6f m/s\n',T,y(2,1));
plot(T*s,y(1,:)); xlabel('t [s]'); ylabel('y [m]'); grid on
end
