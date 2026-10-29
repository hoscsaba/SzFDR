function sol = slip_bvp_v3(mesh,guess,Tguess,p)
% Fixed-parameter, two-segment SLIP BVP (not a general fold continuation).
% p: g, kappa, l0, alpha, E. Velocities use physical time.
% guess: 8-by-numel(mesh), [x1;y1;vx1;vy1;x2;y2;vx2;vy2].
% Tguess: positive stance and flight durations. Mesh covers [0,1].
% Requires g, kappa, l0, E > 0 and 0 < alpha < pi/2.
init=bvpinit(mesh,guess,log(Tguess(:)));
opts=bvpset('RelTol',1e-8,'AbsTol',1e-10,'NMax',10000);
sol=bvp5c(@rhs,@bcs,init,opts);
% Select the physical branch: compression, flight above touchdown,
% descending touchdown and extending lift-off.
Y=deval(sol,linspace(0,1,501));
ell=hypot(Y(1,:),Y(2,:));
assert(all(Y(2,:)>0) && all(ell<=p.l0+1e-5) && ...
    all(Y(6,:)>=p.l0*cos(p.alpha)-1e-5) && Y(8,end)<0 && ...
    Y(1,end)*Y(3,end)+Y(2,end)*Y(4,end)>0,...
    'Nonphysical SLIP branch.');
    function dY=rhs(~,Y,q)
        durations=exp(q(:));
        l=hypot(Y(1),Y(2));
        assert(l>0,'Singular leg length.');
        c=p.kappa*(p.l0/l-1);
        dY=[durations(1)*[Y(3);Y(4);c*Y(1);c*Y(2)-p.g];...
            durations(2)*[Y(7);Y(8);0;-p.g]];
    end
    function res=bcs(a,b,~)
        res=[a(1)+p.l0*sin(p.alpha);...
            a(2:4)-b(6:8);a(5:8)-b(1:4);...
            hypot(b(1),b(2))-p.l0;...
            (a(3)^2+a(4)^2)/2+p.g*p.l0*cos(p.alpha)-p.E];
    end
end
