# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:25:22 2015

@author: MC. Jose Luis Rodriguez Solis
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap


from shapely.geometry import Polygon
#import shapefile
from shapely.geometry import Point
exec("import sys; reload(sys); sys.setdefaultencoding('utf8')")
#------------------------------------------------------------------------------
#
# las condiciones de uso del programa
#
#año final de la base de datos
yearf= 2017
mes = 5          # el mes para filtrar
posx= -99.00     # posicion longitud 
posy=  11.5      # posicion latitud
dl  =  3.0      # el margen para la posicion actual del CT
baja = 'no'      # se desea bajar los datos de nuevo
opcion = 1 #uno para un circulo, 2 para un cuadrado con las dimensiones abajo 
#
yearini = 1950
#
#pl = [(-100,40),(-20,40),(-20,5),(-100,5),(-100,40)]
pl = [(-120,20),(-80,20),(-80,5),(-120,5),(-120,20)]#
#------------------------------------------------------------------------------
#
# Dominio
#
yi =  5           # latitud inicial
yf = 35           # latitud final
xi =-135          # longitud inicial
xf =-80.5             # longitud final
#------------------------------------------------------------------------------
#
#
month = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
month = month[mes-1]
mes="{0:02d}".format(mes)
C = np.loadtxt('/home/luis/Documents/tools/mexdiv.dat')
#
#------------------------------------------------------------------------------
if baja == 'si':
    os.system("wget 'http://www.nhc.noaa.gov/data/hurdat/hurdat2-nepac-1949-2017-050418.txt' -O hur_pac.dat")
    os.system("sed -i 's/N/ /g' hur_pac.dat")
    os.system("sed -i 's/W/ /g' hur_pac.dat")
    os.system("sed -i 's/E/ /g' hur_pac.dat")
    os.system("sed -i 's/,/ /g' hur_pac.dat")

a = open('hur_pac.dat')
b = a.readlines()

dat = []
for i in range(0,len(b)):
    c = b[i].split()
    dat.insert(i,c)

Nx = np.empty(19); Nx[:]= np.NaN; Nx=Nx.tolist()
#
# limpiando y ordenando latitud, longitud e intensidad
#
t   = []
lon = []
lat = []
inte= []
for i in range (0,len(dat)):
    if len (dat[i]) > 10 and len (dat[i]) < 20:
        ver    = dat [i]
        ver[5] = float(ver[5])
        ver[4] = float(ver[4])
        ver[3] = float(ver[3])
        dat[i] = ver
        t.append(ver[0])
        lon.append(-1*ver[4])
        lat.append(ver[3])
        inte.append(ver[5])
    elif len (dat[i])<10:
        dat[i] = Nx
        t.append(np.NaN)
        lon.append(np.NaN)
        lat.append(np.NaN)
        inte.append(np.NaN)
#==============================================================================
# poniendo (aislando) cada evento en una lista (list), comienza en uno debido
# debido a que el primer dato es NaN
#==============================================================================
k = 0
sel = []
TC = []
for i in range(0,len(t)):
    if  np.isnan(float(t[i])) == False:
        sel.append([t[i], lon[i], lat[i], inte[i]])
    elif np.isnan(float(t[i])) == True and len(sel)>0:
        TC.append(np.asarray(sel))
        sel = []

#==============================================================================
# buscando las fechas deseadas
#==============================================================================
nx = np.empty([1,4]); nx[:]= np.NaN
tclist=[]
tcmonth = []
for i in range (0,len(TC)):
    tc = TC[i]
    for j in range(0,len(tc)):
        ver    = tc[j]
        strt = ver[0]
        if  strt.find(mes,4) == 4:
            tclist.extend(tc)
            tclist.extend(nx)
            tcmonth.append(tc)
            break
            
tclist=np.asarray(tclist)
lonlist=tclist[:,1]
latlist=tclist[:,2]


#==============================================================================
# para filtrar por una posicion especifica dada arriba con CIRCULO
#==============================================================================   

plt.close('all')
fig, ax = plt.subplots(num=6, figsize=(10,6))
m = Basemap(projection='cyl',llcrnrlat=yi,urcrnrlat=yf,\
            llcrnrlon=xi,urcrnrlon=xf,resolution='l')
#m.fillcontinents(color='0.0')
#m.fillcontinents(color=[0.2980,0.6392,0.0000])
#m.fillcontinents(color=[0.4000,0.6039,0.1960],lake_color=[0.3215,0.5215,0.7176])
#m.drawmapboundary(fill_color='w')
#m.drawmapboundary(fill_color=[0.3215,0.5215,0.7176])
m.bluemarble()
m.drawcoastlines(linewidth=0.25,color='0.1')
m.drawcountries(linewidth=0.25,color='0.1')
parallels = np.arange(yi,yf+0.1,5)
m.drawparallels(parallels,labels=[1,0,0,0], linewidth= 0.1 ,fontsize=8,color='0.5')
meridians = np.arange(xi,xf+0.1,5)
m.drawmeridians(meridians,labels=[0,0,0,1], linewidth= 0.1, fontsize=8,color='0.5')


