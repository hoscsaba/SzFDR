"""P2/P3 independent mathematical and source checks. Run from repository root."""
from pathlib import Path
from collections import Counter
import re
import numpy as np
ROOT=Path.cwd()
# Hessian contribution: H=x^2+y^2-1, xdot=(x,2y).
x=np.array([.7,.4]); F=np.array([x[0],2*x[1]])
Hx=2*x; Hess=2*np.eye(2); Fx=np.diag([1.,2.])
a=F@Hess@F+Hx@Fx@F
h=1e-4
def height(t): return x[0]**2*np.exp(2*t)+x[1]**2*np.exp(4*t)-1
assert abs(a-(height(h)-2*height(0)+height(-h))/h**2)<1e-7
print('PASS: normal acceleration including Hessian contribution')
# Projection onto a section along the vector field.
F=np.array([0.,2.,1.]); n=np.array([0.,1.,0.])
P=np.eye(3)-np.outer(F,n)/(n@F)
assert np.allclose(P@P,P) and np.allclose(n@P,0) and np.allclose(P@F,0)
print('PASS: Poincare projection is idempotent and removes time-shift direction')
# Full augmented continuation crosses the fold mu=x^2.
yold=np.array([.3,.09]); yi=np.array([.2,.04]); ds=.3
v=(yi-yold)/np.linalg.norm(yi-yold); yp=yi+ds*v; y=yp.copy()
for _ in range(12):
    res=np.array([y[1]-y[0]**2,v@(y-yp)])
    J=np.array([[-2*y[0],1.],v])
    y-=np.linalg.solve(J,res)
assert y[0]<0 and abs(y[1]-y[0]**2)<1e-12 and abs(v@(y-yp))<1e-12
print('PASS: full pseudo-arclength corrector crosses a fold without component division')
# Energy derivative for SLIP stance using physical velocities.
g,kappa,l0=9.81,112.5,1.; q=np.array([-.3,.8]); vel=np.array([2.,-.4])
ell=np.linalg.norm(q); force=kappa*(l0/ell-1)*q+np.array([0.,-g])
Edot=vel@force+g*vel[1]-kappa*(l0-ell)*(q@vel)/ell
assert abs(Edot)<1e-12
print('PASS: SLIP energy conservation with physical-time velocities')
# Scalar impacting-branch fixed point: retain admissibility and derivative.
for nu in [.15,.6,.8,.9]:
 for mu in [.001,.1,.3]:
    fixed=2*mu/(1+np.sqrt(1+4*(1-nu)**2*mu))
    assert 0<fixed<mu
    assert abs(nu*fixed+np.sqrt(mu-fixed)-fixed)<1e-12
print('PASS: scalar fixed points satisfy the equation and branch conditions')
# Vector Nordmark derivative on the impacting branch.
N=np.array([[.3,.1],[.2,.4]]); E=np.array([.7,-.2]); c=np.array([1.,-.5])
x=np.array([-.4,-.2]); offset=-.1
hfun=lambda q: c@N@q+offset
f=lambda q:N@q+E*np.sqrt(-hfun(q))
J=N-np.outer(E,c@N)/(2*np.sqrt(-hfun(x)))
delta=1e-6
FD=np.column_stack([(f(x+delta*e)-f(x-delta*e))/(2*delta) for e in np.eye(2)])
assert np.max(abs(J-FD))<1e-9
print('PASS: vector Nordmark derivative matches finite differences')
# All local document dependencies, references and citations.
main=(ROOT/'SzFDR_jegyzet_v3.tex').read_text()
paths=[ROOT/(n+'.tex') for n in re.findall(r'\\input\{([^}]+)\}',main)]
assert len(paths)==9 and len(set(paths))==9
alltext=main+'\n'+'\n'.join(p.read_text() for p in paths)
labels=re.findall(r'\\label\{([^}]+)\}',alltext)
for block in re.findall(r'\\lstinputlisting\[([\s\S]*?)\]\{',alltext):
 labels.extend(re.findall(r'\blabel\s*=\s*\{([^}]+)\}',block))
assert not [k for k,n in Counter(labels).items() if n>1]
refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',alltext))
assert not refs-set(labels), refs-set(labels)
cites=set(re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',alltext))
keys=set(re.findall(r'\\bibitem\{([^}]+)\}',alltext))
assert not cites-keys
assert not re.search(r'\\sum(?![A-Za-z_])|textvisiblespace|nincs kész|ide esetleg',alltext)
for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',alltext):
 path=ROOT/name
 assert path.exists() or any(path.with_suffix(e).exists() for e in ['.pdf','.png','.jpg']),name
for name in re.findall(r'\\lstinputlisting(?:\[[^\]]*\])?\{([^}]+)\}',alltext):
 assert (ROOT/name).is_file(),name
for name in ['sr_m01','sr_01','bif_08','bif_06','bif_015']:
 assert (ROOT/'graphics_v3'/(name+'.pdf')).is_file()
print('PASS: unique labels, resolved references/citations, all graphics and code files present')
