function pts = fold_pal_v3
% Equilibria of xdot=mu-x^2: follow both branches through the fold.
G=@(y) y(2)-y(1)^2; % y=[x;mu]
pts=[1,0.95;1,0.95^2];
for j=3:45
    pts(:,j)=pal_corrector_v3(G,pts(:,j-1),pts(:,j-2),0.06);
end
plot(pts(2,:),pts(1,:),'.-'); grid on
xlabel('mu'); ylabel('x');
end