if opcion ==1:
    pos = Point(posx, posy).buffer(dl)
elif opcion == 2:
    pl = np.asarray(pl)
    pos = Polygon(pl)

tcloc=[]
k  = []
dt = []
tt = []
h1 = []
h2 = []
h3 = []
h4 = []
h5 = [] 
for i in range (0,len(tcmonth)):
    tc = tcmonth[i]
    ver = tc[0]
    fecha = tc[0,0]
    fecha = fecha[0:4]
    locx = float(ver[1])
    locy = float(ver[2])
    pt = Point(locx,locy)
    if fecha >= str(yearini):
        if  pos.contains(pt) == True:
            tcloc.extend(tc)
            tcloc.extend(nx)
            k.append(1)
            vermax = np.max(tc[:,3].astype('float'))
            if vermax<34: # para DT
                tcolor=[0.00000,1.00000,1.00000]
                dt.append(1)
                print ('year: ',fecha[2::],'cat: DT')
            elif vermax>=34 and vermax<=63:
                tcolor=[0.00000,0.20000,1.00000]
                tt.append(1) 
                print ('year: ',fecha[2::],'cat: TT')
            elif vermax>=64 and vermax<=82:
                tcolor=[1.00000,1.00000,0.00000]
                h1.append(1)
                print ('year: ',fecha[2::],'cat: H1')
            elif vermax>=83 and vermax<=95:
                tcolor=[0.85000,0.64400,0.12500]
                h2.append(1)
                print ('year: ',fecha[2::],'cat: H2')
            elif vermax>=96 and vermax<=112:
                tcolor=[1.00000,0.24000,0.00000]
                h3.append(1)
                print ('year: ',fecha[2::],'cat: H3')
            elif vermax>=113 and vermax<=136:
                tcolor=[1.00000,0.50000,0.00000]
                h4.append(1)
                print ('year: ',fecha[2::],'cat: H4')
            elif vermax>=137:
                tcolor=[1.00000,0.00000,1.00000]
                h4.append(1)
                print ('year: ',fecha[2::],'cat: H5')
            fecha = fecha[2::]
            plt.plot(tc[:,1].astype('float'),tc[:,2].astype('float'),color=tcolor,linewidth=0.5)
            plt.plot(tc[:,1].astype('float'),tc[:,2].astype('float'),color=tcolor,marker='.',ms=4,linewidth=0.1)
            plt.text(tc[len(tc)//3,1].astype('float'),tc[len(tc)//3,2].astype('float'),fecha,color='w',fontsize=6,horizontalalignment='center')
            

plt.plot(C[:,0],C[:,1],color='0.1',linewidth=0.25)

if opcion == 1:
    plt.plot (posx,posy,color='0.5',marker='o',markersize=4,linewidth=0.3)
    circle=plt.Circle((posx,posy),dl,edgecolor='0.5', facecolor="w",linewidth=0.5,fill=False)
    radio = (posx-dl)**2 + (posy-dl)**2    
    fig.gca().add_artist(circle)

elif opcion == 2:
    plt.plot(pl[:,0],pl[:,1])

plt.title(u'Total de Ciclones Tropicales cercanos a la posición ['+str(posy)+'$^o$N,'+\
          str(abs(posx))+'$^o$W]\npara todos los meses de '+month+' entre '+str(yearini)+'-2017',\
          loc='left',fontsize=9)

plt.text(0.01,0.11, u'Total: '+str(len(k)),\
        transform=ax.transAxes,fontsize=8,color='w')
plt.text(0.01,0.08, \
        u'Datos: hurdat2/NHC',transform=ax.transAxes,fontsize=8,color='w')
plt.text(0.01,0.05, \
        u'Radio de influencia '+str(dl)+' grados',transform=ax.transAxes,fontsize=8,color='w')
plt.text(0.01,0.02, \
        u'twitter:@jluis_rds',transform=ax.transAxes,fontsize=8,color='w')


plt.text(0.01,0.96, \
        str(len(dt))+u' -  DT ',color=[0.00000,1.00000,1.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.92, \
        str(len(tt))+u' -  TT ',color=[0.00000,0.20000,1.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.88, \
        str(len(h1))+u' -  Hur I',color=[1.00000,1.00000,0.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.84, \
        str(len(h2))+u' -  Hur II',color=[1.00000,0.64400,0.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.80, \
        str(len(h3))+u' -  Hur III',color=[1.00000,0.27000,0.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.76, \
        str(len(h4))+u' -  Hur IV',color=[1.00000,0.00000,0.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')
plt.text(0.01,0.72, \
        str(len(h5))+u' -  Hur V',color=[1.00000,0.00000,1.00000],transform=ax.transAxes,fontsize=8,fontweight='bold')


plt.savefig(u'actual_positionpac_'+str(dl)+'_ini'+mes+'.png', bbox_inches='tight')





