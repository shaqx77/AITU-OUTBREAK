"""v0.6 second campus pass: run after detail_upgrade.py, before building."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,random
R=Path(__file__).resolve().parents[1]/'assets'
j=json.loads((R/'floor3.tmj').read_text(encoding='utf8'));W=j['width']
L={l['name']:l for l in j['layers']};floor,walls,furn=[L[n]['data'] for n in ('Floor','Walls','Furniture')]
objects=L['Interaction']['objects']
objects[:]=[o for o in objects if not (o['type']=='room' and o['y']==5*16 and o['x']>=108*16)
           and not(o['type']=='door' and o['y']==19*16 and o['x']>=108*16)]
def obj(t,name,x,y,w,h,**props):
    objects.append(dict(id=j['nextobjectid'],type=t,name=name,x=x*16,y=y*16,width=w*16,height=h*16,
                        visible=True,rotation=0,properties=[dict(name=k,type='bool',value=v) for k,v in props.items()]))
    j['nextobjectid']+=1
# Keep the lecture hall on the left, rebuild right as a computer classroom.
for y in range(5,20):
    for x in range(108,154):
        i=y*W+x;floor[i]=1;furn[i]=0
        walls[i]=5 if x in (108,132,153) or y in (5,19) else 0
obj('room','LECTURE LEFT',108,5,25,15)
obj('room','COMPUTER CLASSROOM',132,5,22,15)
for x,name in ((119,'LECTURE DOOR'),(141,'IT CLASS DOOR')):
    for xx in range(x,x+3):walls[19*W+xx]=0;furn[20*W+xx]=0
    obj('door',name,x,19,3,1,open=True)
# Clear adjacent locker segments for both new entrances.
for x in (118,122,140,144):furn[20*W+x]=0
for y in (11,14,17):
    for x in (111,117,125):
        furn[y*W+x]=6;furn[y*W+x+1]=31;furn[(y+1)*W+x]=8;furn[(y+1)*W+x+1]=8
    for x in (135,141,148):
        furn[y*W+x]=6;furn[y*W+x+1]=31;furn[(y+1)*W+x]=8
for x in (110,130,134,151):furn[6*W+x]=10
for y in (9,12):furn[y*W+152]=51
furn[7*W+135]=33;furn[7*W+149]=34;furn[7*W+150]=35
for o in objects:
    if o['type']=='projector':o.update(x=124*16,y=7*16)
    if o['type']=='keycard':o.update(x=119*16,y=9*16)

# Hand drawn grout cracks and sparse green moss / fallen leaves.
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def b(n,rect,c):
    x,y=n%16*16,n//16*16;d.rectangle((x+rect[0],y+rect[1],x+rect[2],y+rect[3]),fill=c)
def tile(n,source):
    im.paste(im.crop((source%16*16,source//16*16,source%16*16+16,source//16*16+16)),(n%16*16,n//16*16))
for n,source in ((56,2),(57,0),(58,2),(59,0)):
    tile(n,source)
    # These remain walkable floor tiles, never collision props.
    for xx,yy in ((2,3),(7,10),(12,5)):
        b(n,(xx,yy,xx+2,yy),'#4c7157');b(n,(xx+1,yy-1,xx+3,yy-1),'#6d8661')
        b(n,(xx+1,yy+1,xx+1,yy+2),'#394e42')
    b(n,(0,12,1,15),'#455e50');b(n,(2,14,4,15),'#58715b')
    b(n,(9,0,9,2),'#354a54');b(n,(10,3,11,3),'#41565c')
rng=random.Random(608)
for y in range(j['height']):
    for x in range(W):
        i=y*W+x
        if not floor[i] or walls[i]:continue
        if floor[i] in (57,58,59,60):floor[i]=3 if floor[i] in (57,59) else 1
        if rng.random()<(.29 if y in (21,24) else .065):
            floor[i]=(57 if floor[i]==3 else 58) if (x+y)%2 else (59 if floor[i]==3 else 60)
im.save(R/'tiles.png')

# Preserve 4 directions and all walk frames, add small anatomy/clothing clusters.
im=Image.open(R/'people.png').convert('RGBA');d=ImageDraw.Draw(im)
for row in (0,1,4):
    for direction in range(4):
        for frame in range(3):
            ox=(direction*3+frame)*32;oy=row*48
            def p(x,y,w,h,c):d.rectangle((ox+x,oy+y,ox+x+w-1,oy+y+h-1),fill=c)
            if row in (0,4):
                # Hoodie drawstrings, ribbed cuffs, ID lanyard and sewn bag pockets.
                p(5,27,3,2,'#91c2c4');p(28,27,3,2,'#679da9')
                p(10,19,1,6,'#b1d5d1');p(23,19,1,6,'#b1d5d1')
                p(10,35,2,4,'#5a7188');p(21,35,1,3,'#5a7188')
                if row==0:
                    p(13,21,8,1,'#e8c69a');p(12,24,1,7,'#e5bb89')
                    p(20,26,2,5,'#c9a576');p(14,29,5,1,'#392f32')
                    p(15,30,4,2,'#c19364');p(17,30,1,1,'#f0d3a3')
                else:
                    p(17,18,1,9,'#b8c9c7');p(16,27,4,4,'#d2dfd5');p(17,28,2,1,'#416d80')
                    p(13,31,9,1,'#29657f')
                if direction==0:
                    p(10,7,2,1,'#cb9b76');p(14,11,1,1,'#ead0a6');p(17,13,3,1,'#c28d73')
            else:
                # Ragged student jacket, exposed infected skin, fingers and trousers.
                p(4,22,2,6,'#70877e');p(29,24,2,6,'#718c7e')
                p(6,33,1,3,'#455c54');p(29,33,1,3,'#4b6254')
                p(11,21,3,3,'#3d414e');p(12,22,1,1,'#88a087')
                p(22,28,3,3,'#354651');p(23,28,1,2,'#9ca58b')
                p(14,31,2,3,'#778070');p(20,36,3,2,'#586157')
                p(10,39,3,1,'#718084');p(23,34,1,3,'#839186')
                p(17,19,1,8,'#9faca0');p(17,28,3,3,'#778d83')
                if direction==0:
                    p(10,12,3,2,'#5e776d');p(21,12,3,1,'#596b62')
                    p(12,10,2,1,'#e0a577');p(21,10,2,1,'#e0a577')
                    p(15,14,5,2,'#414a46');p(16,14,2,1,'#a8ad91')
                elif direction==1:p(23,12,2,2,'#718571')
                elif direction==2:p(9,12,2,2,'#718571')
im.save(R/'people.png')
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
print('Split lecture/IT classroom, moss/leaf tile variants and character detail ready')
