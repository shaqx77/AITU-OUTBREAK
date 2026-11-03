"""v0.5 locker, large lecture hall and biologist rescue quest. Run after story_upgrade.py."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1]/'assets'
story=json.loads((R/'story.json').read_text(encoding='utf8'))
story['intro'][3]['text']='Давай я постою на шухере у двери, чтобы зомби не вошли.\nА ты заходи в компьютер: там есть первая подсказка.'
story['intro'][5]['text']='Хорошо. Вы прикрывайте дверь, а я проверю компьютер.\nПотом заберу свои вещи — без них далеко не уйти.'
story['quest']={'speaker':'КОМПЬЮТЕР / ПЕРВОЕ ЗАДАНИЕ','portrait':0,'text':'Забери телефон и личные вещи из своего локера.\nОн в левом конце коридора блока 3, вдоль стены.\nОстальные сведения сейчас недоступны.'}
story['lockerPin']='2008'
story['video']=[
 {'speaker':'Д-Р СЕРИК / БИОЛОГ / ЗАПИСЬ','portrait':2,'text':'Если вы смотрите эту запись, заражение уже началось.\nЯ знал, что это может произойти, и подготовил решение.'},
 {'speaker':'Д-Р СЕРИК / БИОЛОГ / ЗАПИСЬ','portrait':2,'text':'Заражённых ещё можно вылечить. Нейтрализатор нужно\nраспылить через общую вентиляцию университета.'},
 {'speaker':'Д-Р СЕРИК / БИОЛОГ / ЗАПИСЬ','portrait':2,'text':'Карта на кафедре нужна только здесь, в третьем блоке:\nона открывает эту запись и завершает местное задание.'},
 {'speaker':'Д-Р СЕРИК / БИОЛОГ / ЗАПИСЬ','portrait':2,'text':'В блоке 2 включите резервное питание. Затем найдите\nбезопасный кабинет 354 в первом блоке. Газ хранится там.'},
 {'speaker':'Д-Р СЕРИК / БИОЛОГ / ЗАПИСЬ','portrait':2,'text':'В 354 подключите картридж к распределителю, выберите\nВСЕ БЛОКИ и запустите вентиляцию. Запишите этот план.'}]
story['notes']=['Посмотреть запись биолога в блоке 3', 'Включить резервное питание в служебной блока 2', 'Найти безопасную аудиторию 354 в блоке 1', 'Взять газовый нейтрализатор в 354', 'Подключить газ и включить общий кондиционер']
(R/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf8')
j=json.loads((R/'floor3.tmj').read_text());L={l['name']:l for l in j['layers']};W=j['width'];fl=L['Floor']['data'];wa=L['Walls']['data'];fu=L['Furniture']['data'];objects=L['Interaction']['objects']
objects[:]=[o for o in objects if o['type'] not in ('bottles','bell','lightpanel','locker','projector','serum','powerpanel','vent') and not(o['type']=='door' and o['y']==19*16 and o['x']>=108*16) and not(o['type']=='room' and o['x']>=108*16 and o['y']==5*16)]
def prop(o,k,v):
 ps=o.setdefault('properties',[]);ps[:]=[p for p in ps if p['name']!=k];ps.append({'name':k,'type':'bool' if isinstance(v,bool) else 'string','value':v})
for o in objects:
 if o['type']=='keycard':o.update(name='LECTERN KEYCARD',x=129*16,y=9*16)
 if o['type']=='door' and o['name']=='CAM DOOR':prop(o,'open',True);o['properties']=[p for p in o.get('properties',[]) if p['name']!='requires']
 if o['type']=='door' and o['name']=='361 DOOR':prop(o,'open',False)
def obj(t,name,x,y,w=16,h=16,props=None):
 id=j['nextobjectid'];j['nextobjectid']+=1
 o={'id':id,'type':t,'name':name,'x':x,'y':y,'width':w,'height':h,'rotation':0,'visible':True};objects.append(o)
 if props:
  for k,v in props.items():prop(o,k,v)
 return o
# Merge the former switchboard and adjacent classroom into one large lecture hall.
for y in range(5,20):
 for x in range(108,154):
  fl[y*W+x]=1;fu[y*W+x]=0;wa[y*W+x]=5 if x in (108,153) or y in (5,19) else 0
for x in [129,130,131]:wa[19*W+x]=0
obj('room','LARGE LECTURE',108*16,5*16,46*16,15*16)
obj('door','LECTURE DOOR',129*16,19*16,48,16,{'open':True})
for y in [11,14,17]:
 for x in [112,118,124,136,142,148]:
  fu[y*W+x]=6;fu[y*W+x+1]=31;fu[(y+1)*W+x]=8;fu[(y+1)*W+x+1]=8
for x in [110,151]:fu[6*W+x]=10
obj('projector','BIOLOGIST RECORDING',135*16,7*16)
obj('locker','MY LOCKER 08',110*16,20*16,16,32)
for x in [109,110,111,112,113]:fu[20*W+x]=45
obj('serum','NEUTRALIZER 354',8*16,8*16)
obj('powerpanel','BACKUP POWER',59*16,28*16)
obj('vent','DISTRIBUTION 354',18*16,7*16)
# Use only known, passable interactable positions. Furniture stays beside objectives.
fu[8*W+8]=0;fu[28*W+59]=0;fu[9*W+129]=0
flags={t['id']:t for t in j['tilesets'][0]['tiles']}
flags[44]={'id':44,'properties':[{'name':'solid','type':'bool','value':True},{'name':'blocksVision','type':'bool','value':True}]}
j['tilesets'][0]['tiles']=list(flags.values())
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
im=Image.open(R/'tiles.png').convert('RGBA');d=ImageDraw.Draw(im)
def b(n,box,c):
 x=n%16*16;y=n//16*16;d.rectangle((x+box[0],y+box[1],x+box[2],y+box[3]),fill=c)
def clear(n):b(n,(0,0,15,15),(0,0,0,0))
clear(44);b(44,(0,0,15,15),'#273d50');b(44,(1,0,14,13),'#91a5aa');b(44,(2,1,13,2),'#c2d4cd');b(44,(2,4,13,4),'#5d7d8e');b(44,(2,6,13,6),'#5d7d8e');b(44,(10,8,12,11),'#274c65');b(44,(11,9,11,10),'#7fefd1');b(44,(1,14,14,15),'#3e5368')
clear(45);b(45,(1,2,14,13),'#183443');b(45,(2,3,13,11),'#9ac0b8');b(45,(6,5,6,9),'#42c5c7');b(45,(7,6,8,8),'#42c5c7');b(45,(9,7,10,7),'#42c5c7')
clear(46);b(46,(4,0,11,15),'#243a4e');b(46,(5,1,10,4),'#83ceca');b(46,(5,5,10,12),'#43979f');b(46,(6,7,9,9),'#bce7cf');b(46,(5,13,10,14),'#b8d0bc')
im.save(R/'tiles.png')
# Fifth player row: hoodie without a backpack until the locker is opened.
people=Image.open(R/'people.png').convert('RGBA');out=Image.new('RGBA',(384,240));out.paste(people.crop((0,0,384,192)),(0,0));out.paste(people.crop((0,0,384,48)),(0,192));pd=ImageDraw.Draw(out)
for cell in range(12):
 ox=cell*32;oy=192
 pd.rectangle((ox+11,oy+20,ox+24,oy+35),fill='#3b879c');pd.rectangle((ox+12,oy+20,ox+14,oy+31),fill='#65aab5');pd.rectangle((ox+22,oy+21,ox+24,oy+33),fill='#2a6076');pd.rectangle((ox+15,oy+28,ox+21,oy+30),fill='#4b9daa')
out.save(R/'people.png')
print('Locker, large lecture hall and rescue quest data ready')
