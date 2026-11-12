import math, numpy as np, colorsys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
W,H=1080,1920
OUT="/home/claude/leo5/out/"
def pal(v,stops):
    v=np.clip(v,0,1); out=np.zeros(v.shape+(3,))
    for (a,ca),(b,cb) in zip(stops[:-1],stops[1:]):
        f=np.clip((v-a)/(b-a),0,1)[...,None]; sel=((v>=a)&(v<=b))[...,None]
        out=np.where(sel,np.array(ca)/255*(1-f)+np.array(cb)/255*f,out)
    return out
VIO=[(0,(10,3,22)),(.35,(52,16,120)),(.62,(124,58,237)),(.82,(196,160,255)),(1,(245,235,255))]
PNK=[(0,(18,3,16)),(.35,(110,15,90)),(.62,(219,39,160)),(.82,(250,170,225)),(1,(255,240,250))]
def waves(stops,seed=0,w=W,h=H):
    y,x=np.mgrid[0:h,0:w].astype(np.float32); x/=w; y/=w
    r=np.random.RandomState(seed)
    wx=x+0.16*np.sin(y*5+np.sin(x*3)*2+seed)+0.05*np.sin(y*17)
    wy=y+0.12*np.sin(x*4+1+seed)
    hgt=np.sin(wx*14+wy*6)*0.6+np.sin(wx*5-wy*11+1.7)*0.4+0.15*np.sin((wx-wy)*25)
    hgt=(hgt-hgt.min())/(hgt.max()-hgt.min())
    gy,gx=np.gradient(hgt*90)
    n=np.stack([-gx,-gy,np.ones_like(gx)],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
    L=np.array([-0.5,-0.7,0.5]); L/=np.linalg.norm(L)
    dif=np.clip((n*L).sum(-1),0,1)
    hv=np.array([0,0,1.0])+L; hv/=np.linalg.norm(hv)
    spec=np.clip((n*hv).sum(-1),0,1)**40
    v=0.15+0.55*dif+0.25*hgt
    col=pal(v,stops)+spec[...,None]*0.7
    # vignette
    cy,cx=h/2/w,0.5; d=np.sqrt((x-cx)**2+(y-cy)**2)
    col*=np.clip(1.15-d*0.9,0.35,1)[...,None]
    return Image.fromarray((np.clip(col,0,1)*255).astype(np.uint8))
def disc(size,tint=0.0):
    s=size; y,x=np.mgrid[0:s,0:s].astype(np.float32); c=s/2
    dx,dy=x-c,y-c; r=np.sqrt(dx*dx+dy*dy)/c; a=np.arctan2(dy,dx)
    hue=(a/(2*math.pi)*2+r*1.3+tint)%1
    hsv=np.stack([hue,np.full_like(hue,0.45),np.full_like(hue,1.0)],-1)
    rgb=np.vectorize(lambda h:0)(0)
    import matplotlib.colors as mc
    rgb=mc.hsv_to_rgb(hsv)
    streak=(np.cos(2*(a-0.7))**8)*0.6+(np.cos(2*(a+0.9))**16)*0.4
    base=np.array([0.42,0.30,0.70])
    col=base*(0.6+0.3*r[...,None])+rgb*0.30+streak[...,None]*0.55
    grooves=0.04*np.sin(r*900)
    col+=grooves[...,None]
    alpha=(r<=1).astype(np.float32)
    col=np.where((r<0.40)[...,None],np.array([0.07,0.03,0.14])+0.05*rgb,col)
    col=np.where(((r>=0.40)&(r<0.42))[...,None],np.array([0.85,0.8,1.0]),col)
    edge=np.clip((1-r)*60,0,1)
    im=Image.fromarray((np.clip(col,0,1)*255).astype(np.uint8)).convert("RGBA")
    im.putalpha(Image.fromarray((edge*alpha*255).astype(np.uint8)))
    return im
# ---------- icons (white line + glow) ----------
def icon_layer(kind,size=900,wd=26):
    S=size*2; im=Image.new("L",(S,S),0); d=ImageDraw.Draw(im); c=S/2; w=wd*2
    L=lambda pts:d.line(pts,fill=255,width=w,joint="curve")
    def ring(r,width=w): d.ellipse((c-r,c-r,c+r,c+r),outline=255,width=width)
    if kind=="sparkle":
        pts=[]
        for i in range(8):
            rr=250 if i%2==0 else 46; a=-math.pi/2+i*math.pi/4
            pts.append((c+rr*math.cos(a),c+rr*math.sin(a)))
        d.polygon(pts,fill=255)
    elif kind=="calendar":
        d.rounded_rectangle((c-230,c-190,c+230,c+220),radius=40,outline=255,width=w)
        L([(c-230,c-80),(c+230,c-80)])
        for xx in (c-110,c+110): L([(xx,c-250),(xx,c-140)])
        L([(c-95,c+70),(c-20,c+140),(c+110,c-10)])
    elif kind=="pen":  # modern wireless rotary pen, filled, diagonal
        a=math.radians(-45); ca,sa=math.cos(a),math.sin(a)
        def R(px,py): return (c+px*ca-py*sa, c+px*sa+py*ca)
        d.polygon([R(-360,-70),R(60,-70),R(60,70),R(-360,70)],fill=255)          # body
        d.polygon([R(-360,-70),R(-390,-55),R(-390,55),R(-360,70)],fill=255)
        d.polygon([R(75,-64),R(250,-58),R(250,58),R(75,64)],fill=255)            # grip
        for gx in (110,150,190,230): d.line([R(gx,-60),R(gx,60)],fill=0,width=10)
        d.polygon([R(265,-52),R(345,-26),R(345,26),R(265,52)],fill=255)          # cartridge
        d.line([R(345,0),R(430,0)],fill=255,width=16)                              # needle
        d.line([R(-250,-70),R(-250,70)],fill=0,width=12); d.line([R(60,-70),R(60,70)],fill=0,width=14)
        d.ellipse([R(-120,0)[0]-22,R(-120,0)[1]-22,R(-120,0)[0]+22,R(-120,0)[1]+22],fill=0)
    elif kind=="emblem":
        ring(420,w); ring(300,max(8,w//2))
        f=ImageFont.truetype("/home/claude/fonts/Oswald.ttf",88); f.set_variation_by_axes([600])
        for txt,start,dirn in (("ТАТУ · KAISHI",-math.pi/2,1),):
            pass
        text="ТАТУ ✦ KAISHI ✦ ТАШКЕНТ ✦ "
        dj=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",60)
        n=len(text)
        for i,ch in enumerate(text):
            ang=-math.pi/2+i*2*math.pi/n
            tile=Image.new("L",(160,160),0); td=ImageDraw.Draw(tile)
            fo=dj if ch=="✦" else f
            tw=td.textlength(ch,font=fo); td.text((80-tw/2,30),ch,font=fo,fill=255)
            tile=tile.rotate(-math.degrees(ang)-90,resample=Image.BICUBIC)
            px=c+360*math.cos(ang)-80; py=c+360*math.sin(ang)-80
            im.paste(255,(int(px),int(py)),tile)
        sub=icon_layer("pen",size=int(size*0.55),wd=wd).resize((int(S*0.55),int(S*0.55)))
        im.paste(255,(int(c-sub.width/2),int(c-sub.height/2)),sub)
    elif kind=="stars3":
        for k,(dx,dy,rr) in enumerate([(-230,40,95),(0,-40,130),(230,40,95)]):
            pts=[]
            for i in range(10):
                r_=rr if i%2==0 else rr*.42; a=-math.pi/2+i*math.pi/5
                pts.append((c+dx+r_*math.cos(a),c+dy+r_*math.sin(a)))
            d.polygon(pts,fill=255)
    elif kind=="drop":
        top=(c,c-270); r=180; cc=(c,c+60)
        a0=math.asin(r/(cc[1]-top[1]))
        arc=[(cc[0]+r*math.cos(th),cc[1]+r*math.sin(th)) for th in [(-a0)+(math.pi+2*a0)*k/100 for k in range(101)]]
        d.line([top]+arc+[top],fill=255,width=w,joint="curve")
    elif kind=="pencil":
        a=math.radians(-45); ca,sa=math.cos(a),math.sin(a)
        def R(px,py): return (c+px*ca-py*sa, c+px*sa+py*ca)
        d.polygon([R(-260,-55),R(140,-55),R(140,55),R(-260,55)],outline=255,width=w)
        d.polygon([R(140,-55),R(270,0),R(140,55)],outline=255,width=w)
        L([R(-190,-55),R(-190,55)])
    elif kind=="heart":
        pts=[]
        for k in range(300):
            t=k/300*2*math.pi; x=16*math.sin(t)**3; y=13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t)
            pts.append((c+x*15,c-y*15-10))
        d.line(pts+[pts[0]],fill=255,width=w,joint="curve")
    elif kind=="cup":
        d.rounded_rectangle((c-200,c-110,c+120,c+220),radius=44,outline=255,width=w)
        d.arc((c+50,c-50,c+240,c+140),start=-90,end=90,fill=255,width=w)
        for xx in (c-100,c-40,c+20): d.arc((xx-30,c-280,xx+30,c-150),start=120,end=240,fill=255,width=w-8)
    elif kind=="bolt":
        d.polygon([(c+40,c-300),(c-170,c+40),(c-10,c+40),(c-60,c+300),(c+170,c-60),(c+10,c-60)],outline=255,width=w)
    elif kind=="note":
        L([(c-60,c+160),(c-60,c-230),(c+190,c-280),(c+190,c+110)])
        d.ellipse((c-200,c+100,c-40,c+220),fill=255); d.ellipse((c+50,c+50,c+210,c+170),fill=255)
    elif kind=="smile":
        ring(250,w); d.ellipse((c-110,c-90,c-60,c-40),fill=255); d.ellipse((c+60,c-90,c+110,c-40),fill=255)
        d.arc((c-150,c-120,c+150,c+150),start=25,end=155,fill=255,width=w)
    return im.resize((size,size),Image.LANCZOS)
def glow_icon(base,kind,center,size,col=(255,255,255),glow=(190,140,255)):
    m=icon_layer(kind,size)
    x0,y0=int(center[0]-size/2),int(center[1]-size/2)
    big=Image.new("L",base.size,0); big.paste(m,(x0,y0))
    g1=big.filter(ImageFilter.GaussianBlur(30)); g2=big.filter(ImageFilter.GaussianBlur(10))
    out=base.convert("RGB")
    for g,cl,k in ((g1,glow,1.0),(g2,glow,0.8)):
        layer=Image.new("RGB",base.size,cl); out=Image.composite(ImageChops.add(out,ImageChops.multiply(layer,Image.merge("RGB",(g,g,g)))),out,Image.new("L",base.size,255))
    out.paste(Image.new("RGB",base.size,col),(0,0),big)
    return out
