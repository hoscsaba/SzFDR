function circle_sliding_fields_v3
% Same fields as Figure 2.1; attracting sliding on the left arc.
circle_switch_fields_v3;
t=linspace(3*pi/4,5*pi/4,201);
plot(cos(t),sin(t),'Color',[0.1,0.51,0.29],'LineWidth',3);
plot(cos(t([1,end])),sin(t([1,end])),'ko','MarkerFaceColor','w');
t=[0.83,1,1.17]*pi; x=cos(t); y=sin(t);
l1=2*(y.^2-x.^2); l2=2*x.*(y-1); a=l1./(l1-l2);
u=(1-a).*x+a; v=-(1-a).*y-a.*x; speed=hypot(u,v);
quiver(x,y,0.2*u./speed,0.2*v./speed,0,'Color',[0.1,0.51,0.29]);
end
