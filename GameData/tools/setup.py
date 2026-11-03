"""Fetch pinned source dependencies. Run once before configuring CMake."""
from pathlib import Path
import urllib.request, zipfile, io
ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'vendor'
V.mkdir(exist_ok=True)
def get(url,path):
    p=V/path
    if p.exists(): return
    print('Fetch',path,flush=True)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(urllib.request.urlopen(url,timeout=90).read())
def archive(url,name):
    if (V/name).exists(): return
    print('Fetch',name,flush=True)
    data=urllib.request.urlopen(url,timeout=90).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        prefix=z.namelist()[0].split('/')[0]+'/'
        for item in z.infolist():
            rel=item.filename[len(prefix):]
            if not rel or item.is_dir():continue
            p=V/name/rel
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(z.read(item))
archive('https://codeload.github.com/glfw/glfw/zip/refs/tags/3.4','glfw')
archive('https://codeload.github.com/g-truc/glm/zip/refs/tags/1.0.1','glm')
get('https://raw.githubusercontent.com/JoeyDeVries/LearnOpenGL/a545a703f95893258d16dbe32f5ccbb6400fd213/includes/glad/glad.h',Path('glad/glad.h'))
get('https://raw.githubusercontent.com/JoeyDeVries/LearnOpenGL/a545a703f95893258d16dbe32f5ccbb6400fd213/src/glad.c',Path('glad.c'))
get('https://raw.githubusercontent.com/JoeyDeVries/LearnOpenGL/a545a703f95893258d16dbe32f5ccbb6400fd213/includes/KHR/khrplatform.h',Path('KHR/khrplatform.h'))
get('https://raw.githubusercontent.com/nlohmann/json/v3.11.3/single_include/nlohmann/json.hpp',Path('json.hpp'))
get('https://raw.githubusercontent.com/nothings/stb/f0569113c93ad095470c54bf34a17b36646bbbb5/stb_image.h',Path('stb_image.h'))
get('https://raw.githubusercontent.com/mackron/miniaudio/0.11.21/miniaudio.h',Path('miniaudio.h'))
print('Dependencies ready',flush=True)

