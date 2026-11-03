# AITU OUTBREAK 0.11

### [Download AITU:OUTBREAK 0.11 for Windows](https://github.com/shaqx77/AITU-OUTBREAK/raw/refs/heads/main/AITU-OUTBREAK.exe)

Download **AITU-OUTBREAK.exe** using the link above, then double-click it on Windows 10/11 x64. **Only this one file is needed to play.** No separate JSON files, GameData folder, archive, installer or development tools are needed. The game runs on Windows after downloading; GitHub displays the project and hosts the download.

All maps, textures, shaders and sounds are embedded in the executable. On launch, the game prepares and verifies its resources automatically in `%LOCALAPPDATA%\AITU-OUTBREAK\Runtime`. Missing or damaged cached resources are restored from the executable. An OpenGL 3.3-capable graphics driver is required.

**GameData** contains the editable source and original resources for development. The current release and all in-game text are in English.

You arrive early for Discrete Mathematics in room 361. **Duman Adilet** guards the door while you investigate. Recover three ingredients and meet **Kamila Batkuldinova** in safe classroom 354.

**New Game** starts with a character creator: male/female character, five skin tones, four hair options and four clothing colours. The selected appearance is used in gameplay and student dialogue portraits, and is saved for the next launch. Use W/S to select a row, A/D to change it, or use the mouse. Enter begins the opening scene; Escape returns to the menu.

The yellow **GOAL** banner shows your current task and a location hint. Follow the yellow floor chevrons through doors and corridors; the active object gets a gold marker, including on the phone map. Large campus signs identify laboratories, the archive, service room and safe classroom. Numbered lockers make personal locker **08** easy to find.

- **Block 3:** collect your phone and bag, unlock the lecture hall, watch the recording, read the cold-storage protocol and recover the culture base. Use the local access card to leave.
- **Block 2:** repair four power circuits, read the filtration protocol and set the filter, buffer and pressure valves to recover the stabilizer.
- **Block 1:** find the archive laboratory, calibrate its scanner over three sweeps and recover the catalyst.
- **Room 354:** blend stabilizer, culture base and catalyst, connect the cartridge, select ALL BLOCKS and start ventilation. Kamila thanks you after everyone is cured.

Open locker **08** with PIN **2008** to collect your phone, bag and **three empty glass bottles**. Q or right-click throws a bottle toward the cursor to distract patrols. The small **security post inside the block-3 service room** contains a spare baton, CCTV console and guard's shift log. Take the baton with E; G or Space temporarily stuns a nearby infected person, followed by a short cooldown.

Read protocol cards, search supply lockers and inspect offices. The archive has research shelves, records cabinets, a catalogue workstation and preservation notes that explain how to recover the catalyst. Collected ingredients and repaired circuits survive checkpoint retries.

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
| G / Space | Stun a nearby infected person after collecting the security baton |
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

Windows builds embed the complete resource bundle automatically. To test edited resources without rebuilding the bundle, launch with `--external-assets`; this development option loads `GameData/assets` or `assets` beside the executable. Normal launches always use the embedded resources.

Team: Yerassyl Altynbayev, Nurali Amangeldi, Daniyar Urazbayev. Groups: IT-2504 / IT-2503.
