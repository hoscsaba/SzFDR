"""Exact reference figures for Chapter 6; requires NumPy and Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':10.5,'axes.labelsize':10.5,'legend.fontsize':9.5,
                     'svg.fonttype':'path','pdf.fonttype':42})
blue='#2166ac'; orange='#c35c19'; green='#21846b'
def save(fig,name):
    fig.tight_layout(pad=.7)
    for folder,ext in [('graphics_v3','pdf'),('graphics_svg','svg')]:
        (ROOT/folder).mkdir(exist_ok=True)
        fig.savefig(ROOT/folder/f'{name}.{ext}')
    plt.close(fig)
# Stick and slip: analytic segments, same constants as MATLAB example.
U,Fs,Fk=.3,.6,.4
Ts=2*(Fs-Fk)/U; Tl=2*np.pi-2*np.arctan((Fs-Fk)/U); T=Ts+Tl
fig,axs=plt.subplots(2,1,figsize=(6.3,3.7),sharex=True)
for j in range(2):
    s=np.linspace(0,Ts,120); q=np.linspace(0,Tl,400)
    t=np.r_[s,Ts+q]+j*T
    x=np.r_[2*Fk-Fs+U*s,Fk+(Fs-Fk)*np.cos(q)+U*np.sin(q)]
    w=np.r_[s*0,-(Fs-Fk)*np.sin(q)+U*np.cos(q)-U]
    axs[0].plot(t,x,color=blue);axs[1].plot(t,w,color=orange)
    for ax in axs: ax.axvspan(j*T,j*T+Ts,color=blue,alpha=.12)
axs[0].set_ylabel('$x$');axs[1].set_ylabel('$v-U$');axs[1].set_xlabel('$t$')
for ax in axs: ax.grid(alpha=.25)
save(fig,'stick_slip_cycle')
# Ball: exact flight arcs, finite depiction of the infinite sequence.
g,r,h0=9.81,.7,1.; V=np.sqrt(2*g*h0); t1=V/g; Tz=t1*(1+r)/(1-r)
fig,axs=plt.subplots(1,2,figsize=(6.3,2.8))
s=np.linspace(0,t1,100);axs[0].plot(s,h0-g*s*s/2,color=blue)
ta=t1
for n in range(1,13):
    u=r**n*V; s=np.linspace(0,2*u/g,90)
    axs[0].plot(ta+s,u*s-g*s*s/2,color=blue);ta+=s[-1]
axs[0].axvline(Tz,color=orange,linestyle='--',label='$T_Z$')
axs[0].set(xlabel='$t$ [s]',ylabel='$h$ [m]');axs[0].legend()
n=np.arange(1,13);axs[1].semilogy(n,2*r**n*V/g,'o-',color=blue,markersize=3)
axs[1].set(xlabel='$n$',ylabel=r'$\Delta t_n$ [s]',ylim=(.01,1))
axs[1].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
for ax in axs:ax.grid(alpha=.25)
save(fig,'zeno_ball')
# Exact admissible branches, including unstable fixed point.
fig,ax=plt.subplots(figsize=(6.3,3.1));ml=np.linspace(-.2,0,200);mr=np.linspace(0,.2,200)
ax.plot(ml,2*ml,color=blue,label='Stabil fixpont')
ax.plot(mr,-2*mr/7,color=green,label='Stabil kétciklus');ax.plot(mr,6*mr/7,color=green)
ax.plot(mr,2*mr/5,'--',color=orange,label='Instabil fixpont')
ax.axvline(0,color='0.6',lw=.7);ax.axhline(0,color='0.6',lw=.7)
ax.set(xlabel=r'$\mu$',ylabel='$x$');ax.grid(alpha=.2);ax.legend(loc='lower right')
save(fig,'border_collision')
# Smooth friction: curve intersections yield exact creep velocities.
fig,ax=plt.subplots(figsize=(6.3,3.0));v=np.linspace(-.1,.25,700)
for eps in [.2,.05,.01]:
    line,=ax.plot(v,np.tanh(v/eps),label=fr'$\varepsilon={eps:g}$')
    ax.plot(eps*np.arctanh(.5),.5,'o',color=line.get_color(),markersize=5)
ax.axhline(.5,color='0.3',ls='--',label='$q=1/2$');ax.axvline(0,color='0.6',lw=.7)
ax.set(xlabel='$v$',ylabel=r'$\tanh(v/\varepsilon)$');ax.legend(loc='lower right');ax.grid(alpha=.2)
save(fig,'friction_regularization')
# Local sliding birth; incoming coordinate c is not a model parameter.
fig,ax=plt.subplots(figsize=(6.3,3.0));xx=np.linspace(-1.2,1.2,400)
ax.axhline(0,color='0.5',lw=1)
ax.plot(xx,xx**2/2+.15,color=blue,label='$c>0$: nincs érintés')
ax.plot(xx,xx**2/2,'--',color=orange,label='$c=0$: grazing')
c=-.18;entry=-np.sqrt(-2*c);xx1=np.linspace(-1.2,entry,120);xx2=np.linspace(0,1.2,120)
ax.plot(xx1,xx1**2/2+c,color=green,label='$c<0$: sliding szakasz')
ax.plot([entry,0],[0,0],color=green,lw=4);ax.plot(xx2,xx2**2/2,color=green)
ax.annotate('',xy=(-.1,0),xytext=(-.45,0),arrowprops={'arrowstyle':'->','color':'black'})
ax.set(xlabel='$x$',ylabel='$y$',ylim=(-.06,.9));ax.grid(alpha=.2);ax.legend(loc='upper center')
save(fig,'sliding_birth')
print(f'Ts={Ts:.9f}, Tl={Tl:.9f}, T={T:.9f}, Tz={Tz:.9f}')
