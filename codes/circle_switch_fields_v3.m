function circle_switch_fields_v3
% H=1-x1^2-x2^2; F1=[x1;-x2] inside, F2=[1;-x1] outside.
[x,y]=meshgrid(linspace(-1.5,1.5,17));
r=hypot(x,y);
figure; hold on
for inside=[true,false]
    if inside
        u=x; v=-y; mask=r<0.88; color=[0.81,0.22,0.22];
    else
        u=ones(size(x)); v=-x; mask=r>1.12; color=[0.1,0.46,0.73];
    end
    speed=hypot(u,v); mask=mask & speed>0;
    quiver(x(mask),y(mask),0.13*u(mask)./speed(mask),...
        0.13*v(mask)./speed(mask),0,'Color',color);
end
t=linspace(0,2*pi,501); plot(cos(t),sin(t),'k--'); plot(0,0,'ko');
axis equal; axis([-1.65,1.65,-1.65,1.65]); xlabel('x_1'); ylabel('x_2');
end
