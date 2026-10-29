function spring_continuation_v3
% Reduced pseudo-arclength continuation; each period comes from bvp5c.
for mode=1:2
    if mode==1, mu0=2; ds=0.5; name='spring_k'; lab='k [N/m]';
    else, mu0=1; ds=1; name='spring_m'; lab='m [kg]'; end
    z0=[mu0;period(mu0,mode)]; z1=[mu0+0.05;period(mu0+0.05,mode)];
    Z=[z0,z1];
    for n=1:30
        v=(z1-z0)/norm(z1-z0); p=z1+ds*v; z=p;
        for j=1:8
            h=1e-4*max(1,z(1));
            g=[period(z(1),mode)-z(2);v'*(z-p)];
            if norm(g,inf)<1e-9, break; end
            d=(period(z(1)+h,mode)-period(z(1)-h,mode))/(2*h);
            z=z-[d,-1;v']\g;
        end
        assert(norm(g,inf)<1e-9,'Corrector did not converge.');
        Z(:,end+1)=z; z0=z1; z1=z;
    end
    mu=linspace(Z(1,1),Z(1,end),301);
    if mode==1
        exact=2*pi*sqrt(5./mu); check=2*pi*sqrt(5./Z(1,:));
    else
        exact=2*pi*sqrt(mu/10); check=2*pi*sqrt(Z(1,:)/10);
    end
    fprintf('%s: max period error = %.3g s\n',name,max(abs(Z(2,:)-check)));
    f=figure('Color','w','Units','centimeters','Position',[2,2,16,9]);
    plot(mu,exact,'LineWidth',1.3); hold on
    plot(Z(1,:),Z(2,:),'o','MarkerSize',4,'MarkerFaceColor','w');
    ax=gca; set(ax,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'Box','off','GridAlpha',0.15);
    xlabel(lab); ylabel('T [s]'); grid on
    legend('Analitikus','BVP + pseudo-arclength continuation','Location','best',...
        'FontName','Times New Roman','FontSize',11,'Box','off');
    savefigure(f,name,[16,9]);
end
end

function T=period(mu,mode)
if mode==1, k=mu; m=5; else, k=10; m=mu; end
w=sqrt(k/m);
rhs=@(~,y,q) q*[y(2);-w*w*y(1)];
bc=@(a,b,~) [a(1)-1;a(2);b(1)];
guess=@(s) [cos(pi*s/2);-w*sin(pi*s/2)];
init=bvpinit(linspace(0,1,21),guess,0.98*pi/(2*w));
sol=bvp5c(rhs,bc,init,bvpset('RelTol',1e-9,'AbsTol',1e-11));
T=4*sol.parameters;
end

function savefigure(f,name,sz)
root=fileparts(fileparts(mfilename('fullpath')));
set(f,'PaperUnits','centimeters','PaperSize',sz,...
    'PaperPosition',[0,0,sz],'PaperPositionMode','manual');
for item={'graphics_v3','graphics_svg'}
    folder=fullfile(root,item{1}); if ~isfolder(folder), mkdir(folder); end
end
print(f,fullfile(root,'graphics_v3',[name,'.pdf']),'-dpdf','-vector');
print(f,fullfile(root,'graphics_svg',[name,'.svg']),'-dsvg','-vector');
end
