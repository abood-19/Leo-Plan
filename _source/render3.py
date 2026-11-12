import os, shutil, html, sys
from PIL import Image as _I
def _cp(src,dst):
    im=_I.open(src)
    if im.mode=="RGBA" and im.getextrema()[3][0]<255:
        dst=dst[:-4]+".png"; im.save(dst,optimize=True)
    else: im.convert("RGB").save(dst,"JPEG",quality=86,optimize=True,progressive=True)
    return dst
sys.path.insert(0,"/home/claude/leo3")
from content import *
e=html.escape
PACKDIR="/home/claude/leo3/pack"
SHORT_RU={"Пятница":"Пт","Суббота":"Сб","Воскресенье":"Вс","Понедельник":"Пн","Вторник":"Вт","Среда":"Ср","Четверг":"Чт"}

UI={
 "title":("Лео · план недели","مراجعة خطة ليو"),
 "week":("Неделя 15–21 ноября","أسبوع ١٥–٢١ نوفمبر"),
 "updated":("Обновляется каждую субботу","بيتحدّث كل سبت"),
 "tabs":[("week",("Неделя","الأسبوع")),("profile",("Профиль","البروفايل")),("hl",("Хайлайты","الهايلايتس")),("texts",("Тексты","النصوص")),("pics",("Картинки","الصور"))],
 "prep":("Перед стартом · один раз","قبل البداية · مرة وحدة"),
 "prep_d":("Сделай это до воскресенья: профиль, хайлайты, папки.","قبل الأحد: البروفايل، الهايلايتس، الملفات."),
 "ideas":("Идеи на следующую неделю","أفكار للأسبوع الجاي"),
 "rules":("Пять правил","٥ قواعد"),
 "where":("Куда","وين"),"copy":("Копировать","نسخ"),"ok":("Скопировано","تم النسخ"),"sel":("Выделено","محدد"),
 "open":("Открыть","فتح"),
 "acc_t":("Тату-аккаунт","حساب التاتو"),"acc_p":("Личный аккаунт","الحساب الشخصي"),
 "dm":("Ответы в Direct","ردود الدايركت"),"tags":("Хэштеги","الهاشتاقات"),
 "pics_d":("Нажми «Открыть» — картинка откроется в полном размере, её можно сохранить.","اضغط «فتح» بتنفتح الصورة بحجمها الكامل وبتنحفظ."),
 "hl_d":("Порядок слева направо. Обложка и что лежит внутри.","الترتيب من الشمال لليمين. الغلاف وشو جوّا."),
 "inside":("Внутри","جوّا"),
}
RULES=[
 ("Один пост в день на аккаунт, в 19:30. Готовь утром и ставь «Запланировать».","منشور واحد باليوم لكل حساب، ٧:٣٠. التجهيز الصبح والجدولة."),
 ("Первые 2 секунды видео — самый сильный кадр.","أول ثانيتين من الفيديو أقوى لقطة."),
 ("Одна тату — четыре поста за две недели. Не выкладывай всё сразу.","تاتو وحدة = ٤ منشورات على أسبوعين. لا تنزّل كل شي مرة وحدة."),
 ("Все видео сразу в папки: Работы, Процесс, Эскизы, Личное. Исходники не удаляй.","كل الفيديوهات فوراً بالملفات. لا تحذف الأصلي."),
 ("Не проси лайки. Отвечай на комментарии в первый час.","لا تطلب لايكات. رد على التعليقات بأول ساعة."),
]

