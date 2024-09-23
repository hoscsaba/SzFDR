function fun_mx_example
clear all, clc
x0=[0.1; 0.2]; tmax=0.1;
[t,x1]=ode45(@linode,[0 tmax],x0);
fprintf('\n ode45 -> t=%3.2f: x=(%+5.3f, %+5.3f)\n',tmax,x1(end,1),x1(end,2));

x2=fun_sol_mx(tmax)*x0;
fprintf('\n FSM   -> t=%3.2f: x=(%+5.3f, %+5.3f)\n',tmax,x2(1),x2(2));
fun_sol_mx(0)
end

function dxdt=linode(t,x)
dxdt=[1  3;
      1 -1]*x;
end

function out=fun_sol_mx(t)
a=exp(2*t); b=exp(-2*t);
out=1/4*[3*a+b 3*a-3*b
    a-b a+3*b];
end

%%% OUTPUT
% ode45 -> t=0.10: x=(+0.172, +0.194)
%
% FSM   -> t=0.10: x=(+0.172, +0.194)
%
% ans =
%
%     1     0
%     0     1