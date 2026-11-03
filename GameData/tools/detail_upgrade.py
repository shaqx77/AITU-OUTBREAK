"""v0.6. Run after rescue_upgrade.py; safe to repeat on the resulting map."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, math, wave, struct

R = Path(__file__).resolve().parents[1] / 'assets'
j = json.loads((R / 'floor3.tmj').read_text(encoding='utf8'))
layers = {l['name']: l for l in j['layers']}
old_width, width = j['width'], 174
for layer in j['layers']:
    if layer['type'] == 'tilelayer':
        data = layer['data']
        layer['data'] = [data[y*old_width+x] if x < old_width else 0
                         for y in range(j['height']) for x in range(width)]
        layer['width'] = width
j['width'] = width
floor, walls, furniture = [layers[n]['data'] for n in ('Floor', 'Walls', 'Furniture')]
objects = layers['Interaction']['objects']

def add(layer, kind, name, x, y, w=16, h=16, **props):
    o = dict(id=j['nextobjectid'], type=kind, name=name, x=x, y=y,
             width=w, height=h, rotation=0, visible=True)
    j['nextobjectid'] += 1
    o['properties'] = [dict(name=k, type='bool' if isinstance(v,bool) else
                           'float' if isinstance(v,(int,float)) else 'string', value=v)
                       for k,v in props.items()]
    layers[layer]['objects'].append(o)
    return o

# Replace only the former service office in block 3. Block 2 power quest stays intact.
objects[:] = [o for o in objects if not (
    (o['type']=='room' and o['x']==108*16 and o['y']==26*16)
    or (o['type']=='door' and o['y']==26*16 and 108*16<=o['x']<128*16)
    or o['name'].startswith(('V06 ', 'DEPT ')))]

def room(x,y,w,h,name,door_x=None):
    for yy in range(y,y+h):
        for xx in range(x,x+w):
            i=yy*width+xx
            floor[i]=1; furniture[i]=0
            walls[i]=5 if xx in (x,x+w-1) or yy in (y,y+h-1) else 0
    add('Interaction','room',name,x*16,y*16,w*16,h*16)
    if door_x is not None:
        for xx in range(door_x,door_x+2): walls[y*width+xx]=0
        add('Interaction','door',name+' DOOR',door_x*16,y*16,32,16,open=True)

room(108,26,10,15,'DEPT COMPUTER SCIENCE',111)
room(117,26,11,15,'DEPT SOFTWARE ENGINEERING',121)
room(156,18,15,16,'V06 SERVICE')
for y in (22,23):
    for x in range(153,157):
        floor[y*width+x]=3; walls[y*width+x]=0; furniture[y*width+x]=0
add('Interaction','door','V06 SERVICE DOOR',156*16,22*16,16,32,open=True)

# Offices: narrow workstations, books, printers, server racks and meeting corners.
for left,right in ((109,116),(118,127)):
    for x in range(left+1,right-1,3):
        for y in (30,35):
            furniture[y*width+x]=6; furniture[y*width+x+1]=31
            furniture[(y+1)*width+x]=8
    for y in (28,33,38): furniture[y*width+right-1]=51 if y!=33 else 52
    furniture[38*width+left+1]=10
for x in (158,160,162,164,166,168):
    furniture[20*width+x]=52
    furniture[30*width+x]=51 if x%4 else 53
for y in (25,28): furniture[y*width+169]=53
add('Interaction','note','V06 SERVICE LOG',160*16,25*16,text='Фильтры заменены. Резервное питание — в служебной блока 2.')

# Lockers follow the corridor walls, leaving every door approach open.
for base in (4,56,108):
    openings=set()
    for o in objects:
        if o['type']=='door' and o['y']==19*16:
            openings.update(range(int(o['x']/16)-1, int((o['x']+o['width'])/16)+1))
    for x in range(base+1,base+45):
        if x in openings: continue
        furniture[20*width+x]=45 if x%4==0 else 49 if x%4==1 else 50
    # Stone floor border and flush drainage/grilles, clear of the walking lanes.
    for x in range(base,base+46):
        floor[21*width+x]=54
        floor[24*width+x]=55
        if x%7==0: floor[23*width+x]=56
locker=next(o for o in objects if o['type']=='locker')
locker.update(x=151*16,y=20*16)
furniture[20*width+151]=45

# Opposite ends, with non-overlapping short patrols rather than crossing mid-corridor.
zombies=layers['Enemies']['objects']
block3=[o for o in zombies if any(p['name']=='block' and p['value']==3 for p in o.get('properties',[]))]
for o,x,end,y in zip(block3,(111,145),(119,150),(23,24)):
    o.update(x=x*16,y=y*16)
    o['polyline']=[dict(x=0,y=0),dict(x=(end-x)*16,y=0)]

lights=layers['Lighting']['objects']
lights[:]=[o for o in lights if not o['name'].startswith('V06 ')]
for base in (4,56,108):
    for offset in (6,18,31,42):
        add('Lighting','light','V06 EMERGENCY', (base+offset)*16,21.6*16,
            radius=94, flicker=True, emergency=True)
add('Lighting','light','V06 SERVICE LIGHT',163*16,25*16,radius=108,flicker=True)
for x in (112,122):
    add('Lighting','light','V06 OFFICE LIGHT',x*16,33*16,radius=85,flicker=True)

flags={t['id']:t for t in j['tilesets'][0]['tiles']}
for tile in (48,49,50,51,52):
    flags[tile]=dict(id=tile,properties=[dict(name=n,type='bool',value=True) for n in ('solid','blocksVision')])
j['tilesets'][0]['tiles']=list(flags.values())
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
story=json.loads((R/'story.json').read_text(encoding='utf8'))
story['quest']['text']=story['quest']['text'].replace('левом','правом')
(R/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf8')

# Original pixel atlas details. No filters: every highlight stays on the pixel grid.
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def box(n,rect,c):
    x,y=n%16*16,n//16*16
    d.rectangle((x+rect[0],y+rect[1],x+rect[2],y+rect[3]),fill=c)
def clear(n): box(n,(0,0,15,15),(0,0,0,0))
for n,body in ((44,'#a2b9bc'),(48,'#6f95a6'),(49,'#9fabb7')):
    clear(n);box(n,(0,0,15,15),'#1d3147');box(n,(1,0,14,13),body)
    box(n,(2,1,13,1),'#c9e0df');box(n,(2,3,13,3),'#4d6f82')
    for y in (5,6):box(n,(3,y,8,y),'#3a576c')
    box(n,(11,8,12,11),'#263f52');box(n,(12,8,12,8),'#74edce')
    box(n,(3,8,7,10),'#d8e4de');box(n,(4,9,5,9),'#476175')
    box(n,(1,14,14,14),'#60788d');box(n,(2,15,13,15),'#162b42')
clear(50);box(50,(0,0,15,15),'#34424e');box(50,(1,1,14,14),'#b7b2a1')
for x in range(2,14,3):
    box(50,(x,2,x+1,12),['#537f92','#a16d60','#c5ae6a','#70958c'][x//3%4])
    box(50,(x,3,x+1,3),'#d0d9c7')
box(50,(1,13,14,14),'#53616a')
clear(51);box(51,(1,0,14,15),'#172b3d');box(51,(2,1,13,14),'#334f62')
for y in (2,5,8,11):
    box(51,(3,y,12,y+1),'#162c3c');box(51,(4,y,5,y),'#59ddbc');box(51,(9,y,11,y),'#6b8692')
clear(52);box(52,(1,4,14,14),'#40586b');box(52,(3,1,12,7),'#cbd8d0')
box(52,(2,8,13,10),'#a2b8bc');box(52,(4,11,11,14),'#152c3b');box(52,(11,8,12,8),'#5bebbd')
for n in (53,54,55):
    box(n,(0,0,15,15),'#63798d');box(n,(1,1,14,14),'#71869b')
    box(n,(0,15,15,15),'#3d586d');box(n,(15,0,15,15),'#4f697b')
    if n==53:
        box(n,(0,0,15,2),'#254554');box(n,(0,3,15,3),'#55b6b1')
    elif n==54:
        box(n,(0,12,15,14),'#284858');box(n,(0,11,15,11),'#55b6b1')
    else:
        box(n,(2,5,13,10),'#334f63')
        for x in range(3,13,2): box(n,(x,6,x,9),'#718a98')
# Add readable keycaps, notebook margins and desk edge screws.
for n in (5,30):
    for x in (2,13): box(n,(x,13,x,13),'#48596a')
    box(n,(1,14,14,14),'#8b8777')
    if n==5:
        for y in (9,11):
            for x in range(2,8,2): box(n,(x,y,x,y),'#92aeb7')
    else:
        box(n,(4,5,4,10),'#b98c82')
        for y in (6,8,10): box(n,(6,y,11,y),'#9aaca7')
im.save(R/'tiles.png')

# Three short, original voiced vowel murmurs; played with the student's typewriter.
rate=22050
for k in range(3):
    samples=[];duration=.095+k*.014
    for i in range(int(rate*duration)):
        t=i/rate;u=t/duration;f0=112+k*13+7*math.sin(u*4)
        # Harmonic voice source with low nasal vowel formants and soft envelope.
        value=0
        for h in range(1,19):
            freq=f0*h
            weight=.6*math.exp(-((freq-(410+k*50))/190)**2)+.22*math.exp(-((freq-1120)/240)**2)
            value+=math.sin(2*math.pi*freq*t)*weight/h
        samples.append(int(max(-1,min(1,value*math.sin(math.pi*u)**1.5))*.45*32767))
    with wave.open(str(R/f'mutter-{k}.wav'),'wb') as wav:
        wav.setparams((1,2,rate,0,'NONE','not compressed'))
        wav.writeframes(struct.pack('<'+'h'*len(samples),*samples))
print('v0.6 map, departments, right service, lockers, emergency lamps and murmurs ready')
