function M = Monodromia_mx_pelda_v3
% Variational matrix on p(t)=[cos(t);sin(t)], initialized with I.
I = eye(2);
opts = odeset('RelTol',1e-10,'AbsTol',1e-12);
[~,Y] = ode45(@variational,[0,2*pi],I(:),opts);
M = reshape(Y(end,:),2,2);
exact = diag([exp(-4*pi),1]);
disp('Computed multipliers:'); disp(eig(M));
fprintf('Matrix error: %.3e\n',norm(M-exact,inf));
    function dP = variational(t,Pvec)
        x = cos(t); y = sin(t);
        A = [1-3*x^2-y^2,-1-2*x*y;1-2*x*y,1-x^2-3*y^2];
        P = reshape(Pvec,2,2);
        AP = A*P; dP = AP(:);
    end
end
