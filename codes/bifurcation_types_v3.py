"""Local normal-form branch diagrams for sections 1.4.1 and 1.4.2."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'serif','font.size':11,'axes.titlesize':11,
 'axes.labelsize':11,'svg.fonttype':'path','pdf.fonttype':42})
m = np.linspace(-.18,0,200); p = np.linspace(0,.18,200)
def branch(ax,x,y,stable=True):
 ax.plot(x,y,'-' if stable else '--',color='#2166ac' if stable else '#b2182b',lw=1.7)
def panel(ax,kind,title):
 ax.axhline(0,color='.8',lw=.6);ax.axvline(0,color='.8',lw=.6)
 if kind=='fold':
  branch(ax,p,np.sqrt(p));branch(ax,p,-np.sqrt(p),False)
 elif kind=='tc':
  branch(ax,m,0*m);branch(ax,p,0*p,False)
  branch(ax,m,m,False);branch(ax,p,p)
 elif kind in ['pitch','pd']:
  branch(ax,m,0*m);branch(ax,p,0*p,False)
  branch(ax,p,np.sqrt(p));branch(ax,p,-np.sqrt(p))
 elif kind=='subpitch':
  branch(ax,m,0*m);branch(ax,p,0*p,False)
  branch(ax,m,np.sqrt(-m),False);branch(ax,m,-np.sqrt(-m),False)
 elif kind in ['hopf','ns']:
  branch(ax,m,0*m);branch(ax,p,0*p,False);branch(ax,p,np.sqrt(p))
 else:
  branch(ax,m,0*m);branch(ax,p,0*p,False);branch(ax,m,np.sqrt(-m),False)
 ax.plot(0,0,'ko',ms=3)
 radial=kind in ['hopf','ns','subhopf','subns']
 ax.set(xlim=(-.2,.2),ylim=(-.05,.48) if radial else (-.48,.48),
        xlabel=r'$\mu$',ylabel=r'$r$' if radial else r'$u$',title=title.replace(": ", "\n"))
 ax.set_xticks([-.15,0,.15]);ax.set_yticks([0,.4] if radial else [-.4,0,.4])
 ax.spines[['top','right']].set_visible(False)
def diagram(name,items):
 fig,axs=plt.subplots(3,2,figsize=(16/2.54,19/2.54))
 for ax,(kind,title) in zip(axs.flat,items):panel(ax,kind,title)
 fig.subplots_adjust(left=.12,right=.98,bottom=.075,top=.95,wspace=.45,hspace=.75)
 for folder,ext in [('graphics_v3','pdf'),('graphics_svg','svg')]:
  fig.savefig(ROOT/folder/f'{name}.{ext}')
 plt.close(fig)
diagram('equilibrium_bifurcations',[
 ('fold','Saddle-node'),('tc','Transcritical'),('pitch','Pitchfork: supercritical'),
 ('subpitch','Pitchfork: subcritical'),('hopf','Hopf: supercritical'),('subhopf','Hopf: subcritical')])
diagram('cycle_bifurcations',[
 ('fold','Fold of cycles'),('pd','Period-doubling: supercritical'),
 ('tc','Transcritical of cycles'),('pitch','Pitchfork of cycles: supercritical'),
 ('ns','Neimark–Sacker: supercritical'),('subns','Neimark–Sacker: subcritical')])
