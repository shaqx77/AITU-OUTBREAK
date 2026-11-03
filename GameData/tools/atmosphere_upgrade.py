"""v0.8 campus dressing. Run after phone_quest_upgrade.py. No network assets."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,random
R=Path(__file__).resolve().parents[1]/'assets'
j=json.loads((R/'floor3.tmj').read_text(encoding='utf8'));W=j['width'];L={l['name']:l for l in j['layers']}
floor,walls,fu=[L[n]['data'] for n in ('Floor','Walls','Furniture')];objects=L['Interaction']['objects']
objects[:]=[o for o in objects if not o['name'].startswith('V08 ')]
def obj(t,name,x,y,w=1,h=1,**props):
    o=dict(id=j['nextobjectid'],type=t,name='V08 '+name,x=x*16,y=y*16,width=w*16,height=h*16,visible=True,rotation=0)
    j['nextobjectid']+=1
    o['properties']=[dict(name=k,type='bool' if isinstance(v,bool) else 'float' if isinstance(v,(int,float)) else 'string',value=v) for k,v in props.items()]
    objects.append(o);return o
def put(index,x,y):fu[y*W+x]=index+1
def prop(name,x,y,kind,text,sound):obj('officeprop',name,x,y,kind=kind,text=text,sound=sound)

# Busy faculty offices: workstations, filing cabinets, printing corners, coolers.
for left,right,title in ((109,116,'COMPUTER SCIENCE'),(118,126,'SOFTWARE ENGINEERING')):
    for y in range(27,40):
        for x in range(left,right+1):fu[y*W+x]=0
    for x,y in ((left+1,29),(left+1,34),(left+4,34)):
        put(68,x,y);put(85,x+1,y);put(7,x,y+1)
    for y,index in ((29,69),(32,70),(35,71),(38,69)):put(index,right,y)
    put(72,left,37);put(74,left+1,37);put(73,left,32)
    put(75,left,28);put(74,left+2,39);put(71,right-2,39)
    put(82,left+2,29);put(83,left+1,38)
    prop(title+' PRINTER',left+1,36,'printer','Очередь печати: резюме, портфолио и FINAL_final.pdf. Принтер снова зажевал лист.','printer.wav')
    prop(title+' COOLER',left+1,32,'cooler','В кулере ещё есть вода. На стаканчике написано: «Не трогать — идёт защита».','water.wav')
    prop(title+' FILES',right-1,33,'files','Резюме студентов, портфолио, папки проектов и ведомости. Кажется, здесь работали до самой тревоги.','files.wav')

# Service room: taller racks, redundant switches, a chaotic sysadmin desk.
for y in range(19,33):
    for x in range(157,170):fu[y*W+x]=0
for x in (158,160,162,164,166,168):put(64 if x%4 else 65,x,20)
for y in (24,27):
    for x in (158,160,162):put(65 if y==24 else 64,x,y)
put(66,166,24);put(67,167,24);put(7,166,25);put(82,168,24)
put(72,169,26);put(80,157,30);put(83,159,31);put(71,161,31)
prop('SYSADMIN DESK',167,26,'desk','Три монитора, остывший кофе, кабели и открытый журнал: «Починил всё. Кроме апокалипсиса».','keyboard.wav')
prop('SERVER LOG',159,25,'server','Сервер резервного копирования всё ещё работает. На стикере: «Не выключать! Даже если все стали зомби».','server.wav')

# An enclosed, accessible cleaning closet within the service room.
for y in range(28,34):
    for x in range(165,171):
        floor[y*W+x]=1;fu[y*W+x]=0;walls[y*W+x]=5 if x in (165,170) or y in (28,33) else 0
for y in (30,31):walls[y*W+165]=0
obj('room','MOP ROOM',165,28,6,6)
obj('door','MOP DOOR',165,30,1,2,open=True)
put(78,166,29);put(79,169,29);put(76,169,31);put(83,166,32)
obj('mopweapon','MOP',167,31)
prop('CLEANING NOTE',168,30,'cleaning','Коморка уборщика: ведро, химия и швабра. На двери: «Чистота — залог выживания».','paper.wav')

# Bookcases remain background furniture, with no interaction objects.
for x,y in ((133,30),(133,34),(152,30),(152,35),(134,9),(152,15),(110,8),(130,8),(57,29),(99,29),(5,14),(47,29)):
    if floor[y*W+x] and not walls[y*W+x]:put(71,x,y)

# Visual-only ground clutter and damaged fixtures. Never blocks a corridor.
rng=random.Random(808)
for base in (4,56,108):
    for _ in range(17):
        x=rng.randrange(base+2,base+44);y=rng.choice((21,22,23,24))
        obj('debris','CLUTTER',x+rng.random()*.5,y+rng.random()*.5,kind=rng.randrange(5))
    for x,y in ((base+8,23),(base+35,22)):
        obj('debris','FALLEN LIGHT',x,y,kind=5)
    for offset in (13,38):obj('hazard','SPARK WIRE',base+offset,21,phase=rng.random()*6)
for left,right in ((109,116),(118,126),(157,169)):
    for _ in range(12):
        x=rng.randrange(left,right);y=rng.randrange(29,39) if left<150 else rng.randrange(23,28)
        if floor[y*W+x] and not walls[y*W+x]:obj('debris','OFFICE CLUTTER',x+.2,y+.3,kind=rng.randrange(5))

# Detailed 16px pixel atlas: every highlight follows the original pixel grid.
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def b(n,rect,c):
    x,y=n%16*16,n//16*16;d.rectangle((x+rect[0],y+rect[1],x+rect[2],y+rect[3]),fill=c)
def clear(n):b(n,(0,0,15,15),(0,0,0,0))
for n in range(64,86):clear(n)
for n,col in ((64,'#527d91'),(65,'#52918b')):
    b(n,(1,0,14,15),'#152736');b(n,(2,1,13,14),'#304959');b(n,(3,1,3,14),col)
    for y in (2,5,8,11):
        b(n,(4,y,12,y+1),'#122633');b(n,(5,y,6,y),'#6df0c3');b(n,(10,y,11,y),'#648c9f')
    b(n,(4,14,12,14),'#758e94')
for n in (66,67,68,85):
    b(n,(0,2,15,14),'#4a4e50');b(n,(0,1,15,12),'#aa9d7b');b(n,(0,0,15,1),'#d7c49e')
    if n in (66,68):
        b(n,(1,2,12,8),'#152a39');b(n,(2,3,11,7),'#317589');b(n,(3,4,9,4),'#74d6cb')
        b(n,(6,8,7,9),'#40535b');b(n,(2,10,12,12),'#3d535e')
        for x in range(3,12,2):b(n,(x,10,x,11),'#9cb5b6')
    else:
        b(n,(2,3,12,9),'#d5dfcd');b(n,(3,4,3,8),'#a67572')
        for y in (4,6,8):b(n,(5,y,11,y),'#93a6a3')
        b(n,(12,10,14,12),'#53696d')
for n,base in ((69,'#789597'),(70,'#8c9a9b'),(71,'#846c56')):
    b(n,(0,0,15,15),'#263946');b(n,(1,1,14,14),base)
    if n!=71:
        for y in (2,6,10):
            b(n,(2,y,13,y+3),'#526e7a');b(n,(5,y+1,10,y+1),'#cad6c7');b(n,(7,y+2,8,y+2),'#273c4c')
    else:
        for yy in (2,9):
            for x,col in ((2,'#a36e6e'),(5,'#6aadb1'),(8,'#c3ad76'),(11,'#7e9b77')):
                b(n,(x,yy,x+1,yy+4),col);b(n,(x,yy+1,x+1,yy+1),'#e0dac4')
        b(n,(1,7,14,8),'#b39a73');b(n,(1,14,14,15),'#b39a73')
b(72,(1,4,14,14),'#405968');b(72,(3,0,12,7),'#dce3d3');b(72,(2,8,13,10),'#9eb9b9');b(72,(4,11,11,14),'#1a2e3e');b(72,(11,8,12,8),'#5eeec1')
b(73,(3,7,12,15),'#aec5c4');b(73,(4,0,11,8),'#529cb5');b(73,(5,1,8,2),'#b4e4e3');b(73,(4,9,11,12),'#3d5769');b(73,(5,9,6,10),'#d46c7c');b(73,(9,9,10,10),'#6cc6ce')
for y in (5,8,11):
    b(74,(1,y,14,y+2),'#d7decc');b(74,(2,y,13,y),'#eef0d7');b(74,(3,y+1,10,y+1),'#93a59f')
b(75,(0,0,15,15),'#6e5d4d');b(75,(1,1,14,14),'#af9270')
for x,y in ((2,2),(8,3),(3,9),(10,10)):
    b(75,(x,y,x+3,y+4),'#e0ddbd');b(75,(x+1,y,x+1,y),'#c76675');b(75,(x+1,y+2,x+2,y+2),'#8a9c9a')
b(76,(3,5,12,13),'#3d879e');b(76,(2,4,13,6),'#90b9bd');b(76,(4,7,5,11),'#7bc5ca');b(76,(5,2,10,2),'#9aafb0');b(76,(4,3,4,5),'#9aafb0');b(76,(11,3,11,5),'#9aafb0')
b(77,(7,0,8,11),'#c7a67b');b(77,(4,11,11,13),'#729eab');b(77,(2,13,13,15),'#b9c5b9')
for x in range(3,13,2):b(77,(x,14,x,15),'#78979a')
b(78,(1,0,14,15),'#647c87');b(78,(2,1,13,14),'#97afb0')
for x,col in ((3,'#7bbaac'),(7,'#c18c99'),(10,'#77acc0')):
    b(78,(x,6,x+2,12),col);b(78,(x+1,4,x+1,6),'#e2dfca');b(78,(x,9,x+2,10),'#e2dfca')
b(79,(0,2,15,13),'#b7c9c2');b(79,(2,4,13,11),'#627d89');b(79,(4,5,11,9),'#9fbabc');b(79,(7,0,8,5),'#c9d4ca');b(79,(8,0,11,1),'#d9dfd0')
b(80,(3,1,12,15),'#223440');b(80,(4,3,11,5),'#487e88');b(80,(5,4,9,4),'#63d8b5')
for y in (8,10,12):b(80,(5,y,10,y),'#617581')
b(81,(1,6,12,9),'#8a6870');b(81,(6,3,9,14),'#3f5866');b(81,(3,2,12,4),'#b17a77');b(81,(2,11,14,12),'#607b86')
b(82,(4,5,10,11),'#d6d7bd');b(82,(5,5,9,6),'#5a4542');b(82,(11,7,12,9),'#c6cec0');b(82,(3,12,12,13),'#405561')
b(83,(1,5,14,14),'#a18a62');b(83,(2,6,13,7),'#c4ac7e');b(83,(3,2,8,5),'#b7a075');b(83,(9,3,13,6),'#796e55');b(83,(7,8,8,13),'#cdbb91')
b(84,(0,0,15,15),'#6c8093');b(84,(0,7,9,8),'#223849');b(84,(8,8,9,15),'#223849');b(84,(0,6,6,6),'#9da5a3')
im.save(R/'tiles.png')
flags={t['id']:t for t in j['tilesets'][0]['tiles']}
for index in range(64,86):
    flags[index]=dict(id=index,properties=[dict(name='solid',type='bool',value=index not in (74,75,77,81,82,84)),dict(name='blocksVision',type='bool',value=index in (64,65,69,70,71,78))])
j['tilesets'][0]['tiles']=list(flags.values())
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
print('v0.8 offices, server room, cleaning closet, background bookcases and escape debris ready')
