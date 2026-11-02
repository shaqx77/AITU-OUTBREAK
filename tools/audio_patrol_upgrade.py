"""v0.9: phased routes, new menu/horror cues, recorded CC0 vocal fragments.
Run after v0.8 asset generators. Requires numpy and soundfile.
Sources bundled under tools/audio-sources; attribution there and in THIRD_PARTY.md.
"""
from pathlib import Path
import json,wave,hashlib
import numpy as np
import soundfile as sf
R=Path(__file__).resolve().parents[1]/'assets';S=Path(__file__).resolve().parent/'audio-sources';SR=32000
manifest=json.loads((R/'sound-manifest.json').read_text());rng=np.random.default_rng(909)
def save(name,v,category,source=None):
    v=np.asarray(v,float);v-=np.mean(v,axis=0);peak=np.max(np.abs(v))
    if peak>.86:v*=.86/peak
    pcm=np.round(v*32767).astype('<i2')
    with wave.open(str(R/name),'wb') as w:w.setnchannels(1 if v.ndim==1 else v.shape[1]);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
    manifest[name]=dict(category=category,seconds=round(len(v)/SR,3),peak=round(float(np.max(np.abs(v))),4),rms=round(float(np.sqrt(np.mean(v*v))),4),sha256=hashlib.sha256(pcm.tobytes()).hexdigest())
    if source:manifest[name]['source']=source
def recording(name,rate=1):
    v,sr=sf.read(str(S/name));v=np.mean(v,axis=1) if v.ndim>1 else v
    v=np.interp(np.arange(int(len(v)*SR/sr/rate))*sr*rate/SR,np.arange(len(v)),v)
    energy=np.convolve(v*v,np.ones(320)/320,mode='same');where=np.where(energy>max(1e-6,energy.max()*.035))[0]
    return v[max(0,where[0]-160):min(len(v),where[-1]+161)] if len(where) else v
