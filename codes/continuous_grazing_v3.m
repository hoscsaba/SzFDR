% Exact compliant contact and same-time grazing correction.
clear; close all;
root = fileparts(fileparts(mfilename('fullpath')));
a = 1; kappa = 4; e = .1;
V = sqrt(2*a*e); T0 = 2*V/a;
Tc = 2/sqrt(kappa)*atan(V*sqrt(kappa)/a);
t = linspace(0,1.2*T0,500);
h0 = -V*t+a*t.^2/2;
h = a/kappa*(1-cos(sqrt(kappa)*t))...
    -V/sqrt(kappa)*sin(sqrt(kappa)*t);
i = t > Tc; d = t(i)-Tc;
h(i) = V*d+a*d.^2/2;
f = figure('Units','centimeters','Position',[2 2 16 14]);
tiledlayout(2,1,'TileSpacing','compact');
nexttile;
plot(t,h0,'k--',t,h,'b','LineWidth',1.5); yline(0,':');
xline(Tc,':'); xline(T0,':');
xlabel('t [s]'); ylabel('h [m]'); grid on;
legend('Reference','Compliant contact','Location','northwest');
nexttile;
e = logspace(-5,-1,120); V = sqrt(2*a*e);
d = 2*V/a-2/sqrt(kappa)*atan(V*sqrt(kappa)/a);
dv = a*d; leading = 4*kappa/3*sqrt(2/a)*e.^1.5;
loglog(e,dv,'b',e,leading,'k--','LineWidth',1.5); grid on;
xlabel('\epsilon [m]'); ylabel('\Delta v [m/s]');
legend('Exact','Order 3/2','Location','northwest');
fprintf('Small-epsilon ratio exact/leading: %.8f\n',dv(1)/leading(1));
for ax = findall(f,'Type','axes')'
    set(ax,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'TitleFontSizeMultiplier',1);
end
set(findall(f,'Type','legend'),'FontName','Times New Roman','FontSize',11);
set(f,'PaperUnits','centimeters','PaperSize',[16 14],...
    'PaperPosition',[0 0 16 14]);
print(f,fullfile(root,'graphics_v3','continuous_grazing.pdf'),'-dpdf','-painters');
print(f,fullfile(root,'graphics_svg','continuous_grazing.svg'),'-dsvg');
