function [yn,info] = pal_corrector_v3(G,yi,yold,ds,scale)
% G: R^q -> R^(q-1), including all discretized orbit/phase equations.
% Requires fsolve, ds > 0, scale > 0 and distinct yi, yold of equal size.
% Inputs are fixed during correction.
yi=yi(:); yold=yold(:);
if nargin<5, scale=ones(size(yi)); end
scale=scale(:);
v=(yi-yold)./scale;
v=v/norm(v); predictor=yi+ds*(scale.*v);
opts=optimoptions('fsolve','Display','off',...
    'FunctionTolerance',1e-10,'StepTolerance',1e-11);
[yn,res,flag]=fsolve(@augmented,predictor,opts);
assert(flag>0 && norm(res,inf)<1e-8,...
    'Correction failed: reduce ds and retry without updating yi.');
info.predictor=predictor; info.tangent=v;
info.residual=norm(res,inf); info.exitflag=flag;
    function out=augmented(y)
        g=G(y);
        out=[g(:);v.'*((y-predictor)./scale)];
    end
end
