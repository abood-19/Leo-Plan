import math, os
from PIL import Image, ImageDraw, ImageFont, ImageOps
OS="/home/claude/fonts/Oswald.ttf"; IN="/home/claude/fonts/Inter.ttf"
BG=(6,4,10); P=(22,13,36); R=(170,90,255); R2=(110,40,200); T=(244,238,255); M=(165,152,196)
OUT="/home/claude/leo3/pack"
def F(path,size,w):
    f=ImageFont.truetype(path,size)
    try: f.set_variation_by_axes([w] if path==OS else [32,w])
    except Exception as e: print("var",e)
    return f
def tw(d,t,f): return d.textlength(t,font=f)
def save(im,name): os.makedirs(os.path.dirname(f"{OUT}/{name}"),exist_ok=True); im.save(f"{OUT}/{name}")

# ---------- icons on 2x canvas ----------
def icon(d,kind,cx,cy,col,w=26):
    L=lambda pts: d.line(pts,fill=col,width=w,joint="curve")
    if kind=="machine":
        d.rounded_rectangle((cx-70,cy-260,cx+70,cy+40),radius=40,outline=col,width=w)
        for y in (cy-170,cy-110,cy-50): L([(cx-70,y),(cx+70,y)])
        d.polygon([(cx-50,cy+40),(cx+50,cy+40),(cx,cy+170)],outline=col,width=w)
        L([(cx,cy+170),(cx,cy+250)])
        d.ellipse((cx-22,cy+275,cx+22,cy+319),fill=R)
    elif kind=="pencil":
        a=math.radians(-45); 
        def rot(x,y): return (cx+x*math.cos(a)-y*math.sin(a), cy+x*math.sin(a)+y*math.cos(a))
        body=[rot(-230,-55),rot(140,-55),rot(140,55),rot(-230,55)]
        d.polygon(body,outline=col,width=w)
        tip=[rot(140,-55),rot(260,0),rot(140,55)]
        d.polygon(tip,outline=col,width=w)
        L([rot(-160,-55),rot(-160,55)])
        d.ellipse([rot(260,0)[0]-20,rot(260,0)[1]-20,rot(260,0)[0]+20,rot(260,0)[1]+20],fill=R)
    elif kind=="calendar":
        d.rounded_rectangle((cx-230,cy-190,cx+230,cy+220),radius=36,outline=col,width=w)
        L([(cx-230,cy-80),(cx+230,cy-80)])
        for x in (cx-110,cx+110): L([(x,cy-250),(x,cy-140)])
        d.line([(cx-95,cy+70),(cx-20,cy+140),(cx+110,cy-10)],fill=R,width=w+6,joint="curve")
    elif kind=="review":
        d.rounded_rectangle((cx-250,cy-200,cx+250,cy+130),radius=60,outline=col,width=w)
        d.polygon([(cx-120,cy+125),(cx-40,cy+125),(cx-140,cy+240)],fill=col)
        pts=[]
        for i in range(10):
            r=95 if i%2==0 else 40; ang=-math.pi/2+i*math.pi/5
            pts.append((cx+r*math.cos(ang),cy-35+r*math.sin(ang)))
        d.polygon(pts,fill=R)
    elif kind=="drop":
        pts=[]
        for i in range(0,181):
            t=math.radians(i*2)
            r=190
            if i<=90: # bottom circle half via param
                pass
        # build droplet: top point + circle
        top=(cx,cy-270); c=(cx,cy+70); r=190
        ang0=math.asin(r/ (cy+70-(cy-270)))
        pts=[top]
        for k in range(0,101):
            th=math.pi/2+ang0 - k*(2*(math.pi/2+ang0)-2*0)/100  # sweep
        arc=[]
        start=-math.pi/2+ (math.pi/2-ang0)
        # tangent angle points
        a1=-ang0+0; 
        for k in range(101):
            th=(-math.pi/2+ (math.pi/2-ang0)) - 0 + k*( (2*math.pi - 2*(math.pi/2-ang0)) )/100
        arc=[(c[0]+r*math.cos(th),c[1]+r*math.sin(th)) for th in [(-ang0)+(math.pi+2*ang0)*k/100 for k in range(101)]]
        d.line([top]+arc+[top],fill=col,width=w,joint="curve")
        d.arc((cx-110,cy-10,cx+110,cy+210),start=100,end=170,fill=R,width=w)
    elif kind=="cup":
        d.rounded_rectangle((cx-190,cy-120,cx+130,cy+210),radius=40,outline=col,width=w)
        d.arc((cx+60,cy-60,cx+250,cy+130),start=-90,end=90,fill=col,width=w)
        for x in (cx-90,cx-30,cx+30):
            d.arc((x-30,cy-280,x+30,cy-150),start=120,end=240,fill=R,width=w-6)
    elif kind=="note":
        L([(cx-60,cy+160),(cx-60,cy-230),(cx+190,cy-280),(cx+190,cy+110)])
        d.ellipse((cx-200,cy+100,cx-40,cy+220),fill=col)
        d.ellipse((cx+50,cy+50,cx+210,cy+170),fill=R)
    elif kind=="arrow":
        L([(cx-220,cy),(cx+200,cy)]); L([(cx+80,cy-120),(cx+220,cy),(cx+80,cy+120)])

