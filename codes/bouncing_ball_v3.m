function [t,y,impacts] = bouncing_ball_v3
% First eight impacts only; no continuation past the Zeno time.
g=9.81; r=0.7; h0=1; ta=0; z=[h0;0];
t=0; y=z.'; impacts=[];
for j=1:8
    flight=(z(2)+sqrt(z(2)^2+2*g*z(1)))/g;
    opts=odeset('Events',@ground,'RelTol',1e-9,'AbsTol',1e-11,...
        'InitialStep',flight/100,'MaxStep',flight/10);
    [tt,zz,te,ze]=ode45(@(~,z) [z(2);-g],[ta,ta+1.2*flight],z,opts);
    assert(~isempty(te),'Ground event not found.');
    t=[t;tt(2:end)]; y=[y;zz(2:end,:)];
    ta=te(end); z=[0;-r*ze(end,2)];
    impacts(end+1)=ta;
    t=[t;ta]; y=[y;z.']; % Store both sides of the velocity jump.
end
Tz=sqrt(2*h0/g)*(1+r)/(1-r);
fprintf('Last computed impact: %.8f s; Zeno time: %.8f s\n',ta,Tz);
plot(t,y(:,1)); xlabel('t [s]'); ylabel('h [m]'); grid on
    function [value,stop,direction]=ground(t,z)
        value=z(1);
        if t==ta && z(2)>0, value=eps(h0); end
        stop=1; direction=-1;
    end
end
