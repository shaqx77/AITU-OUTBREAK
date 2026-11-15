#pragma once
// Fixed-scene measurements for the two graphics modes.
void benchmarkGraphics(Game& game){
 glfwSwapInterval(0);std::ofstream out(diagnostics/"benchmark.csv");
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

void benchmarkGameplay(Game& game){
 glfwSwapInterval(0);
 game.start(false,false);
 constexpr int width=1280,height=720,warmup=60,frames=600;
 constexpr float step=1.f/60.f;
 auto frame=[&](){
  game.tick(step);
  game.render(width,height);
  glFinish();
 };
 for(int i=0;i<warmup;i++)frame();
 const double start=glfwGetTime();
 for(int i=0;i<frames;i++)frame();
 const double seconds=glfwGetTime()-start;
 std::ofstream out(diagnostics/"benchmark-gameplay.csv");
 if(!out)throw std::runtime_error("Cannot open benchmark-gameplay.csv");
 out<<"renderer,version,scene,width,height,frames,total_ms,fps\n";
 out<<'"'<<reinterpret_cast<const char*>(glGetString(GL_RENDERER))<<"\",\""
    <<reinterpret_cast<const char*>(glGetString(GL_VERSION))
    <<"\",2d_spawn_idle,"<<width<<','<<height<<','<<frames<<','
    <<seconds*1000<<','<<frames/seconds<<'\n';
 std::cout<<"2D spawn idle benchmark: "<<frames/seconds
          <<" FPS (simulation and completed rendering at 1280x720, VSync off).\n";
}
