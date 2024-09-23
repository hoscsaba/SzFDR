function pseudoivhossz_pelda

	clear all, close all, clc

	global y1_frozen v y_prev h

	h=0.1;

	y0_1=0.2; y1_frozen=y0_1; y0_2=fzero(@G2,0);
	y1_1=h; y1_frozen=y1_1; y1_2=fzero(@G2,y0_2);

	pts=[y0_1 y0_2;y1_1 y1_2];

	figure(1)
	plot(pts(:,1),pts(:,2),'r*'), grid on, hold on, axis equal

	for i=1:300
		v=pts(end,:)-pts(end-1,:);
		v=v/norm(v);

		y_prev=pts(end,:);
		y_pred=pts(end,:)+h*v;
		ynew=fsolve(@G_PAC,y_pred)
		pts=[pts;ynew];
		
		plot(ynew(1),ynew(2),'r*'), hold on, drawnow
	end
end

function out = G(y)
	%out=y(1)^2+y(2)^2-1;
	out=sin(y(1))+sin(y(2))-0.01;
end

function out = G2(y2)
	global y1_frozen
	out=G([y1_frozen,y2]);
end

function out = G_PAC(y)
	global v y_prev h
	out(1,1)=G(y);
	out(2,1)=dot(y-y_prev,v)-h;
end