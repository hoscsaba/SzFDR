function bvp_cannon

g   = 9.81;  rho = 1.225; Cd  = 0.47; 
A   = 0.01; m   = 5.0; k   = 0.5*rho*Cd*A; 
X   = 800.0; Y = 100.0;  V0 = 300.0;  

odefun = @(tau, y, p) odefun_tau(tau, y, p, g, k, m);
bcfun = @(ya, yb, ~) bcfun_bvp(ya, yb, X, Y, V0);

T0 = hypot(X,Y)/V0;
theta0 = atan2(Y, X);  vx0 = V0*cos(theta0); vy0 = V0*sin(theta0);

guess = @(tau) [X*tau; Y*tau; vx0*ones(size(tau)); vy0*ones(size(tau))];
tau_mesh = linspace(0, 1, 51);
solinit = bvpinit(tau_mesh, guess, T0);

opts = bvpset('RelTol',1e-6,'AbsTol',1e-8,'NMax',5000);
sol  = bvp5c(odefun, bcfun, solinit, opts);

T  = sol.parameters;   
tau_plot = linspace(0,1,400);
Ysol = deval(sol, tau_plot);
x_traj  = Ysol(1,:); y_traj  = Ysol(2,:); 
vx0_sol = Ysol(3,1); vy0_sol = Ysol(4,1);
theta   = atan2(vy0_sol, vx0_sol); 

fprintf('T      = %.6f s\n', T);
fprintf('theta  = %.6f rad (%.3f deg)\n', theta, theta*180/pi);

figure; hold on; box on; grid on;
plot(x_traj, y_traj, 'LineWidth', 1.6);
plot(0,0,'ko','MarkerFaceColor','k');
plot(X,Y,'rs','MarkerFaceColor','r');
xlabel('x [m]'); ylabel('y [m]');
legend('trajectory','start','target','Location','best');
end

function dydtau = odefun_tau(~, y, p, g, k, m)
T  = p;
vx = y(3,:);
vy = y(4,:);
v  = sqrt(vx.^2 + vy.^2);
dydtau = T * [ vx; ...
               vy; ...
              -(k/m).*v.*vx; ...
              -g - (k/m).*v.*vy ];
end

function res = bcfun_bvp(ya, yb, X, Y, V0)
res = [ ya(1); ...
        ya(2); ...
        yb(1) - X; ...
        yb(2) - Y; ...
        ya(3)^2 + ya(4)^2 - V0^2 ];
end
