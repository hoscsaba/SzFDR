function friction_regularization_v3
% Ideal versus tanh friction: braking and creep, m=F=1.
widths=[0.1,0.03,0.01]; colors=lines(3);
opts=odeset('RelTol',1e-10,'AbsTol',1e-12);
t=linspace(0,2,2001); ideal=max(1-t,0);
f=canvas; a1=nexttile; hold on; a2=nexttile; hold on
plot(a1,t,ideal,'k--','LineWidth',1.5,'DisplayName','Idealis');
for j=1:3
    e=widths(j);
    sol=ode15s(@(~,v)-tanh(v/e),[0,2],1,opts);
    v=deval(sol,t); exact=e*asinh(sinh(1/e)*exp(-t/e));
    label=sprintf('epsilon = %g',e);
    plot(a1,t,v,'Color',colors(j,:),'LineWidth',1.2,'DisplayName',label);
    plot(a2,t,v-ideal,'Color',colors(j,:),'LineWidth',1.2,'DisplayName',label);
    fprintf('Braking e=%g: ODE error %.3g, max speed error %.6g\n',...
        e,max(abs(v-exact)),max(abs(v-ideal)));
    assert(max(abs(v-exact))<1e-7);
end
style(a1,'v'); style(a2,'v_{epsilon}-v_{ideal}');
xlim(a2,[0.7,1.3]); xlabel(a2,'t');
legend(a1,'show','Location','northeast','FontSize',11,...
    'FontName','Times New Roman','Box','off');
savefigure(f,'regularization_braking');

% At q=1/2 the ideal solution stays at x=v=0.
t=unique([linspace(0,1,301),linspace(1,100,501)]);
f=canvas; a1=nexttile; hold on; a2=nexttile; hold on
for ax=[a1,a2]
    plot(ax,[0,100],[0,0],'k--','LineWidth',1.5,'DisplayName','Idealis');
end
for j=1:3
    e=widths(j); rhs=@(~,y)[y(2);0.5-tanh(y(2)/e)];
    sol=ode15s(rhs,[0,100],[0;0],opts); y=deval(sol,t);
    label=sprintf('epsilon = %g',e);
    plot(a1,t,y(2,:),'Color',colors(j,:),'LineWidth',1.2,'DisplayName',label);
    plot(a2,t,y(1,:),'Color',colors(j,:),'LineWidth',1.2,'DisplayName',label);
    fprintf('Creep e=%g: v(100)=%.8g, x(100)=%.8g\n',e,y(2,end),y(1,end));
    assert(abs(y(2,end)-e*atanh(0.5))<1e-8);
end
style(a1,'v'); style(a2,'x'); xlim(a1,[0,1]); xlabel(a2,'t');
legend(a2,'show','Location','northwest','FontSize',11,...
    'FontName','Times New Roman','Box','off');
savefigure(f,'regularization_creep');
end

function f=canvas
f=figure('Color','w','Units','centimeters','Position',[2,2,16,12]);
tiledlayout(2,1,'TileSpacing','compact','Padding','compact');
end
function style(ax,lab)
set(ax,'FontName','Times New Roman','FontSize',11,...
    'LabelFontSizeMultiplier',1,'Box','off','GridAlpha',0.15);
ylabel(ax,lab); xlabel(ax,'t'); grid(ax,'on');
end
function savefigure(f,name)
root=fileparts(fileparts(mfilename('fullpath')));
set(f,'PaperUnits','centimeters','PaperSize',[16,12],...
    'PaperPosition',[0,0,16,12],'PaperPositionMode','manual');
for item={'graphics_v3','graphics_svg'}
    folder=fullfile(root,item{1}); if ~isfolder(folder), mkdir(folder); end
end
print(f,fullfile(root,'graphics_v3',[name,'.pdf']),'-dpdf','-vector');
print(f,fullfile(root,'graphics_svg',[name,'.svg']),'-dsvg','-vector');
end
