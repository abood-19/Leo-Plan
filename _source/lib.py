import os, subprocess, sys
IC={
"calendar":'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M9 15.5l2 2 4-4"/>',
"pen":'<g transform="rotate(-45 12 12)"><rect x="1.5" y="10" width="12" height="4" rx="2"/><rect x="13.8" y="10.4" width="4.6" height="3.2" rx="1"/><path d="M18.6 11l2.4.8v.4l-2.4.8M21 12h1.8M5 10v4"/></g>',
"pencil":'<path d="M4 20l1.2-4.2L15.8 5.2a2.1 2.1 0 0 1 3 3L8.2 18.8 4 20z"/><path d="M14 7l3 3"/>',
"star":'<path d="M12 3.2l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6-4.5-4.2 6.1-.7z"/>',
"drop":'<path d="M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
"moon":'<path d="M19.5 14.5A8 8 0 1 1 9.5 4.5a6.5 6.5 0 0 0 10 10z"/><path d="M17 3.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6z"/>',
"dagger":'<path d="M12 2l1.8 3v10h-3.6V5z"/><path d="M7 15h10M12 15v5"/><circle cx="12" cy="21.3" r="1"/>',
"eye":'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
"coffee":'<path d="M5 9h11v5.5a4.5 4.5 0 0 1-4.5 4.5h-2A4.5 4.5 0 0 1 5 14.5z"/><path d="M16 10h1.5a2.5 2.5 0 0 1 0 5H16M8.5 3.5v2.5M12 3.5v2.5"/>',
"bolt":'<path d="M13 2L4.5 13.5H11L10 22l8.5-11.5H12z"/>',
"music":'<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
}
TAT=[("01_Запись","calendar"),("02_Работы","pen"),("03_Эскизы","pencil"),("04_Отзывы","star"),("05_Уход","drop"),("06_Обо_мне","moon")]
PER=[("01_Тату","dagger"),("02_Я","eye"),("03_Будни","coffee"),("04_Вайб","bolt"),("05_Музыка","music")]
def svgicon(k,size,stroke,extra=""):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" {extra}>{IC[k]}</svg>'
BASE='<html><head><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden}}{css}</style></head><body>{body}</body></html>'
NOISE="<svg width='0' height='0' style='position:absolute'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .08 0'/></filter></svg><svg style='position:absolute;inset:0' width='1080' height='1920'><rect width='100%' height='100%' filter='url(#n)'/></svg>"
def aura(k,acc):
    blobs=[("#c4b5fd",230,650,520),("#f9a8d4",820,820,460),("#a5b4fc",420,1260,520),("#fef3ff",640,980,300)] if acc=="t" else [("#fbcfe8",260,700,500),("#fda4af",800,880,460),("#e9d5ff",450,1250,520),("#fff7ed",620,980,300)]
    b="".join(f'<div style="position:absolute;left:{x-r}px;top:{y-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:{c};filter:blur(110px)"></div>' for c,x,y,r in blobs)
    body=f'<div style="position:absolute;inset:0;background:#f3eefc">{b}</div>{NOISE}<div style="position:absolute;left:340px;top:760px;filter:drop-shadow(0 0 2px rgba(90,40,160,.5)) drop-shadow(0 8px 24px rgba(90,40,160,.45))">{svgicon(k,400,"#ffffff").replace('stroke-width="1.5"','stroke-width="1.8"')}</div>'
    return BASE.format(css="",body=body)
def glass(k,acc):
    c1,c2,c3=("#7c3aed","#db2777","#2563eb") if acc=="t" else ("#db2777","#f97316","#a855f7")
    body=f'''<div style="position:absolute;inset:0;background:#0b0614"></div>
<div style="position:absolute;left:250px;top:640px;width:400px;height:400px;border-radius:50%;background:{c1};filter:blur(50px)"></div>
<div style="position:absolute;left:470px;top:820px;width:400px;height:400px;border-radius:50%;background:{c2};filter:blur(50px)"></div>
<div style="position:absolute;left:300px;top:930px;width:330px;height:330px;border-radius:50%;background:{c3};filter:blur(60px);opacity:.75"></div>
<div style="position:absolute;left:250px;top:670px;width:580px;height:580px;border-radius:150px;background:rgba(255,255,255,.12);backdrop-filter:blur(36px);-webkit-backdrop-filter:blur(36px);border:2px solid rgba(255,255,255,.35);box-shadow:inset 0 2px 0 rgba(255,255,255,.4),0 40px 80px rgba(0,0,0,.45)"></div>
{NOISE}<div style="position:absolute;left:360px;top:780px">{svgicon(k,360,"#ffffff")}</div>'''
    return BASE.format(css="",body=body)
def neon(k,acc):
    col,core=("#a855f7","#f5e9ff") if acc=="t" else ("#ec4899","#ffe4f3")
    ic=svgicon(k,460,core,'style="filter:drop-shadow(0 0 4px {c}) drop-shadow(0 0 14px {c}) drop-shadow(0 0 34px {c}) drop-shadow(0 0 70px {c})"'.format(c=col))
    body=f'''<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#1d1424 0,#0a070d 55%,#040305 100%)"></div>
<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 2px,transparent 2px 64px),repeating-linear-gradient(90deg,rgba(255,255,255,.02) 0 2px,transparent 2px 128px)"></div>
<div style="position:absolute;left:290px;top:710px;width:500px;height:500px;border-radius:50%;background:{col};opacity:.18;filter:blur(90px)"></div>
{NOISE}<div style="position:absolute;left:310px;top:730px">{ic}</div>'''
    return BASE.format(css="",body=body)
def chrome(k,acc):
    c1,c2=("#c4b5fd","#f0abfc") if acc=="t" else ("#f9a8d4","#c4b5fd")
    svg=f'''<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="{c1}"/><stop offset=".5" stop-color="#4b3b63"/><stop offset=".62" stop-color="#e9e3f5"/><stop offset=".8" stop-color="{c2}"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
<filter id="c" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="6" result="b"/>
<feSpecularLighting in="b" surfaceScale="5" specularConstant="1.4" specularExponent="30" lighting-color="#fff" result="s"><fePointLight x="420" y="700" z="300"/></feSpecularLighting>
<feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/><feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k2="1" k3="1"/></filter>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter></defs>
<rect width="1080" height="1920" fill="#050307"/>
<ellipse cx="540" cy="1240" rx="330" ry="40" fill="{c1}" opacity=".25" filter="url(#gl)"/>
<g transform="translate(270 690) scale(22.5)" fill="none" stroke="{c1}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".5" filter="url(#gl)">{IC[k]}</g>
<g filter="url(#c)"><g transform="translate(270 690) scale(22.5)" fill="none" stroke="url(#g)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{IC[k]}</g></g>
</svg>'''
    return BASE.format(css="",body=svg)
STYLES={"aura":aura,"glass":glass,"neon":neon,"chrome":chrome}
def render(style,acc,name,k,out="out"):
    d=f"{out}/{style}/{'tattoo' if acc=='t' else 'personal'}"; os.makedirs(d,exist_ok=True)
    h=f"{d}/{name}.html"; open(h,"w").write(STYLES[style](k,acc))
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--virtual-time-budget=2000","--window-size=1080,1920",f"--screenshot={d}/{name}.png",f"file://{os.path.abspath(h)}"],capture_output=True,timeout=90)
    os.remove(h)
if __name__=="__main__":
    only=sys.argv[1:]
    for st in STYLES:
        if only and st not in only: continue
        for n,k in TAT: render(st,"t",n,k)
        for n,k in PER: render(st,"p",n,k)
