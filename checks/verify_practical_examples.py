"""Independent reference checks; does not execute MATLAB solvers."""
import numpy as np
from math import sqrt, pi, atan, atanh
# Energy, bounce accumulation and exact remaining-time bound.
g,r,h=9.81,.7,1.; V=sqrt(2*g*h); t1=V/g; Tz=t1*(1+r)/(1-r)
for n in [1,2,8,30]:
    tn=t1+sum(2*r**j*V/g for j in range(1,n))
    u=r**n*V
    assert abs(Tz-tn-2*u/(g*(1-r)))<2e-15
    assert abs((r*u)**2/u**2-r**2)<1e-15
print('PASS: bounce energy ratio, Zeno time and truncation bound')
# Independently integrate the slipping ODE to its stated terminal time.
U,Fs,Fk=.3,.6,.4; Tl=2*pi-2*atan((Fs-Fk)/U)
z=np.array([Fs,U]);dt=Tl/4000; velocities=[]
def f(z):return np.array([z[1],-z[0]+Fk])
for j in range(4000):
    a=f(z);b=f(z+dt*a/2);c=f(z+dt*b/2);d=f(z+dt*c)
    z+=dt*(a+2*b+2*c+d)/6
    velocities.append(z[1])
assert np.max(abs(z-[2*Fk-Fs,U]))<1e-11
assert max(velocities[:-1])<U and abs(z[0])<Fs
print('PASS: stick/slip return, correct slip direction, admissible reattachment')
# Border collision branch admissibility and two-step multiplier.
def P(x,mu):return mu+(.5*x if x<=0 else -1.5*x)
for mu in [-.2,-.01]:assert abs(P(2*mu,mu)-2*mu)<1e-14
for mu in [.01,.2]:
    L,R=-2*mu/7,6*mu/7
    assert L<0<R and abs(P(L,mu)-R)<1e-14 and abs(P(R,mu)-L)<1e-14
    step=1e-7
    multiplier=(P(P(L+step,mu),mu)-P(P(L-step,mu),mu))/(2*step)
    assert abs(multiplier+.75)<1e-9
print('PASS: border-collision fixed points and stable admissible two-cycle')
# Sliding mixture and entry point for y=x*x/2+c.
for x in [-.8,-.1]:
    alpha=x/(x-1)
    assert 0<alpha<1 and abs((1-alpha)*x+alpha)<1e-15
c=-.18;entry=-sqrt(-2*c)
assert abs(entry**2/2+c)<1e-15
print('PASS: attracting sliding field and entry geometry')
# Smoothed friction stationary velocity and elastic-contact restitution.
for eps in [.2,.05,.01]:
    v=eps*atanh(.5)
    assert abs(.5-np.tanh(v/eps))<1e-14
for K in [100,10000]:
    w=sqrt(K);tc=pi/w
    assert abs(V/w*np.sin(w*tc))<1e-14
    assert abs(V*np.cos(w*tc)+V)<1e-14
print('PASS: creep equilibrium and elastic contact gives restitution one')
