"""Explicit piecewise vector field for Figure 2.2; PDF and vector SVG."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':11,'svg.fonttype':'path','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(4.9,4.5))
a=np.linspace(-1.5,1.5,17);X,Y=np.meshgrid(a,a);R=np.hypot(X,Y)
for inside,color in [(True,'#cf3737'),(False,'#1976b9')]:
    mask=(R<.88) if inside else (R>1.12)
    U,V=(X,-Y) if inside else (np.ones_like(X),-X)
    speed=np.hypot(U,V);mask&=speed>1e-12
    ax.quiver(X[mask],Y[mask],U[mask]/speed[mask],V[mask]/speed[mask],
              color=color,angles='xy',scale_units='xy',scale=7.5,width=.0045,pivot='mid')
t=np.linspace(0,2*np.pi,501);ax.plot(np.cos(t),np.sin(t),'k--',lw=1.4)
ax.plot(0,0,'ko',ms=4)
ax.text(.15,.43,r'$F_1,\ H>0$',color='#cf3737',bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
ax.text(-1.47,1.34,r'$F_2,\ H<0$',color='#1976b9',bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
ax.annotate(r'$\Sigma:\ H=0$',xy=(.8,.6),xytext=(.83,1.08),
            arrowprops={'arrowstyle':'->','lw':.9},bbox=dict(facecolor='white',edgecolor='none'))
ax.set(xlim=(-1.65,1.65),ylim=(-1.65,1.65),xlabel='$x_1$',ylabel='$x_2$')
ax.set_aspect('equal');ax.set_xticks([-1.5,-1,0,1,1.5]);ax.set_yticks([-1.5,-1,0,1,1.5])
t=np.linspace(3*np.pi/4,5*np.pi/4,201)
ax.plot(np.cos(t),np.sin(t),color='#19834a',lw=3.5)
ax.plot(np.cos(t[[0,-1]]),np.sin(t[[0,-1]]),'o',mfc='white',mec='#19834a',ms=6,zorder=5)
t=np.array([.83,1,1.17])*np.pi
x,y=np.cos(t),np.sin(t)
l1=2*(y*y-x*x);l2=2*x*(y-1);alpha=l1/(l1-l2)
u=(1-alpha)*x+alpha;v=-(1-alpha)*y-alpha*x
speed=np.hypot(u,v)
ax.quiver(x,y,u/speed,v/speed,color='#19834a',angles='xy',scale_units='xy',scale=5,width=.009,pivot='mid',zorder=6)
ax.text(-1.55,.3,r'$\Sigma_s$',color='#19834a',bbox=dict(facecolor='white',edgecolor='none'))
fig.tight_layout(pad=.5)
for folder,ext in [('graphics_v3','pdf'),('graphics_svg','svg')]:
    fig.savefig(ROOT/folder/f'circle_sliding_fields.{ext}')
plt.close(fig)
