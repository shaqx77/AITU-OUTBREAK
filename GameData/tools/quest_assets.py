"""Current v0.11 map content and English story. No previous releases required."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets'
p=A/'floor3.tmj';m=json.loads(p.read_text(encoding='utf8'));layers={l['name']:l for l in m['layers']};objects=layers['Interaction']['objects'];w=m['width']
translations=[
'There is still water in the cooler. Someone wrote on a cup: Do not touch - project defence in progress.',
'Cleaning closet: buckets, detergent and a mop. The sign reads: A clean floor is a survival skill.',
'Print queue: resumes, portfolios and FINAL_final.pdf. The printer has jammed again.',
'Student resumes, portfolios, project folders and grade sheets. Work continued here until the alarm.',
'The backup server is still running. A sticker says: Do not switch off, even during an outbreak.',
'Three monitors, cold coffee, loose cables and an open log: Fixed everything except the apocalypse.',
'Filters replaced. Backup power is in the lower-left technical room of block 2.'
]
strings=set()
def collect(x):
 if isinstance(x,str) and re.search('[\u0400-\u04ff]',x):strings.add(x)
 if isinstance(x,dict):
  for v in x.values():collect(v)
 if isinstance(x,list):
  for v in x:collect(v)
collect(m)
if strings:
 assert len(strings)==7
 mapping=dict(zip(sorted(strings),translations))
 def translate(x):
  if isinstance(x,str):return mapping.get(x,x)
  if isinstance(x,list):return [translate(v) for v in x]
  if isinstance(x,dict):return {k:translate(v) for k,v in x.items()}
  return x
 m=translate(m);layers={l['name']:l for l in m['layers']};objects=layers['Interaction']['objects']
# Idempotent additions, with clear access around every interaction.
objects[:]=[o for o in objects if o['type'] not in ('antidote','labnote','cache','mentor')]
next_id=max(o['id'] for l in m['layers'] if l['type']=='objectgroup' for o in l['objects'])+1
def add(kind,name,x,y,**props):
 global next_id
 o=dict(id=next_id,type=kind,name=name,x=x*16,y=y*16,width=16,height=16,rotation=0,visible=True,properties=[dict(name=k,type='int' if isinstance(v,int) else 'string',value=v) for k,v in props.items()]);next_id+=1;objects.append(o)
 for yy in range(y-1,y+2):
  for xx in range(x-1,x+2):
   if 0<=xx<w and 0<=yy<m['height']:layers['Furniture']['data'][yy*w+xx]=0
 return o
add('antidote','CULTURE BASE',146,15,component=0,label='Recover culture base')
add('labnote','COLD STORAGE PROTOCOL',138,8,component=0,text='CULTURE BASE / BLOCK 3\nNever warm a live sample before cooling the chamber.\nRecovery order: COOLANT (3), CULTURE (1), SEAL (2).\nThe station needs four seconds to seal the base. Save this ingredient before leaving the block.')
add('antidote','STABILIZER FILTER',92,12,component=1,label='Filter the stabilizer')
add('labnote','FILTRATION PROTOCOL',84,8,component=1,text='STABILIZER / BLOCK 2\nFirst restore the backup electrical supply downstairs.\nSet FILTER to 3, BUFFER to 1 and PRESSURE to 2.\nThen start the filter and wait for the sealed vial. Do not carry an unstable sample.')
add('antidote','CATALYST SCANNER',17,33,component=2,label='Calibrate the catalyst scanner')
add('labnote','CATALYST PROTOCOL',19,28,component=2,text='CATALYST / BLOCK 1\nThe cabinet lock responds to a calibrated scanner.\nPress SPACE while the marker crosses the green zone.\nThree accurate locks release the catalyst. There is no time limit. Take your time.')
add('mentor','KAMILA BATKULDINOVA',19,15)
for i,(x,text) in enumerate(((112,'Cold storage is above room 361. Read the protocol before touching the sample.'),(80,'The backup room and the filter lab use the same power supply. Visit both.'),(36,'The catalyst is in the lower archive lab. Kamila is waiting in safe classroom 354.'))):add('cache','EMERGENCY SUPPLIES',x,21,index=i,text=text)
m['nextobjectid']=next_id;p.write_text(json.dumps(m,ensure_ascii=False,separators=(',',':')),encoding='utf8')
story={
'intro':[
 {'speaker':'STUDENT','portrait':0,'text':'I arrived before everyone else today.\nFor once, I will not be late for Discrete Mathematics.'},
 {'speaker':'STUDENT','portrait':0,'text':'Why is the classroom empty?\nThe corridor is silent too. Something feels wrong.'},
 {'speaker':'STUDENT','portrait':0,'text':'What?! The lights went out! There is someone at the door.\nThose are not ordinary students. An outbreak has started.'},
 {'speaker':'Duman Adilet','portrait':1,'text':'Stay calm. I will guard the doorway so none of them get in.\nCheck the computer; it has your first clue.'},
 {'speaker':'Duman Adilet','portrait':1,'text':'The password is decimal 10 converted to binary.\nEnter all four digits. Take your phone and your bag afterward.'},
 {'speaker':'STUDENT','portrait':0,'text':'Understood, Duman Adilet. You watch the door.\nI will check the computer and find a way to help everyone.'}],
'quest':{'speaker':'COMPUTER / FIRST OBJECTIVE','portrait':0,'text':'Collect your phone and personal belongings from locker 08.\nIt is at the far-right end of the block-3 corridor.\nThe locker PIN is a four-digit number you know well.'},
'password':'1010','binary':'1010','decimal':'10','lockerPin':'2008',
'video':[
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'If you are watching this, the outbreak has started.\nI prepared a neutralizer, but kept the ingredients apart for safety.'},
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'There are THREE ingredients. The CULTURE BASE is in the\nblock-3 computer lab, upstairs from room 361. Read its protocol.'},
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'Take the access card from this lectern. It only opens the\nblock-3 passage. Recover the culture base before you leave.'},
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'In block 2, repair four backup circuits in the lower power room.\nThen recover the STABILIZER in the upper-right filter lab.\nThe valve settings are written beside the equipment.'},
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'In block 1, the CATALYST is locked in the lower archive lab.\nCalibrate its scanner. Kamila Batkuldinova is waiting in room 354.'},
 {'speaker':'DR. OMAR / BIOLOGIST / RECORDING','portrait':2,'text':'In 354, blend STABILIZER, then BASE, then CATALYST.\nConnect the cartridge, select ALL BLOCKS and start ventilation.\nSave the plan on your phone. Everyone can still be cured.'}],
'notes':['B3: recover culture base','B2: restore backup power','B2: filter stabilizer','B1: recover catalyst','354: blend and distribute antidote'],
'messenger':{'name':'NURALI','messages':['Bro, where are you? Something terrible is happening in C1.3...','The lights are flickering. Someone is scratching at the door. This is not a joke.','Did you hear those screams? I am seriously scared.'],'reply':'Yes! I noticed it too. What is happening here?','followup':'I have no idea. Just be careful. I will keep the door locked.'}}
(A/'story.json').write_text(json.dumps(story,ensure_ascii=False,indent=2),encoding='utf8')
cfg=json.loads((A/'config.json').read_text(encoding='utf8'));cfg['professor']='Duman Adilet';cfg['finalProfessor']='Kamila Batkuldinova';cfg['language']='en';(A/'config.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
print('English story and three recovery stations installed.')