def fade(v,seconds=.018):
    n=min(int(seconds*SR),len(v)//3);v=v.copy();v[:n]*=np.linspace(0,1,n);v[-n:]*=np.linspace(1,0,n);return v
# Use natural syllable fragments; no synthetic oscillators, extreme pitch or TTS.
for who,rate,names in (
 ('student',1.06,('ready.ogg','go.ogg','war_look_out.ogg')),
 ('teacher',1.0,('hold.ogg','round.ogg','war_reloading.ogg')),
 ('biologist',.96,('wrong.ogg','hold.ogg','ready.ogg'))):
    for k,name in enumerate(names):
        v=recording(name,rate);duration=int(SR*(.22+k*.025));width=min(duration,len(v));
        # Retain a voiced interior portion rather than the intelligible whole word.
        start=int(max(0,len(v)-width)*(.35+k*.12));clip=fade(v[start:start+width])
        clip*=.38/max(.001,float(np.max(np.abs(clip))))
        save(f'murmur-{who}-{k}.wav',clip,'edited recorded human syllable; CC0 Kenney',name)
for k,name in enumerate(('grunt_01.ogg','grunt_02.ogg','grunt_03.ogg')):
    v=fade(recording(name),.025);v*=.58/max(.001,float(np.max(np.abs(v))))
    save(f'zombie-spot-{k}.wav',v,'recorded mouth/creature grunt; CC0 rubberduck',name)

def cue(menu):
    duration=40 if menu else 48;n=int(duration*SR);x=np.arange(n)/SR;out=np.zeros((n,2))
    def add(v,start,gain,pan=0):
        idx=(np.arange(len(v))+int(start*SR))%n
        out[idx,0]+=v*gain*np.sqrt((1-pan)/2);out[idx,1]+=v*gain*np.sqrt((1+pan)/2)
    def note(freq,duration,decay=3):
        t=np.arange(int(duration*SR))/SR
        return (np.sin(2*np.pi*freq*t)+.12*np.sin(2*np.pi*freq*2*t))*np.minimum(1,t*35)*np.exp(-t*decay)*np.minimum(1,(duration-t)*30)
    if menu:
        # Restrained neon title theme: minor keys, a rounded bass and wide echoes.
        beat=.625;roots=(146.832,116.541,130.813,110)
        for bar in range(16):
            root=roots[bar//4];start=bar*2.5
            for interval,pan in ((1,-.5),(2**(3/12),0),(1.5,.5)):
                add(note(root*interval,3.5,.45),start,.07,pan)
            for k in range(4):add(note(root/2,.40,6),start+k*beat,.16)
            for k,mul in enumerate((2,2**(15/12),3,2**(15/12))):add(note(root*mul,.7,4),start+k*beat+.3125,.06,(-1 if k%2 else 1)*.6)
            for k in (0,2):
                t=np.arange(int(SR*.24))/SR;add(np.sin(2*np.pi*(48*t+28*(1-np.exp(-35*t))/35))*np.exp(-t*20),start+k*beat,.13)
        out+=np.roll(out.copy(),int(.46875*SR),axis=0)[:,::-1]*.22
    else:
        # Slow horror ambience: breathy upper textures, dissonant drones and sparse pulses.
        for freq,amp,phase in ((36.708,.065,.1),(73.416,.095,.4),(146.832,.037,1.7),(155.563,.023,2.1),(220,.018,.9)):
            # Integer cycles at the boundary make the bed loop without a click.
            f=round(freq*duration)/duration;lfo=.55+.45*np.sin(2*np.pi*x/duration*2+phase)**2
            for ch in range(2):out[:,ch]+=np.sin(2*np.pi*f*x+phase+ch*.18)*amp*lfo
        raw=rng.normal(0,1,n);spec=np.fft.rfft(raw);freq=np.fft.rfftfreq(n,1/SR)
        spec*=np.exp(-((freq-1150)/650)**2);air=np.fft.irfft(spec,n);air/=max(1,np.max(np.abs(air)))
        out[:,0]+=air*.04*(.5+.5*np.sin(2*np.pi*x/12))
        out[:,1]+=np.roll(air,int(.19*SR))*.035*(.5+.5*np.cos(2*np.pi*x/12))
        for start in (2,9,16,26,34,42):
            t=np.arange(int(.4*SR))/SR;thump=np.sin(2*np.pi*57*t)*np.exp(-t*17)*np.minimum(1,t*140)
            add(thump,start,.08);add(thump,start+.37,.05)
        for start,f,pan in ((5,466.16,-.7),(14,622.25,.65),(23,440,-.4),(37,466.16,.6)):
            add(note(f,4,1.4),start,.04,pan);add(note(f*1.003,4,1.8),start+.23,.025,-pan)
    out*=.69/max(.01,float(np.max(np.abs(out))))
    save('menu.wav' if menu else 'outbreak.wav',out,'original neon menu loop' if menu else 'original slow horror ambience')
cue(True);cue(False)
t=np.arange(int(.11*SR))/SR
save('menu-ui.wav',.10*(np.sin(2*np.pi*660*t)+.4*np.sin(2*np.pi*990*t))*np.exp(-t*40)*np.minimum(1,t*200),'original menu selection')
(R/'sound-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
info=json.loads((R/'music-info.json').read_text());info['menu.wav']={'title':'AITU Midnight Signal','seconds':40,'original':True};info['outbreak.wav']={'title':'C1.3 No One Answers','seconds':48,'style':'slow horror ambience','original':True};(R/'music-info.json').write_text(json.dumps(info,indent=2),encoding='utf8')

j=json.loads((R/'floor3.tmj').read_text());enemies=next(l for l in j['layers'] if l['name']=='Enemies')['objects']
for k,o in enumerate(o for o in enemies if any(p['name']=='block' and p['value']==3 for p in o.get('properties',[]))):
    x=111 if k==0 else 149;o.update(x=x*16,y=23*16);o['polyline']=[{'x':0,'y':0},{'x':(130-x)*16,'y':0}]
    props=o.setdefault('properties',[]);props[:]=[p for p in props if p['name'] not in ('phaseDelay','patrolDwell')]
    props.extend([dict(name='phaseDelay',type='float',value=0.0 if k==0 else 7.0),dict(name='patrolDwell',type='float',value=1.2)])
(R/'floor3.tmj').write_text(json.dumps(j),encoding='utf8')
cfg=json.loads((R/'config.json').read_text());cfg['startFullscreen']=True;(R/'config.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
assert len({v['sha256'] for v in manifest.values()})==len(manifest)
print('v0.9 phased center routes, recorded voices, separate menu and horror cues ready')
