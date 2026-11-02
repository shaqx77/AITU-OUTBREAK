"""Original v0.8 music, nonverbal character voices and action-specific Foley.
No speech engine, samples from games, downloads or third-party recordings.
Requires numpy. Writes deterministic PCM WAV plus a sound manifest.
"""
from pathlib import Path
import numpy as np
import wave,json,hashlib
R=Path(__file__).resolve().parents[1]/'assets';SR=32000
rng=np.random.default_rng(8082026);manifest={}
def save(name,samples,category):
    samples=np.asarray(samples,dtype=np.float64)
    peak=np.max(np.abs(samples))
    if peak>.92:samples*=.92/peak
    pcm=np.round(samples*32767).astype('<i2')
    with wave.open(str(R/name),'wb') as w:
        w.setnchannels(1 if pcm.ndim==1 else pcm.shape[1]);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
    manifest[name]=dict(category=category,seconds=round(len(samples)/SR,3),peak=round(float(np.max(np.abs(samples))),4),rms=round(float(np.sqrt(np.mean(samples*samples))),4),sha256=hashlib.sha256(pcm.tobytes()).hexdigest())
def t(d):return np.arange(int(SR*d))/SR
def noise(d,decay=12):
    x=t(d);return rng.normal(0,1,len(x))*np.exp(-decay*x)
def tone(d,f,decay=8):
    x=t(d);return np.sin(2*np.pi*f*x)*np.exp(-decay*x)*np.minimum(1,x*150)
def chirp(d,a,b,decay=8):
    x=t(d);return np.sin(2*np.pi*(a*x+(b-a)*x*x/(2*d)))*np.exp(-decay*x)*np.minimum(1,x*170)
def mix(*parts):
    out=np.zeros(max(len(v) for v in parts))
    for v in parts:out[:len(v)]+=v
    return out
def delay(v,sec):return np.pad(v,(int(SR*sec),0))
def fx(name,v):save(name,v,'original action Foley')

# Shoes on tile: heel transient, sole brush, toe contact; three variants.
for k in range(3):
    x=t(.19);n=rng.normal(0,1,len(x));brush=np.convolve(n,np.ones(5)/5,mode='same')
    v=.13*np.sin(2*np.pi*(100+11*k)*x)*np.exp(-x*48)+.08*brush*np.exp(-x*27)
    v+=np.where(x>.055,.06*np.sin(2*np.pi*180*x)*np.exp(-np.maximum(0,x-.055)*65),0)
    fx(f'step-{k}.wav',v)
