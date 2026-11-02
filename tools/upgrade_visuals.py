"""AITU-inspired original pixel tiles and campus furnishing pass.
Run after make_assets.py to recreate the v2 art/map; modifies generated assets.
References: https://astanait.edu.kz/ru/project8 (virtual campus, not an exact replica).
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,random
R=Path(__file__).resolve().parents[1]/'assets';im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def r(n,box,c):
 x=n%16*16;y=n//16*16;d.rectangle((x+box[0],y+box[1],x+box[2],y+box[3]),fill=c)
def clear(n):r(n,(0,0,15,15),(0,0,0,0))
# Low-contrast broad porcelain tiles and ash parquet, not a dark repeated grid.
for n in range(4):
 if n==0:
  r(n,(0,0,15,15),'#9a9188');r(n,(0,0,0,15),'#817b78');r(n,(8,0,8,15),'#b1a59a')
  for y in [3,7,11,15]:r(n,(1,y,15,y),'#867e77')
  r(n,(2,5,6,5),'#a39a8b');r(n,(10,9,14,9),'#ada091')
 elif n==2:
  r(n,(0,0,15,15),'#565a75');r(n,(0,0,15,0),'#51566c');r(n,(0,0,0,15),'#51566c')
 else:
  r(n,(0,0,15,15),'#8c969d' if n==1 else '#b4bdc0');r(n,(0,0,15,0),'#7d8991' if n==1 else '#a1afb2');r(n,(0,0,0,15),'#7d8991' if n==1 else '#a1afb2');r(n,(1,1,15,1),'#98a3a8' if n==1 else '#c2c9c8')
# Solid walls: contemporary silver-grey panels with a crisp navy cap.
r(4,(0,0,15,15),'#202c3d');r(4,(0,0,15,2),'#d0d6d5');r(4,(1,3,14,11),'#889699');r(4,(1,3,14,4),'#b6c2c3');r(4,(1,12,14,14),'#414f61');r(4,(0,15,15,15),'#172338')
# White ash desks with laptops and orange/teal ergonomic seats.
clear(5);r(5,(0,4,15,13),'#293246');r(5,(0,1,14,10),'#c7b69a');r(5,(1,1,13,2),'#efdfbc');r(5,(0,10,14,11),'#8f8377');r(5,(2,12,3,14),'#344357');r(5,(12,12,13,14),'#344357');r(5,(5,3,11,7),'#233950');r(5,(6,4,10,6),'#56bbc6');r(5,(4,8,12,9),'#6b737c');r(5,(2,3,3,4),'#f5edc8')
clear(6);r(6,(0,1,15,15),'#303b4a');r(6,(1,0,14,12),'#c2b296');r(6,(1,0,14,1),'#e1d6ba');r(6,(2,2,6,11),'#d0bfa0');r(6,(8,2,13,11),'#ab9c89');r(6,(6,5,6,7),'#4a5965');r(6,(12,5,12,7),'#52616c')
clear(7);r(7,(4,9,11,14),'#253449');r(7,(3,1,12,9),'#914953');r(7,(4,1,11,2),'#f1a078');r(7,(4,3,11,7),'#cb775d');r(7,(4,10,5,14),'#9da7a6');r(7,(10,10,11,14),'#9da7a6')
# Glass facades. Blocking movement but transparent for both light and AI sight.
clear(16);r(16,(0,0,15,15),'#4e8290');r(16,(1,2,14,12),'#5a9ba7');r(16,(2,3,5,9),'#7cbdc3');r(16,(2,3,12,3),'#aed8d5');r(16,(0,0,15,1),'#bccaca');r(16,(0,14,15,15),'#5b687a');r(16,(0,0,1,15),'#cbd3cf');r(16,(14,0,15,15),'#34485b')
# Carpet blocks, colored lounge furniture, workstation, light path, server.
for n,col in [(17,'#485f73'),(18,'#61536f')]:
 r(n,(0,0,15,15),col)
 for y in range(1,16,3):r(n,(0,y,15,y),'#526477' if n==17 else '#6c5b79')
clear(19);r(19,(0,3,15,14),'#203d42');r(19,(1,1,14,11),'#477b60');r(19,(1,1,14,3),'#81a873');r(19,(2,5,7,10),'#5d956e');r(19,(9,5,13,10),'#548965');r(19,(0,4,1,12),'#a1b084');r(19,(14,4,15,12),'#304e49');r(19,(2,13,13,14),'#142d3b')
clear(20);r(20,(2,3,13,13),'#2e3549');r(20,(2,1,12,10),'#b36f51');r(20,(3,1,11,3),'#ecb07a');r(20,(4,5,11,10),'#d69569')
clear(21);r(21,(0,0,15,12),'#b9ae98');r(21,(1,0,14,1),'#eee6ca');r(21,(1,11,14,12),'#6c7883');r(21,(2,2,13,8),'#1a2e49');r(21,(3,3,12,6),'#45c8c9');r(21,(4,4,8,4),'#b8ffff');r(21,(3,10,12,10),'#616a7c')
r(22,(0,0,15,15),'#849098');r(22,(0,7,15,9),'#4d9db1');r(22,(1,7,14,7),'#79d3d5')
r(23,(0,0,15,15),'#849098');r(23,(0,7,15,9),'#d2af69');r(23,(0,7,15,7),'#ffe29b')
clear(24);r(24,(0,0,15,15),'#283b4e');r(24,(1,1,14,13),'#63778b');r(24,(2,2,13,11),'#182c45');r(24,(3,4,12,4),'#46627a');r(24,(3,7,12,7),'#46627a');r(24,(3,10,12,10),'#46627a');r(24,(4,4,4,4),'#69e8be');r(24,(10,7,10,7),'#ef7cac');r(24,(4,13,11,14),'#a9b4b7')
clear(25);r(25,(2,1,13,14),'#323b4f');r(25,(3,2,12,12),'#7e2b5b');r(25,(4,3,11,9),'#cb497e');r(25,(4,10,11,11),'#43a7c6');r(25,(4,4,7,4),'#f9b7b4')
clear(26);r(26,(0,5,15,11),'#364b62');r(26,(1,4,14,9),'#485c75');r(26,(2,4,13,5),'#9ab1b5');r(26,(3,6,11,7),'#6c91a5');r(26,(0,9,15,10),'#11263b')
clear(27);r(27,(6,2,10,14),'#246569');r(27,(7,0,9,2),'#a1e1d6');r(27,(6,5,10,8),'#9ac9b2');r(27,(7,10,9,12),'#47b9b1')
clear(28);r(28,(1,1,14,14),'#243c4d');r(28,(2,2,13,11),'#2584a8');r(28,(3,3,12,4),'#86e7e5');r(28,(3,6,8,6),'#c2e6dc');r(28,(3,9,11,9),'#629fb2')
clear(29);r(29,(4,3,12,10),'#c1b2a1');r(29,(5,4,10,9),'#8f7469');r(29,(3,10,6,14),'#78666b');r(29,(11,9,13,11),'#4a4958')
clear(30);r(30,(0,4,15,13),'#293246');r(30,(0,1,14,10),'#c7b69a');r(30,(0,1,13,2),'#efdfbc');r(30,(0,10,14,11),'#8f8377');r(30,(12,12,13,14),'#344357');r(30,(3,4,9,8),'#dedac8');r(30,(4,5,8,5),'#8d9ca4');r(30,(11,3,12,4),'#4b8e97')
im.save(R/'tiles.png')
j=json.loads((R/'floor3.tmj').read_text());W=j['width'];layers={l['name']:l for l in j['layers']};fl=layers['Floor']['data'];wall=layers['Walls']['data'];furn=layers['Furniture']['data']
# Deterministic pass: same set of decorations if run again.
for b,x in [(1,4),(2,56),(3,108)]:
 for yy in range(20,26):
  for xx in range(x,x+46):fl[yy*W+xx]=2
 for xx in range(x,x+46):fl[23*W+xx]=23 if b!=2 else 24
 for yy in range(6,19):
  for xx in range(x+24,x+45):fl[yy*W+xx]=18 if b==2 else 19
 # Glass panels between corridor and classrooms, preserving all door openings.
 for xx in range(x+2,x+44):
  for yy in [19,26]:
   if wall[yy*W+xx] and xx%5!=0:wall[yy*W+xx]=17
 # Open corridor furniture stays outside the clear two central travel lanes.
 for xx in [x+5,x+6,x+29,x+30]:furn[20*W+xx]=20
 for xx in [x+14,x+37]:furn[25*W+xx]=27
 # Workstations in the computer lab, clear walkways preserved.
 if b==2:
  for yy in [9,13,17]:
   for xx in [x+3,x+8,x+13]:furn[yy*W+xx]=22
 for yy in [8,12,16]:furn[yy*W+x+44]=25
 # Magenta wall posters.
 for xx in [x+3,x+24,x+40]:furn[6*W+xx]=26
# Wider two-seat desks and a furnished final classroom.
for yy in range(j['height']):
 for xx in range(W-1):
  if furn[yy*W+xx]==6 and furn[yy*W+xx+1]==0:furn[yy*W+xx+1]=31
for xx in [8,15,20]:
 for yy in [12,16]:
  furn[yy*W+xx]=6;furn[yy*W+xx+1]=31;furn[(yy+1)*W+xx]=8;furn[(yy+1)*W+xx+1]=8
objects=layers['Interaction']['objects'];nextid=max(o['id'] for l in j['layers'] if l['type']=='objectgroup' for o in l['objects'])+1
objects[:]=[o for o in objects if o['type'] not in ('bottles','room')]
for x,y in [(146,32),(80,24),(12,15)]:
 if not any(o['type']=='bottles' and int(o['x'])==x*16 for o in objects):
  objects.append({'id':nextid,'name':'BOTTLES','type':'bottles','x':x*16,'y':y*16,'width':16,'height':16,'rotation':0,'visible':True});nextid+=1
# Explicit editable room bounds, used for fully lit occupied rooms.
for block,x0 in [(1,4),(2,56),(3,108)]:
 for x,y,w,h in [(x0,5,20,15),(x0+23,5,23,15),(x0,26,20,15),(x0+23,26,23,15)]:
  objects.append({'id':nextid,'name':'ROOM','type':'room','x':x*16,'y':y*16,'width':w*16,'height':h*16,'rotation':0,'visible':True});nextid+=1
j['nextobjectid']=nextid
def flag(id,solid,vision):return {'id':id,'properties':[{'name':'solid','type':'bool','value':solid},{'name':'blocksVision','type':'bool','value':vision}]}
j['tilesets'][0]['tiles']=[flag(4,True,True),flag(5,True,False),flag(6,True,True),flag(16,True,False),flag(19,True,True),flag(20,True,False),flag(21,True,False),flag(24,True,True),flag(26,True,False),flag(30,True,False)]
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
import wave,struct,math
random.seed(2)
with wave.open(str(R/'impact.wav'),'wb') as f:
 f.setparams((1,2,22050,0,'NONE','not compressed'))
 f.writeframes(b''.join(struct.pack('<h',int(10000*math.exp(-i/1700)*random.uniform(-1,1))) for i in range(11025)))
print('AITU-inspired campus pass applied')

