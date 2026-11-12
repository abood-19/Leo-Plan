import sys; sys.path.insert(0,'/home/claude/leo5')
from hl import *
import os
SETS={
 "tattoo":{"stops":VIO,"glow":(190,140,255),"tint":0.0,"items":[("01_Запись","calendar"),("02_Работы","emblem"),("03_Эскизы","pencil"),("04_Отзывы","stars3"),("05_Уход","drop"),("06_Обо_мне","sparkle")]},
 "personal":{"stops":PNK,"glow":(255,140,220),"tint":0.4,"items":[("01_Тату","emblem"),("02_Я","sparkle"),("03_Будни","cup"),("04_Вайб","bolt"),("05_Музыка","note")]},
}
for acc,cfg in SETS.items():
    bg=waves(cfg["stops"],seed=1 if acc=="tattoo" else 2)
    dk=disc(820,cfg["tint"])
    for style in ("wave","disc"):
        os.makedirs(f"out/{acc}/{style}",exist_ok=True)
        for name,kind in cfg["items"]:
            base=bg.copy().convert("RGBA")
            if style=="disc":
                base.alpha_composite(dk,((W-820)//2,(H-820)//2))
            sz=760 if style=="wave" else 330
            if kind=="emblem": sz=900 if style=="wave" else 330
            im=glow_icon(base,kind,(W/2,H/2),sz,glow=cfg["glow"])
            im.save(f"out/{acc}/{style}/{name}.png")
print("ok")
