// Perspective campus inspection. Coordinates use one world unit per map tile.
// This view shares the map with the game; it is not a pre-rendered image.
#pragma once
struct CampusVertex {glm::vec3 position,normal,color;};
struct CampusView {
 GLuint vao=0,vbo=0,shaderProgram=0;int count=0;bool overview=false;
 float yaw=-.35f,pitch=.82f,distance=53,lightAngle=.3f;glm::vec3 target{132,0,23};
 glm::vec3 eye{},light{};std::vector<CampusVertex> mesh;
 CampusView(){shaderProgram=fileProgram("campus.vert","campus.frag");glGenVertexArrays(1,&vao);glGenBuffers(1,&vbo);}
 void cube(glm::vec3 p,glm::vec3 size,glm::vec3 color){
  const glm::vec3 corner[]={{0,0,0},{1,0,0},{1,1,0},{0,1,0},{0,0,1},{1,0,1},{1,1,1},{0,1,1}};
  const int face[][4]={{1,0,3,2},{4,5,6,7},{0,4,7,3},{5,1,2,6},{3,7,6,2},{0,1,5,4}};
  const glm::vec3 normal[]={{0,0,-1},{0,0,1},{-1,0,0},{1,0,0},{0,1,0},{0,-1,0}};
  for(int f=0;f<6;f++)for(int k:{0,1,2,0,2,3})mesh.push_back({p+corner[face[f][k]]*size,normal[f],color});
 }
 void rebuild(const Map& map,V player){
  mesh.clear();for(int y=0;y<map.h;y++)for(int x=0;x<map.w;x++){int i=y*map.w+x;if(!map.floor[i])continue;
   glm::vec3 ground=x>104?glm::vec3(.42,.48,.52):glm::vec3(.54,.51,.43);
   if(map.floor[i]>=57&&map.floor[i]<=60)ground=glm::mix(ground,glm::vec3(.23,.39,.27),.45f);
   ground*=((x+y)%2?.94f:1.f);cube({x,-.18f,y},{1,.18f,1},ground);
   if(map.walls[i]){bool glass=map.walls[i]==6;cube({x,0,y},{1,glass?1.1f:1.65f,1},glass?glm::vec3(.19,.49,.62):glm::vec3(.29,.37,.44));}
   else if(map.furniture[i]){int id=map.furniture[i];float height=id>=65?1.3f:.60f;glm::vec3 color=id>=65?glm::vec3(.13,.25,.30):glm::vec3(.63,.46,.28);cube({x+.08f,0,y+.08f},{.84f,height,.84f},color);if(id>=20&&id<=25)cube({x+.2f,height,y+.15f},{.5f,.38f,.1f},{.17,.73,.85});}
  }
  for(auto& o:map.objects)if(o.type=="powerpanel"||o.type=="vent")cube({o.b.x/T,1.1f,o.b.y/T},{1.3f,.8f,.3f},{.23,.65,.48});
  for(auto& z:map.zombies){auto p=z.pos/float(T);cube({p.x-.17f,0,p.y-.12f},{.34f,.8f,.24f},{.27,.39,.30});cube({p.x-.14f,.8f,p.y-.12f},{.28f,.28f,.24f},{.48,.61,.40});}
  auto p=player/float(T);cube({p.x-.18f,0,p.y-.14f},{.36f,.8f,.28f},{.13,.57,.78});cube({p.x-.14f,.8f,p.y-.12f},{.28f,.28f,.24f},{.81,.61,.43});
  count=int(mesh.size());glBindVertexArray(vao);glBindBuffer(GL_ARRAY_BUFFER,vbo);glBufferData(GL_ARRAY_BUFFER,mesh.size()*sizeof(CampusVertex),mesh.data(),GL_STATIC_DRAW);
  for(int i=0;i<3;i++){glEnableVertexAttribArray(i);glVertexAttribPointer(i,3,GL_FLOAT,GL_FALSE,sizeof(CampusVertex),(void*)(size_t(i)*sizeof(glm::vec3)));}mesh.clear();
 }
 void frame(int width,int height,float time,bool enabled,bool animate){
  glBindFramebuffer(GL_FRAMEBUFFER,0);glViewport(0,0,width,height);glClearColor(.018f,.028f,.045f,1);glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
  glEnable(GL_DEPTH_TEST);glDepthFunc(GL_LESS);glEnable(GL_CULL_FACE);glCullFace(GL_BACK);glFrontFace(GL_CCW);glDisable(GL_BLEND);
  eye=target+distance*glm::vec3(std::cos(pitch)*std::sin(yaw),std::sin(pitch),std::cos(pitch)*std::cos(yaw));
  float angle=lightAngle+time*.32f;light=target+glm::vec3(std::cos(angle)*14,10+std::sin(angle*.7f)*3,std::sin(angle)*13);
  auto view=glm::lookAt(eye,target,glm::vec3(0,1,0));auto projection=glm::perspective(glm::radians(48.f),float(width)/std::max(1,height),.1f,400.f);
  glUseProgram(shaderProgram);glUniformMatrix4fv(glGetUniformLocation(shaderProgram,"view"),1,GL_FALSE,&view[0][0]);glUniformMatrix4fv(glGetUniformLocation(shaderProgram,"projection"),1,GL_FALSE,&projection[0][0]);
  glUniform3fv(glGetUniformLocation(shaderProgram,"eye"),1,&eye[0]);glUniform3fv(glGetUniformLocation(shaderProgram,"lightPosition"),1,&light[0]);glUniform1i(glGetUniformLocation(shaderProgram,"lightingEnabled"),enabled);
  glBindVertexArray(vao);glDrawArrays(GL_TRIANGLES,0,count);
  glDisable(GL_CULL_FACE);glDisable(GL_DEPTH_TEST);glEnable(GL_BLEND);glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);
 }
 void toggleOverview(){overview=!overview;target=overview?glm::vec3(87,0,23):glm::vec3(132,0,23);distance=overview?123.f:53.f;}
};
