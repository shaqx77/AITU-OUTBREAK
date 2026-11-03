# AITU OUTBREAK 0.11

Start **AITU-OUTBREAK.exe**. Keep **GameData** beside it. The current English release, resources and editable source are included.

You arrive early for Discrete Mathematics in room 361. **Duman Adilet** guards the door while you investigate. Recover three ingredients and meet **Kamila Batkuldinova** in safe classroom 354.

- **Block 3:** collect your phone and bag, unlock the lecture hall, watch the recording, read the cold-storage protocol and recover the culture base. Use the local access card to leave.
- **Block 2:** repair four power circuits, read the filtration protocol and set the filter, buffer and pressure valves to recover the stabilizer.
- **Block 1:** find the archive laboratory, calibrate its scanner over three sweeps and recover the catalyst.
- **Room 354:** blend stabilizer, culture base and catalyst, connect the cartridge, select ALL BLOCKS and start ventilation. Kamila thanks you after everyone is cured.

Read protocol cards, search supply lockers, inspect offices, distract patrols with bottles and use the mop for temporary defence. Collected ingredients and repaired circuits survive checkpoint retries.

## Controls

| Keys | Action |
| --- | --- |
| WASD / arrows | Move |
| Shift | Quiet walk |
| E | Interact |
| Tab | Phone: messages, tasks and map |
| 1 / 2 / 3 on phone Home | Chat / tasks / map |
| A / D in phone; H; M | Tabs; Home; map overview |
| Q / right mouse | Throw a bottle toward the cursor |
| G / Space | Stun a nearby infected person after collecting the mop |
| F | Flashlight |
| Escape, then R | Pause, then retry checkpoint |
| E / Enter / Space in dialogue | Reveal text, then continue |
| F11 | Fullscreen / window |
| F1 / H outside phone | Help |
| B | Lighting comparison |
| P | Pause simulation and animation |
| F2 | Optional perspective campus view / 2D game |
| WASD / Z X / J L / F3 in 3D | Orbit / zoom / move light / whole floor |

Wire panel: drag matching wires, or choose a left row then a right row with 1–4. Laboratory stations show their own controls. Read the protocol beside each station first.

## Build

Windows 10/11 x64, OpenGL 3.3-capable driver. Rebuilding needs CMake 3.20+, Visual Studio 2022 C++ build tools and a Windows SDK. C++17 dependencies are bundled.

```powershell
cmake -S GameData -B build -A x64
cmake --build build --config Release --parallel 4
ctest --test-dir build -C Release --output-on-failure
.\build\Release\AITU-OUTBREAK.exe --windowed
```

The game uses native OpenGL 3.3 core and external GLSL shaders. F2 exposes a perspective camera, depth testing, face culling and movable lighting. The 2D game uses room lighting, circular visibility and post-processing. Required library and asset notices are in **GameData/THIRD_PARTY.md**.

Team: Yerassyl Altynbayev, Nurali Amangeldi, Daniyar Urazbayev. Groups: IT-2504 / IT-2503.
