"""v0.10: replace dialogue only with whole recorded wordless NPC 'hm' sounds.
Run AFTER audio_patrol_upgrade.py. Requires numpy + soundfile.
Bundled CC0 sources: NoisyRedFox, https://freesound.org/people/NoisyRedFox/packs/41303/
These are independent NPC recordings, original NPC recordings.
"""
from pathlib import Path
import hashlib, json, wave
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SOURCES = ROOT / 'tools/audio-sources'
SR = 32000
manifest = json.loads((ASSETS / 'sound-manifest.json').read_text())
unchanged = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
             for p in ASSETS.glob('*.wav') if not p.name.startswith('murmur-')}
clips = []
for who, rate, sounds in (
    ('student', 1.09, ('question', 'talking', 'okay')),
    ('teacher', .98, ('hm', 'talking', 'thinking')),
    ('biologist', .88, ('thinking', 'okay', 'hm')),
):
    for index, sound in enumerate(sounds):
        filename = f'NoisyRedFox-{sound}.mp3'
        voice, source_rate = sf.read(str(SOURCES / filename))
        if voice.ndim > 1:
            voice = voice.mean(axis=1)
        voice = np.interp(np.arange(int(len(voice) * SR / source_rate / rate)) * source_rate * rate / SR,
                          np.arange(len(voice)), voice)
        voice -= voice.mean()
        # Preserve the complete vocal gesture, with only 8ms edge fades.
        edge = min(int(SR * .008), len(voice) // 4)
        voice[:edge] *= np.linspace(0, 1, edge)
        voice[-edge:] *= np.linspace(1, 0, edge)
        voice *= .43 / max(.001, np.abs(voice).max())
        pcm = np.round(voice * 32767).astype('<i2').tobytes()
        name = f'murmur-{who}-{index}.wav'
        with wave.open(str(ASSETS / name), 'wb') as out:
            out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR); out.writeframes(pcm)
        manifest[name] = dict(category='whole recorded wordless NPC hm; CC0 NoisyRedFox',
                              seconds=round(len(voice)/SR, 3), peak=round(float(abs(voice).max()), 4),
                              rms=round(float(np.sqrt(np.mean(voice*voice))), 4),
                              sha256=hashlib.sha256(pcm).hexdigest(), source=filename)
        clips.extend((voice, np.zeros(int(SR * .25))))
assert len({m['sha256'] for m in manifest.values()}) == len(manifest)
for name, digest in unchanged.items():
    assert hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() == digest, name
(ASSETS / 'sound-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
preview = ROOT / 'previews'
preview.mkdir(exist_ok=True)
with wave.open(str(preview / 'murmur-preview.wav'), 'wb') as out:
    out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR)
    out.writeframes(np.round(np.concatenate(clips) * 32767).astype('<i2').tobytes())
print('9 natural NPC murmurs replaced; all other WAV assets unchanged; preview created.')
