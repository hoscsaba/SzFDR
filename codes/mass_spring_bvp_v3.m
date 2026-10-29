function [T,sol] = mass_spring_bvp_v3(k,m,x0)
% First-quarter BVP and symmetry reconstruction; k, m, x0 > 0.
if nargin<1, k=10; end
if nargin<2, m=5; end
if nargin<3, x0=1; end
w = sqrt(k/m);
Qguess = 0.98*pi/(2*w);
guess = @(s) [x0*cos(pi*s/2);-x0*w*sin(pi*s/2)];
init = bvpinit(linspace(0,1,21),guess,Qguess);
opts = bvpset('RelTol',1e-9,'AbsTol',1e-11,'NMax',5000);
sol = bvp5c(@rhs,@bcs,init,opts);
Q = sol.parameters(1); T = 4*Q;
Y = deval(sol,linspace(0,1,201));
assert(Q>0 && Y(2,end)<0 && all(Y(1,1:end-1)>0),...
    'The solution must cover the first quarter period.');
fprintf('T = %.10g, exact = %.10g\n',T,2*pi/w);
% Reconstruct a full period from the numerical quarter period.
tau=linspace(0,1,401); q=min(floor(4*tau),3); s=4*tau-q;
s(mod(q,2)==1)=1-s(mod(q,2)==1);
y=deval(sol,s); sx=[1,-1,-1,1]; sv=[1,1,-1,-1];
y=y.*[sx(q+1);sv(q+1)];
exact=[x0*cos(w*T*tau);-x0*w*sin(w*T*tau)];
fprintf('Max errors: x=%.3g, v=%.3g\n',max(abs(y-exact),[],2));
f=figure('Color','w','Units','centimeters','Position',[2,2,16,12]);
tl=tiledlayout(f,2,1,'TileSpacing','compact','Padding','compact');
labels={'x [m]','v [m/s]'}; marks=1:16:numel(tau);
for j=1:2
    ax=nexttile(tl); hold(ax,'on');
    plot(tau,exact(j,:),'Color',[0.12,0.35,0.65],'LineWidth',1.3);
    plot(tau(marks),y(j,marks),'o','Color',[0.8,0.3,0.1],...
        'MarkerSize',4,'MarkerFaceColor','w','LineWidth',0.9);
    set(ax,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'Box','off','TickDir','out',...
        'XLim',[0,1],'XTick',0:0.25:1,'GridAlpha',0.15);
    grid on; ylabel(labels{j});
    if j==1
        legend('Analitikus','BVP + szimmetria',...
            'Location','southoutside','Orientation','horizontal',...
            'FontName','Times New Roman','FontSize',11,'Box','off');
    end
end
xlabel('t/T');
% Fixed physical size keeps 11 pt lettering in the LaTeX document.
set(f,'PaperUnits','centimeters','PaperSize',[16,12],...
    'PaperPosition',[0,0,16,12],'PaperPositionMode','manual');
root=fileparts(fileparts(mfilename('fullpath')));
pdfdir=fullfile(root,'graphics_v3'); svgdir=fullfile(root,'graphics_svg');
if ~isfolder(pdfdir), mkdir(pdfdir); end
if ~isfolder(svgdir), mkdir(svgdir); end
print(f,fullfile(pdfdir,'mass_spring_bvp.pdf'),'-dpdf','-vector');
print(f,fullfile(svgdir,'mass_spring_bvp.svg'),'-dsvg','-vector');

    function dY = rhs(~,Y,p)
        dY = p(1)*[Y(2);-w^2*Y(1)];
    end
    function res = bcs(ya,yb,~)
        res = [ya(1)-x0;ya(2);yb(1)];
    end
end
