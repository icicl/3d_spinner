import math
from PIL import Image
def read(im,x,y):
    sx,sy=16,16
    if max(abs(x),abs(y))>0.5:return (0,0,0,0)
    return im[round((x+0.5)*(sx-1)),round((y+0.5)*(sy-1))]

def edgeC(i):
    im=Image.open(i).convert('RGBA')
    il=im.load()
    sx,sy=im.size
    c=[]
    for y in range(sy):
        if any(il[x,y][3] for x in range(sx)):
            for x in range(sx):
                if il[x,y][3]:break
            c+=[il[x,y]]
            for x in range(sx-1,-1,-1):
                if il[x,y][3]:break
            c+=[il[x,y]]
    r=sorted(c)[len(c)//2]
    return r
    
def frame(im,angle,width,fname,sz,border=8,edgeC=None):
    angle%=360
    r=-1
    r2=1
    if angle>=180:r2=-1
    if angle%180!=angle%90:
#    if angle>90 and angle <270:
#        angle=180-angle
        r=1
    io=Image.new("RGBA",sz,(0,0,0,0))
    il=io.load()
    if angle%180!=90:
        for x in range(sz[0]):
            for y in range(sz[1]):#+(r*r2)*width/(2*sz[1]*math.cos(math.radians(angle)))
                il[x,y]=read(im,(x/(sz[0]-1)-0.5)/math.cos(math.radians(angle))+(width/(sz[0]-1))*r*r2*math.tan(math.radians(angle))/2,y/(sz[1]-1)-0.5)
#                il[x,y]=read(im,((x-border)/(sz[0]-border-1)-0.5)/math.cos(math.radians(angle))+(width/(sz[0]-border-1)-0.5)*math.sin(math.radians(angle))/2,(y-border)/(sz[1]-border-1)-0.5)
        for y in range(sz[1]):
            x=(sz[0]-1)*((1-r)//2)
            l=(0,0,0,0)
            b=1
            while (x>=0 and x<sz[1]) and (l[3]==0 or il[x,y][3]):
                try:
                    l=il[x,y]
                except:
                    b=0
                    break
                x+=r
            if l!=(0,0,0,0):
                if edgeC:
                    l=edgeC
                for dx in range(b*abs(round(width*math.sin(math.radians(angle))))):
                    il[x+r*dx,y]=l
    else:
        sx,sy=16,16
        dd=0
        for y in range(sy):
            if any(im[x,y][3] for x in range(sx)):
                for x in range(sz[0]//2-width//2,sz[0]//2+width//2):
                    for dy in range(sz[1]//sy+2*dd):
                        il[x,y*sz[1]//sy+dy-dd]=edgeC
#                        il[x,y*sz[1]//sy+dy+border]=edgeC
    io.save('out2/'+fname)
import os

def gif(i):
    ims = []
    for f in sorted(os.listdir('out')):
        if i in f:
            ims+=[Image.open('out/'+f)]
    ims[0].save(i+'.gif','GIF',save_all=True,append_images=ims[1:],duration=20,loop=0,transparency=0)

i='diamond'

W=16
#if 0:
#    frame(Image.open(i+'.png).load(),90,W,i+'_'+str(90).zfill(3)+'.png',(128,128),(255,0,0,255))
indir='in2/'
if 1:
    for i in os.listdir(indir):#['diamond','gold_ingot','emerald','iron_ingot']:
        print(i)
        ec=edgeC(indir+i)
        for a in range(0,360,5):
            frame(Image.open(indir+i).convert('RGBA').load(),a,W,i+'_'+str(a).zfill(3)+'.png',(128,128),8,ec)
#        gif(i[:-4])
#gif('emerald')
