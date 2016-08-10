#!/usr/bin/env python3
from pys import sd;
from gensim import gensim, fromenergy;
import numpy as np;
c=299792458
cycles = 80e-15/(780e-9/c);
Es = [10,1,0.1,0.01,0.001,1e-4];
defd = dict(
    dumpinterval=1e-15,
    singlescale=True,
    no_pmovies=True,
    lspexec='lsp-10-xy',
    fp='nc',
    #target
    n_s=1e23,
    solid_len=10,
    expf=1.5,
    #movne
    movne={'clim':(1e14,1e21)},
    #pbs options
    autozipper=True,
    dir=True,
)
pbsfmt='{l}um-{I:0.2e}-l={scale:0.3}um'
def mkpbsbase(d):
    d['pbsbase']=pbsfmt.format(
        l=int(d['l']/1e-6),I=d['I'],scale=d['expf']);
def mkpbs(d):
    d['pbses'] = [
        dict(pbsname=d['pbsbase']),
        dict(pbsname=d['pbsbase']+'-nocoll',
             lspexec='lsp-10-xy-no_collisions'),];
    return d;

defds=[]
for E in Es:
    d = sd(fromenergy(E,cycles=cycles), **defd);
    d.update(
        lim =( -50, 10, -120, 120,0,0),
        tlim=( -40,  0, -110, 110,0,0),
        res =( 60*5, 240*5, 0),
        timestep = 2e-16,
        totaltime= d['T']*3.0,
        description="10um",
        #movne
        movne={'clim':(1e14,1e21)},
        angular=True,
    );
    defds.append(d);


####################################
# 10um scans
####################################
#10um, scale=1.5um
for d in defds:
    d['pbsbase']=pbsfmt.format(
        l=int(d['l']/1e-6),I=d['I'],scale=d['expf']);
    d['pbses'] = [
        dict(pbsname=d['pbsbase']),
        dict(pbsname=d['pbsbase']+'-nocoll',
           lspexec='lsp-10-xy-no_collisions'),];
    gensim(**d);
#10um, scale=19.2um
longs = [sd(
    d,
    n_s=1e21,
    expf=19.2,
    lim =( -250, 10, -120, 120,0,0),
    tlim=( -240,  0, -110, 110,0,0),
    res =( 260*4, 240*4, 0),
    totaltime=d['T']*3.5,)
         for d in defds];
for d in longs:
    mkpbsbase(d);
    mkpbs(d);
    gensim(**d);
####################################
# 3um scans
####################################
#3um, scale=1.5um
for E in Es:
    d = sd(fromenergy(E,l=3e-6,cycles=cycles), **defd);
    d.update(
        lim =( -50, 10, -60, 60, 0,0),
        tlim=( -40,  0, -50, 50, 0,0),
        res =( 60*10, 120*10, 0),
        timestep = 1e-16,
        totaltime= d['T']*3.75,
        description="3um",
        #movne
        movne={'clim':(1e15,1e22)},
    );
    mkpbsbase(d);
    mkpbs(d);
    gensim(**d);
#3um, scale=5.77um
for E in Es:
    d = sd(fromenergy(E,l=3e-6,cycles=cycles), **defd);
    d.update(
        n_s=1e23,
        expf=5.77,
        lim =( -90, 10, -60, 60, 0,0),
        tlim=( -80,  0, -50, 50, 0,0),
        res =( 100*10, 120*10, 0),
        totaltime=d['T']*3.75,
        timestep = 1e-16,
        description="3um w/ 5.77um scale plasma",
        #movne
        movne={'clim':(1e15,1e22)},
    );
    mkpbsbase(d);
    mkpbs(d);
    gensim(**d);

####################################
# 3um scans with shelf
####################################
def mkshelf(xdim=(0,50e-4),
          slen=10.0e-4,
          sh=1e19,solid=1e23):
    sdim = (xdim[1] - slen, xdim[1]);
    @np.vectorize
    def out(x):
        if x <= xdim[0] or x >= xdim[1]:
            return 0.0;
        elif sdim[0] <= x <= sdim[1]:
            return solid;
        else:
            return sh;
    return out;

for E in Es:
    d = sd(fromenergy(E,l=3e-6,cycles=cycles), **defd);
    d.update(
        lim =( -50, 20, -45, 45, 0,0),
        tlim=( -40, 10, -35, 35, 0,0),
        res =( 70*10, 90*10, 0),
        timestep = 1e-16,
        totaltime= d['T']*4,
        description="3um",
        fp=(0,0,0),
        #movne
        movne={'clim':(1e15,1e22)},
        #density
        singlescale=None,
        dens_dat="shelf.dat",
        externalf_1D=True,
        f_1D=mkshelf(),
    );
    d['pbsbase']='{l}um-{I:0.2e}-shelf'.format(
        l=int(d['l']/1e-6),I=d['I']);
    mkpbs(d);
    gensim(**d);

#############################
# 1um scans
#############################
for E in Es:
    d = sd(fromenergy(E,l=1e-6,cycles=cycles), **defd);
    d.update(
        n_s=1e23,
        expf=1.92,
        #
        lim =( -42.5, 10, -15, 15, 0,0),
        tlim=( -32.5,  0, -10, 10, 0,0),
        res =( 52.5*30, 30*30, 0),
        timestep = 1e-16,
        totaltime= d['T']*4,
        description="1um",
        #movne
        movne={'clim':(5e17,1e23)},
    );
    mkpbsbase(d);
    mkpbs(d);
    gensim(**d);


#############################
# 1um shelf
#############################
shelf_1um=[]
for E in Es:
    d = sd(fromenergy(E,l=1e-6,cycles=cycles), **defd);
    d.update(
        lim =( -42.5, 10, -15, 15, 0,0),
        tlim=( -32.5,  0, -10, 10, 0,0),
        res =( 52.5*30, 30*30, 0),
        timestep = 1e-16,
        totaltime= d['T']*4,
        description="1um",
        fp=(0,0,0),
        #movne
        movne={'clim':(5e17,1e23)},
        #density
        singlescale=None,
        dens_dat="shelf.dat",
        externalf_1D=True,
        f_1D=mkshelf(xdim=(0,42.5e-4),sh=1e19),
    );
    d['pbsbase']='{l}um-{I:0.2e}-shelf={sh}'.format(
        l=int(d['l']/1e-6),I=d['I'],sh=1e19);
    mkpbs(d);
    gensim(**d);
    shelf_1um.append(d);
    
for d in shelf_1um:
    sh = 1e18
    d.update(
        f_1D=mkshelf(xdim=(0,42.5e-4),sh=sh));
    d['pbsbase']='{l}um-{I:0.2e}-shelf={sh}'.format(
        l=int(d['l']/1e-6),I=d['I'],sh=sh);
    mkpbs(d);
    gensim(**d);