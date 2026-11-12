import math
FONT_CSS="@font-face{font-family:Rubik;src:url(Rubik.ttf)}@font-face{font-family:Oswald;src:url(Oswald.ttf)}"
DEFS='''
<defs>
 <radialGradient id="bg" cx="50%" cy="48%" r="70%"><stop offset="0" stop-color="{b1}"/><stop offset=".55" stop-color="{b2}"/><stop offset="1" stop-color="#030106"/></radialGradient>
 <linearGradient id="iri" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#f6ecff"/><stop offset=".18" stop-color="{c1}"/><stop offset=".34" stop-color="#ffffff"/>
  <stop offset=".48" stop-color="{c2}"/><stop offset=".62" stop-color="#8ef0ff"/><stop offset=".76" stop-color="#ffffff"/>
  <stop offset=".9" stop-color="{c1}"/><stop offset="1" stop-color="#3b1670"/></linearGradient>
 <filter id="chrome" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="13" result="b"/>
  <feSpecularLighting in="b" surfaceScale="9" specularConstant="1.3" specularExponent="26" lighting-color="#ffffff" result="s"><fePointLight x="380" y="560" z="420"/></feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feDiffuseLighting in="b" surfaceScale="9" diffuseConstant="1.05" lighting-color="#ffffff" result="d"><feDistantLight azimuth="225" elevation="48"/></feDiffuseLighting>
  <feComposite in="d" in2="SourceAlpha" operator="in" result="d2"/>
  <feBlend in="SourceGraphic" in2="d2" mode="multiply" result="m"/>
  <feComposite in="m" in2="s2" operator="arithmetic" k1="0" k2="1" k3="0.9" k4="0"/>
 </filter>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>
 <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="120"/></filter>
 <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter>
 <path id="arc" d="M 540 960 m -372 0 a 372 372 0 1 1 744 0 a 372 372 0 1 1 -744 0"/>
</defs>'''
def sparkle(x,y,r,op=1):
    return f'<path d="M{x} {y-r} Q{x+r*.12} {y-r*.12} {x+r} {y} Q{x+r*.12} {y+r*.12} {x} {y+r} Q{x-r*.12} {y+r*.12} {x-r} {y} Q{x-r*.12} {y-r*.12} {x} {y-r}Z" fill="#fff" opacity="{op}"/>'
def page(motif,theme="v",label="KAISHI ✦ TATTOO ✦ TASHKENT ✦ "):
    if theme=="v": b1,b2,c1,c2,g="#3a1670","#12061f","#c9a6ff","#ff9fe0","#8b5cf6"
    else: b1,b2,c1,c2,g="#5e0f47","#1c0414","#ffa6dc","#c9a6ff","#ec4899"
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<style>{FONT_CSS} .t{{font-family:Oswald;font-weight:500;font-size:30px;letter-spacing:9px;fill:#e9dcff;opacity:.75}}</style>
{DEFS.format(b1=b1,b2=b2,c1=c1,c2=c2)}
<rect width="1080" height="1920" fill="url(#bg)"/>
<circle cx="380" cy="760" r="300" fill="{g}" opacity=".35" filter="url(#soft)"/>
<circle cx="720" cy="1180" r="260" fill="{c2}" opacity=".18" filter="url(#soft)"/>
<circle cx="540" cy="960" r="410" fill="none" stroke="#e9dcff" stroke-opacity=".35" stroke-width="2"/>
<circle cx="540" cy="960" r="430" fill="none" stroke="#e9dcff" stroke-opacity=".12" stroke-width="1"/>
<text class="t"><textPath href="#arc" startOffset="0">{label*2}</textPath></text>
<g filter="url(#glow)" opacity=".55"><g fill="{g}">{motif}</g></g>
<g filter="url(#chrome)"><g fill="url(#iri)">{motif}</g></g>
{sparkle(770,760,30)}{sparkle(320,1170,20,.85)}{sparkle(740,1190,13,.7)}{sparkle(330,760,11,.6)}
<rect width="1080" height="1920" filter="url(#grain)"/>
</svg>'''
    return svg
