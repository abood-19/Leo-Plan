import sys; sys.path.insert(0,'/home/claude/leo3')
from sigil import render
from glyphs import GL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BG=(6,4,10); OUT="/home/claude/leo3/pack/"
VIO=((95,20,255),(170,60,255),(235,190,255)); MAG=((190,20,170),(255,70,205),(255,205,240))
OS="/home/claude/fonts/Oswald.ttf"; IN="/home/claude/fonts/Inter.ttf"
def F(p,s,w):
    f=ImageFont.truetype(p,s); f.set_variation_by_axes([w] if p==OS else [32,w]); return f
def cover(key,path,hue,size=980):
    im=Image.new("RGB",(1080,1920),BG); g=render(GL[key],hue=hue,size=size)
    im.paste(g,((1080-size)//2,(1920-size)//2)); im.save(OUT+path)
for k,p in [("З","Запись"),("Р","Работы"),("Э","Эскизы"),("stars","Отзывы"),("У","Уход"),("Л","Обо_мне")]:
    n={"Запись":"03","Работы":"01","Эскизы":"02","Отзывы":"04","Уход":"05","Обо_мне":"06"}[p]
    cover(k,f"1_tattoo_account/highlights/{n}_{p}.png",VIO)
for k,p in [("Т","01_Тату"),("Я","02_Я"),("Б","03_Будни"),("В","04_Вайб"),("note","05_Музыка")]:
    cover(k,f"2_personal_account/highlights/{p}.png",MAG)
def glowtext(im,xy,text,font,col,glow):
    lay=Image.new("RGB",im.size,(0,0,0)); d=ImageDraw.Draw(lay); d.text(xy,text,font=font,fill=glow)
    b=lay.filter(ImageFilter.GaussianBlur(18))
    from PIL import ImageChops
    im.paste(ImageChops.add(im,b)); ImageDraw.Draw(im).text(xy,text,font=font,fill=col)
def ctext(im,y,t,f,col,glow=None):
    d=ImageDraw.Draw(im); x=(1080-d.textlength(t,font=f))/2
    if glow: glowtext(im,(x,y),t,f,col,glow)
    else: d.text((x,y),t,font=f,fill=col)
# artist story
im=Image.new("RGB",(1080,1920),BG); g=render(GL["Л"],hue=VIO,size=900); im.paste(g,(90,260))
ctext(im,1200,"ТАТУ-МАСТЕР",F(OS,120,700),(244,238,255),(140,50,255))
ctext(im,1350,"Ташкент · эскизы под тебя",F(IN,44,400),(190,175,225))
ctext(im,1700,"@kaishi_tattoo",F(IN,40,500),(170,90,255))
im.save(OUT+"1_tattoo_account/stories/00_Тату-мастер.png")
# reviews story with stars
im=Image.new("RGB",(1080,1920),BG); g=render(GL["stars"],hue=VIO,size=1000); im.paste(g,(40,-60))
ctext(im,700,"ОТЗЫВЫ",F(OS,110,700),(244,238,255),(140,50,255))
d=ImageDraw.Draw(im); d.rounded_rectangle((96,880,984,1560),radius=30,outline=(170,90,255),width=4)
ctext(im,1195,"сюда скриншот отзыва",F(IN,36,500),(165,152,196))
ctext(im,1640,"Спасибо, что доверяете мне свою кожу",F(IN,40,400),(220,210,240))
im.save(OUT+"1_tattoo_account/stories/03_Отзыв.png")
# personal music story with note
im=Image.new("RGB",(1080,1920),BG); g=render(GL["note"],hue=MAG,size=760); im.paste(g,(160,240))
ctext(im,1050,"МОЯ МУЗЫКА",F(OS,110,700),(255,236,250),(230,40,190))
ctext(im,1190,"канал в Telegram",F(IN,44,400),(220,190,215))
d=ImageDraw.Draw(im); d.rounded_rectangle((96,1380,984,1560),radius=28,outline=(255,70,205),width=4)
ctext(im,1448,"место для ссылки",F(IN,36,500),(200,160,195))
ctext(im,1610,"t.me/music_stayleo",F(IN,36,400),(200,160,195))
im.save(OUT+"2_personal_account/stories/03_Моя_музыка.png")
# personal "my tattoos" story
im=Image.new("RGB",(1080,1920),BG); g=render(GL["Т"],hue=MAG,size=760); im.paste(g,(160,240))
ctext(im,1050,"МОИ ТАТУ — ТАМ",F(OS,100,700),(255,236,250),(230,40,190))
ctext(im,1185,"работы, эскизы и запись",F(IN,44,400),(220,190,215))
d=ImageDraw.Draw(im); d.rounded_rectangle((96,1380,984,1560),radius=28,outline=(255,70,205),width=4)
ctext(im,1448,"место для @kaishi_tattoo",F(IN,36,500),(200,160,195))
im.save(OUT+"2_personal_account/stories/01_Мои_тату_там.png")
print("covers ok")
