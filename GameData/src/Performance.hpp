#pragma once
// Reproducible local measurements and a backup video rendered by the actual game.
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
