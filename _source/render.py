import os, shutil, html, sys
sys.path.insert(0,"/home/claude/leo2")
from content import *
from PIL import Image, ImageOps
e=html.escape
PACKDIR="/home/claude/leo2/pack"

def build(L, out):
    i = 0 if L=="ru" else 1
    t=lambda p: p[i]
    shutil.rmtree(out,ignore_errors=True); os.makedirs(out+"/img")
    # images
    IMG={}; n=0
    for g in PACK:
        for it in g[2]:
            n+=1; a=f"img/{n:02d}.png"; shutil.copy(f"{PACKDIR}/{it[0]}",out+"/"+a); IMG[it[0]]=a
    ph=ImageOps.fit(Image.open("/home/claude/site/img/leo.jpg").convert("RGB"),(720,960),centering=(0.5,0.3))
    ph.save(out+"/img/leo.jpg",quality=86)
    rtl = L=="ar"
    SHORT={"Пятница":"Пт","Суббота":"Сб","Воскресенье":"Вс","Понедельник":"Пн","Вторник":"Вт","Среда":"Ср","Четверг":"Чт"}
    def copyblock(c,k):
        where,desc,text=c
        return f'''<article class="cb"><div class="cb-h"><div class="cb-w"><span class="lbl">{e(t(META["where"]))}</span><span class="wt">{e(t(where))}</span></div><button class="copy" type="button" aria-label="{e(t(META["copy"]))}: {e(t(where))}">{e(t(META["copy"]))}</button></div><p class="cb-d">{e(t(desc))}</p><pre class="cb-t" dir="auto">{e(t(text))}</pre></article>'''
    def sec(id,num,title,lead,body):
        return f'<section id="{id}"><header class="sh"><span class="sn" aria-hidden="true">{num}</span><div><h2>{e(title)}</h2>{f"<p>{e(lead)}</p>" if lead else ""}</div></header>{body}</section>'
    # strategy
    st='<div class="strat">'+"".join(f'<article class="sc"><span class="scn">{k:02d}</span><h3>{e(t(h))}</h3><ul>'+"".join(f"<li>{e(x)}</li>" for x in t(b).split("\n"))+'</ul></article>' for k,(h,b) in enumerate(STRATEGY,1))+'</div>'
    S=[]
    S.append(sec("strategy","01",t(("Стратегия","الاستراتيجية")),t(("Как мы ведём оба аккаунта. Прочитай один раз целиком.","كيف منمشي الحسابين. يقرأها ليو مرة وحدة كاملة.")),st))
    tb='<div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(NAME[:1]+TATTOO))+'</div>'
    S.append(sec("tattoo","02","@kaishi_tattoo",t(("Тату-аккаунт. Всё, что меняем в профиле, по порядку.","حساب التاتو. كل التعديلات بالبروفايل بالترتيب.")),tb))
    pb=f'<div class="duo"><article class="sc warn"><h3>{e(t(PERSONAL_NOTE[0]))}</h3><p>{e(t(PERSONAL_NOTE[1]))}</p></article><article class="sc"><h3>{e(t(PERSONAL_FORMULA[0]))}</h3><ul>'+"".join(f"<li>{e(x)}</li>" for x in t(PERSONAL_FORMULA[1]).split("\n"))+'</ul></article></div>'
    pb+='<div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(NAME[1:]+PERSONAL))+'</div>'
    S.append(sec("personal","04","@wenx.xz_",t(("Личный аккаунт. Новая схема публикаций и связка с тату.","الحساب الشخصي. طريقة نشر جديدة وربط مع التاتو.")),pb))
    # week
    acc={"tattoo":("тату","تاتو"),"personal":("личный","شخصي"),"prep":("подготовка","تجهيز")}
    def weekhtml(W,routine):
        wk=""
        if routine: wk+=f'<article class="routine"><h3>{e(t(DAILY[0]))}</h3><ol>'+"".join(f'<li><time>{e(tm)}</time><span>{e(t(x))}</span></li>' for tm,x in DAILY[1])+'</ol></article>'
        wk+='<nav class="days" aria-label="days">'+"".join(f'<a href="#{d[0]}"><b>{e(t(d[1]))}</b><span>{e(SHORT.get(t(d[2]),t(d[2])))}</span></a>' for d in W)+'</nav>'
        for d in W:
            did,dt,wd,ti,accs,tasks,texts=d
            chips="".join(f'<span class="chip {a}">{e(t(acc[a]))}</span>' for a in accs)
            tl="".join(f'<li><label><input type="checkbox" id="{did}-{k}" data-day="{did}"><span class="box" aria-hidden="true"></span><time>{e(tm)}</time><span class="tx">{e(t(x))}</span></label></li>' for k,(tm,x) in enumerate(tasks))
            tx=('<div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(texts))+'</div>') if texts else ""
            wk+=f'''<article class="day" id="{did}"><div class="day-h"><div class="dd"><span class="dn">{e(t(dt))}</span><span class="dw">{e(t(wd))}</span></div><div class="dt"><h3>{e(t(ti))}</h3><div class="chips">{chips}</div></div><div class="prog" data-day="{did}"><span class="pc">0/{len(tasks)}</span><span class="pb"><i></i></span></div></div><ul class="tasks">{tl}</ul>{tx}</article>'''
        return wk
    # highlight map
    def hmap(accn):
        h='<div class="hmap">'
        for a_,nm,cov,stories in HMAP:
            if a_!=accn: continue
            h+=f'<div class="hrow"><div class="hcov"><a href="{IMG[cov]}" target="_blank" rel="noopener"><img src="{IMG[cov]}" alt="{e(t(nm))}" loading="lazy"></a><b>{e(t(nm))}</b></div><div class="hst">'
            for f,cap in stories:
                if f: h+=f'<figure><a href="{IMG[f]}" target="_blank" rel="noopener"><img src="{IMG[f]}" alt="{e(t(cap))}" loading="lazy"></a><figcaption>{e(t(cap))}</figcaption></figure>'
                else: h+=f'<div class="hph">{e(t(cap))}</div>'
            h+='</div></div>'
        return h+'</div>'
    hm=f'<h3 class="gt">@kaishi_tattoo</h3>'+hmap("tattoo")+f'<h3 class="gt">@wenx.xz_</h3>'+hmap("personal")
    S.insert(2,sec("highlights","03",t(("Хайлайты","الهايلايتس")),t(("Оба аккаунта: порядок слева направо, обложка и что лежит внутри.","الحسابين: الترتيب من الشمال لليمين، الغلاف، وشو جوّا كل واحد.")),hm))
    lb=f'<article class="sc warn solo"><h3>{e(t(LNK_NOTE[0]))}</h3><p>{e(t(LNK_NOTE[1]))}</p></article><div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(LNK))+'</div>'
    S.append(sec("lnk","05","lnk.bio",t(("Страница со всеми ссылками. Главное — запись на тату первой строкой.","صفحة كل الروابط. الأهم: الحجز أول سطر.")),lb))
    S.append(sec("direct","06","Direct",t(("Готовые ответы. Сохрани их в «Быстрые ответы», чтобы вставлять в одно касание.","ردود جاهزة. تنحفظ بـ «الردود السريعة» عشان تنحط بكبسة.")),'<div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(DM))+'</div>'))
    S.append(sec("tags","07",t(("Хэштеги","الهاشتاقات")),t(("3–5 на пост. Всегда базовые три плюс хэштеги рубрики.","٣–٥ بكل منشور. الأساسية الثلاثة دايماً وزيادة هاشتاقات الفقرة.")),'<div class="cbs">'+"".join(copyblock(c,k) for k,c in enumerate(TAGS))+'</div>'))
    S.append(sec("week","08",t(("Неделя 1 · 13–21 ноября","الأسبوع ١ · ١٣–٢١ نوفمبر")),t(("Фундамент. Что сделать и во сколько, какие тексты куда. Галочки сохраняются.","الأساس. شو يعمل وإيمتى، وأي نص لوين. علامات الصح بتنحفظ.")),weekhtml(WEEK,True)))
    S.append(sec("week2","09",t(("Неделя 2 · 22–28 ноября","الأسبوع ٢ · ٢٢–٢٨ نوفمبر")),t(("Ритм. Первые рубрики ВОПРОС и ДО / ПОСЛЕ, карусель с пользой, первая работа в ленте.","الإيقاع. أول فقرة ВОПРОС و ДО / ПОСЛЕ، كاروسيل مفيد، وأول شغل بالصفحة.")),weekhtml(WEEK2,False)))
    ih='<div class="ideas">'+"".join(f'<article class="idea"><div class="ih"><span class="chip {a_}">{e(r_)}</span></div><h3>{e(t(ti))}</h3><p>{e(t(ds))}</p></article>' for r_,a_,ti,ds in IDEAS)+'</div>'
    S.append(sec("ideas","10",t(("Идеи для видео","أفكار فيديوهات")),t(("Запас на ближайшие недели. Каждая идея — готовая рубрика и обложка.","مخزون للأسابيع الجاية. كل فكرة إلها فقرة وغلاف جاهز.")),ih))
    # pack
    pk=""
    for acc_,gt,items in PACK:
        pk+=f'<h3 class="gt">{e(t(gt))}</h3><div class="grid {items[0][3]}">'
        for f,ti,use,shape in items:
            a=IMG[f]
            pk+=f'<figure class="pi {shape}"><a class="pimg" href="{a}" target="_blank" rel="noopener"><img src="{a}" alt="{e(t(ti))}" loading="lazy"></a><figcaption><b>{e(t(ti))}</b><span>{e(t(use))}</span><a class="open" href="{a}" target="_blank" rel="noopener">{e(t(META["open"]))} ↗</a></figcaption></figure>'
        pk+='</div>'
    S.append(sec("pack","11",t(("Дизайн-пакет","حزمة التصاميم")),t(("В стиле сайта: те же цвета и шрифты. Нажми на картинку — откроется в полном размере, там её можно сохранить.","بستايل الموقع: نفس الألوان والخطوط. اضغط على الصورة بتنفتح بحجمها الكامل وبتنحفظ.")),pk))

    navh="".join(f'<a href="#{a}">{e(t(b))}</a>' for a,b in META["nav"])
    fontb = '"Inter",system-ui,sans-serif' if L=="ru" else '"IBM Plex Sans Arabic","Inter",system-ui,sans-serif'
    page=f'''<title>{e(t(META["title"]))}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=Inter:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap">
<style>
/* Layout: brand book. Full-bleed cover with portrait, then one 1040px column; cards set off only where they hold copyable text. Single dark theme on purpose: Leo's brand (site palette). */
:root{{--bg:#0a0707;--p:#120a0a;--p2:#1a1010;--line:#2b1b1a;--line2:#3b2321;--t:#efe7dc;--m:#a79c92;--r:#d0201b;--r2:#8e0f0f;--ok:#d0201b;
--fd:"Oswald","Arial Narrow",sans-serif;--fb:{fontb};color-scheme:dark}}
html{{background:var(--bg);scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--t);font-family:var(--fb);font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:20;background:var(--bg)}}
body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:30;opacity:.07;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")}}
.in{{max-width:1040px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}}
/* cover */
.cover{{position:relative;border-bottom:1px solid var(--line);overflow:hidden}}
.cover .in{{display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:end;padding-block:72px 56px}}
.kick{{font:500 12px/1 var(--fd);letter-spacing:.24em;color:var(--m);text-transform:uppercase;display:flex;gap:10px;align-items:center}}
.kick::before{{content:"";width:28px;height:2px;background:var(--r)}}
h1{{font:700 clamp(68px,15vw,168px)/.86 var(--fd);margin:22px 0 22px;letter-spacing:-.01em;text-transform:uppercase}}
h1 i{{font-style:normal;color:var(--r)}}
h1 small{{display:block;font:400 clamp(20px,3.2vw,34px)/1 var(--fd);letter-spacing:.32em;color:var(--m);margin-top:14px}}
.intro{{max-width:52ch;color:var(--m);margin:0}}
.handles{{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}}
.handles a{{font:500 13px var(--fd);letter-spacing:.08em;color:var(--t);text-decoration:none;border:1px solid var(--line2);border-radius:99px;padding:6px 14px}}
.handles a:hover,.handles a:focus-visible{{border-color:var(--r);outline:none}}
.portrait{{position:relative;margin:0;aspect-ratio:3/4;max-width:100%;border-radius:4px;overflow:hidden}}
.portrait img{{width:100%;height:100%;object-fit:cover;filter:grayscale(.15) contrast(1.05)}}
.portrait::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(10,7,7,.85)),linear-gradient(90deg,rgba(208,32,27,.18),transparent 40%)}}
.portrait figcaption{{position:absolute;inset:auto 16px 14px;z-index:1;font:500 12px var(--fd);letter-spacing:.2em;color:var(--t);text-transform:uppercase}}
/* top bar */
.bar{{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:rgba(10,7,7,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.bar .in{{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-block:10px}}
.bar a{{flex:none;font:500 13px var(--fd);letter-spacing:.12em;text-transform:uppercase;color:var(--m);text-decoration:none;padding:6px 12px;border-radius:4px}}
.bar a:hover,.bar a:focus-visible{{color:var(--t);background:var(--p2);outline:none}}
/* sections */
section{{padding-top:88px;scroll-margin-top:56px}}
.sh{{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:end;margin-bottom:32px;padding-bottom:22px;border-bottom:1px solid var(--line)}}
.sn{{font:700 clamp(64px,10vw,112px)/.8 var(--fd);color:transparent;-webkit-text-stroke:1.5px var(--r)}}
h2{{font:700 clamp(30px,5vw,48px)/1 var(--fd);text-transform:uppercase;margin:0;letter-spacing:.01em;overflow-wrap:anywhere}}
.sh p{{color:var(--m);margin:10px 0 0;max-width:62ch}}
/* strategy */
.strat{{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}}
.sc{{background:var(--bg);padding:26px 26px 22px;min-width:0}}
.scn{{font:500 12px var(--fd);letter-spacing:.2em;color:var(--r)}}
.sc h3{{font:600 22px/1.2 var(--fd);text-transform:uppercase;letter-spacing:.02em;margin:8px 0 12px}}
.sc ul{{margin:0;padding:0;list-style:none;display:grid;gap:8px}}
.sc li{{position:relative;padding-inline-start:18px;color:#d9d0c4;font-size:15px}}
.sc li::before{{content:"";position:absolute;inset-inline-start:0;top:.75em;width:8px;height:1px;background:var(--r)}}
.sc p{{margin:0;color:#d9d0c4;font-size:15px}}
.strat .sc:last-child:nth-child(odd){{grid-column:1/-1}}
.duo{{display:grid;grid-template-columns:1fr 1.3fr;gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:28px}}
.sc.warn h3{{color:var(--r)}}
/* copy blocks */
.cbs{{display:grid;gap:14px}}
.cb{{background:var(--p);border:1px solid var(--line);border-radius:6px;padding:18px 18px 18px;min-width:0}}
.cb-h{{display:flex;justify-content:space-between;align-items:flex-start;gap:14px}}
.cb-w{{display:flex;flex-direction:column;gap:4px;min-width:0}}
.lbl{{font:500 11px var(--fd);letter-spacing:.24em;color:var(--r);text-transform:uppercase}}
.wt{{font:600 17px/1.3 var(--fb)}}
.cb-d{{color:var(--m);font-size:14px;margin:8px 0 12px;max-width:70ch}}
.cb-t{{margin:0;background:var(--bg);border:1px solid var(--line);border-inline-start:2px solid var(--r);border-radius:4px;padding:14px 16px;white-space:pre-wrap;word-break:break-word;font:400 15px/1.65 var(--fb);color:var(--t)}}
.copy{{flex:none;font:500 12px var(--fd);letter-spacing:.14em;text-transform:uppercase;background:transparent;color:var(--t);border:1px solid var(--line2);border-radius:4px;padding:8px 14px;cursor:pointer;transition:background .15s,border-color .15s}}
.copy:hover{{border-color:var(--r)}}
.copy:focus-visible{{outline:2px solid var(--r);outline-offset:2px}}
.copy.ok{{background:var(--r);border-color:var(--r);color:#fff}}
/* week */
.routine{{border:1px solid var(--r2);border-radius:6px;padding:20px 22px;margin-bottom:24px;background:linear-gradient(90deg,rgba(142,15,15,.14),transparent 60%)}}
.routine h3{{font:600 18px var(--fd);letter-spacing:.06em;text-transform:uppercase;margin:0 0 12px}}
.routine ol{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:8px 24px}}
.routine li{{display:flex;gap:12px;font-size:15px;min-width:0}}
time{{font:500 14px var(--fd);letter-spacing:.06em;color:var(--r);min-width:52px;font-variant-numeric:tabular-nums}}
.days{{display:flex;gap:6px;overflow-x:auto;margin-bottom:24px;scrollbar-width:none}}
.days a{{flex:1 0 64px;text-decoration:none;color:var(--t);border:1px solid var(--line);border-radius:6px;padding:10px 8px;text-align:center;display:flex;flex-direction:column;gap:2px}}
.days a b{{font:700 26px/1 var(--fd)}}
.days a span{{font:500 11px var(--fd);letter-spacing:.14em;color:var(--m);text-transform:uppercase}}
.days a:hover,.days a:focus-visible{{border-color:var(--r);outline:none}}
.days a.all b{{color:var(--r)}}
.day{{border-top:1px solid var(--line);padding-block:28px;scroll-margin-top:64px}}
.day-h{{display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center;margin-bottom:16px}}
.dd{{display:flex;flex-direction:column;align-items:center;min-width:72px}}
.dn{{font:700 64px/.85 var(--fd)}}
.dw{{font:500 11px var(--fd);letter-spacing:.2em;color:var(--m);text-transform:uppercase;margin-top:6px}}
.dt h3{{font:600 24px/1.15 var(--fd);text-transform:uppercase;margin:0 0 8px;letter-spacing:.02em}}
.chips{{display:flex;gap:6px;flex-wrap:wrap}}
.chip{{font:500 11px var(--fd);letter-spacing:.16em;text-transform:uppercase;padding:3px 9px;border-radius:3px}}
.chip.tattoo{{background:var(--r);color:#fff}}.chip.personal{{background:var(--t);color:var(--bg)}}.chip.prep{{border:1px solid var(--line2);color:var(--m)}}
.prog{{display:flex;flex-direction:column;align-items:flex-end;gap:6px}}
.pc{{font:500 13px var(--fd);color:var(--m);font-variant-numeric:tabular-nums}}
.pb{{width:84px;height:3px;background:var(--line);border-radius:2px;overflow:hidden}}
.pb i{{display:block;height:100%;width:0;background:var(--r);transition:width .3s}}
.tasks{{list-style:none;margin:0 0 18px;padding:0;border:1px solid var(--line);border-radius:6px}}
.tasks li+li{{border-top:1px solid var(--line)}}
.tasks label{{display:grid;grid-template-columns:22px 60px 1fr;gap:12px;align-items:start;padding:12px 16px;cursor:pointer}}
.tasks input{{position:absolute;opacity:0;width:1px;height:1px}}
.box{{width:18px;height:18px;border:1.5px solid var(--line2);border-radius:3px;margin-top:3px;display:grid;place-items:center;transition:.15s}}
.tasks input:checked+.box{{background:var(--r);border-color:var(--r)}}
.tasks input:checked+.box::after{{content:"";width:5px;height:9px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg) translate(-1px,-1px)}}
.tasks input:focus-visible+.box{{outline:2px solid var(--r);outline-offset:2px}}
.tasks input:checked~.tx{{color:var(--m);text-decoration:line-through;text-decoration-color:var(--r2)}}
.tx{{font-size:15px;min-width:0}}
/* pack */
.gt{{font:600 16px var(--fd);letter-spacing:.12em;text-transform:uppercase;margin:40px 0 14px;color:var(--t);display:flex;align-items:center;gap:12px}}
.gt::after{{content:"";flex:1;height:1px;background:var(--line)}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
.grid.hl{{grid-template-columns:repeat(auto-fill,minmax(130px,1fr))}}
.grid.post{{grid-template-columns:repeat(auto-fill,minmax(170px,1fr))}}
.pi{{margin:0;min-width:0;display:flex;flex-direction:column;gap:10px}}
.pimg{{display:block;border:1px solid var(--line);border-radius:4px;overflow:hidden;background:var(--p)}}
.pimg:focus-visible{{outline:2px solid var(--r)}}
.pimg img{{display:block;width:100%;height:auto;transition:transform .4s}}
.pimg:hover img{{transform:scale(1.02)}}
.pi.hl .pimg{{aspect-ratio:1;border-radius:50%}}
.pi.hl .pimg img{{height:100%;object-fit:cover;transform:scale(1.75)}}
.pi.hl .pimg:hover img{{transform:scale(1.8)}}
.pi.cover .pimg{{background:repeating-conic-gradient(#241a19 0 25%,#171010 0 50%) 0 0/20px 20px}}
.pi figcaption{{display:flex;flex-direction:column;gap:3px;font-size:13px}}
.pi figcaption b{{font:600 15px var(--fd);letter-spacing:.06em;text-transform:uppercase}}
.pi figcaption span{{color:var(--m);line-height:1.45}}
.open{{color:var(--r);text-decoration:none;font:500 12px var(--fd);letter-spacing:.1em;text-transform:uppercase;margin-top:4px}}
.open:hover,.open:focus-visible{{text-decoration:underline;outline:none}}
.upd{{border-bottom:1px solid var(--line);background:var(--p)}}
.upd .in{{display:flex;flex-wrap:wrap;gap:6px 18px;padding-block:12px;font-size:13px;color:var(--m)}}
.ub{{font:500 12px var(--fd);letter-spacing:.18em;text-transform:uppercase;color:var(--r)}}
.ul b{{color:var(--t);font-weight:600}}
.sc.solo{{border:1px solid var(--line);border-radius:6px;margin-bottom:14px}}
.hmap{{display:grid;gap:12px}}
.hrow{{display:grid;grid-template-columns:110px 1fr;gap:18px;align-items:start;border:1px solid var(--line);border-radius:6px;padding:14px;background:var(--p)}}
.hcov{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.hcov a{{display:block;width:84px;height:84px;border-radius:50%;overflow:hidden;border:1px solid var(--line2)}}
.hcov img{{width:100%;height:100%;object-fit:cover;transform:scale(1.75)}}
.hcov b{{font:600 14px var(--fd);letter-spacing:.08em;text-transform:uppercase}}
.hst{{display:flex;gap:10px;overflow-x:auto;min-width:0;padding-bottom:4px}}
.hst figure{{margin:0;flex:none;width:96px}}
.hst figure a{{display:block;border:1px solid var(--line);border-radius:4px;overflow:hidden}}
.hst img{{display:block;width:100%;aspect-ratio:9/16;object-fit:contain;background:var(--bg)}}
.hst figcaption{{font-size:12px;color:var(--m);margin-top:5px;line-height:1.35}}
.hph{{flex:none;width:96px;aspect-ratio:9/16;border:1px dashed var(--line2);border-radius:4px;display:grid;place-items:center;text-align:center;font-size:12px;color:var(--m);padding:8px;line-height:1.35}}
.ideas{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}}
.idea{{background:var(--bg);padding:20px;min-width:0}}
.idea h3{{font:600 19px/1.2 var(--fd);text-transform:uppercase;margin:12px 0 8px;letter-spacing:.02em}}
.idea p{{margin:0;color:var(--m);font-size:14px}}
footer{{margin-top:96px;border-top:1px solid var(--line);padding-block:28px 48px;color:var(--m);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px}}
footer b{{font:700 22px var(--fd);color:var(--t);letter-spacing:.04em}}
footer b i{{font-style:normal;color:var(--r)}}
@media (max-width:760px){{
 .cover .in{{grid-template-columns:1fr;padding-block:40px 36px;gap:28px}}
 .portrait{{order:-1;aspect-ratio:4/3}}
 .strat,.duo{{grid-template-columns:1fr}}
 .routine ol{{grid-template-columns:1fr}}
 .day-h{{grid-template-columns:auto 1fr;}}
 .prog{{grid-column:1/-1;flex-direction:row;align-items:center;justify-content:space-between}}
 .pb{{flex:1;margin-inline-start:12px}}
 .tasks label{{grid-template-columns:22px 52px 1fr;padding:12px}}
 .sh{{gap:14px}}
}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*{{transition:none!important}}}}
</style>
<div{' dir="rtl" lang="ar"' if rtl else ' lang="ru"'}>
<header class="cover"><div class="in">
 <div>
  <div class="kick">{e(t(META["kicker"]))}</div>
  <h1>Лео<i>.</i><small>INSTAGRAM</small></h1>
  <p class="intro">{e(t(META["intro"]))}</p>
  <div class="handles" dir="ltr"><a href="https://www.instagram.com/kaishi_tattoo/" target="_blank" rel="noopener">@kaishi_tattoo</a><a href="https://www.instagram.com/wenx.xz_/" target="_blank" rel="noopener">@wenx.xz_</a><a href="{SITE}" target="_blank" rel="noopener">Leo.Tattoo ↗</a></div>
 </div>
 <figure class="portrait"><img src="img/leo.jpg" alt="Лео"><figcaption>Tashkent · Tattoo</figcaption></figure>
</div></header>
<div class="upd"><div class="in"><span class="ub">{e(t(UPDATED))}</span>{"".join(f'<span class="ul"><b>{e(t(d_))}</b> {e(t(x_))}</span>' for d_,x_ in CHANGELOG)}</div></div>
<nav class="bar" aria-label="sections"><div class="in">{navh}</div></nav>
<main class="in">
{"".join(S)}
<footer><b>ЛЕО<i>.</i></b><span>{e(t(META["foot"]))}</span></footer>
</main>
</div>
<script>
(function(){{
 var L="{L}", T={{c:"{t(META['copy'])}",ok:"{t(META['copied'])}",sel:"{t(META['selected'])}"}};
 document.querySelectorAll('.copy').forEach(function(b){{
  b.addEventListener('click',function(){{
   var pre=b.closest('.cb').querySelector('.cb-t');
   function ok(){{b.textContent=T.ok;b.classList.add('ok');setTimeout(function(){{b.textContent=T.c;b.classList.remove('ok')}},1600)}}
   function sel(){{var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent=T.sel}}
   try{{navigator.clipboard.writeText(pre.innerText).then(ok,sel)}}catch(e){{sel()}}
  }});
 }});
 var KEY="leo-plan1-"+L, st={{}};
 try{{st=JSON.parse(localStorage.getItem(KEY)||"{{}}")}}catch(e){{st={{}}}}
 function prog(day){{
  var bx=document.querySelectorAll('input[data-day="'+day+'"]'), n=0;
  bx.forEach(function(x){{if(x.checked)n++}});
  var p=document.querySelector('.prog[data-day="'+day+'"]'); if(!p)return;
  p.querySelector('.pc').textContent=n+'/'+bx.length;
  p.querySelector('.pb i').style.width=(bx.length?n/bx.length*100:0)+'%';
 }}
 var days={{}};
 document.querySelectorAll('.tasks input').forEach(function(x){{
  if(st[x.id]) x.checked=true; days[x.dataset.day]=1;
  x.addEventListener('change',function(){{st[x.id]=x.checked;try{{localStorage.setItem(KEY,JSON.stringify(st))}}catch(e){{}};prog(x.dataset.day)}});
 }});
 Object.keys(days).forEach(prog);
}})();
</script>'''
    open(out+"/index.html","w",encoding="utf-8").write(page)
    return n

print(build("ru","/home/claude/leo2/web_ru"), build("ar","/home/claude/leo2/web_ar"))
