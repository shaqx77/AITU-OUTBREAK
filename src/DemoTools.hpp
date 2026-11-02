#pragma once
// Reproducible local measurements and a backup video rendered by the actual game.
void benchmarkGraphics(Game& game){
 glfwSwapInterval(0);std::ofstream out("benchmark.csv");
 out<<"renderer,version,mode,width,height,frames,total_ms,fps\n";
 game.graphicsMode=true;game.campus.rebuild(game.map,game.map.type("spawn")->pos());
 for(int effect=0;effect<2;effect++){
  game.lightingEnabled=effect!=0;for(int i=0;i<30;i++){game.anim=i*.016f;game.render(1280,720);}glFinish();
  double start=glfwGetTime();const int frames=180;
  for(int i=0;i<frames;i++){game.anim=i*.016f;game.render(1280,720);glFinish();}
  double duration=glfwGetTime()-start;
  out<<'"'<<reinterpret_cast<const char*>(glGetString(GL_RENDERER))<<"\",\""<<reinterpret_cast<const char*>(glGetString(GL_VERSION))<<"\","<<(effect?"lighting_on":"lighting_off")<<",1280,720,"<<frames<<','<<duration*1000<<','<<frames/duration<<'\n';
 }
 std::cout<<"Benchmark saved to benchmark.csv (CPU + GPU completed-frame timing, not GPU-only).\n";
}
void recordDemo(Game& game){
 glfwSwapInterval(0);std::ofstream raw("demo.rgb",std::ios::binary);std::vector<unsigned char> pixels(640*360*3);int previous=-1;
 for(int i=0;i<1200;i++){
  float t=i/20.f;int phase=t<10?0:t<16?1:t<20?2:t<27?3:t<30?4:5;
  if(phase!=previous){
   if(phase==1||phase==2||phase==3||phase==4){game.start(false,false);game.graphicsMode=false;game.laptopUnlocked=game.hasPhone=game.lectureKey=game.notesRecorded=game.cardSwiped=game.keycard=true;game.hasMop=true;game.bottles=3;game.syncGates();game.player=V(140*T+8,23*T+8);game.toastTime=0;}
   if(phase==2){game.screen=Screen::Phone;game.phoneTab=1;}
   if(phase==3){game.player=V(65*T,32*T);game.screen=Screen::Wiring;game.wires.fill(false);game.wireStatus="Соедините одинаковые цвета и номера.";}
   if(phase==4){game.map.zombies[4].pos=game.player+V(45,0);}
   if(phase==5){game.start(true,false);game.graphicsMode=false;game.hasMop=true;game.serum=true;game.screen=Screen::Ending;game.ending=0;game.toastTime=0;}
   previous=phase;
  }
  if(phase==0){game.graphicsMode=true;game.anim=t;game.campus.yaw=-.35f+t*.07f;game.lightingEnabled=t<4||t>=6;}
  else if(phase==1){game.tick(.05f);}
  else if(phase==2){game.anim+=.05f;}
  else if(phase==3){int pair=int(t-22);static const int destination[]={2,0,3,1};if(pair>=0&&pair<4&&!game.wires[pair])game.connectWire(pair,destination[pair]);game.anim+=.05f;}
  else if(phase==4){game.anim+=.05f;if(t>28&&game.mopCooldown<=0)game.swingMop();game.mopCooldown=std::max(0.f,game.mopCooldown-.05f);}
  else {game.tick(.05f);if(t>59.3f&&game.finalTeacherReady)game.messageAge=999;}
  game.render(640,360);glFinish();glPixelStorei(GL_PACK_ALIGNMENT,1);glReadPixels(0,0,640,360,GL_RGB,GL_UNSIGNED_BYTE,pixels.data());raw.write(reinterpret_cast<const char*>(pixels.data()),pixels.size());
 }
 std::cout<<"Rendered 60-second backup video to demo.rgb, RGB24, 640x360, 20 FPS, bottom-up.\n";
}
