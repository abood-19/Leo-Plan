import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
S=2000  # working canvas
def bez(p,n=60):
    # catmull-rom through points
    pts=[p[0]]+p+[p[-1]]; out=[]
    for i in range(1,len(pts)-2):
        p0,p1,p2,p3=[np.array(x,float) for x in pts[i-1:i+3]]
        for t in np.linspace(0,1,n,endpoint=False):
            t2,t3=t*t,t*t*t
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    out.append(np.array(p[-1],float)); return np.array(out)
def stroke(d,pts,w,head=.15,tail=.6,sc=2):
    c=bez([(x*sc,y*sc) for x,y in pts]); n=len(c)
    # tangent normals
    tg=np.gradient(c,axis=0); tg/=np.linalg.norm(tg,axis=1,keepdims=True)+1e-9
    nm=np.stack([-tg[:,1],tg[:,0]],1)
    t=np.linspace(0,1,n)
    prof=np.where(t<head,(t/head)**.6,((1-t)/(1-head))**tail*1.0)
    prof=np.clip(prof,0,1)*w*sc
    L=c+nm*prof[:,None]/2; R=c-nm*prof[:,None]/2
    poly=[tuple(x) for x in L]+[tuple(x) for x in R[::-1]]
    d.polygon(poly,fill=255)
    return c
def thorn(d,base,ang,length,w,bend=0.35,sc=2):
    x,y=base; a=math.radians(ang)
    p1=(x+math.cos(a)*length*.5+math.cos(a+math.pi/2)*length*bend*.5, y+math.sin(a)*length*.5+math.sin(a+math.pi/2)*length*bend*.5)
    p2=(x+math.cos(a)*length, y+math.sin(a)*length+0)
    stroke(d,[(x,y),p1,p2],w,head=.05,tail=1.1,sc=sc)
def render(build, hue=((95,20,255),(170,60,255),(235,190,255)), size=1080):
    m=Image.new("L",(S,S),0); d=ImageDraw.Draw(m); build(d)
    a=np.asarray(m,dtype=np.float32)/255
    def blur(r): return np.asarray(m.filter(ImageFilter.GaussianBlur(r)),dtype=np.float32)/255
    g1=blur(90); g2=blur(30); g3=blur(10); inner=np.asarray(m.filter(ImageFilter.GaussianBlur(14)),dtype=np.float32)/255
    c1,c2,c3=[np.array(h,np.float32)/255 for h in hue]
    img=np.zeros((S,S,3),np.float32)+np.array([6,4,10],np.float32)/255
    img+=g1[...,None]*c1*1.9
    img+=g2[...,None]*c2*1.1
    k=np.clip((inner-.45)/.55,0,1)[...,None]**1.5
    core=a[...,None]*(c2*(1-k)+c3*k)
    img=img*(1-a[...,None]*.85)+core*1.15+g3[...,None]*c3*.25*a[...,None]
    img=np.clip(img,0,1)
    out=Image.fromarray((img*255).astype(np.uint8)).resize((size,size),Image.LANCZOS)
    return out
