function bvp_cannon_shooting
% Shooting: find launch angles whose trajectories reach (X,Y).
g=9.81; k=0.5*1.225*0.47*0.01; m=5; V0=300;
X=800; Y=100; tmax=120;
angles=linspace(1e-3,pi/2-1e-3,181);
values=arrayfun(@residual,angles);
idx=find(values(1:end-1).*values(2:end)<0);
assert(~isempty(idx),'No launch-angle root bracketed on the search grid.');
figure; hold on; grid on
for j=idx
    theta=fzero(@residual,angles(j:j+1));
    [~,z,te,ze]=trajectory(theta);
    plot(z(:,1),z(:,2),'DisplayName',sprintf('%.3f deg',theta*180/pi));
    fprintf('theta=%.6f deg, T=%.6f s, error=%.3e m\n',...
        theta*180/pi,te,ze(end,2)-Y);
end
plot(X,Y,'r^','DisplayName','target');
xlabel('x [m]'); ylabel('y [m]'); legend('show');

    function r=residual(theta)
        [~,~,te,ze]=trajectory(theta);
        r=NaN; % Trajectories that do not reach x=X cannot bracket a root.
        if ~isempty(te), r=ze(end,2)-Y; end
    end
    function [t,z,te,ze]=trajectory(theta)
        z0=[0;0;V0*cos(theta);V0*sin(theta)];
        opts=odeset('RelTol',1e-8,'AbsTol',1e-10,...
            'Events',@target,'MaxStep',0.5);
        [t,z,te,ze]=ode45(@rhs,[0,tmax],z0,opts);
    end
    function dz=rhs(~,z)
        drag=k/m*hypot(z(3),z(4));
        dz=[z(3);z(4);-drag*z(3);-g-drag*z(4)];
    end
    function [value,stop,direction]=target(~,z)
        value=z(1)-X; stop=1; direction=1;
    end
end
