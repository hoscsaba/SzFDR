"""Figures 4.1-4.2: exact free flight, bracketed impact times, PDF and SVG."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':11,'svg.fonttype':'path','pdf.fonttype':42})
R=.95

def flight(t,y,h,w):
    c=1/(1-w*w); A=y[0]-c*np.cos(w*t); B=y[1]+c*w*np.sin(w*t)
    return np.array([A*np.cos(h)+B*np.sin(h)+c*np.cos(w*(t+h)),
                    -A*np.sin(h)+B*np.cos(h)-c*w*np.sin(w*(t+h))])

def simulate(w,steps=300):
    T=2*np.pi/w; end=100*T; dt=T/steps; t=0.; y=np.array([1.,0.])
    rows=[[t,*y]]; hits=[]
    while t<end-1e-12:
        h=min(dt,end-t); z=flight(t,y,h,w)
        if z[0]<0:
            lo=0.;hi=h
            for _ in range(45):
                mid=(lo+hi)/2
                if flight(t,y,mid,w)[0]>0:lo=mid
                else:hi=mid
            h=(lo+hi)/2; z=flight(t,y,h,w);t+=h
            assert h>0 and z[1]<-1e-8, f'Contact w={w}, t={t}, y={y}, h={h}, z={z}'
            hits.append([t,z[1],-R*z[1]])
            rows.extend([[t,0,z[1]],[t,np.nan,np.nan]])
            y=np.array([0.,-R*z[1]])
        else:t+=h;y=z
        rows.append([t,*y])
    return np.array(rows),np.array(hits)

figp,ap=plt.subplots(3,1,figsize=(6.2,7.8),layout='constrained')
figt,at=plt.subplots(3,1,figsize=(6.2,7.8),layout='constrained')
allrows=[]; allhits=[]
for w in [3.,2.76,2.9]:
    rows,hits=simulate(w);T=2*np.pi/w
    keep=rows[:,0]>=88*T; h=hits[hits[:,0]>=88*T]
    allrows.append(rows[keep]);allhits.append(h)
    print(f'omega={w}: {len(h)} impacts in plotted window; min |v-|={min(abs(h[:,1])):.6g}')
    # Independent temporal refinement verifies impact counts and event values.
    fine,fh=simulate(w,600)
    early=hits[hits[:,0]<10*T]; ef=fh[fh[:,0]<10*T]
    print('refinement:',len(hits),len(fh),'early error',np.max(abs(ef-early)) if ef.shape==early.shape else 'counts differ')
    assert ef.shape==early.shape and np.max(abs(ef-early))<2e-7
    np.savetxt(ROOT/'graphics_v3'/f'impact_w{w:g}.csv',rows[keep],delimiter=',',header='t,u,v')
umax=max(np.nanmax(z[:,1]) for z in allrows)*1.08
vmax=max(np.nanmax(abs(z[:,2])) for z in allrows)*1.1
for i,(w,z,h) in enumerate(zip([3.,2.76,2.9],allrows,allhits)):
    T=2*np.pi/w;p=ap[i];a=at[i]
    for ax in (p,a):
        ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
        ax.set_title(f'({chr(97+i)})  '+r'$\omega='+f'{w:g}'+r'$',loc='left',fontsize=12)
    p.axvspan(-.05*umax,0,color='.93');p.axvline(0,color='.35',lw=1)
    p.plot(z[:,1],z[:,2],color='#2166ac',lw=1.1,label='Szabad mozgás')
    p.scatter(np.zeros(len(h)),h[:,1],s=20,c='#c15c18',marker='v',zorder=5,label='Ütközés előtt')
    p.scatter(np.zeros(len(h)),h[:,2],s=20,facecolors='white',edgecolors='#19834a',zorder=5,label='Ütközés után')
    event=h[len(h)//2]
    p.annotate('',xy=(0,event[2]),xytext=(0,event[1]),arrowprops=dict(arrowstyle='->',ls='--',color='#19834a',lw=1.5))
    p.set(xlim=(-.05*umax,umax),ylim=(-vmax,vmax),xlabel='$u$',ylabel='$v$')
    a.axhline(0,color='.35',lw=1)
    a.plot(z[:,0]/T-88,z[:,1],color='#2166ac',lw=1.2)
    a.scatter(h[:,0]/T-88,np.zeros(len(h)),s=22,c='#c15c18',zorder=5,label='Ütközés: $u=0$')
    a.set(xlim=(0,12),ylim=(-.05*umax,umax),xlabel=r'$(t-t_a)/T$,  $t_a=88T$',ylabel='$u(t)$')
    a.set_xticks(range(0,13,2))
ap[0].legend(loc='upper right',fontsize=9,framealpha=.95)
at[0].legend(loc='upper right',fontsize=9)
for fig,name in [(figp,'impact_phase'),(figt,'impact_time')]:
    for folder,ext in [('graphics_v3','pdf'),('graphics_svg','svg')]:fig.savefig(ROOT/folder/f'{name}.{ext}')
    fig.savefig(ROOT/'graphics_v3'/f'{name}_preview.png',dpi=130)
    plt.close(fig)
