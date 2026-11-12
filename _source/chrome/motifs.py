import math
C=(540,960)
def heart_banner():
    h='<path d="M540 1150 C 300 990 300 760 440 740 C 500 732 530 770 540 800 C 550 770 580 732 640 740 C 780 760 780 990 540 1150 Z"/>'
    b='<path d="M330 960 L 750 960 L 720 990 L 750 1020 L 330 1020 L 360 990 Z"/>'
    return h+b
def dagger():
    return ('<path d="M540 600 L 575 700 L 575 1080 L 505 1080 L 505 700 Z"/>'
            '<rect x="400" y="1080" width="280" height="42" rx="21"/>'
            '<rect x="512" y="1122" width="56" height="150" rx="16"/>'
            '<circle cx="540" cy="1300" r="40"/>')
def hourglass():
    return ('<rect x="380" y="640" width="320" height="44" rx="22"/><rect x="380" y="1236" width="320" height="44" rx="22"/>'
            '<path d="M420 684 L 660 684 C 660 820 580 880 560 960 C 580 1040 660 1100 660 1236 L 420 1236 C 420 1100 500 1040 520 960 C 500 880 420 820 420 684 Z M 470 1200 L 610 1200 C 600 1130 560 1100 540 1090 C 520 1100 480 1130 470 1200 Z" fill-rule="evenodd"/>')
def pen():
    return ('<g transform="translate(540 960) scale(1.3) translate(-575 -960) rotate(-40 575 960)"><rect x="300" y="905" width="330" height="110" rx="50"/>'
            '<rect x="640" y="915" width="140" height="90" rx="20"/><path d="M790 925 L 860 950 L 860 970 L 790 995 Z"/>'
            '<rect x="860" y="954" width="70" height="12" rx="6"/></g>')
def drop():
    return '<path d="M540 640 C 620 790 720 890 720 1030 C 720 1140 640 1220 540 1220 C 440 1220 360 1140 360 1030 C 360 890 460 790 540 640 Z"/>'
def star():
    pts=[]
    for i in range(10):
        r=300 if i%2==0 else 130; a=-math.pi/2+i*math.pi/5
        pts.append(f"{C[0]+r*math.cos(a):.1f},{C[1]+20+r*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" stroke-linejoin="round"/>'
def bolt(): return '<path d="M600 620 L 400 1000 L 530 1000 L 470 1300 L 690 900 L 560 900 L 640 620 Z"/>'
def moon_star():
    return '<path d="M600 650 A 310 310 0 1 0 820 1150 A 250 250 0 1 1 600 650 Z"/>'+'<path d="M610 900 Q 625 975 700 990 Q 625 1005 610 1080 Q 595 1005 520 990 Q 595 975 610 900 Z"/>'
def cassette_old():
    return ('<path d="M330 790 h420 a40 40 0 0 1 40 40 v260 a40 40 0 0 1 -40 40 h-420 a40 40 0 0 1 -40 -40 v-260 a40 40 0 0 1 40 -40 Z M 430 900 a 45 45 0 1 0 0.1 0 Z M 650 900 a 45 45 0 1 0 0.1 0 Z M 410 1040 l 30 -60 h200 l30 60 Z" fill-rule="evenodd"/>')
def cup():
    return ('<path d="M380 820 h300 v230 a110 110 0 0 1 -110 110 h-80 a110 110 0 0 1 -110 -110 Z"/>'
            '<path d="M680 870 a90 90 0 0 1 0 180 v-40 a50 50 0 0 0 0 -100 Z"/>'
            '<path d="M470 650 c-40 40 40 80 0 130 M540 630 c-40 40 40 90 0 150 M610 650 c-40 40 40 80 0 130" fill="none" stroke="#000" stroke-width="22" stroke-linecap="round"/>')
def eye():
    return ('<path d="M290 960 Q 540 680 790 960 Q 540 1240 290 960 Z M 540 845 a 115 115 0 1 0 0.1 0 Z" fill-rule="evenodd"/><circle cx="540" cy="960" r="55"/>')
def letter(ch,size=560):
    return f'<text x="540" y="{960+size*0.36:.0f}" text-anchor="middle" style="font-family:Rubik;font-weight:900;font-size:{size}px">{ch}</text>'

def cassette():
    return ('<path d="M300 780 h480 a46 46 0 0 1 46 46 v268 a46 46 0 0 1 -46 46 h-480 a46 46 0 0 1 -46 -46 v-268 a46 46 0 0 1 46 -46 Z'
            ' M 380 850 h320 a20 20 0 0 1 20 20 v110 a20 20 0 0 1 -20 20 h-320 a20 20 0 0 1 -20 -20 v-110 a20 20 0 0 1 20 -20 Z" fill-rule="evenodd"/>'
            '<circle cx="450" cy="925" r="42"/><circle cx="630" cy="925" r="42"/>'
            '<path d="M400 1140 l 40 -70 h200 l40 70 Z"/>')
def heart_banner2():
    return heart_banner()
