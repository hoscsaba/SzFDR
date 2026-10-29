function impact_portraits_v3
% Figures 4.1-4.2; uses impact_monodromy_v3.m from this directory.
f1=figure; f2=figure;
for j=1:3
    w=[3,2.76,2.9]; w=w(j); T=2*pi/w;
    [~,~,t,y]=impact_monodromy_v3([1;0],0,100*T,0,w,0.95,0);
    keep=t>=88*T; t=t(keep); y=y(keep,:);
    % NaN separates the two sides of an instantaneous velocity jump.
    jumps=[false;diff(t)==0]; yp=y; yp(jumps,:)=NaN;
    figure(f1); subplot(3,1,j); plot(yp(:,1),yp(:,2));
    xlabel('u'); ylabel('v'); title(sprintf('omega = %g',w)); grid on
    figure(f2); subplot(3,1,j); plot(t/T-88,y(:,1));
    xlabel('(t-88T)/T'); ylabel('u(t)'); grid on
end
end
