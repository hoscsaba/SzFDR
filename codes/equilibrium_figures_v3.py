"""Original linear phase portraits (PDF/SVG), not reproductions of book figures."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':10.5,'axes.titlesize':10.5,'axes.labelsize':10.5,
                     'svg.fonttype':'path','pdf.fonttype':42})
grid=np.linspace(-2,2,101);X,Y=np.meshgrid(grid,grid)
blue='#2166ac';orange='#c35c19'
def portrait(ax,A,title):
    U=A[0,0]*X+A[0,1]*Y;V=A[1,0]*X+A[1,1]*Y
    ax.streamplot(X,Y,U,V,density=.9,color='0.35',linewidth=.75,arrowsize=1.1)
    ax.axhline(0,color='0.8',lw=.6,zorder=0);ax.axvline(0,color='0.8',lw=.6,zorder=0)
    ax.plot(0,0,'ko',ms=4,zorder=5)
    ax.set(xlim=(-2,2),ylim=(-2,2),xlabel='$y_1$',ylabel='$y_2$',title=title)
    ax.set_aspect('equal');ax.set_xticks([-2,0,2]);ax.set_yticks([-2,0,2])
def save(fig,name):
    fig.tight_layout(pad=.5)
    for folder,ext in [('graphics_v3','pdf'),('graphics_svg','svg')]:
        (ROOT/folder).mkdir(exist_ok=True)
        fig.savefig(ROOT/folder/f'{name}.{ext}')
    plt.close(fig)
fig,ax=plt.subplots(figsize=(3.28,3.28))
portrait(ax,np.diag([-1,1]),r'Nyereg: $\lambda_1=-1,\ \lambda_2=1$')
ax.axhline(0,color=blue,lw=1.8);ax.axvline(0,color=orange,lw=1.8)
for a,b in [((1.5,0),(.8,0)),((-1.5,0),(-.8,0)),((0,.8),(0,1.5)),((0,-.8),(0,-1.5))]:
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':blue if a[1]==0 else orange,'lw':2})
save(fig,'phase_saddle')
fig,axs=plt.subplots(1,2,figsize=(6.3,3.15))
portrait(axs[0],np.diag([-1,-2]),r'Stabil csomó: $-1,\,-2$')
portrait(axs[1],np.diag([1,2]),r'Instabil csomó: $1,\,2$')
save(fig,'phase_nodes')
fig,axs=plt.subplots(1,2,figsize=(6.3,3.15))
for ax,alpha,title in zip(axs,[-.35,.35],['Stabil fókusz','Instabil fókusz']):
 portrait(ax,np.array([[alpha,-1],[1,alpha]]),title+fr': ${alpha:g}\pm i$')
save(fig,'phase_foci')