def highlight(kind,name,theme="dark",photo=None,bw=False):
    W,H=2160,3840; bg=BG if theme=="dark" else T
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    cx,cy=W//2,H//2
    disc=P if theme=="dark" else P
    d.ellipse((cx-560,cy-560,cx+560,cy+560),fill=disc)
    d.ellipse((cx-600,cy-600,cx+600,cy+600),outline=R,width=10)
    if photo:
        ph=Image.open(photo).convert("RGB")
        if bw: ph=ImageOps.grayscale(ph).convert("RGB")
        s=1100; ph=ImageOps.fit(ph,(s,s),centering=(0.5,0.28))
        mask=Image.new("L",(s,s),0); ImageDraw.Draw(mask).ellipse((0,0,s,s),fill=255)
        im.paste(ph,(cx-s//2,cy-s//2),mask)
    else:
        icon(d,kind,cx,cy,T if theme=="dark" else BG)
    im=im.resize((1080,1920),Image.LANCZOS); save(im,name)

LEO="/home/claude/site/img/leo.jpg"
H=[("machine","1_tattoo_account/highlights/01_Работы.png"),("pencil","1_tattoo_account/highlights/02_Эскизы.png"),
   ("calendar","1_tattoo_account/highlights/03_Запись.png"),("review","1_tattoo_account/highlights/04_Отзывы.png"),
   ("drop","1_tattoo_account/highlights/05_Уход.png")]
for k,n in H: highlight(k,n)
highlight(None,"1_tattoo_account/highlights/06_Обо_мне.png",photo=LEO)
P2=[("machine","2_personal_account/highlights/01_Тату.png"),("cup","2_personal_account/highlights/03_Будни.png"),("note","2_personal_account/highlights/04_Вайб.png")]
for k,n in P2: highlight(k,n,theme="light")
highlight(None,"2_personal_account/highlights/02_Я.png",theme="light",photo=LEO,bw=True)

# ---------- shared layout bits ----------
MX=96
def topbar(d,W,label,y=170,col=M):
    f=F(OS,34,500); d.text((MX,y),"ЛЕО  TATTOO",font=f,fill=T)
    d.rectangle((MX,y+58,MX+60,y+64),fill=R)
    if label:
        x=W-MX-tw(d,label,f); d.text((x,y),label,font=f,fill=col)
def big(d,x,y,lines,size,cols=None,lh=1.02):
    f=F(OS,size,700)
    bot=y
    for i,l in enumerate(lines):
        d.text((x,y+i*int(size*lh)),l,font=f,fill=(cols[i] if cols else T))
        bot=d.textbbox((x,y+i*int(size*lh)),l,font=f)[3]
    return bot
def wrap(d,text,f,maxw):
    out=[];line=""
    for w in text.split():
        t=(line+" "+w).strip()
        if tw(d,t,f)<=maxw: line=t
        else: out.append(line); line=w
    out.append(line); return out
def para(d,x,y,text,size,col=T,maxw=880,w=400,lh=1.4):
    f=F(IN,size,w)
    for l in wrap(d,text,f,maxw): d.text((x,y),l,font=f,fill=col); y+=int(size*lh)
    return y

# ---------- stories 1080x1920 ----------
def story_booking():
    W,Hh=1080,1920; im=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(im)
    topbar(d,W,"ЗАПИСЬ")
    y=big(d,MX,330,["ЗАПИСЬ","ОТКРЫТА"],170,[T,R])
    y=para(d,MX,y+30,"Выбери день на сайте, заявка сразу придёт мне в Telegram.",42,M)
    steps=[("01","Открой ссылку ниже"),("02","Опиши идею и место"),("03","Выбери день: Вс–Чт")]
    y+=50
    for n,s in steps:
        d.text((MX,y),n,font=F(OS,46,600),fill=R); d.text((MX+110,y+4),s,font=F(IN,44,500),fill=T)
        y+=96; d.line((MX,y-24,W-MX,y-24),fill=(40,28,60),width=2)
    by=1340
    d.rounded_rectangle((MX,by,W-MX,by+190),radius=28,outline=R,width=4)
    t="место для ссылки"; f=F(IN,36,500); d.text(((W-tw(d,t,f))/2,by+72),t,font=f,fill=M)
    t="leotattoouz-gif.github.io/Leo.Tattoo"; f=F(IN,30,400); d.text(((W-tw(d,t,f))/2,by+230),t,font=f,fill=M)
    save(im,"1_tattoo_account/stories/01_Запись_открыта.png")
def story_dates():
    W,Hh=1080,1920; im=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(im)
    topbar(d,W,"НЕДЕЛЯ")
    big(d,MX,330,["СВОБОДНЫЕ","ДАТЫ"],150,[T,R])
    days=["ВС","ПН","ВТ","СР","ЧТ"]; y=720
    for dd in days:
        d.rounded_rectangle((MX,y,W-MX,y+130),radius=22,fill=P)
        d.text((MX+40,y+30),dd,font=F(OS,60,600),fill=T)
        d.text((MX+190,y+42),"__.__",font=F(IN,44,400),fill=M)
        d.rounded_rectangle((W-MX-230,y+30,W-MX-40,y+100),radius=35,outline=R,width=4)
        f=F(IN,30,500); t="свободно"; d.text((W-MX-135-tw(d,t,f)/2,y+46),t,font=f,fill=T)
        y+=158
    para(d,MX,1560,"Зачеркни занятые дни. Запись по ссылке в профиле.",38,M)
    save(im,"1_tattoo_account/stories/02_Свободные_даты.png")
def story_review():
    W,Hh=1080,1920; im=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(im)
    topbar(d,W,"ОТЗЫВ")
    big(d,MX,330,["СЛОВА","КЛИЕНТА"],150,[T,R])
    d.rounded_rectangle((MX,700,W-MX,1450),radius=30,fill=P)
    f=F(IN,34,500); t="сюда скриншот отзыва"; d.text(((W-tw(d,t,f))/2,1055),t,font=f,fill=M)
    para(d,MX,1520,"Спасибо, что доверяете мне свою кожу.",40,T)
    save(im,"1_tattoo_account/stories/03_Отзыв.png")
def story_link_personal():
    W,Hh=1080,1920; im=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(im)
    f=F(OS,34,500); d.text((MX,170),"WENX.XZ_",font=f,fill=T); d.rectangle((MX,228,MX+60,234),fill=R)
    big(d,MX,330,["МОИ ТАТУ","ЖИВУТ","ТАМ"],160,[T,T,R])
    y=para(d,MX,880,"Работы, эскизы и запись — в отдельном аккаунте.",42,M)
    d.rounded_rectangle((MX,1150,W-MX,1330),radius=28,outline=R,width=4)
    t="место для @упоминания"; f=F(IN,36,500); d.text(((W-tw(d,t,f))/2,1218),t,font=f,fill=M)
    save(im,"2_personal_account/stories/01_Мои_тату_там.png")
for fn in (story_booking,story_dates,story_review,story_link_personal): fn()

# ---------- carousel 1080x1350 ----------
def slide(lines,cols,sub,idx,total,name,size=150,foot="листай →"):
    W,Hh=1080,1350; im=Image.new("RGB",(W,Hh),BG); d=ImageDraw.Draw(im)
    topbar(d,W,f"{idx:02d} / {total:02d}",y=96)
    if 1<idx and ("kak_" in name or "5_vop" in name):
        fn=F(OS,420,700); n=f"{idx-1}"; d.text((W-MX-tw(d,n,fn),180),n,font=fn,fill=(30,18,52))
    y=big(d,MX,560 if size>=170 else 420,lines,size,cols)
    if sub: para(d,MX,y+44,sub,46,M,maxw=820)
    f=F(IN,32,500); d.text((MX,Hh-140),"@kaishi_tattoo · Ташкент",font=f,fill=M)
    if foot: t=foot; d.text((W-MX-tw(d,t,f),Hh-140),t,font=f,fill=R)
    save(im,name)
C="1_tattoo_account/carousels/kak_zapisatsya/"
slide(["КАК","ЗАПИСАТЬСЯ","НА ТАТУ"],[T,T,R],"Четыре шага. Займёт пару минут.",1,5,C+"01.png",140)
slide(["ИДЕЯ"],[R],"Напиши, что хочешь, где и примерный размер. Можно прислать референсы.",2,5,C+"02.png",200)
slide(["ЭСКИЗ"],[R],"Я рисую эскиз под тебя и называю цену. Правим, пока не понравится.",3,5,C+"03.png",200)
slide(["ДЕНЬ"],[R],"Выбираешь свободный день: воскресенье — четверг.",4,5,C+"04.png",200)
slide(["ЗАПИСЬ","НА САЙТЕ"],[T,R],"Ссылка в профиле. Заявка сразу приходит мне в Telegram.",5,5,C+"05.png",160,foot="ссылка в профиле")
slide(["ЭСКИЗЫ","НЕДЕЛИ"],[T,R],"Каждый бью один раз. Пиши номер в Direct.",1,6,"1_tattoo_account/carousels/eskizy_nedeli_cover.png",170)

# ---------- reel cover overlays (transparent, 1080x1920, label inside 4:5 safe zone) ----------
def overlay(label,num,name,light=False):
    W,Hh=1080,1920; im=Image.new("RGBA",(W,Hh),(0,0,0,0)); d=ImageDraw.Draw(im)
    top=(Hh-1350)//2
    # gradient bottom for legibility
    for i in range(420):
        a=int(200*(i/420)); d.line((0,top+1350-420+i,W,top+1350-420+i),fill=(6,4,10,a))
    f=F(OS,110,700); y=top+1350-260
    d.rectangle((MX,y-34,MX+70,y-26),fill=R+(255,))
    d.text((MX,y),label,font=f,fill=T+(255,))
    if num: 
        f2=F(OS,44,500); d.text((W-MX-tw(d,num,f2),y+50),num,font=f2,fill=M+(255,))
    save(im,name)
for lab,fn in [("ПРОЦЕСС","01_Процесс"),("ДО / ПОСЛЕ","02_До_после"),("ЭСКИЗ","03_Эскиз"),("ВОПРОС","04_Вопрос")]:
    overlay(lab,"№__","1_tattoo_account/reel_covers/"+fn+".png")
for lab,fn in [("БУДНИ","01_Будни"),("МЫСЛИ","02_Мысли"),("ВАЙБ","03_Вайб")]:
    overlay(lab,"","2_personal_account/reel_covers/"+fn+".png")
print("ok")

# ================= v3 additions =================
def spark(d,cx,cy,col,w=26):
    pts=[]
    for i in range(8):
        r=250 if i%2==0 else 70; a=-math.pi/2+i*math.pi/4
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    d.polygon(pts,outline=col,width=w)
    d.ellipse((cx+150,cy-260,cx+210,cy-200),fill=R)
_old_icon=icon
def icon(d,kind,cx,cy,col,w=26):
    if kind=="spark": return spark(d,cx,cy,col,w)
    return _old_icon(d,kind,cx,cy,col,w)
highlight("spark","2_personal_account/highlights/04_Вайб.png",theme="light")
highlight("note","2_personal_account/highlights/05_Музыка.png",theme="light")

def base(light=False,label=None,handle="ЛЕО  TATTOO"):
    W,Hh=1080,1920; im=Image.new("RGB",(W,Hh),T if light else BG); d=ImageDraw.Draw(im)
    fg=BG if light else T
    f=F(OS,34,500); d.text((MX,170),handle,font=f,fill=fg); d.rectangle((MX,228,MX+60,234),fill=R)
    if label: d.text((W-MX-tw(d,label,f),170),label,font=f,fill=M if not light else M)
    return im,d,fg
def frame(d,box,txt,light=False):
    d.rounded_rectangle(box,radius=28,outline=R,width=4)
    f=F(IN,34,500); x0,y0,x1,y1=box
    d.text(((x0+x1-tw(d,txt,f))/2,(y0+y1)/2-20),txt,font=f,fill=M if light else M)

# Уход
im,d,fg=base(label="УХОД")
y=big(d,MX,330,["УХОД","ЗА ТАТУ"],150,[T,R])
rows=[("2–4 ч","Снять плёнку"),("2× в день","Мыть тёплой водой и мылом без запаха"),("тонко","Заживляющий крем"),("2 недели","Без бассейна, сауны и солнца"),("никогда","Не чесать и не сдирать корочки")]
y+=70
for a,b in rows:
    d.text((MX,y),a,font=F(OS,38,600),fill=R)
    yy=para(d,MX+250,y+6,b,40,T,maxw=W-MX*2-250 if False else 640)
    y=max(y+70,yy)+30; d.line((MX,y-22,1080-MX,y-22),fill=(40,28,60),width=2)
para(d,MX,1640,"Вопрос по заживлению — пиши в Direct.",38,M)
save(im,"1_tattoo_account/stories/04_Уход.png")

# Обо мне
im,d,fg=base(label="ОБО МНЕ")
ph=ImageOps.fit(Image.open(LEO).convert("RGB"),(888,700),centering=(0.5,0.3))
im.paste(ph,(MX,300))
d.rectangle((MX,300,MX+888,1000),outline=R,width=3)
y=big(d,MX,1060,["Я ЛЕО"],140,[T])
y=para(d,MX,y+30,"Тату-мастер из Ташкента. Каждый эскиз рисую сам, под одного человека.",42,M,maxw=880)
frame(d,(MX,1560,1080-MX,1720),"место для @wenx.xz_")
save(im,"1_tattoo_account/stories/05_Обо_мне.png")

# Ответ на вопрос
im,d,fg=base(label="ВОПРОС")
big(d,MX,330,["ТЫ","СПРОСИЛ"],150,[T,R])
frame(d,(MX,700,1080-MX,1060),"сюда стикер с вопросом")
d.text((MX,1140),"ОТВЕТ",font=F(OS,60,700),fill=R)
for k in range(4): d.line((MX,1270+k*95,1080-MX,1270+k*95),fill=(50,34,33),width=2)
save(im,"1_tattoo_account/stories/06_Ответ.png")

# Personal: новая работа (repost frame)
im,d,fg=base(light=False,label="ТАТУ",handle="WENX.XZ_")
big(d,MX,330,["НОВАЯ","РАБОТА"],150,[BG,R])
frame(d,(MX,700,1080-MX,1540),"сюда репост поста",light=False)
para(d,MX,1600,"Больше работ — @kaishi_tattoo",40,M)
save(im,"2_personal_account/stories/02_Новая_работа.png")

# Personal: моя музыка
im,d,fg=base(light=False,label="МУЗЫКА",handle="WENX.XZ_")
big(d,MX,330,["ПОД ЭТО","Я БЬЮ","ТАТУ"],150,[BG,BG,R])
para(d,MX,860,"Мой музыкальный канал в Telegram.",42,M)
frame(d,(MX,1150,1080-MX,1330),"место для ссылки",light=False)
para(d,MX,1380,"t.me/music_stayleo",36,M)
save(im,"2_personal_account/stories/03_Моя_музыка.png")

# Carousel: 5 вопросов перед первой тату
C2="1_tattoo_account/carousels/5_voprosov/"
slide(["5 ВОПРОСОВ","ПЕРЕД","ПЕРВОЙ ТАТУ"],[T,T,R],"Сохрани, пригодится перед сеансом.",1,6,C2+"01.png",130)
QA=[("БОЛЬНО?","Терпимо. Зависит от места: рука — легче, рёбра и стопа — сильнее."),
    ("СКОЛЬКО ЖИВЁТ?","Всю жизнь. Через годы линии могут чуть расплыться, это нормально."),
    ("КАК ГОТОВИТЬСЯ?","Выспаться, поесть, не пить алкоголь накануне."),
    ("СКОЛЬКО ЗАЖИВАЕТ?","Обычно 2–4 недели. Уход — в хайлайте «Уход»."),
    ("С ЧЕГО НАЧАТЬ?","Напиши идею и место. Эскиз нарисую под тебя.")]
for k,(q,a) in enumerate(QA,2):
    slide([q],[R],a,k,6,C2+f"0{k}.png",104 if len(q)>10 else 150,foot="листай →" if k<6 else "ссылка в профиле")
print("v3 ok")