fx('door-open.wav',mix(.16*chirp(.32,150,61,8),delay(.15*noise(.12,40),.17)))
fx('door-close.wav',mix(.20*tone(.28,83,16),.15*noise(.16,35),delay(.12*tone(.09,740,40),.055)))
fx('locker-open.wav',mix(.14*chirp(.5,410,135,6),delay(.12*noise(.18,24),.23)))
fx('keys.wav',sum(.09*tone(.55,f,12+i*3) for i,f in enumerate((1270,1810,2360,3070))))
fx('keys-error.wav',mix(.11*tone(.25,820,22),delay(.09*noise(.12,34),.035)))
fx('pin-error.wav',mix(.10*tone(.11,510,28),delay(.10*tone(.12,410,28),.12),delay(.10*tone(.15,310,25),.25)))
fx('switch.wav',mix(.12*noise(.07,60),delay(.09*tone(.1,390,35),.025)))
fx('channel.wav',mix(.08*chirp(.18,650,870,18),delay(.06*tone(.12,950,25),.08)))
fx('card-pickup.wav',mix(.12*noise(.13,35),delay(.14*tone(.19,670,18),.06)))
fx('swipe-ok.wav',mix(.13*tone(.23,740,15),delay(.13*tone(.27,1110,14),.12)))
fx('swipe-fail.wav',mix(.12*tone(.18,220,17),delay(.12*tone(.2,164,15),.13)))
fx('pc-unlock.wav',mix(.13*chirp(.28,330,990,7),delay(.12*tone(.23,1320,14),.16)))
fx('pc-error.wav',.12*chirp(.27,370,175,8))
fx('ui.wav',.10*tone(.07,940,50))
fx('reply.wav',mix(.09*tone(.11,780,30),delay(.08*tone(.12,1050,32),.045)))
fx('notification.wav',mix(.12*tone(.42,740,12),delay(.12*tone(.34,1108,13),.13)))
fx('paper.wav',.11*noise(.35,8)*np.sin(2*np.pi*19*t(.35))**2)
fx('files.wav',mix(.09*noise(.23,15),delay(.08*noise(.24,15),.12),delay(.07*noise(.16,22),.28)))
fx('keyboard.wav',mix(*(delay(.09*noise(.045,65),i*.068) for i in range(5))))
fx('printer.wav',mix(.10*chirp(.8,150,220,3)*np.sin(2*np.pi*8*t(.8))**2,.06*noise(.8,3)))
fx('water.wav',mix(*(delay(.08*chirp(.10,580-40*i,230-12*i,24),i*.13) for i in range(5))))
fx('server.wav',mix(.07*tone(.7,120,2),.035*tone(.7,620,2),delay(.08*tone(.12,1450,32),.2)))
fx('vending.wav',mix(.10*tone(.8,95,2),delay(.10*noise(.22,19),.35),delay(.14*tone(.18,340,23),.58)))
fx('power.wav',mix(.12*chirp(.9,50,160,2),delay(.16*noise(.15,35),.1),delay(.06*tone(.3,740,13),.55)))
fx('cartridge.wav',mix(.13*noise(.16,30),delay(.14*tone(.16,280,22),.09)))
fx('vent.wav',.09*noise(1.8,0.5)*(1-np.exp(-t(1.8)*5))+.06*chirp(1.8,45,140,.5))
fx('projector.wav',mix(.07*tone(.65,180,3),.03*noise(.65,3),delay(.08*tone(.15,850,24),.12)))
fx('camera.wav',mix(.12*noise(.07,50),delay(.07*tone(.20,560,16),.04)))
fx('bottle-throw.wav',.08*noise(.22,9)*np.sin(np.pi*t(.22)/.22)**2)
fx('impact.wav',mix(.19*noise(.23,19),*(delay(.09*tone(.62,f,10+i*2),i*.018) for i,f in enumerate((1550,2270,3110,4060)))))
fx('mop-pickup.wav',mix(.10*noise(.20,17),.12*chirp(.24,250,140,12)))
fx('mop-swing.wav',.14*noise(.27,4)*np.sin(np.pi*t(.27)/.27)**2)
fx('mop-hit.wav',mix(.20*tone(.25,115,18),.15*noise(.13,24),delay(.10*tone(.16,205,24),.03)))
fx('retry.wav',mix(.13*tone(.3,293,9),delay(.12*tone(.38,220,9),.12)))
fx('blackout.wav',mix(.18*noise(.12,40),delay(.08*chirp(.65,180,48,4),.025)))
fx('spark.wav',.11*noise(.16,27)*np.sin(2*np.pi*83*t(.16))**2)
fx('celebrate.wav',mix(.1*tone(.55,587,5),delay(.1*tone(.6,740,5),.13),delay(.12*tone(.8,880,4),.26)))

# Formant-weighted glottal vowels: three clearly different nonverbal characters.
for who,base,formants in (('student',182,(510,1450,2450)),('teacher',128,(430,1170,2230)),('biologist',100,(350,1030,2100))):
    for k in range(3):
        d=.115+k*.025;x=t(d);f=base*(1+.07*np.sin(x*24+k))
        phase=2*np.pi*np.cumsum(f)/SR;v=np.zeros(len(x))
        for h in range(1,30):
            freq=base*h
            weight=sum(g*np.exp(-((freq-c)/(120+70*i))**2) for i,(c,g) in enumerate(zip(formants,(1,.55,.22))))
            v+=weight*np.sin(h*phase+k*.2)/(h**.65)
        v+=.035*rng.normal(0,1,len(x));v*=np.sin(np.pi*x/d)**1.1
        v*=.38/max(.01,float(np.max(np.abs(v))))
        save(f'murmur-{who}-{k}.wav',v,'original nonverbal character voice; no speech')

