function border_collision_v3
% Continuous map, slopes 1/2 and -3/2; stable fixed point becomes a 2-cycle.
mu=linspace(-0.2,0.2,401); x=zeros(size(mu));
figure; hold on
for j=1:180
    left=x<=0;
    x=mu+(0.5*left-1.5*(~left)).*x;
    if j>160, plot(mu,x,'.','Color',[0.1,0.35,0.7]); end
end
xlabel('mu'); ylabel('x'); grid on
end
