"""Original code-native pixel tiles, font atlas, Tiled map, and synthesized audio."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,math,random,wave,struct
R=Path(__file__).resolve().parents[1]/'assets'; R.mkdir(exist_ok=True)
random.seed(361)
im=Image.new('RGBA',(256,256));d=ImageDraw.Draw(im)
def tile(n): return (n%16*16,n//16*16)
def rect(n,box,c):
 x,y=tile(n);d.rectangle((x+box[0],y+box[1],x+box[2],y+box[3]),fill=c)
for n,base in [(0,'#263343'),(1,'#374354'),(2,'#333346'),(3,'#495565')]:
 rect(n,(0,0,15,15),base);rect(n,(0,0,15,0),'#172332');rect(n,(0,0,0,15),'#1b2936')
 rect(n,(2,2,14,2),'#435165');rect(n,(7,7,8,8),'#475060')
# Wall, desk, cabinet, chair, paper, plant, door, floor marker.
rect(4,(0,0,15,15),'#17202f');rect(4,(0,0,15,3),'#607080');rect(4,(1,5,14,13),'#354354');rect(4,(1,14,15,15),'#111a2c')
rect(5,(0,3,15,13),'#181d29');rect(5,(0,1,14,10),'#92704d');rect(5,(1,1,13,2),'#c5a075');rect(5,(1,11,2,14),'#29303e');rect(5,(12,11,13,14),'#29303e');rect(5,(4,3,10,7),'#acb4ae');rect(5,(5,4,10,4),'#536a77')
rect(6,(1,0,14,15),'#17232c');rect(6,(2,0,13,13),'#506479');rect(6,(3,1,6,12),'#637789');rect(6,(8,1,12,12),'#35475b');rect(6,(6,6,7,8),'#adc8c9')
rect(7,(3,4,12,14),'#141c2d');rect(7,(3,2,11,9),'#51546d');rect(7,(4,2,10,3),'#807c91');rect(7,(4,10,5,14),'#4e6072');rect(7,(10,10,11,14),'#4e6072')
rect(8,(3,4,11,12),'#aaa6a0');rect(8,(4,6,9,6),'#4f6072');rect(8,(5,8,10,8),'#5f6875')
rect(9,(4,9,11,15),'#734f52');rect(9,(2,5,13,10),'#315c5d');rect(9,(5,1,10,12),'#527660');rect(9,(6,3,8,9),'#81a27c')
rect(10,(0,0,15,15),'#121b2a');rect(10,(1,1,14,14),'#826a56');rect(10,(2,2,13,4),'#b08f68');rect(10,(11,9,12,10),'#66e6ce')
rect(11,(2,2,13,13),'#293547');rect(11,(3,3,12,10),'#4bd2bd');rect(11,(4,4,11,8),'#15434f');rect(11,(4,12,11,13),'#8da2ac')
rect(12,(1,0,14,15),'#26364d');rect(12,(2,1,12,4),'#fc6a9b');rect(12,(3,6,9,12),'#3c8196');rect(12,(10,6,11,10),'#71f7da');rect(12,(3,14,11,15),'#101d31')
rect(13,(2,3,13,12),'#bcab87');rect(13,(3,4,12,11),'#474e65');rect(13,(4,5,10,5),'#def1d7');rect(13,(4,7,11,7),'#e8b6b7');rect(13,(4,9,9,9),'#bcd0d0')
rect(14,(2,2,13,13),'#61717f');rect(14,(3,3,12,11),'#293a4b');rect(14,(5,4,6,9),'#53e8cb');rect(14,(9,4,10,9),'#e56b94')
rect(15,(0,0,15,15),'#ffffff')
im.save(R/'tiles.png')
# Pixel character atlas: 4 directions x 3 animation phases, rows player/zombie/teacher/student.
sp=Image.new('RGBA',(192,96));sd=ImageDraw.Draw(sp)
for kind in range(4):
 for direction in range(4):
  for frame in range(3):
   ox=(direction*3+frame)*16;oy=kind*24
   def b(x,y,w,h,c):sd.rectangle((ox+x,oy+y,ox+x+w-1,oy+y+h-1),fill=c)
   skin=['#e1b898','#95a990','#d6b9a6','#d4ab8d'][kind];shirt=['#62cbd4','#775e82','#c8c5d1','#d69481'][kind]
   off=[0,-1,1][frame]
   b(3,20,11,2,'#101628');b(4,16,3,5+off,'#263549');b(9,16,3,5-off,'#263549');b(3,20+off,4,2,'#111a2a');b(9,20-off,4,2,'#111a2a')
   b(3,9,10,8,'#172337');b(4,9,8,7,shirt);b(1,10,3,6,skin);b(12,10,3,6,skin)
   b(4,1,8,8,'#222132');b(5,3,7,6,skin);b(4,1,8,3,'#33303d');b(3,3,2,3,'#33303d')
   if direction==0:b(6,6,1,1,'#172034');b(10,6,1,1,'#172034')
   if direction==1:b(4,3,3,5,'#35313e')
   if direction==2:b(9,3,3,5,'#35313e')
   if direction==3:b(4,2,8,6,'#33303d')
   if kind==0:
    b(5,10,6,7,'#c58b5d');b(6,11,4,4,'#79594c');b(5,10,1,7,'#e6b888')
   if kind==1:b(6,6,1,1,'#f589a0');b(10,6,1,1,'#f589a0');b(4,14,2,2,'#454253')
   if kind==2:b(6,5,6,2,'#263247');b(7,9,2,6,'#535679')
sp.save(R/'people.png')
# Fixed-width Cyrillic-capable font atlas, baked to binary alpha for crisp pixel text.
font=ImageFont.truetype(str(Path(__file__).parent/'fonts'/'PressStart2P-Regular.ttf'),8)
chars=list(range(32,127))+list(range(0x410,0x450))+[0x401,0x451,0x2014,0x2192,0x2713]
fa=Image.new('RGBA',(256,math.ceil(len(chars)/32)*16));fd=ImageDraw.Draw(fa)
for i,cp in enumerate(chars):fd.text((i%32*8,i//32*16+2),chr(cp),font=font,fill='white')
a=fa.getchannel('A').point(lambda x:255 if x>90 else 0);fa.putalpha(a);fa.save(R/'font.png')
(R/'font.json').write_text(json.dumps(chars),encoding='utf8')
# Three wings, each a mini hub with functional rooms. Right-to-left traversal.
W,H=158,46
floor=[0]*(W*H);walls=[0]*(W*H);furn=[0]*(W*H)
def fill(a,x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy*W+xx]=t
rooms=[];inter=[];enemy=[];lights=[];rest=[];oid=1
def obj(layer,name,typ,x,y,props=None,w=16,h=16):
 global oid
 o={'id':oid,'name':name,'type':typ,'x':x,'y':y,'width':w,'height':h,'rotation':0,'visible':True}
 oid+=1
 if props:o['properties']=[{'name':k,'type':'bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'float' if isinstance(v,float) else 'string','value':v} for k,v in props.items()]
 layer.append(o);return o
for block,x0 in [(1,4),(2,56),(3,108)]:
 fill(floor,x0,20,46,6,2)
 # Exterior shell and rooms.
 for x,y,w,h,name in [(x0,5,20,15,'354' if block==1 else 'CAM' if block==2 else 'POWER'),(x0+23,5,23,15,'NOTICE' if block==2 else 'CLASS'),(x0,26,20,15,'SECRET' if block==1 else 'SERVICE'),(x0+23,26,23,15,'361' if block==3 else 'CLASS')]:
  fill(floor,x,y,w,h,1 if block!=2 else 3)
  fill(walls,x,y,w,1,5);fill(walls,x,y+h-1,w,1,5);fill(walls,x,y,1,h,5);fill(walls,x+w-1,y,1,h,5)
  doorx=x+w//2;doory=y+h-1 if y<20 else y
  fill(walls,doorx-1,doory,3,1,0)
  # door object spans the opening and closes with E, route doors start open.
  obj(inter,name+' DOOR','door',(doorx-1)*16,doory*16,{'open':True},48,16)
  rooms.append((x,y,w,h,name))
  if name not in ['354','POWER','SECRET']:
   for yy in range(y+4,y+h-2,4):
    for xx in range(x+3,x+w-3,5):furn[yy*W+xx]=6;furn[(yy+1)*W+xx]=8
  furn[(y+1)*W+x+1]=7
  furn[(y+1)*W+x+w-2]=10
  obj(lights,'ROOM','lamp',(x+w/2)*16,(y+h/2)*16,{'radius':150.0,'flicker':True})
 # corridor borders except door holes
 for yy in [19,26]:
  for xx in range(x0,x0+46):
   if floor[(yy)*W+xx]==0:walls[yy*W+xx]=5
 # two zombies per block with open patrol lines
 for k in range(2):
  route=[{'x':0,'y':0},{'x':(24 if k==0 else -24)*16,'y':0}]
  o=obj(enemy,'PATROL','zombie',(x0+8+k*28)*16,(22+k*2)*16,{'block':block});o['polyline']=route
 for k in [8,25,40]:obj(lights,'CORRIDOR','lamp',(x0+k)*16,23*16,{'radius':115.0,'flicker':True})
for x in [50,51,52,53,54,55,102,103,104,105,106,107]:fill(floor,x,22,1,2,4)
for a,b in [(50,56),(102,108)]:
 fill(walls,a,21,b-a,1,5);fill(walls,a,24,b-a,1,5)
obj(inter,'GATE 2','gate',103*16,22*16,{'requires':'power'},16,32)
obj(inter,'GATE 1','gate',51*16,22*16,{'requires':'code'},16,32)
obj(inter,'361','spawn',144*16,36*16)
obj(inter,'POWER','power',111*16,8*16)
obj(inter,'BELL','bell',128*16,21*16)
obj(inter,'TIMETABLE','schedule',84*16,7*16)
obj(inter,'NOTICE','notice',82*16,7*16)
obj(inter,'ACCESS','terminal',58*16,21*16)
obj(inter,'VENDING','vending',87*16,24*16)
obj(inter,'CAMERA','camera',60*16,8*16)
obj(inter,'NOTE','note',136*16,30*16)
obj(inter,'CARTRIDGE','cartridge',8*16,8*16)
obj(inter,'VENT','vent',18*16,7*16)
obj(inter,'TEACHER','teacher',11*16,9*16)
obj(inter,'SECRET','secret',8*16,30*16)
for x,y,w,h,name in rooms:
 for k in range(4):
  xx=random.randint(x+2,x+w-3);yy=random.randint(y+2,y+h-3)
  if furn[yy*W+xx]==0:obj(rest,'PAPER','paper',xx*16,yy*16)
def tl(name,data,id):return {'id':id,'name':name,'type':'tilelayer','width':W,'height':H,'visible':True,'opacity':1,'x':0,'y':0,'data':data}
def ol(name,objects,id):return {'id':id,'name':name,'type':'objectgroup','visible':True,'opacity':1,'x':0,'y':0,'draworder':'topdown','objects':objects}
mp={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','infinite':False,'width':W,'height':H,'tilewidth':16,'tileheight':16,'nextlayerid':8,'nextobjectid':oid,'layers':[tl('Floor',floor,1),tl('Walls',walls,2),tl('Furniture',furn,3),ol('Interaction',inter,4),ol('Enemies',enemy,5),ol('Lighting',lights,6),ol('Restoration',rest,7)],'tilesets':[{'firstgid':1,'name':'AITU','image':'tiles.png','imagewidth':256,'imageheight':256,'tilewidth':16,'tileheight':16,'tilecount':256,'columns':16,'tiles':[{'id':4,'properties':[{'name':'solid','type':'bool','value':True},{'name':'blocksVision','type':'bool','value':True}]},{'id':5,'properties':[{'name':'solid','type':'bool','value':True}]},{'id':6,'properties':[{'name':'solid','type':'bool','value':True},{'name':'blocksVision','type':'bool','value':True}]}]}]}
(R/'floor3.tmj').write_text(json.dumps(mp),encoding='utf8')
(R/'config.json').write_text(json.dumps({'playerSpeed':78,'quietSpeed':43,'zombieSpeed':32,'chaseSpeed':64,'visionRange':126,'suspicionSeconds':0.85,'professor':'Преподаватель','course':'Computer Graphics','code':'1140'},ensure_ascii=False,indent=2),encoding='utf8')
# Small original synthesizer soundscape; no third-party music.
def wav(name,duration,func):
 rate=22050
 with wave.open(str(R/name),'wb') as f:
  f.setparams((1,2,rate,0,'NONE','not compressed'))
  f.writeframes(b''.join(struct.pack('<h',max(-32767,min(32767,int(func(i/rate)*32767)))) for i in range(int(duration*rate))))
wav('bell.wav',1.6,lambda t:.23*math.exp(-t*2.8)*(math.sin(t*2*math.pi*880)+.35*math.sin(t*2*math.pi*1320)))
wav('hum.wav',2,lambda t:.12*math.sin(t*2*math.pi*95)*(1-t/2)+random.uniform(-.025,.025))
wav('click.wav',.09,lambda t:.15*math.sin(t*2*math.pi*480)*max(0,1-t/.09))
wav('alarm.wav',.5,lambda t:.12*math.sin(t*2*math.pi*(300+math.sin(t*18)*90)))
wav('cheer.wav',2,lambda t:.13*math.sin(t*2*math.pi*(330 if t<.5 else 440 if t<1 else 550))*(1-t/2))
notes=[55,55,65.41,49]
wav('outbreak.wav',16,lambda t:.08*math.sin(2*math.pi*notes[int(t/4)%4]*t)+.025*math.sin(2*math.pi*110*t)*(0.3+0.7*max(0,1-(t%0.5)*7)))
notes2=[261.63,329.63,392,523.25,392,329.63,293.66,392]
wav('restored.wav',8,lambda t:.12*math.sin(2*math.pi*notes2[int(t)%8]*t)*math.exp(-(t%1)*2)+.04*math.sin(2*math.pi*130.81*t))
print('Assets generated')
