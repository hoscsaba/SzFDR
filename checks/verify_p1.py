"""Independent mathematical and source checks; requires Python 3 and NumPy.
Does not execute MATLAB. Run from the SzFDR repository root.
"""
from pathlib import Path
from collections import defaultdict
import re
import numpy as np
from math import sin,cos,sqrt,exp,pi
ROOT=Path.cwd()

def transition(z,t):
    L=np.array([[0.,1.],[-1.,-2*z]])
    val,V=np.linalg.eig(L)
    return np.real_if_close(V@np.diag(np.exp(t*val))@np.linalg.inv(V)).real

def printed_transition(z,t):
    w=sqrt(1-z*z); c=cos(w*t); s=sin(w*t)/w
    return exp(-z*t)*np.array([[c+z*s,s],[-s,c-z*s]])

for z in [0.,.05,.2,.9]:
    for t in [0.,.4,2.3]:
        N=printed_transition(z,t)
        assert np.allclose(N,transition(z,t),atol=1e-12)
        assert abs(np.linalg.det(N)-exp(-2*z*t))<1e-12
    h=1e-6
    assert np.max(abs((printed_transition(z,h)-printed_transition(z,-h))/(2*h)
                      -np.array([[0,1],[-1,-2*z]])))<1e-9
print('PASS: N(0)=I, N\'(0)=L, exp(Lt), Liouville determinant')

# Evaluate the stated Folkers X, checking X'=A X independently by differences.
def X(t):
    g=exp(t+sin(t))
    return np.array([[g,exp(-t)],[g*(2+cos(t)),0.]])
for t in [.1,1.2,3.]:
    A=np.array([[-1,1],[0,1+cos(t)-sin(t)/(2+cos(t))]])
    h=1e-6
    assert np.allclose((X(t+h)-X(t-h))/(2*h),A@X(t),rtol=1e-8,atol=1e-8)
C=np.linalg.solve(X(0),X(2*pi))
assert np.allclose(C,np.diag([exp(2*pi),exp(-2*pi)]),atol=1e-10)
print('PASS: Folkers fundamental solution and corrected multipliers')

# The unit-cycle variational system is verified by integrating its Jacobian.
def jac(t):
    x,y=cos(t),sin(t)
    return np.array([[1-3*x*x-y*y,-1-2*x*y],[1-2*x*y,1-x*x-3*y*y]])
M=np.eye(2); n=16000; h=2*pi/n
for j in range(n):
    t=j*h; k1=jac(t)@M; k2=jac(t+h/2)@(M+h*k1/2)
    k3=jac(t+h/2)@(M+h*k2/2); k4=jac(t+h)@(M+h*k3)
    M+=h*(k1+2*k2+2*k3+k4)/6
assert np.max(abs(M-np.diag([exp(-4*pi),1.])))<1e-10
print('PASS: unit-cycle monodromy by independent RK4 integration')

# Verify sliding inequalities on either side of Dk=Pm and at equality.
for P,D,m,k in [(.3,.2,.7,.1),(.01,.2,.7,.1),(.02,.2,1.,.1)]:
    cap=D*.5
    for v in [-1.,-.2,0.,.2,1.]:
        actual=((D*k-P*m)*v-cap<0 and (D*k-P*m)*v+cap>0)
        assert actual == (abs((D*k-P*m)*v)<cap)
assert abs(.2*.5/abs(.2*.1-.3*.7)-.5263157894736842)<1e-14
print('PASS: sliding signs, both denominator signs and degenerate case')

# Full impact map: exact forced flights, event bisection, saltation derivative.
z=.05; w=3.; r=.8; wall=0.; L=np.array([[0.,1.],[-1.,-2*z]])
val,V=np.linalg.eig(L); Vi=np.linalg.inv(V)
def N(t): return (V@np.diag(np.exp(t*val))@Vi).real
D=(1-w*w)**2+(2*z*w)**2; a=(1-w*w)/D; b=2*z*w/D
def particular(t): return np.array([a*cos(w*t)+b*sin(w*t),-a*w*sin(w*t)+b*w*cos(w*t)])
def flight(y,ta,tb): return particular(tb)+N(tb-ta)@(y-particular(ta))
def impact_map(y,tf=2*pi/w):
    y=np.array(y,float); ta=0.; P=np.eye(2); count=0
    while ta<tf-1e-12:
        tb=ta; yl=y.copy(); hit=False
        while tb<tf:
            tn=min(tb+.01,tf); yn=flight(y,ta,tn)
            if yl[0]>wall and yn[0]<=wall:
                lo,hi=tb,tn
                for _ in range(48):
                    mid=(lo+hi)/2
                    if flight(y,ta,mid)[0]>wall: lo=mid
                    else: hi=mid
                ti=(lo+hi)/2; ym=flight(y,ta,ti)
                assert ym[1]<-1e-8
                vp=-r*ym[1]; am=-2*z*ym[1]+cos(w*ti)
                ap=-2*z*vp+cos(w*ti)
                S=np.array([[-r,0.],[(ap+r*am)/ym[1],-r]])
                P=S@N(ti-ta)@P
                y=np.array([wall,vp]); ta=ti; count+=1; hit=True
                assert count<100
                break
            tb=tn; yl=yn
        if not hit:
            return flight(y,ta,tf),N(tf-ta)@P,count
    return y,P,count
start=np.array([1.,0.]); end,M,count=impact_map(start)
assert count>0
h=1e-5
FD=np.column_stack([(impact_map(start+h*e)[0]-impact_map(start-h*e)[0])/(2*h)
                    for e in np.eye(2)])
error=np.max(abs(M-FD))
assert error<2e-7
assert abs(np.linalg.det(M)-exp(-2*z*2*pi/w)*r**(2*count))<1e-10
print(f'PASS: {count} transverse impacts, saltation vs finite difference error {error:.3e}')

# Quarter-period shooting residual: three unknowns x(0),v(0),Q.
A0=1.; w0=sqrt(2.); Q=pi/(2*w0)
def residual(p):
    x,v,q=p
    return np.array([x-A0,v,x*cos(w0*q)+v/w0*sin(w0*q)])
p=np.array([A0,0.,Q]); h=1e-6
J=np.column_stack([(residual(p+h*e)-residual(p-h*e))/(2*h) for e in np.eye(3)])
assert np.linalg.norm(residual(p))<1e-14 and abs(np.linalg.det(J))>1.
assert abs(4*Q-2*pi/w0)<1e-14
print('PASS: quarter-period BVP residual and nonsingular shooting Jacobian')

main=(ROOT/'SzFDR_jegyzet_v3.tex').read_text()
chapters=[ROOT/(x+'.tex') for x in re.findall(r'\\input\{([^}]+)\}',main)]
assert len(chapters)==9 and len(set(chapters))==9
labels=defaultdict(list); refs=set()
for p in chapters:
    active='\n'.join(line for line in p.read_text().splitlines() if not line.lstrip().startswith('%'))
    for label in re.findall(r'\\label\{([^}]+)\}',active): labels[label].append(p.name)
    for block in re.findall(r'\\lstinputlisting\[([\s\S]*?)\]\{',active):
        for label in re.findall(r'\blabel\s*=\s*\{([^}]+)\}',block): labels[label].append(p.name)
    refs.update(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',active))
assert not {k:v for k,v in labels.items() if len(v)>1}
assert not refs-labels.keys(),refs-labels.keys()
print('PASS: nine unique document inputs, unique labels and resolved references')
print('NOTE: MATLAB/bvp5c/ode45 code was not executed in this environment.')
