function phase_portraits_v3
% The five linear phase portraits used in Section 1.1.
A={diag([-1,1]),diag([-1,-2]),diag([1,2]),...
   [-0.35,-1;1,-0.35],[0.35,-1;1,0.35]};
names={'Saddle','Stable node','Unstable node','Stable focus','Unstable focus'};
[x,y]=meshgrid(linspace(-2,2,41));
figure; tiledlayout(3,2);
for j=1:5
    nexttile;
    u=A{j}(1,1)*x+A{j}(1,2)*y;
    v=A{j}(2,1)*x+A{j}(2,2)*y;
    streamslice(x,y,u,v); hold on; plot(0,0,'ko','MarkerFaceColor','k');
    axis equal; axis([-2,2,-2,2]); grid on
    xlabel('y_1'); ylabel('y_2'); title(names{j});
end
end
