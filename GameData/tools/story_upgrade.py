"""Recreate v0.4's escape quest, dialogue data, map props and detailed pixel sprites.
Run AFTER make_assets.py and upgrade_visuals.py when recreating assets.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,random
R=Path(__file__).resolve().parents[1]/'assets'
story={'intro':[
 {'speaker':'СТУДЕНТ','portrait':0,'text':'Сегодня я пришёл раньше всех.\nНаконец-то не опоздаю на дискретную математику.'},
 {'speaker':'СТУДЕНТ','portrait':0,'text':'Но почему аудитория пустая?\nВ коридоре тоже никого... Слишком тихо.'},
 {'speaker':'СТУДЕНТ','portrait':0,'text':'Что?! Свет погас! За дверью кто-то есть.\nЭто не обычные студенты... Началось заражение.'},
 {'speaker':'ПРЕПОДАВАТЕЛЬ','portrait':1,'text':'Не выходи без плана. Они реагируют на шум.\nНа компьютере у кафедры есть задание.'},
 {'speaker':'ПРЕПОДАВАТЕЛЬ','portrait':1,'text':'Пароль — число 1010 из двоичной системы.\nПереведи его в десятичную и введи ответ.'},
 {'speaker':'СТУДЕНТ','portrait':0,'text':'Открыть компьютер. Найти путь наружу.\nГлавное — не дать им себя заметить.'}],
 'quest':{'speaker':'КОМПЬЮТЕР / ПЛАН ЭВАКУАЦИИ','portrait':1,'text':'Выйди из 361 и пройди через три блока.\nНайди ключ-карту в кабинете 354, блок 1.\nИспользуй её у выхода в левом конце коридора.'},
 'password':'10', 'binary':'1010'}
(R/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf8')
cfg=json.loads((R/'config.json').read_text(encoding='utf8'))
cfg.update(playerSpeed=90,quietSpeed=52,zombieSpeed=21,chaseSpeed=40,visionRange=132,suspicionSeconds=1.25,chaseMemory=1.0)
(R/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf8')
j=json.loads((R/'floor3.tmj').read_text());layers={l['name']:l for l in j['layers']};objects=layers['Interaction']['objects'];W=j['width'];furn=layers['Furniture']['data']
for o in objects:
 t=o['type']
 if t=='power':o['type']='lightpanel';o['name']='LIGHTS'
 if t=='terminal':o['type']='directory';o['name']='DIRECTORY'
 if t=='cartridge':o['type']='keycard';o['name']='KEYCARD 354'
 if t=='vent':o.update(type='exit',name='EXIT C1.1',x=5*16,y=22*16,width=32,height=32)
 if t=='teacher':o.update(x=137*16,y=28*16)
 if t=='door' and o['name']=='361 DOOR':o['properties']=[{'name':'open','type':'bool','value':False},{'name':'requires','type':'string','value':'laptop'}]
if not any(o['type']=='laptop' for o in objects):
 objects.append({'id':j['nextobjectid'],'name':'PC 361','type':'laptop','x':134*16,'y':28*16,'width':16,'height':16,'rotation':0,'visible':True});j['nextobjectid']+=1
# University fixtures: bookshelves, projector, podium, water points and notice boards.
for x in [4,56,108]:
 for y in [8,9,10,11]:furn[y*W+x+1]=41
 furn[27*W+x+25]=39
 furn[27*W+x+37]=34
 furn[7*W+x+22]=40
 furn[25*W+x+42]=43
# Lecture-room front remains walkable and the laptop can be approached on all sides.
furn[27*W+137]=33;furn[27*W+141]=35;furn[27*W+142]=35;furn[27*W+143]=35
newflags=[(32,True,True),(38,True,False),(40,True,True),(42,False,False)]
existing={t['id']:t for t in j['tilesets'][0]['tiles']}
for id,solid,vision in newflags:existing[id]={'id':id,'properties':[{'name':'solid','type':'bool','value':solid},{'name':'blocksVision','type':'bool','value':vision}]}
j['tilesets'][0]['tiles']=list(existing.values())
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def b(n,box,c):
 x=n%16*16;y=n//16*16;d.rectangle((x+box[0],y+box[1],x+box[2],y+box[3]),fill=c)
def clear(n):b(n,(0,0,15,15),(0,0,0,0))
clear(32);b(32,(2,4,13,15),'#5d554f');b(32,(1,1,14,6),'#c9b799');b(32,(2,1,13,2),'#f4ddaf');b(32,(4,6,11,13),'#887a64');b(32,(5,8,10,8),'#b9a787')
clear(33);b(33,(2,4,13,11),'#667582');b(33,(2,3,13,8),'#c7d2ce');b(33,(10,5,12,7),'#203c55');b(33,(11,5,12,6),'#7bd1d5');b(33,(4,10,10,12),'#3b4d62')
clear(34);b(34,(0,0,15,13),'#d1d7d0');b(34,(0,0,15,1),'#6a8190');b(34,(1,2,14,11),'#baccc9');b(34,(2,3,13,3),'#637e89');b(34,(2,6,11,6),'#7b9199');b(34,(2,9,10,9),'#8ba3a9');b(34,(1,13,14,14),'#334b64')
clear(35);b(35,(4,2,12,11),'#263f53');b(35,(5,3,11,10),'#ced9d1');b(35,(8,4,8,7),'#3d5164');b(35,(8,7,10,7),'#3d5164')
clear(36);b(36,(1,4,14,12),'#1a4053');b(36,(2,3,13,10),'#54bcc3');b(36,(3,4,12,5),'#e5efd7');b(36,(4,7,7,9),'#d0a56a');b(36,(9,7,11,7),'#207887')
clear(37);b(37,(1,0,14,15),'#263c4c');b(37,(2,1,13,14),'#72989a');b(37,(4,3,11,10),'#154b55');b(37,(5,5,10,5),'#91e4bd');b(37,(5,6,5,8),'#91e4bd');b(37,(11,11,12,12),'#ecd18a')
clear(38);b(38,(3,7,12,15),'#adbcc0');b(38,(4,1,11,8),'#4e9dbc');b(38,(5,1,10,2),'#a8d9d9');b(38,(4,9,10,12),'#394c61');b(38,(6,9,8,10),'#ef929d')
clear(39);b(39,(1,1,14,14),'#253647');b(39,(2,2,13,12),'#e1ba6d');b(39,(7,4,8,8),'#4f4f50');b(39,(7,10,8,11),'#4f4f50')
clear(40);b(40,(0,0,15,15),'#7c6a5a');b(40,(1,1,14,13),'#403f48')
for xx,col in [(2,'#be7281'),(5,'#76a4b1'),(8,'#baab7d'),(11,'#7c9e88')]:
 b(40,(xx,2,xx+1,6),col);b(40,(xx,9,xx+1,12),col)
b(40,(0,7,15,8),'#b29a78');b(40,(0,14,15,15),'#b29a78')
clear(42);b(42,(1,1,14,14),'#3c5061');b(42,(2,2,13,12),'#61a6b1');b(42,(4,3,11,5),'#c3dcce');b(42,(3,8,12,9),'#3c788d');b(42,(4,11,10,11),'#96c9bf')
im.save(R/'tiles.png')
# More detailed 32x48 source sprites with hair shading, seams, lanyards and hands.
people=Image.new('RGBA',(384,192));pd=ImageDraw.Draw(people)
for kind in range(4):
 for direction in range(4):
  for frame in range(3):
   ox=(direction*3+frame)*32;oy=kind*48
   def p(x,y,w,h,c):pd.rectangle((ox+x,oy+y,ox+x+w-1,oy+y+h-1),fill=c)
   skin=['#d6ab85','#92a38f','#d0b08e','#d5b294'][kind];shade=['#aa785f','#657a73','#a47c67','#a77761'][kind];shirt=['#3b879c','#676376','#4a526e','#a98377'][kind]
   step=[0,-2,2][frame]
   p(5,42,23,4,'#172536');p(9,32,6,10+step,'#273d54');p(19,32,6,10-step,'#273d54');p(10,33,2,7,'#486178');p(22,33,2,7,'#3c526b');p(7,41+step,8,4,'#172536');p(19,41-step,9,4,'#172536');p(8,41+step,6,1,'#7c8d95');p(21,41-step,6,1,'#647a87')
   p(7,17,20,17,'#1c3046');p(8,17,18,15,shirt);p(9,18,4,12,'#65aab5' if kind==0 else '#788695');p(24,19,3,12,'#293e55');p(4,20,4,12,shirt);p(27,20,4,12,shirt);p(4,30,4,5,skin);p(28,30,3,5,skin);p(5,33,2,2,shade);p(28,33,2,2,shade)
   p(8,4,17,14,'#202a39');p(10,6,15,11,skin);p(10,13,3,4,shade);p(22,7,3,9,shade);p(8,2,17,6,'#252b36');p(9,1,12,3,'#35404b');p(11,2,9,1,'#5a5951');p(7,6,4,7,'#282e38');p(9,14,3,3,'#282e38')
   if direction==0:
    p(12,9,3,2,'#272c3a');p(21,9,2,2,'#272c3a');p(13,9,1,1,'#f3d5b0');p(18,10,2,3,shade);p(15,14,5,1,'#845a52')
   elif direction==1:p(9,5,8,12,'#2b3340');p(23,10,3,3,skin);p(22,9,2,2,'#252e3a')
   elif direction==2:p(18,5,7,12,'#2b3340');p(8,10,3,3,skin);p(11,9,2,2,'#252e3a')
   else:p(8,4,17,13,'#2b3440');p(11,3,9,3,'#4a4c48')
   if kind==0:
    p(11,20,13,16,'#bd865d');p(12,20,11,3,'#ddb17c');p(13,25,9,8,'#815d4c');p(14,26,7,2,'#ab7955');p(11,22,2,12,'#edc795');p(23,22,2,10,'#775b50');p(17,29,2,1,'#e0b68c')
   if kind==1:p(12,10,2,2,'#c47c9b');p(21,10,2,2,'#c47c9b');p(9,26,4,2,'#46495e');p(20,23,3,6,'#4d5266');p(16,18,2,10,'#9aa795');p(16,28,4,3,'#344953')
   if kind==2:p(11,8,7,4,'#27394b');p(19,8,7,4,'#27394b');p(12,9,4,2,'#99b7b5');p(20,9,4,2,'#99b7b5');p(16,18,5,13,'#c6c7be');p(18,20,2,8,'#5ebac3');p(16,30,5,4,'#4d7f8d');p(9,3,7,1,'#a2a397')
people.save(R/'people.png')
print('Escape story and detailed campus assets ready')
