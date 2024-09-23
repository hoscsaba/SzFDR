function Monodromia_mx_pelda
clear all, clc

[t,x1]=ode45(@linode,[0 2*pi],[1 0]);
[t,x2]=ode45(@linode,[0 2*pi],[0 1]);
M=[x1(end,:)' x2(end,:)'];
e=eigs(M);
fprintf('\n eig(M)    =%+5.3e, %5.3e',e(2),e(1));
fprintf('\n exp(-4*pi)=%+5.3e\n',exp(-4*pi));
end

function dxdt=linode(t,x)
xp=cos(t); yp=sin(t);
Ap=[1-3*xp^2-yp^2,  -1-2*xp*yp;
    1-2*xp*yp,       1-xp^2-3*yp^2];
dxdt=Ap*[x(1);x(2)];
end
