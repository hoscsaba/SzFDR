"""Regenerate v3 square-root figures. Requires NumPy, pdflatex and pgfplots.
Run from the repository root: python3 codes/square_root_figures_v3.py
The PDF figures use vector graphics; data and intermediate TeX stay in graphics_v3.
"""
from pathlib import Path
import subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'graphics_v3'; OUT.mkdir(exist_ok=True)

def step(x,nu,mu): return nu*x+np.sqrt(np.maximum(mu-x,0.))
def figure(name,plots,options):
    source=(r'\documentclass[tikz,border=3pt]{standalone}'+'\n'
        +r'\usepackage{pgfplots}\pgfplotsset{compat=1.18}'+'\n'
        +r'\begin{document}\begin{tikzpicture}\begin{axis}['
        +r'width=9cm,height=6cm,grid=major,grid style={gray!15},'
        +r'tick label style={font=\fontsize{11}{13}\selectfont},label style={font=\fontsize{11}{13}\selectfont},'
        +options+']\n'+plots+'\n'
        +r'\end{axis}\end{tikzpicture}\end{document}')
    (OUT/(name+'.tex')).write_text(source)
    result=subprocess.run(['pdflatex','--cnf-line=extra_mem_top=20000000','--cnf-line=extra_mem_bot=20000000','-interaction=nonstopmode','-halt-on-error',
        name+'.tex'],cwd=OUT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if result.returncode:
        raise RuntimeError(result.stdout[-4000:])

for name,mu in [('sr_m01',-.1),('sr_01',.1)]:
    nu=.9; x=np.linspace(-.25,.8,901)
    np.savetxt(OUT/(name+'_curve.dat'),np.c_[x,step(x,nu,mu)])
    q=.02 if mu<0 else .025; path=[(q,q)]
    for _ in range(24):
        nxt=float(step(q,nu,mu)); path.extend([(q,nxt),(nxt,nxt)]); q=nxt
    np.savetxt(OUT/(name+'_web.dat'),path)
    plots=(r'\addplot[black,thick] table {'+name+'_curve.dat};\n'
        +r'\addplot[gray,dashed,domain=-.25:.8] {x};'+'\n'
        +r'\addplot[blue!65!black,thin] table {'+name+'_web.dat};')
    figure(name,plots,r'xlabel={$w_k$},ylabel={$w_{k+1}$},xmin=-.25,xmax=.8,ymin=-.25,ymax=.8')

mus=np.linspace(-.02,.3,241)
for name,nu in [('bif_08',.8),('bif_06',.6),('bif_015',.15)]:
    x=np.zeros_like(mus); rows=[]
    for j in range(2400):
        x=step(x,nu,mus)
        if j>=2320: rows.append(np.c_[mus,x])
    np.savetxt(OUT/(name+'.dat'),np.vstack(rows))
    figure(name,r'\addplot[only marks,mark=*,mark size=.16pt,black] table {'+name+'.dat};',
        r'xlabel={$\mu$},ylabel={$w_k$},xmin=-.02,xmax=.3,scaled x ticks=false,xtick={0,.1,.2,.3}')
print('Generated five vector PDF figures; 2320 transient + 80 retained iterations per mu.')
