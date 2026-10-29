% Boundary equilibrium examples; dimensionless variables.
clear; close all;
root = fileparts(fileparts(mfilename('fullpath')));
f = figure('Units','centimeters','Position',[2 2 16 18]);
tiledlayout(3,1,'TileSpacing','compact');
u = linspace(-1,0,150); w = linspace(0,1,150);
nexttile; hold on;
plot(u,u,'b',w,w/2,'b','LineWidth',1.5);
plot(w,w,'b--',u,u/2,'b--','LineWidth',1);
title('Persistence'); ylabel('x^*');
nexttile; hold on;
plot(u,u,'b',u,-u,'r','LineWidth',1.5);
plot(w,w,'b--',w,-w,'r--','LineWidth',1);
title('Non-smooth fold'); ylabel('x^*');
nexttile; hold on;
plot(u,0*u,'Color',[0 .5 .2],'LineWidth',1.5);
plot(w,w,'b','LineWidth',1.5);
plot(u,u,'b--','LineWidth',1);
title('Filippov: equilibrium / pseudo-equilibrium'); ylabel('y^*');
for ax = findall(f,'Type','axes')'
    xline(ax,0,':'); yline(ax,0,':'); grid(ax,'on');
    xlabel(ax,'\mu'); xlim(ax,[-1 1]); ylim(ax,[-1.1 1.1]);
    set(ax,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'TitleFontSizeMultiplier',1);
end
set(f,'PaperUnits','centimeters','PaperSize',[16 18],...
    'PaperPosition',[0 0 16 18]);
print(f,fullfile(root,'graphics_v3','boundary_equilibria.pdf'),'-dpdf','-painters');
print(f,fullfile(root,'graphics_svg','boundary_equilibria.svg'),'-dsvg');
