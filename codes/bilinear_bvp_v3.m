function [T,sol] = bilinear_bvp_v3
% Two half cycles: x''=-kp*x for x>0, x''=-km*x for x<0; mass=1.
kp=4; km=1; V=1;
wp=sqrt(kp); wm=sqrt(km);
guess=@(s) [V/wp*sin(pi*s);V*cos(pi*s);...
            -V/wm*sin(pi*s);-V*cos(pi*s)];
init=bvpinit(linspace(0,1,21),guess,0.98*[pi/wp,pi/wm]);
sol=bvp5c(@rhs,@bcs,init,bvpset('RelTol',1e-8,'AbsTol',1e-10));
d=sol.parameters; T=sum(d);
s=linspace(0,1,201); y=deval(sol,s);
assert(all(d>0) && all(y(1,2:end-1)>0) && all(y(3,2:end-1)<0),...
    'Choose the first positive and negative half cycles.');
fprintf('T=%.8f, exact=%.8f\n',T,pi/wp+pi/wm);
% Join the two numerical half cycles without duplicating the junction.
time=[d(1)*s,d(1)+d(2)*s(2:end)];
Y=[y(1:2,:),y(3:4,2:end)];
exact=[V/wp*sin(wp*time);V*cos(wp*time)];
idx=time>d(1); tm=time(idx)-d(1);
exact(:,idx)=[-V/wm*sin(wm*tm);-V*cos(wm*tm)];
fprintf('Max state error=%.3g; closure error=%.3g\n',...
    max(abs(Y-exact),[],'all'),norm(Y(:,end)-[0;V]));
f=figure('Color','w','Units','centimeters','Position',[2,2,16,12]);
tl=tiledlayout(2,1,'TileSpacing','compact','Padding','compact');
labels={'x','v'}; marks=1:16:numel(time);
for j=1:2
    ax=nexttile(tl); plot(time,exact(j,:),'LineWidth',1.3); hold on
    plot(time(marks),Y(j,marks),'o','MarkerSize',4,'MarkerFaceColor','w');
    xline(d(1),'--','T_+','LabelVerticalAlignment','bottom',...
        'HandleVisibility','off','FontName','Times New Roman','FontSize',11);
    set(ax,'FontName','Times New Roman','FontSize',11,...
        'LabelFontSizeMultiplier',1,'Box','off','GridAlpha',0.15);
    ylabel(labels{j}); grid on
    if j==1
        legend('Analitikus','Ket szegmens BVP',...
            'Location','southoutside','Orientation','horizontal',...
            'FontName','Times New Roman','FontSize',11,'Box','off');
    end
end
xlabel('t');
set(f,'PaperUnits','centimeters','PaperSize',[16,12],...
    'PaperPosition',[0,0,16,12],'PaperPositionMode','manual');
root=fileparts(fileparts(mfilename('fullpath')));
for item={'graphics_v3','graphics_svg'}
    folder=fullfile(root,item{1}); if ~isfolder(folder), mkdir(folder); end
end
print(f,fullfile(root,'graphics_v3','bilinear_bvp.pdf'),'-dpdf','-vector');
print(f,fullfile(root,'graphics_svg','bilinear_bvp.svg'),'-dsvg','-vector');
    function dy=rhs(~,y,d)
        dy=[d(1)*[y(2);-kp*y(1)];d(2)*[y(4);-km*y(3)]];
    end
    function r=bcs(a,b,~)
        r=[a(1);a(2)-V;b(1);a(3)-b(1);a(4)-b(2);b(3)];
    end
end
