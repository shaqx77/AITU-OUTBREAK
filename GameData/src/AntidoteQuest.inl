// Included inside Game: three different recovery tasks and the final blending desk.
Object& station(int component){for(auto& o:map.objects)if(o.type=="antidote"&&o.props.value("component",-1)==component)return o;throw std::runtime_error("Missing antidote station");}
Object& protocol(int component){for(auto& o:map.objects)if(o.type=="labnote"&&o.props.value("component",-1)==component)return o;throw std::runtime_error("Missing laboratory protocol");}
int ingredientCount()const{return int(antidoteParts[0])+int(antidoteParts[1])+int(antidoteParts[2]);}
void beginRemedy(int mode){labMode=mode;labProgress=labHits=labCursor=0;labLastCycle=-1;labDials.fill(0);labTime=processingTime=0;labProcessing=false;labHint.clear();screen=Screen::Remedy;audio.play("keyboard.wav",.5f);}
void finishRemedy(){
 if(labMode<3){antidoteParts[labMode]=true;syncGates();notify(labMode==0?"CULTURE BASE SECURED (1/3). Take the access card and leave block 3.":labMode==1?"STABILIZER SECURED (2/3). Head to the archive lab in block 1.":"CATALYST SECURED (3/3). Bring everything to Kamila in room 354.");}
 else {serum=true;notify("ANTIDOTE READY. Connect the cartridge to the ventilation console.");}
 screen=Screen::Play;audio.play("cartridge.wav");savePoint();
}
void chooseReagent(int choice){
 if(labProcessing)return;static const int recovery[]={2,0,1},blend[]={1,0,2};
 int expected=labMode==0?recovery[labProgress]:blend[labProgress];
 if(choice!=expected){labProgress=0;labHint="Wrong order. The station reset safely. Read the protocol.";audio.play("pc-error.wav",.5f);return;}
 labProgress++;labHint="Correct. Continue the protocol.";audio.play("switch.wav",.6f);if(labProgress==3){labProcessing=true;processingTime=0;labHint=labMode==3?"Blending and sealing the aerosol cartridge...":"Cooling and sealing the culture base...";}
}
void checkValves(){if(labProcessing)return;if(labDials==std::array<int,3>{3,1,2}){labProcessing=true;processingTime=0;labHint="Filtration running. Stabilizer pressure is steady.";audio.play("power.wav",.5f);}else{labHint="Not stable yet. Filter 3 / buffer 1 / pressure 2.";audio.play("pc-error.wav",.5f);}}
void lockCatalyst(){if(labProcessing)return;float pointer=std::fmod(labTime*.38f,1.f);if(pointer>=.40f&&pointer<=.63f){int cycle=int(labTime*.38f);if(cycle==labLastCycle)return;labLastCycle=cycle;labHits++;labHint="Calibration locked. Repeat on the next pass.";audio.play("switch.wav",.7f);if(labHits==3){labProcessing=true;processingTime=0;labHint="Calibration complete. Recovering the catalyst...";}}else{labHits=std::max(0,labHits-1);labHint="Too early or too late. Wait for the green zone.";audio.play("pin-error.wav",.45f);}}
void tickRemedy(float dt){
 labTime+=dt;if(key(GLFW_KEY_ESCAPE)){screen=Screen::Play;return;}
 if(labProcessing){processingTime+=dt;if(processingTime>=4)finishRemedy();return;}
 if(labMode==0||labMode==3){for(int i=0;i<3;i++)if(key(GLFW_KEY_1+i))chooseReagent(i);}
 if(labMode==1){if(key(GLFW_KEY_LEFT)||key(GLFW_KEY_A))labCursor=(labCursor+2)%3;if(key(GLFW_KEY_RIGHT)||key(GLFW_KEY_D))labCursor=(labCursor+1)%3;if(key(GLFW_KEY_W)||key(GLFW_KEY_UP))labDials[labCursor]=(labDials[labCursor]+1)%4;if(key(GLFW_KEY_S)||key(GLFW_KEY_DOWN))labDials[labCursor]=(labDials[labCursor]+3)%4;if(key(GLFW_KEY_ENTER))checkValves();}
 if(labMode==2&&(key(GLFW_KEY_SPACE)||key(GLFW_KEY_ENTER)))lockCatalyst();
}
void remedyPanel(){
 r.box(0,0,640,360,glm::vec4(.006,.012,.025,.75));const char* names[]={"BLOCK 3 / CULTURE RECOVERY","BLOCK 2 / STABILIZER FILTRATION","BLOCK 1 / CATALYST CALIBRATION","ROOM 354 / ANTIDOTE BLENDING"};panel(48,27,544,304,names[labMode]);
 glm::vec4 amber(1,.77,.29,1),violet(.76,.53,1,1),mint(.37,.95,.74,1);glm::vec4 palette[]={amber,violet,mint};
 r.text(labMode==0?"Follow the cold-storage recovery protocol.":labMode==1?"Restore a stable flow through all three valves.":labMode==2?"Lock the scanner three times in the green zone.":"Add stabilizer, culture base, then catalyst.",68,66,WHITE,.85f);
 if(labMode==0||labMode==3){
  const char* recover[]={"1  CULTURE","2  SEAL","3  COOLANT"};const char* mix[]={"1  BASE","2  STABILIZER","3  CATALYST"};
  for(int i=0;i<3;i++){float x=88+i*158.f;r.box(x+46,108,33,68,glm::vec4(.15,.23,.3,1));r.outline(x+46,108,33,68,MUTED);r.box(x+50,132+std::sin(anim*2+i)*2,25,39,palette[i]);r.box(x+48,102,29,7,glm::vec4(.66,.74,.76,1));if(button(x,190,125,25,labMode==0?recover[i]:mix[i],false)&&!labProcessing)chooseReagent(i);}
  r.text(labMode==0?"Protocol: COOLANT > CULTURE > SEAL":"Protocol: STABILIZER > BASE > CATALYST",91,229,CYAN,.8f);for(int i=0;i<3;i++)r.box(230+i*63.f,250,45,6,i<labProgress?mint:glm::vec4(.16,.22,.29,1));
 }
 if(labMode==1){const char* label[]={"FILTER","BUFFER","PRESSURE"};for(int i=0;i<3;i++){float x=87+i*159.f;r.text(label[i],x+15,106,palette[i],.85f);r.box(x+9,131,105,45,glm::vec4(.1,.17,.23,1));r.outline(x+9,131,105,45,labCursor==i?WHITE:MUTED);r.text(std::to_string(labDials[i]),x+51,138,palette[i],2);if(button(x+9,184,48,22,"-")&&!labProcessing){labCursor=i;labDials[i]=(labDials[i]+3)%4;}if(button(x+65,184,48,22,"+")&&!labProcessing){labCursor=i;labDials[i]=(labDials[i]+1)%4;}}r.text("Target: FILTER 3 / BUFFER 1 / PRESSURE 2",105,224,CYAN,.8f);if(button(208,246,223,25,"ENTER: START FILTER"))checkValves();}
 if(labMode==2){r.box(87,135,466,38,glm::vec4(.1,.16,.23,1));r.box(87+466*.40f,135,466*.23f,38,glm::vec4(.18,.62,.40,1));float x=87+466*std::fmod(labTime*.38f,1.f);r.box(x-2,129,4,50,WHITE);r.text("LOCKS: "+std::to_string(labHits)+" / 3",260,104,mint);if(button(197,200,245,30,"SPACE: LOCK SCANNER")&&!labProcessing)lockCatalyst();r.text("No time limit. Three accurate locks secure the vial.",102,245,MUTED,.75f);}
 if(labProcessing){r.box(69,284,502,5,glm::vec4(.12,.18,.24,1));r.box(69,284,502*std::clamp(processingTime/4,0.f,1.f),5,mint);}
 r.text(wrapText(labHint.empty()?(labMode==1?"A/D: choose valve. W/S: adjust. ENTER: start.":labMode==2?"SPACE: lock scanner. ESC: return.":"1/2/3: select a vial. ESC: return."):labHint,72),68,301,labHint.find("Wrong")!=std::string::npos?PINK:CYAN,.8f);
}
