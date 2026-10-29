"""Analytic reference checks for simplified examples; does not run MATLAB."""
import numpy as np
from math import pi, sqrt
# Vertical launch: both endpoint data and the free-time solution.
g, h = 9.81, 1.
T = sqrt(2*h/g); v0 = g*T
assert abs(v0*T-g*T*T/2-h)<1e-14
assert abs(v0-g*T)<1e-14
assert 1<v0<8 and 8/g<2
print(f'PASS: launch reference T={T:.9f}, v0={v0:.9f}; shooting bracket valid')
# Independent RK4 integration of each physical-time half wave.
for kp,km,V in [(4.,1.,1.),(2.,7.,.3)]:
    z=np.array([0.,V])
    for k in [kp,km]:
        dt=pi/sqrt(k)/2000
        rhs=lambda x:np.array([x[1],-k*x[0]])
        for _ in range(2000):
            a=rhs(z); b=rhs(z+dt*a/2); c=rhs(z+dt*b/2); d=rhs(z+dt*c)
            z+=dt*(a+2*b+2*c+d)/6
        assert abs(z[0])<1e-10
    assert np.max(abs(z-[0,V]))<1e-10
print('PASS: two-stiffness trajectory closes with continuous velocity and stated period')
# Solve the complete augmented curve, independently using an analytic Jacobian.
pts=[np.array([1.,1.]),np.array([.95,.95**2])]
for _ in range(43):
    tangent=pts[-1]-pts[-2]; tangent/=np.linalg.norm(tangent)
    pred=pts[-1]+.06*tangent; z=pred.copy()
    for _ in range(8):
        residual=np.array([z[1]-z[0]**2,tangent@(z-pred)])
        z-=np.linalg.solve(np.vstack(([-2*z[0],1],tangent)),residual)
    assert abs(z[1]-z[0]**2)<1e-12
    pts.append(z)
assert pts[-1][0]<0 and pts[-1][1]>min(z[1] for z in pts)
print('PASS: specified continuation steps pass the fold and reach the unstable branch')
# Local impact geometry: root/time/speed and restitution correction.
for eps in [1e-5,1e-3]:
    dt=-sqrt(2*eps)
    assert abs(-eps+dt*dt/2)<1e-15
    jump=1.8*sqrt(2*eps)
    assert abs(jump-(-.8*dt-dt))<1e-14
print('PASS: grazing motivation and square-root velocity scaling')
