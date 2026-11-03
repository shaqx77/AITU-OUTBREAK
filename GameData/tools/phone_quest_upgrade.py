"""v0.7 gameplay data. Run after campus_detail_upgrade.py."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,wave,struct
R=Path(__file__).resolve().parents[1]/'assets'
j=json.loads((R/'floor3.tmj').read_text(encoding='utf8'));L={l['name']:l for l in j['layers']};W=j['width']
objs=L['Interaction']['objects'];objs[:]=[o for o in objs if o['type'] not in ('lecturekey','cardreader','keypuzzle','ruler','magnet','keyrack')]
for o in objs:
    if o['type']=='door' and o['name']=='LECTURE DOOR':
        o['properties']=[dict(name='open',type='bool',value=False),dict(name='requires',type='string',value='lecturekey')]
def obj(t,name,x,y):
    objs.append(dict(id=j['nextobjectid'],type=t,name=name,x=x*16,y=y*16,width=16,height=16,rotation=0,visible=True))
    j['nextobjectid']+=1
obj('keyrack','SERVICE KEY RACK',163,25)
obj('cardreader','BLOCK 3 CARD READER',106,22)
L['Furniture']['data'][8*W+136]=0
L['Furniture']['data'][8*W+137]=0
L['Furniture']['data'][7*W+151]=52
L['Furniture']['data'][8*W+151]=0
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
story=json.loads((R/'story.json').read_text(encoding='utf8'))
story['password']='1010';story['decimal']='10';story['binary']='1010'
story['intro'][4]['text']='Пароль — число 10 из десятичной системы.\nПереведи его в двоичную и введи все четыре цифры.'
story['video'][2]['text']='Карта на кафедре нужна только в третьем блоке.\nПроведите ею через считыватель у перехода в блок 2.'
story['messenger']={'name':'НУРАЛИ','messages':[
    'Бро, ты где? В C1.3 творится что-то странное...',
    'Свет мигает. Кто-то скребётся в дверь. Это точно не шутка.',
    'Ты тоже слышал эти крики? Мне реально страшно.'],
    'reply':'Да! Я тоже заметил. Что здесь вообще происходит?',
    'followup':'Не знаю... Просто будь осторожен. Я пока запру дверь.'}
(R/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf8')
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def b(n,rect,c):
    x,y=n%16*16,n//16*16;d.rectangle((x+rect[0],y+rect[1],x+rect[2],y+rect[3]),fill=c)
b(60,(0,0,15,15),(0,0,0,0));b(60,(2,3,7,8),'#d0af64');b(60,(3,4,6,7),'#f2d58b')
b(60,(4,5,5,6),'#51606a');b(60,(7,7,13,9),'#cfaa5b');b(60,(10,9,11,11),'#e2bf70');b(60,(13,9,14,10),'#e2bf70')
b(61,(0,0,15,15),(0,0,0,0));b(61,(1,0,14,15),'#1e3344');b(61,(2,1,13,14),'#8fa9ae')
b(61,(3,3,12,6),'#0d3639');b(61,(4,4,11,4),'#60dec2');b(61,(3,9,12,10),'#142e3d');b(61,(10,12,11,13),'#da6684')
b(62,(0,0,15,15),(0,0,0,0));b(62,(2,6,14,9),'#b5c6c0');b(62,(3,6,14,6),'#e3e7cd')
for x in range(3,15,2):b(62,(x,8,x,9),'#4a6770')
b(63,(0,0,15,15),(0,0,0,0));b(63,(4,4,7,11),'#d66878');b(63,(9,4,12,11),'#d66878');b(63,(5,10,11,12),'#9c435d');b(63,(4,3,7,5),'#bccac4');b(63,(9,3,12,5),'#bccac4')
im.save(R/'tiles.png')
rate=22050
with wave.open(str(R/'notification.wav'),'wb') as f:
    f.setparams((1,2,rate,0,'NONE','not compressed'))
    samples=[]
    for i in range(int(rate*.5)):
        t=i/rate;v=0
        for delay,freq in ((0,740),(.14,1108)):
            u=t-delay
            if 0<=u<.3:v+=math.sin(2*math.pi*freq*u)*math.exp(-u*18)*min(1,u*150)*.18
        samples.append(int(v*32767))
    f.writeframes(struct.pack('<'+'h'*len(samples),*samples))
print('v0.7 lecture key, exit card reader, decimal-to-binary password and messenger data ready')
