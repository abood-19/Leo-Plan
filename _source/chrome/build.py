import sys,os,subprocess
sys.path.insert(0,'/home/claude/leo6')
from svg import page
import motifs as M
SETS=[
 ("tattoo","v",[("01_Запись",M.hourglass()),("02_Работы",M.pen()),("03_Эскизы",M.dagger()),("04_Отзывы",M.heart_banner()),("05_Уход",M.drop()),("06_Обо_мне",M.moon_star())]),
 ("personal","p",[("01_Тату",M.dagger()),("02_Я",M.eye()),("03_Будни",M.cup()),("04_Вайб",M.bolt()),("05_Музыка",M.cassette())]),
]
only=sys.argv[1:] 
for acc,th,items in SETS:
    os.makedirs(f"out/{acc}",exist_ok=True)
    for name,mot in items:
        if only and name not in only: continue
        f=f"out/{acc}/{name}.svg"; open(f,"w").write(page(mot,th))
        html=f"out/{acc}/{name}.html"
        open(html,"w").write(f'<html><body style="margin:0;background:#000">{open(f).read().replace("url(Rubik.ttf)","url(/home/claude/leo6/Rubik.ttf)").replace("url(Oswald.ttf)","url(/home/claude/leo6/Oswald.ttf)")}</body></html>')
        subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--virtual-time-budget=2500","--window-size=1080,1920",f"--screenshot=out/{acc}/{name}.png",f"file://{os.path.abspath(html)}"],capture_output=True,timeout=90)
print("done")
