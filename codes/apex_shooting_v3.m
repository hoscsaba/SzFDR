function v0 = apex_shooting_v3
% Same apex problem as apex_bvp_v3; one unknown launch speed.
g=9.81; h=1;
opts=odeset('Events',@apex,'RelTol',1e-9,'AbsTol',1e-11);
v0=fzero(@residual,[1,8]);
[t,y]=ode45(@(~,y) [y(2);-g],[0,2],[0;v0],opts);
fprintf('v0=%.6f m/s, T=%.6f s\n',v0,t(end));
plot(t,y(:,1)); xlabel('t [s]'); ylabel('y [m]'); grid on
    function r=residual(v)
        [~,~,~,ye]=ode45(@(~,y) [y(2);-g],[0,2],[0;v],opts);
        r=ye(end,1)-h;
    end
    function [value,stop,direction]=apex(~,y)
        value=y(2); stop=1; direction=-1;
    end
end
