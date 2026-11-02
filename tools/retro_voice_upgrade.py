"""v0.11 original text-synchronised character blips, inspired by retro RPG dialogue.
No commercial-game audio is sampled. Run after all older audio generators. Needs numpy.
"""
from pathlib import Path
import numpy as np
import json, wave, hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets';SR=32000
manifest=json.loads((A/'sound-manifest.json').read_text(encoding='utf8'))
def save(name,voice,category):
    voice=np.asarray(voice,float);voice-=voice.mean(axis=0)
    peak=abs(voice).max()
    if peak>.62:voice*=.62/peak
    pcm=np.round(voice*32767).astype('<i2').tobytes()
    with wave.open(str(A/name),'wb') as out:
        out.setnchannels(1 if voice.ndim==1 else voice.shape[1]);out.setsampwidth(2);out.setframerate(SR);out.writeframes(pcm)
    manifest[name]=dict(category=category,seconds=round(len(voice)/SR,4),peak=round(float(abs(voice).max()),4),rms=round(float(np.sqrt(np.mean(voice*voice))),4),sha256=hashlib.sha256(pcm).hexdigest(),source='Original procedural synthesis: tools/retro_voice_upgrade.py')
def vowel(frequency,duration,formants,rough=0):
    t=np.arange(int(SR*duration))/SR
    phase=frequency*t+.018*np.sin(2*np.pi*27*t)
    voice=np.zeros(len(t))
    for h in range(1,44):
        f=h*frequency
        gain=sum(np.exp(-.5*((f-centre)/width)**2)*amp for centre,width,amp in formants)
        voice+=np.sin(2*np.pi*h*phase+rough*np.sin(2*np.pi*41*t))*gain/(h**.36)
    voice*=np.minimum(1,t/.003)*np.minimum(1,(duration-t)/.008)
    return voice/max(.001,abs(voice).max())
preview=[]
for who,base,formants,rough in (
 ('student',215,((700,180,1),(1700,250,.6)),.05),
 ('teacher',132,((420,150,1),(1150,180,.55)),.12),
 ('biologist',94,((550,110,1),(2100,250,.42)),.34)):
    variants=[]
    for i in range(3):
        v=vowel(base*(1+(i-1)*.055),.045+i*.003,formants,rough)*.32
        # Light 11-bit quantisation gives the tiny retro voice its own timbre.
        v=np.round(v*1024)/1024
        save(f'murmur-{who}-{i}.wav',v,f'Original retro RPG dialogue blip: {who}')
        variants.append(v)
    for i in range(13):preview.extend((variants[i%3],np.zeros(int(SR*.031))))
    preview.append(np.zeros(int(SR*.55)))
# Original layered vowel cheers: bright upward glides and overlapping crowd voices.
n=int(SR*2.5);cheer=np.zeros((n,2))
for j in range(9):
    duration=.62+j%3*.11;t=np.arange(int(SR*duration))/SR
    f0=(155+j*21)*(1+.22*np.sin(np.pi*t/duration))
    phase=np.cumsum(f0)/SR
    v=sum(np.sin(2*np.pi*h*phase)*np.exp(-.5*((h*f0-800)/320)**2)/h**.35 for h in range(1,16))
    v*=np.sin(np.pi*t/duration)**.6*.085
    start=int((j*.18)*SR);pan=(j%3-1)*.7
    length=min(len(v),n-start)
    cheer[start:start+length,0]+=v[:length]*(1-pan)*.7
    cheer[start:start+length,1]+=v[:length]*(1+pan)*.7
save('crowd-cheer.wav',cheer,'Original layered synthetic cheering crowd')
(A/'sound-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
P=ROOT/'previews';P.mkdir(exist_ok=True)
with wave.open(str(P/'retro-voices-preview.wav'),'wb') as out:
    out.setnchannels(1);out.setsampwidth(2);out.setframerate(SR);out.writeframes(np.round(np.concatenate(preview)*32767).astype('<i2').tobytes())
assert len({m['sha256'] for m in manifest.values()})==len(manifest)
print('Three original retro RPG voice sets and layered crowd cheer generated.')