def build(L,out,standalone=False):
    i=0 if L=="ru" else 1; t=lambda p:p[i]; rtl=L=="ar"
    shutil.rmtree(out,ignore_errors=True); os.makedirs(out+"/img")
    IMG={}; n=0
    for g in PACK:
        for it in g[2]:
            if it[0] in IMG: continue
            n+=1; a=f"img/{n:02d}.jpg"; a=os.path.relpath(_cp(f"{PACKDIR}/{it[0]}",out+"/"+a),out); IMG[it[0]]=a
    for _,_,cov,st in HMAP:
        for f in [cov]+[x[0] for x in st if x[0]]:
            if f not in IMG: n+=1; a=f"img/{n:02d}.jpg"; a=os.path.relpath(_cp(f"{PACKDIR}/{f}",out+"/"+a),out); IMG[f]=a
    def cb(c):
        where,desc,text=c
        return f'<div class="cb"><div class="cbh"><div><span class="lbl">{e(t(UI["where"]))}</span><b>{e(t(where))}</b></div><button class="copy" type="button">{e(t(UI["copy"]))}</button></div><p class="cbd">{e(t(desc))}</p><pre dir="auto">{e(t(text))}</pre></div>'
    def cbs(lst): return '<div class="cbs">'+"".join(cb(c) for c in lst)+'</div>'
    def tasks(did,ts):
        return '<ul class="tasks">'+"".join(f'<li><label><input type="checkbox" id="{did}-{k}" data-day="{did}"><span class="box"></span><time>{e(tm)}</time><span class="tx">{e(t(x))}</span></label></li>' for k,(tm,x) in enumerate(ts))+'</ul>'
    accn={"tattoo":UI["acc_t"],"personal":UI["acc_p"],"prep":(("Подготовка","تجهيز"))}
    # ---- week tab
    prep=[]
    for d in WEEK:
        if d[0] in ("d13","d14"): prep+=d[5]
    W=f'<div class="whead"><h1>{e(t(UI["week"]))}</h1><p>{e(t(UI["updated"]))}</p></div>'
    W+=f'<details class="day prep" open><summary><span class="dd"><b>★</b></span><span class="dt"><b>{e(t(UI["prep"]))}</b><small>{e(t(UI["prep_d"]))}</small></span><span class="pc" data-day="prep">0/{len(prep)}</span></summary>{tasks("prep",prep)}</details>'
    for d in WEEK:
        did,dt,wd,ti,accs,ts,texts=d
        if did in ("d13","d14"): continue
        short=SHORT_RU.get(t(wd),t(wd)) if L=="ru" else t(wd)
        W+=f'<details class="day" id="{did}"><summary><span class="dd"><b>{e(t(dt))}</b><i>{e(short)}</i></span><span class="dt"><b>{e(t(ti))}</b><small class="acc {accs[0]}">{e(t(accn[accs[0]]))}</small></span><span class="pc" data-day="{did}">0/{len(ts)}</span></summary>{tasks(did,ts)}{cbs(texts) if texts else ""}</details>'
    W+=f'<h2>{e(t(UI["ideas"]))}</h2><div class="ideas">'+"".join(f'<div class="idea"><span class="tag">{e(r_)}</span><b>{e(t(ti))}</b><p>{e(t(ds))}</p></div>' for r_,a_,ti,ds in IDEAS[:4])+'</div>'
    W+=f'<h2>{e(t(UI["rules"]))}</h2><ol class="rules">'+"".join(f'<li>{e(t(r))}</li>' for r in RULES)+'</ol>'
    # ---- profile tab
    hl_where=("Названия хайлайтов","Хайлайт «Запись» → что внутри","Сторис → хайлайт «Уход»","Сторис → хайлайт «Обо мне»","Хайлайт «Тату» → что внутри")
    tat=[c for c in NAME[:1]+TATTOO if c[0][0] not in hl_where]
    per=[c for c in NAME[1:]+PERSONAL if c[0][0] not in hl_where]
    P=f'<nav class="chips"><a href="#p-t">{e(t(UI["acc_t"]))}</a><a href="#p-p">{e(t(UI["acc_p"]))}</a><a href="#p-l">lnk.bio</a></nav>'
    P+=f'<h2 id="p-t">@kaishi_tattoo</h2>'+cbs(tat)
    P+=f'<h2 id="p-p">@wenx.xz_</h2><div class="note"><b>{e(t(PERSONAL_NOTE[0]))}</b><p>{e(t(PERSONAL_NOTE[1]))}</p></div><div class="note"><b>{e(t(PERSONAL_FORMULA[0]))}</b><p>{e(t(PERSONAL_FORMULA[1]))}</p></div>'+cbs(per)
    P+=f'<h2 id="p-l">lnk.bio/Kaishi</h2><div class="note"><b>{e(t(LNK_NOTE[0]))}</b><p>{e(t(LNK_NOTE[1]))}</p></div>'+cbs(LNK)
    # ---- highlights tab
    def hrow(a_):
        h=""
        for acc_,nm,cov,st in HMAP:
            if acc_!=a_: continue
            h+=f'<div class="hrow"><a class="hcov" href="{IMG[cov]}" target="_blank" rel="noopener"><img src="{IMG[cov]}" alt="{e(t(nm))}" loading="lazy"><b>{e(t(nm))}</b></a><div class="hst">'
            for f,cap in st:
                h+=(f'<a class="hs" href="{IMG[f]}" target="_blank" rel="noopener"><img src="{IMG[f]}" alt="" loading="lazy"><span>{e(t(cap))}</span></a>' if f else f'<div class="hs ph"><span>{e(t(cap))}</span></div>')
            h+='</div></div>'
        return h
    tat_hl=[c for c in TATTOO if c[0][0] in hl_where]; per_hl=[c for c in PERSONAL if c[0][0] in hl_where]
    AV="https://ai-thumbnails.s3.amazonaws.com/editor/5e9bb89b-7c66-40ac-a8ea-0a47ccd78d79/6aac6a44-1937-43b8-9469-5afb83647e31.jpeg"
    for _,_,opts in HL_OPT:
        for k_,lab,pay in opts:
            if k_=="img" and pay not in IMG:
                n_=len(IMG)+1; a_=f"img/{n_:02d}.jpg"; a_=os.path.relpath(_cp(f"{PACKDIR}/{pay}",out+"/"+a_),out); IMG[pay]=a_
    kind_lbl={"img":("Готово","جاهز"),"url":("Готово","جاهز"),"pending":("Готово","جاهز"),"prompt":("Сгенерировать","توليد"),"photo":("Снять самому","تصوير")}
    def opts(a_):
        h='<div class="opts">'
        for acc_,nm,ol in HL_OPT:
            if acc_!=a_: continue
            h+=f'<div class="opt"><h3>{e(t(nm))}</h3><div class="ol">'
            for k_,lab,pay in ol:
                src=IMG.get(pay) if k_=="img" else (pay if k_=="url" else (AV if k_=="pending" else None))
                pic=f'<a class="oimg" href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="" loading="lazy"></a>' if src else ""
                body=f'<div class="cb"><div class="cbh"><div><span class="lbl">prompt</span></div><button class="copy" type="button">{e(t(UI["copy"]))}</button></div><pre dir="ltr">{e(pay)}</pre></div>' if k_=="prompt" else ""
                op=f'<a class="open" href="{src}" target="_blank" rel="noopener">{e(t(UI["open"]))} ↗</a>' if src else ""
                h+=f'<div class="oi {k_}">{pic}<div class="ot"><span class="ok_ {k_}">{e(t(kind_lbl[k_]))}</span><b>{e(t(lab))}</b>{op}{body}</div></div>'
            h+='</div></div>'
        return h+'</div>'
    import urllib.parse
    def addimg(path):
        if path not in IMG:
            n_=len(IMG)+1; a_=f"img/{n_:02d}.jpg"; a_=os.path.relpath(_cp(f"{PACKDIR}/{path}",out+"/"+a_),out); IMG[path]=a_
        return IMG[path]
    H=f'<div class="libhead"><h1>{e(t(LIB_HOW[0]))}</h1><p>{e(t(LIB_HOW[1]))}</p></div>'
    for sid,nm,ds in LIB:
        H+=f'<article class="lib {sid}"><div class="libt"><b>{e(t(nm))}</b><span>{e(t(ds))}</span></div>'
        for acc_,lst,lab in (("tattoo",TN,"@kaishi_tattoo"),("personal",PN,"@wenx.xz_")):
            H+=f'<div class="librow"><small>{lab}</small><div class="libc">'
            for f in lst:
                a_=addimg(f"library/{sid}/{acc_}/{f}.png"); nm_=f.split("_",1)[1].replace("_"," ")
                H+=f'<a href="{a_}" target="_blank" rel="noopener"><img src="{a_}" alt="{e(nm_)}" loading="lazy"><span>{e(nm_)}</span></a>'
            H+='</div></div>'
        H+='</article>'
    H+=f'<h2>Pinterest</h2><div class="pins">'+"".join(f'<a href="https://www.pinterest.com/search/pins/?q={urllib.parse.quote(q)}" target="_blank" rel="noopener">{e(lb)} ↗</a>' for lb,q in PIN)+'</div>'
    H+=f'<h2>{e(t(("Лео-кукла для «Обо мне»","دمية ليو لـ «Обо мне»")))}</h2>'+cbs([(("ChatGPT → загрузи своё фото + этот текст","ChatGPT ← يرفع صورته + هالنص"),("Получится 3D-фигурка тебя для обложки «Обо мне» и «Я».","بتطلع دمية ثلاثية الأبعاد إله لغلاف «Обо мне» و«Я»."),(DOLL_P,DOLL_P))])
    H+=f'<h2>{e(t(UI["inside"]))} · @kaishi_tattoo</h2><p class="lead">{e(t(UI["hl_d"]))}</p><div class="hmap">{hrow("tattoo")}</div>'+cbs(tat_hl)
    H+=f'<h2>{e(t(UI["inside"]))} · @wenx.xz_</h2><div class="hmap">{hrow("personal")}</div>'+cbs(per_hl)
    # ---- texts tab
    T=f'<h2>{e(t(UI["dm"]))}</h2>'+cbs(DM)+f'<h2>{e(t(UI["tags"]))}</h2>'+cbs(TAGS)
    # ---- pics tab
    G=f'<p class="lead">{e(t(UI["pics_d"]))}</p>'
    for acc_,gt,items in PACK:
        G+=f'<h2>{e(t(gt))}</h2><div class="grid {items[0][3]}">'
        for f,ti,use,shape in items:
            a=IMG[f]
            G+=f'<figure><a class="pimg" href="{a}" target="_blank" rel="noopener"><img src="{a}" alt="{e(t(ti))}" loading="lazy"></a><figcaption><b>{e(t(ti))}</b><span>{e(t(use))}</span><a class="open" href="{a}" target="_blank" rel="noopener">{e(t(UI["open"]))} ↗</a></figcaption></figure>'
        G+='</div>'
    panels={"week":W,"profile":P,"hl":H,"texts":T,"pics":G}
    tabs="".join(f'<a href="#{k}" data-tab="{k}">{e(t(v))}</a>' for k,v in UI["tabs"])
    body="".join(f'<section class="panel" id="{k}" data-panel="{k}">{v}</section>' for k,v in panels.items())
    fb='"Inter",system-ui,sans-serif' if L=="ru" else '"IBM Plex Sans Arabic","Inter",system-ui,sans-serif'
    css=f'''
/* Layout: one calm column, five tabs. Light lavender ground, violet accent; the neon artwork carries the drama. Single light theme by request. */
:root{{--bg:#f7f5fc;--card:#ffffff;--line:#e6e0f2;--fg:#1d1530;--m:#6b6385;--a:#7c3aed;--a2:#c026d3;--soft:#f0e9ff;--dark:#0b0712;--fb:{fb};--fd:"Oswald","Arial Narrow",sans-serif;color-scheme:light}}
html{{background:var(--bg)}}
body{{background:var(--bg);color:var(--fg);font-family:var(--fb);font-size:16px;line-height:1.6}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:20;background:var(--card)}}
.top{{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--card);border-bottom:1px solid var(--line)}}
.wrap{{max-width:860px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.brand{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:12px 6px}}
.brand b{{font:700 22px var(--fd);letter-spacing:.04em}} .brand b i{{font-style:normal;color:var(--a)}}
.brand span{{font-size:13px;color:var(--m)}}
.tabs{{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding-block:4px 10px}}
.tabs a{{flex:none;text-decoration:none;color:var(--m);font-weight:600;font-size:15px;padding:8px 14px;border-radius:999px}}
.tabs a[aria-current="page"]{{background:var(--a);color:#fff}}
.tabs a:focus-visible{{outline:2px solid var(--a);outline-offset:2px}}
main{{padding-block:20px 80px}}
.panel[hidden]{{display:none}}
h1{{font:700 clamp(30px,6vw,42px)/1.1 var(--fd);margin:0;letter-spacing:.01em}}
h2{{font-size:20px;margin:36px 0 12px;scroll-margin-top:120px}}
.whead p,.lead{{color:var(--m);margin:6px 0 18px}}
.day{{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:10px;overflow:hidden}}
.day summary{{list-style:none;display:grid;grid-template-columns:56px 1fr auto;gap:14px;align-items:center;padding:14px 16px;cursor:pointer}}
.day summary::-webkit-details-marker{{display:none}}
.day summary:focus-visible{{outline:2px solid var(--a);outline-offset:-2px}}
.day[open] summary{{border-bottom:1px solid var(--line)}}
.dd{{display:flex;flex-direction:column;align-items:center;background:var(--soft);border-radius:10px;padding:6px 0}}
.dd b{{font:700 24px/1 var(--fd);color:var(--a)}} .dd i{{font-style:normal;font-size:12px;color:var(--m);margin-top:3px}}
.dt{{display:flex;flex-direction:column;gap:4px;min-width:0}} .dt b{{font-size:16px}} .dt small{{font-size:13px;color:var(--m)}}
.acc{{align-self:flex-start;font-weight:600;font-size:12px!important;padding:2px 8px;border-radius:6px}}
.acc.tattoo{{background:var(--soft);color:var(--a)!important}} .acc.personal{{background:#fde7fb;color:var(--a2)!important}}
.pc{{font-size:13px;color:var(--m);font-variant-numeric:tabular-nums;white-space:nowrap}}
.pc.done{{color:#16a34a;font-weight:600}}
.tasks{{list-style:none;margin:0;padding:6px 0}}
.tasks label{{display:grid;grid-template-columns:22px 52px 1fr;gap:10px;padding:9px 16px;cursor:pointer;align-items:start}}
.tasks input{{position:absolute;opacity:0;width:1px;height:1px}}
.box{{width:20px;height:20px;border:2px solid #cfc6e4;border-radius:6px;margin-top:2px;display:grid;place-items:center}}
.tasks input:checked+.box{{background:var(--a);border-color:var(--a)}}
.tasks input:checked+.box::after{{content:"";width:5px;height:10px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg) translate(-1px,-1px)}}
.tasks input:focus-visible+.box{{outline:2px solid var(--a);outline-offset:2px}}
.tasks time{{font-size:14px;font-weight:600;color:var(--a);font-variant-numeric:tabular-nums}}
.tasks input:checked~.tx{{color:var(--m);text-decoration:line-through}}
.day .cbs{{padding:6px 16px 16px}}
.cbs{{display:grid;gap:10px}}
.cb{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;min-width:0}}
.day .cb{{background:var(--bg)}}
.cbh{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}}
.cbh div{{display:flex;flex-direction:column;min-width:0}}
.lbl{{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--a)}}
.cbh b{{font-size:15px}}
.cbd{{font-size:13px;color:var(--m);margin:4px 0 10px}}
pre{{margin:0;white-space:pre-wrap;word-break:break-word;font:15px/1.6 var(--fb);background:var(--soft);border-radius:8px;padding:12px 14px}}
.copy{{flex:none;font:600 13px var(--fb);background:var(--a);color:#fff;border:0;border-radius:8px;padding:7px 14px;cursor:pointer}}
.copy:focus-visible{{outline:2px solid var(--fg);outline-offset:2px}}
.copy.ok{{background:#16a34a}}
.ideas{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}}
.idea{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;min-width:0}}
.idea b{{display:block;margin:8px 0 4px}} .idea p{{margin:0;font-size:14px;color:var(--m)}}
.tag{{font:600 11px var(--fd);letter-spacing:.1em;background:var(--dark);color:#d9c6ff;padding:3px 8px;border-radius:6px}}
.rules{{margin:0;padding-inline-start:22px;display:grid;gap:8px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap}}
.chips a{{text-decoration:none;color:var(--a);background:var(--soft);font-weight:600;font-size:14px;padding:6px 12px;border-radius:999px}}
.note{{background:var(--card);border:1px solid var(--line);border-inline-start:4px solid var(--a);border-radius:10px;padding:12px 14px;margin-bottom:10px}}
.note p{{margin:4px 0 0;white-space:pre-line;color:var(--m);font-size:15px}}
.hmap{{display:grid;gap:10px;margin-bottom:12px}}
.hrow{{display:grid;grid-template-columns:96px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;align-items:center}}
.hcov{{display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none;color:var(--fg)}}
.hcov img{{width:78px;height:78px;border-radius:50%;object-fit:cover;background:var(--dark);border:3px solid var(--soft);box-shadow:0 0 0 1px var(--line)}}
.hcov b{{font-size:13px}}
.hst{{display:flex;gap:8px;overflow-x:auto;min-width:0}}
.hs{{flex:none;width:84px;display:flex;flex-direction:column;gap:4px;text-decoration:none;color:var(--m);font-size:11px;line-height:1.3}}
.hs img{{width:84px;aspect-ratio:9/16;object-fit:contain;background:var(--dark);border-radius:8px}}
.hs.ph span{{display:grid;place-items:center;text-align:center;width:84px;aspect-ratio:9/16;border:1.5px dashed #cfc6e4;border-radius:8px;padding:6px}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}}
.grid.post{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}}
figure{{margin:0;min-width:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px}}
.pimg{{display:block;border-radius:8px;overflow:hidden;background:var(--dark)}}
.pimg img{{display:block;width:100%;height:auto}}
.grid.hl .pimg img{{aspect-ratio:1;object-fit:cover;object-position:center;transform:scale(1.15)}}
.grid.cover .pimg{{background:repeating-conic-gradient(#2a2238 0 25%,#1a1424 0 50%) 0 0/18px 18px}}
figcaption{{display:flex;flex-direction:column;gap:2px;padding:8px 4px 2px;font-size:13px}}
figcaption span{{color:var(--m);line-height:1.4}}
.open{{color:var(--a);font-weight:600;text-decoration:none;margin-top:4px}}

.opts{{display:grid;gap:12px}}
.opt{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}}
.opt h3{{margin:0 0 10px;font:700 18px var(--fd);letter-spacing:.04em}}
.ol{{display:grid;gap:10px}}
.oi{{display:grid;grid-template-columns:72px 1fr;gap:12px;align-items:start}}
.oi.prompt,.oi.photo{{grid-template-columns:1fr}}
.oimg img{{width:72px;height:72px;border-radius:50%;object-fit:cover;background:var(--dark);border:3px solid var(--soft)}}
.ot{{display:flex;flex-direction:column;gap:4px;min-width:0}}
.ok_{{align-self:flex-start;font-size:11px;font-weight:700;padding:2px 8px;border-radius:6px;background:var(--soft);color:var(--a)}}
.ok_.prompt{{background:#fde7fb;color:var(--a2)}} .ok_.photo{{background:#e8f6ee;color:#15803d}}
.ot .cb{{margin-top:6px;background:var(--bg)}}
.libhead h1{{font-size:clamp(28px,6vw,38px)}} .libhead p{{color:var(--m);margin:6px 0 18px}}
.lib{{border-radius:20px;padding:18px;margin-bottom:14px;color:#fff;overflow:hidden;position:relative}}
.lib.neon{{background:linear-gradient(135deg,#120a1c,#2a0f3d)}} .lib.chrome{{background:linear-gradient(135deg,#0b0a10,#2b2738)}}
.lib.glass{{background:linear-gradient(135deg,#1b0f3a,#3b1257 55%,#1d2b6b)}} .lib.aura{{background:linear-gradient(135deg,#d9c8ff,#ffd0ea 60%,#c7d2fe);color:#2a1d45}}
.lib.flash{{background:linear-gradient(135deg,#1a0b2e,#3a1670)}}
.libt{{display:flex;flex-direction:column;gap:2px;margin-bottom:12px}} .libt b{{font:700 24px var(--fd);letter-spacing:.03em}} .libt span{{font-size:14px;opacity:.8}}
.librow{{margin-top:10px}} .librow small{{font-size:12px;opacity:.7;letter-spacing:.06em}}
.libc{{display:flex;gap:12px;overflow-x:auto;padding:8px 2px 4px;scrollbar-width:none}}
.libc a{{flex:none;width:76px;display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none;color:inherit;font-size:12px}}
.libc img{{width:72px;height:72px;border-radius:50%;object-fit:cover;object-position:center;border:2px solid rgba(255,255,255,.55);box-shadow:0 6px 18px rgba(0,0,0,.35)}}
.libc a:hover img{{transform:scale(1.06)}} .libc img{{transition:transform .2s}}
.pins{{display:flex;flex-wrap:wrap;gap:8px}}
.pins a{{text-decoration:none;font-weight:600;font-size:14px;color:#fff;background:#e60023;padding:8px 14px;border-radius:999px}}
@media (max-width:520px){{.day summary{{grid-template-columns:48px 1fr auto;gap:10px;padding:12px}}.tasks label{{grid-template-columns:22px 46px 1fr;padding:9px 12px}}.day .cbs{{padding:6px 12px 12px}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
'''
    js=f'''
(function(){{
 var tabs=document.querySelectorAll('.tabs a'), panels=document.querySelectorAll('.panel');
 function show(id){{ if(!document.querySelector('[data-panel="'+id+'"]')) id='week';
  panels.forEach(function(p){{p.hidden=p.dataset.panel!==id}});
  tabs.forEach(function(a){{a.dataset.tab===id?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current')}});
 }}
 function route(){{var h=location.hash.slice(1); var el=h&&document.getElementById(h);
  if(el&&!el.classList.contains('panel')){{var p=el.closest('.panel'); if(p){{show(p.dataset.panel); if(el.tagName==='DETAILS') el.open=true; setTimeout(function(){{el.scrollIntoView()}},0); return;}}}}
  show(h||'week'); setTimeout(function(){{window.scrollTo(0,0)}},0);}}
 window.addEventListener('hashchange',route); route();
 var T={{c:"{t(UI['copy'])}",ok:"{t(UI['ok'])}",sel:"{t(UI['sel'])}"}};
 document.querySelectorAll('.copy').forEach(function(b){{b.addEventListener('click',function(){{
  var pre=b.closest('.cb').querySelector('pre');
  function ok(){{b.textContent=T.ok;b.classList.add('ok');setTimeout(function(){{b.textContent=T.c;b.classList.remove('ok')}},1500)}}
  function sel(){{var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent=T.sel}}
  try{{navigator.clipboard.writeText(pre.innerText).then(ok,sel)}}catch(e){{sel()}} }})}});
 var KEY='leo-week-1115-{L}', st={{}}; try{{st=JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{}}
 function prog(day){{var bx=document.querySelectorAll('input[data-day="'+day+'"]'),n=0;bx.forEach(function(x){{if(x.checked)n++}});
  var p=document.querySelector('.pc[data-day="'+day+'"]'); if(p){{p.textContent=n+'/'+bx.length; p.classList.toggle('done',n===bx.length&&n>0)}}}}
 var days={{}}; document.querySelectorAll('.tasks input').forEach(function(x){{ if(st[x.id])x.checked=true; days[x.dataset.day]=1;
  x.addEventListener('change',function(){{st[x.id]=x.checked;try{{localStorage.setItem(KEY,JSON.stringify(st))}}catch(e){{}};prog(x.dataset.day)}})}});
 Object.keys(days).forEach(prog);
}})();'''
    inner=f'''<title>{e(t(UI["title"]))}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap">
<style>{css}</style>'''
    page=f'''<div{' dir="rtl" lang="ar"' if rtl else ' lang="ru"'}>
<header class="top"><div class="wrap"><div class="brand"><b>ЛЕО<i>.</i></b><span>@kaishi_tattoo · @wenx.xz_</span></div><nav class="tabs" aria-label="sections">{tabs}</nav></div></header>
<main class="wrap">{body}</main></div>
<script>{js}</script>'''
    if standalone:
        doc=f'<!doctype html>\n<html lang="{L}"{" dir=\"rtl\"" if rtl else ""}>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex,nofollow">\n<meta name="theme-color" content="#ffffff">\n{inner}\n<style>*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}img{{max-width:100%}}</style>\n</head>\n<body>\n{page}\n</body>\n</html>\n'
    else: doc=inner+"\n"+page
    open(out+"/index.html","w",encoding="utf-8").write(doc)
    return n

if __name__=="__main__":
    print(build("ru","/home/claude/leo3/web_ru"), build("ar","/home/claude/leo3/web_ar"), build("ru","/home/claude/leo3/gh",standalone=True))
