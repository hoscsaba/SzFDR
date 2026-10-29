"""Independent algebra checks for the expanded equilibrium section."""
import numpy as np
from math import exp, cos, sin
A=np.array([[-1.,1.],[0.,-2.]])
S=np.array([[1.,-1.],[0.,1.]])
assert np.allclose(np.linalg.solve(S,A@S),np.diag([-1.,-2.]))
assert not np.allclose(S.T@S,np.eye(2))
P=np.array([[.5,1/6],[1/6,1/3]])
assert np.min(np.linalg.eigvalsh(P))>0
assert np.allclose(A.T@P+P@A,-np.eye(2))
print('PASS: nonorthogonal eigenbasis and positive-definite Lyapunov solution')
for alpha in [-.35,.35]:
    B=np.array([[alpha,-1.],[1.,alpha]])
    vals,V=np.linalg.eig(B)
    for t in [.3,2.]:
        E=(V@np.diag(np.exp(vals*t))@np.linalg.inv(V)).real
        expected=exp(alpha*t)*np.array([[cos(t),-sin(t)],[sin(t),cos(t)]])
        assert np.allclose(E,expected)
        assert np.allclose(E.T@E,exp(2*alpha*t)*np.eye(2))
    v=V[:,np.argmax(vals.imag)]
    realbasis=np.column_stack((v.real,-v.imag))
    assert np.allclose(np.linalg.solve(realbasis,B@realbasis),B)
print('PASS: complex eigenvectors yield the stated real rotation/dilation block')
for lam in [-1.,0.]:
    J=np.array([[lam,1.],[0.,lam]])
    for t in [.1,2.]:
        E=exp(lam*t)*np.array([[1.,t],[0.,1.]])
        dE=lam*E+exp(lam*t)*np.array([[0.,1.],[0.,0.]])
        assert np.allclose(dE,J@E)
print('PASS: Jordan exponential, including the nilpotent unstable boundary case')
for A in [np.diag([-1.,1.]),np.diag([-1.,-2.]),np.diag([1.,2.]),
          np.array([[-.35,-1.],[1.,-.35]]),np.array([[.35,-1.],[1.,.35]])]:
    lam=np.linalg.eigvals(A);tau=np.trace(A);delta=np.linalg.det(A)
    assert np.allclose(lam**2-tau*lam+delta,0)
print('PASS: all five portrait matrices satisfy the stated planar characteristic equation')
