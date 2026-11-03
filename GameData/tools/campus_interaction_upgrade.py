"""Idempotent campus dressing: guard post, archive and wayfinding metadata.

Edits the existing Tiled JSON map without rebuilding or replacing earlier rooms.
"""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1] / 'assets'
path = root / 'floor3.tmj'
campus = json.loads(path.read_text(encoding='utf-8'))
layers = {layer['name']: layer for layer in campus['layers']}
width = campus['width']
furniture = layers['Furniture']['data']
objects = layers['Interaction']['objects']
objects[:] = [o for o in objects if not o['name'].startswith('CAMPUS DETAIL / ')]

def properties(**values):
    return [dict(name=k, type='bool' if isinstance(v, bool) else 'int' if isinstance(v, int) else 'string', value=v) for k, v in values.items()]

def add(object_type, name, x, y, w=1, h=1, **values):
    objects.append(dict(id=campus['nextobjectid'], name='CAMPUS DETAIL / ' + name,
                        type=object_type, x=x*16, y=y*16, width=w*16, height=h*16,
                        rotation=0, visible=True, properties=properties(**values)))
    campus['nextobjectid'] += 1

def put(tile, x, y):
    furniture[y*width+x] = tile+1

# The former closet becomes a tiny security office inside the existing server room.
for o in objects:
    if o.get('type') in ('mopweapon', 'batonweapon'):
        o.update(type='batonweapon', name='SECURITY BATON', x=167*16, y=31*16)
    if o['name'] in ('V08 MOP ROOM', 'SECURITY POST'):
        o['name'] = 'SECURITY POST'
    if o['name'] in ('V08 MOP DOOR', 'SECURITY POST DOOR'):
        o['name'] = 'SECURITY POST DOOR'
    if o['name'] in ('V08 CLEANING NOTE', 'SECURITY SHIFT LOG'):
        o.update(name='SECURITY SHIFT LOG', x=168*16, y=30*16,
                 properties=properties(kind='security', sound='paper.wav', text='SECURITY SHIFT LOG / 08:17\nThe guard left to help evacuate the stairwell. A spare baton is on the wall rack.\nTake it with E. G or SPACE briefly stuns a nearby infected person.\nThe baton needs a short cooldown. It is for making space to escape.'))
    if o['id'] == 5:
        o['name'] = 'ARCHIVE LAB DOOR'
    if o['id'] == 16:
        o['name'] = 'FILTER LAB DOOR'

for y in range(29, 33):
    for x in range(166, 170):
        furniture[y*width+x] = 0
put(70, 166, 29)                 # locked equipment cabinet
put(66, 168, 29); put(67, 169, 29)  # CCTV desk and incident paperwork
put(7, 168, 32)                  # guard's chair
put(73, 169, 31)                 # water cooler
add('officeprop', 'CCTV CONSOLE', 167, 30, kind='security', sound='camera.wav',
    text='SECURITY MONITOR\nCamera 03: the two infected patrol from opposite corridor ends.\nWait for one to turn away, then move along the wall.\nEmpty bottles from your locker can draw them away from a doorway.')

# A working archive, with narrow but connected aisles instead of empty floor.
for y in range(27, 40):
    for x in range(5, 23):
        furniture[y*width+x] = 0
for x in (5, 6, 9, 10, 13, 14, 21, 22):
    put(71, x, 28)
for y in (32, 36, 39):
    for x in (5, 6, 10, 11):
        put(71, x, y)
for y in (32, 36, 39):
    put(69, 22, y)
put(68, 7, 33); put(85, 8, 33); put(7, 7, 34)  # cataloguing workstation
put(72, 20, 38); put(74, 19, 38)               # preservation desk / bound records
put(70, 14, 38); put(83, 6, 38)               # specimen records / archive cart
add('officeprop', 'ARCHIVE CATALOGUE', 9, 34, kind='catalogue', sound='files.wav',
    text='AITU ARCHIVE CATALOGUE\nBlue shelves: course records. Ochre folders: research projects.\nCAT-03: catalyst cartridge, sealed in the preservation scanner.\nRead the yellow protocol card near the north-east wall. Three accurate green-zone locks release the cartridge.')
add('officeprop', 'ARCHIVE RESEARCH FILE', 14, 35, kind='files', sound='paper.wav',
    text='PRESERVATION STUDY / CAT-03\nThe catalyst survives in controlled storage. The scanner tests the seal before opening the cabinet.\nThree locks. Three separate passes. Wait for the green zone; there is no time limit.\nBring the recovered vial to classroom 354.')

signs = [
    ('361 / DISCRETE MATH', 133, 25, 20, 'YOUR FIRST CLASS / LECTERN COMPUTER', ''),
    ('B3 / COMPUTER LAB', 134, 5, 18, 'CULTURE BASE / COLD STORAGE', 'lab'),
    ('B3 / LECTURE HALL', 110, 5, 20, 'RECORDING / LECTERN / ACCESS CARD', ''),
    ('SERVICE / SERVERS', 157, 18, 13, 'KEY RACK / SECURITY POST INSIDE', ''),
    ('SECURITY', 166, 28, 4, 'GUARD POST', ''),
    ('B2 / FILTER LAB', 80, 5, 19, 'STABILIZER / READ THE PROTOCOL', 'lab'),
    ('B2 / BACKUP POWER', 57, 25, 18, 'FOUR CIRCUITS / HVAC RESERVE', ''),
    ('B1 / ARCHIVE LAB', 5, 25, 18, 'CAT-03 / CATALYST PRESERVATION', 'lab'),
    ('354 / SAFE CLASSROOM', 5, 5, 18, 'KAMILA / BLENDING / VENTILATION', ''),
]
for title, x, y, w, subtitle, category in signs:
    add('roomsign', title, x, y, w, 1, subtitle=subtitle, category=category)

# Existing protocol position stays fixed, keeping the route and prior puzzle intact.
path.write_text(json.dumps(campus, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print('Guard post, detailed archive and nine campus signs updated.')
