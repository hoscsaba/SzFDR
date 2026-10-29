% Exact local trajectories; green segments are sliding.
clear; close all;
root = fileparts(fileparts(mfilename('fullpath')));
f = figure('Units','centimeters','Position',[2 2 16 17]);
tiledlayout(2,2,'TileSpacing','compact','Padding','compact');
styles = {'b-','k--','r-'}; green = [0 .55 .2];
for panel = 1:4
    nexttile; hold on; yline(0,':');
    for j = 1:3
        p = (j-2)*.25;
        if panel == 1 || panel == 3
            x = linspace(-1.1,p,100);
            plot(x,x-p,styles{j},'LineWidth',1.3);
            if panel == 1
                if p < 0, plot([p 0],[0 0],'Color',green,'LineWidth',3); end
                x = linspace(max(p,0),1.1,150);
                y = (x.^2-max(p,0)^2)/2;
            else
                if p < 0
                    x = linspace(p,-p,150);
                    plot(x,(p^2-x.^2)/2,styles{j},'LineWidth',1.3);
                end
                x = [abs(p) 1.1]; y = [0 0];
                plot(x,y,'Color',green,'LineWidth',3);
            end
        elseif panel == 2
            c = p/2;
            if c < 0
                hit = -sqrt(-2*c); x = linspace(-1.1,hit,100);
                plot(x,x.^2/2+c,styles{j},'LineWidth',1.3);
                plot([hit 0],[0 0],'Color',green,'LineWidth',3);
                x = linspace(0,1.1,100); y = x.^2/2;
            else
                x = linspace(-1.1,1.1,200); y = x.^2/2+c;
            end
        else
            mu = p/4;
            if mu > 0
                b = sqrt(mu); x = linspace(-b,2*b,150);
                y = mu*x-x.^3/3+2*mu^(3/2)/3;
                plot([-1.1 -b],[0 0],'Color',green,'LineWidth',3);
                plot([2*b 1.1],[0 0],'Color',green,'LineWidth',3);
            else
                x = [-1.1 1.1]; y = [0 0];
                plot(x,y,'Color',green,'LineWidth',3);
            end
        end
        plot(x,y,styles{j},'LineWidth',1.3);
    end
    names = {'Crossing-sliding','Grazing-sliding',...
        'Switching-sliding','Adding-sliding'};
    title(names{panel}); xlabel('x'); ylabel('y');
    if panel == 4, xlabel('s'); ylim([-.015 .04]);
    elseif panel == 2, ylim([-.1 .8]); else, ylim([-.4 .65]); end
    xlim([-1.1 1.1]); grid on;
    set(gca,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'TitleFontSizeMultiplier',1);
end
set(f,'PaperUnits','centimeters','PaperSize',[16 17],...
    'PaperPosition',[0 0 16 17]);
print(f,fullfile(root,'graphics_v3/sliding_geometries.pdf'),'-dpdf');
print(f,fullfile(root,'graphics_svg/sliding_geometries.svg'),'-dsvg');
