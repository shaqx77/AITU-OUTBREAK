# Final project requirements audit

Source: *CG Final Project Requirements 2026–2027*, supplied by the team. Audit date: 2 November 2026. Status is based on this executable and source, not a predicted grade.

| Requirement | Status | Evidence or remaining work |
| --- | --- | --- |
| OpenGL 3.3+ core; no full engine | Done | GLFW core context, GLAD, custom renderers |
| Windowed program, 1280×720, target 30 FPS | Done on tested host | `--windowed`; Intel UHD measured 318 FPS on / 329 off |
| Perspective 3D camera, view matrix, resize-safe aspect | Done | CampusView.hpp; WASD orbit, Z/X zoom; square-window test |
| Non-flat programmable shader pair | Done | campus.vert / campus.frag; diffuse and specular terms |
| Depth test and back-face culling | Done | Enabled for opaque campus geometry; disabled for 2D/UI composition intentionally |
| F1/H help, animation pause, headline toggle | Done | F1/H, P, B; automated state checks |
| Movable light | Done | Animated orbit and manual J/L angle |
| Missing resources, compile/FBO errors reported | Done | Exceptions report to stderr and error.log; FBO completeness checked |
| README, OS/compiler/build/run/exact keys | Done | Root README and CMake; source dependencies included |
| Shaders loaded from files | Done | assets/shaders, shaderFile/fileProgram |
| Start, goal, fail/reset, >1 minute play | Done | Three-block rescue, retry checkpoint, final result |
| Team and technique state on screen | Done | 3D inspection overlay; team names and groups supplied by team |
| Technique visible within first 15 seconds | Done | Inspection scene starts immediately with light enabled |
| Report with pipeline diagram and coded equation | Done | REPORT.pdf |
| Real build screenshots and FPS on/off | Done | screenshots; benchmark.csv; report |
| References and asset/license sources | Done | Report references and THIRD_PARTY.md |
| Named module ownership and contribution table | Partial | Proposed table supplied; actual individual contributions require team confirmation |
| Five-minute presentation and questions | Preparation included | DEFENCE_GUIDE.md; each member must demonstrate knowledge personally |
| 60–120-second backup video | Done locally | docs/demo.mp4 is 60 seconds, generated from actual program frames |
| YouTube/Google Drive video link and access | Pending | Must publish to the required platform and put the URL in the report |
| Assigned topic number and exact title | Not verifiable | Team has not supplied the topic sheet |
| Section 6 must-implement feature checklist | Not verifiable | Section 6 is absent from the supplied document; do not invent an approved topic |
| Can each teammate modify/explain the shader? | Not verifiable by software tests | Live exercises in DEFENCE_GUIDE.md |
| Substantial generated implementation disclosed | Done | Report identifies assisted implementation files and review responsibilities |

The provided document states a November 14 submission deadline and a 10% deduction per late day. The team should confirm its scheduled defence slot with the instructor. This audit does not grant topic approval or certify personal authorship.