# Original coarse breathy zombie groans, original rather than sampled from another game.
for k in range(3):
    x=t(.7+k*.07);phase=2*np.pi*np.cumsum(72+7*k-19*x+5*np.sin(x*14))/SR
    voice=sum(np.sin(h*phase)*np.exp(-((h*(72+7*k)-450)/330)**2)/h**.7 for h in range(1,18))
    voice+=.10*rng.normal(0,1,len(x));voice=np.tanh(voice*1.9)
    voice*=np.sin(np.pi*x/(len(x)/SR))**.65*.30
    save(f'zombie-spot-{k}.wav',voice,'original guttural zombie detection')

def midi(n):return 440*2**((n-69)/12)
def music(restored=False):
    bpm=108 if restored else 92;beat=60/bpm;bars=16;duration=bars*4*beat;count=int(duration*SR)
    out=np.zeros((count,2));roots=[50,46,43,45] if not restored else [62,58,65,60]
    def add(v,start,gain,pan=0):
        indices=(np.arange(len(v))+int(start*SR))%count
        out[indices,0]+=v*gain*np.sqrt((1-pan)/2)
        out[indices,1]+=v*gain*np.sqrt((1+pan)/2)
    def synth(note,d,kind):
        x=t(d);f=midi(note)
        if kind=='pad':
            v=sum(np.sin(2*np.pi*f*(1+det)*x+det*400) for det in (-.003,0,.003))/3
            v+=.18*np.sin(2*np.pi*f*2*x);env=np.minimum(1,x/.28)*np.minimum(1,(d-x)/.6)
        elif kind=='bass':
            v=np.sin(2*np.pi*f*x)+.22*np.sin(2*np.pi*2*f*x)+.1*np.sin(2*np.pi*3*f*x)
            env=np.minimum(1,x*180)*np.exp(-x*5)*np.minimum(1,(d-x)*100)
        else:
            v=np.sin(2*np.pi*f*x)+.25*np.sin(2*np.pi*2*f*x)
            env=np.minimum(1,x*140)*np.exp(-x*7)*np.minimum(1,(d-x)*80)
        return v*env
    for bar in range(bars):
        start=bar*4*beat;root=roots[(bar//2)%4];third=4 if restored else 3
        for n,pan in zip((root,root+third,root+7),(-.5,0,.5)):
            add(synth(n+12,4*beat+.6,'pad'),start,.085,pan)
        for k in range(8):
            add(synth(root-12 if k%4!=3 else root-5,beat*.43,'bass'),start+k*beat/2,.16)
            if bar%4!=3 or k<6:
                arp=[root+24,root+third+24,root+31,root+36][(k+bar%2)%4]
                add(synth(arp,beat*.7,'arp'),start+k*beat/2+beat*.25,.055 if not restored else .07,(-1 if k%2 else 1)*.45)
        for k in range(4):
            xx=t(.25);kick=np.sin(2*np.pi*(43*xx+50*(1-np.exp(-xx*33))/33))*np.exp(-xx*17)
            if k in (0,2) or restored:add(kick,start+k*beat,.25)
            if k in (1,3):
                sn=.5*noise(.22,18)+.25*tone(.22,190,19);add(sn,start+k*beat,.14)
        for k in range(8):
            hh=noise(.06,55);hh=np.concatenate(([0],np.diff(hh)))
            add(hh,start+k*beat/2,.017,(-.35 if k%2 else .35))
    # Circular stereo echoes keep the loop boundary continuous.
    dry=out.copy();out+=np.roll(dry,int(beat*.75*SR),axis=0)[:,::-1]*.15
    out+=np.roll(dry,int(beat*1.5*SR),axis=0)*.07
    out=np.tanh(out*1.15);out*=.73/max(.01,float(np.max(np.abs(out))))
    save('restored.wav' if restored else 'outbreak.wav',out,'original loop: hopeful synthwave' if restored else 'original loop: dark stealth synthwave')
music(False);music(True)
(R/'music-info.json').write_text(json.dumps({'outbreak.wav':{'title':'C1.3 After Hours','bpm':92,'key':'D minor','bars':16,'original':True},'restored.wav':{'title':'354 First Light','bpm':108,'bars':16,'original':True}},indent=2),encoding='utf8')
(R/'sound-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
assert len({v['sha256'] for v in manifest.values()})==len(manifest)
assert all(v['peak']<=.921 and v['rms']>0 for v in manifest.values())
print(f'{len(manifest)} original sounds created; all PCM hashes distinct, no clipping or silent files')
