function [yT,M,tout,yout,nImpact] = impact_monodromy_v3(y0,t0,T,zeta,omega,r,sigma)
% Fixed-phase state map and its derivative for u''+2*zeta*u'+u=cos(omega*t).
% Domain: u>sigma; transverse reset: [u;v] -> [u;-r*v].
% M is a monodromy matrix only when yT=y0 for the chosen T.
% Requires T, omega > 0, zeta >= 0, 0 < r <= 1 and y0(1) > sigma.
% Start and end away from impact; grazing/sticking require another model.
y0 = y0(:);
L = [0,1;-1,-2*zeta];
Phi = eye(2);
z = [y0;Phi(:)];
ta = t0; tf = t0+T;
timeTol = 100*eps(max([1,abs(t0),abs(tf)]));
tout = t0; yout = y0.'; nImpact = 0;
while ta < tf
    opts = odeset('RelTol',1e-10,'AbsTol',1e-12,...
        'MaxStep',min(T,2*pi/omega)/100,'Events',@wall_event);
    [tt,zz,te,ze] = ode45(@rhs,[ta,tf],z,opts);
    tout = [tout;tt(2:end)]; %#ok<AGROW>
    yout = [yout;zz(2:end,1:2)]; %#ok<AGROW>
    if isempty(te)
        z = zz(end,:).';
        break
    end
    ti = te(end); z = ze(end,:).';
    assert(ti-ta>timeTol,'No progress: possible sticking or event chatter.');
    assert(tf-ti>timeTol,'Choose a final phase away from an impact.');
    vm = z(2);
    assert(vm < -1e-8,'Near-grazing impact: saltation is singular.');
    am = -sigma-2*zeta*vm+cos(omega*ti);
    vp = -r*vm;
    ap = -sigma-2*zeta*vp+cos(omega*ti);
    S = [-r,0;(ap+r*am)/vm,-r];
    Phi = S*reshape(z(3:6),2,2);
    z = [sigma;vp;Phi(:)];
    nImpact = nImpact+1;
    tout = [tout;ti]; %#ok<AGROW>
    yout = [yout;z(1:2).']; %#ok<AGROW>
    ta = ti;
end
yT = z(1:2); M = reshape(z(3:6),2,2);

    function dz = rhs(t,zlocal)
        P = reshape(zlocal(3:6),2,2);
        dP = L*P;
        dz = [zlocal(2);-zlocal(1)-2*zeta*zlocal(2)+cos(omega*t);dP(:)];
    end

    function [value,isterminal,direction] = wall_event(t,zlocal)
        value = zlocal(1)-sigma;
        % On restart the state is on the wall and moves into the domain.
        if t == ta && zlocal(2)>0
            value = eps(max(1,abs(sigma)));
        end
        isterminal = 1; direction = -1;
    end
end
