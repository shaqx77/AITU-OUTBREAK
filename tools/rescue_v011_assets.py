"""Run last after older map generators: dedicated block-2 HVAC backup room.
Idempotent; source main.cpp already contains wiring/cinematic/phone implementation.
"""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]/'assets'
p=R/'floor3.tmj';m=json.loads(p.read_text(encoding='utf8'))
layers={l['name']:l for l in m['layers']};w=m['width']
for o in layers['Interaction']['objects']:
    if o['id']==111:o['name']='BACKUP POWER ROOM'
    if o['name']=='SERVICE DOOR':o['name']='POWER ROOM DOOR'
    if o['type']=='powerpanel':o.update(x=62*16,y=29*16,width=32,height=16)
for y in range(27,40):
    for x in range(57,75):layers['Furniture']['data'][y*w+x]=0
for x in (57,59,70,72,74):layers['Furniture']['data'][28*w+x]=65
for x in (57,58,72,73):layers['Furniture']['data'][38*w+x]=70
p.write_text(json.dumps(m,ensure_ascii=False,separators=(',',':')),encoding='utf8')
p=R/'story.json';j=json.loads(p.read_text(encoding='utf8'))
j['video'][3]['text']='В блоке 2 найдите комнату резервного питания.\nСоедините четыре разрезанных провода по цветам.\nБез питания кондиционер и вентиляция не запустятся.'
j['notes'][1]='Блок 2: соединить 4 пары проводов резервного питания'
p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
print('Block-2 backup power room and biologist instructions updated.')
