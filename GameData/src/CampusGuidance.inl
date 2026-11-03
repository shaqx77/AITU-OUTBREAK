// Character setup, readable campus signage and collision-aware objective guidance.
Renderer::Appearance creatorOriginal;int creatorRow=0;
std::vector<V> guidancePath;int guidanceID=-1;V guidanceStart{};float guidanceAge=0;
std::filesystem::path appearanceFile()const{
 if(assets.parent_path().parent_path().filename()=="Runtime")return assets.parent_path().parent_path().parent_path()/"player-profile.json";
 return diagnostics/"player-profile.json";
}
void loadAppearance(){try{std::ifstream in(appearanceFile());if(!in)return;json j;in>>j;r.avatar.gender=j.value("gender",0);r.avatar.skin=j.value("skin",1);r.avatar.hair=j.value("hair",0);r.avatar.outfit=j.value("outfit",0);r.avatar.clamp();}catch(const std::exception&){} }
void saveAppearance(){std::ofstream out(appearanceFile());out<<r.avatar.data().dump(2);}
void openCreator(){creatorOriginal=r.avatar;creatorRow=0;screen=Screen::Character;}
void changeAppearance(int amount){int* values[]={&r.avatar.gender,&r.avatar.skin,&r.avatar.hair,&r.avatar.outfit};int count[]={2,5,4,4};*values[creatorRow]=(*values[creatorRow]+amount+count[creatorRow])%count[creatorRow];audio.play("menu-ui.wav",.4f);}
void confirmCharacter(){r.avatar.clamp();saveAppearance();start();}
void tickCreator(){if(key(GLFW_KEY_ESCAPE)){r.avatar=creatorOriginal;screen=Screen::Menu;return;}if(key(GLFW_KEY_DOWN)||key(GLFW_KEY_S))creatorRow=(creatorRow+1)%4;if(key(GLFW_KEY_UP)||key(GLFW_KEY_W))creatorRow=(creatorRow+3)%4;if(key(GLFW_KEY_LEFT)||key(GLFW_KEY_A))changeAppearance(-1);if(key(GLFW_KEY_RIGHT)||key(GLFW_KEY_D))changeAppearance(1);if(key(GLFW_KEY_ENTER))confirmCharacter();}
void creatorPanel(){
 r.box(0,0,640,360,glm::vec4(.015,.025,.055,.97));r.text("AITU / STUDENT ID",28,18,CYAN,.8f);r.text("CREATE YOUR SURVIVOR",28,41,WHITE,1.45f);r.text("Your appearance stays with you throughout the story.",29,70,MUTED,.75f);
 r.box(29,96,204,210,glm::vec4(.06,.11,.18,1));r.outline(29,96,204,210,glm::vec4(.23,.38,.49,1));r.box(40,106,181,78,glm::vec4(.08,.16,.23,1));r.studentPortrait(52,111,69);r.text("STUDENT",132,119,WHITE,.7f);r.text("AITU / 361",132,137,CYAN,.6f);r.text("IT DEPARTMENT",132,154,MUTED,.5f);
 int facing=int(anim*.65f)%4;r.student(V(129,285),facing,int(anim*3)%3,true,2.6f);r.box(47,292,169,1,glm::vec4(.22,.35,.44,1));
 const char* row[]={"CHARACTER","SKIN TONE","HAIR","CLOTHING"};const char* gender[]={"MALE","FEMALE"};const char* hairs[]={"MIDNIGHT","CHESTNUT","SAND","PLUM"};const char* outfits[]={"TEAL","VIOLET","RUST","BLUE"};
 for(int i=0;i<4;i++){float y=101+i*48.f;bool selected=creatorRow==i;r.box(252,y,359,42,selected?glm::vec4(.12,.19,.28,1):glm::vec4(.055,.09,.15,1));if(selected)r.box(252,y,3,42,CYAN);r.text(row[i],264,y+4,selected?CYAN:MUTED,.65f);
  if(i==0){for(int n=0;n<2;n++)if(button(367+n*115.f,y+8,105,26,gender[n],r.avatar.gender==n)){creatorRow=i;r.avatar.gender=n;}}
  if(i==1){for(int n=0;n<5;n++){float x=385+n*42.f;r.box(x,y+9,30,24,r.skinColor(n));r.outline(x-2,y+7,34,28,r.avatar.skin==n?WHITE:glm::vec4(.17,.25,.32,1));if(click&&inside(mouse,x-2,y+7,34,28)){creatorRow=i;r.avatar.skin=n;}}}
  if(i>=2){int value=i==2?r.avatar.hair:r.avatar.outfit;if(button(367,y+8,34,26,"<")){creatorRow=i;changeAppearance(-1);}r.text(i==2?hairs[value]:outfits[value],418,y+13,WHITE,.8f);r.box(542,y+10,18,20,i==2?r.hairColor(value):r.outfitColor(value));if(button(571,y+8,32,26,">")){creatorRow=i;changeAppearance(1);}}
 }
 r.text("W/S: row   A/D: change   ESC: back",252,298,MUTED,.7f);if(button(252,319,359,27,"ENTER: BEGIN THE STORY",true))confirmCharacter();
}
const Object* goalTarget()const{
 auto type=[&](const std::string& name)->const Object*{return map.type(name);};
 if(cured)return nullptr;if(!laptopUnlocked)return type("laptop");if(!hasPhone)return type("locker");if(!lectureKey)return type("keyrack");if(!notesRecorded)return type("projector");
 for(int i=0;i<3;i++){
  if(i==1){if(!keycard&&!cardSwiped)return type("keycard");if(!cardSwiped)return type("cardreader");if(!powerRestored)return type("powerpanel");}
  if(!antidoteParts[i])for(auto& o:map.objects)if(o.type==(protocolSeen[i]?"antidote":"labnote")&&o.props.value("component",-1)==i)return &o;
 }
 if(!reachedSafe)return type("mentor");if(!serum)return type("serum");return type("vent");
}
std::string targetName(const Object& o)const{
 if(o.type=="laptop")return "361 / COMPUTER";if(o.type=="locker")return "LOCKER 08";if(o.type=="keyrack")return "SERVICE / KEY RACK";if(o.type=="projector")return "LECTURE / PLAY";if(o.type=="keycard")return "LECTURE / ACCESS CARD";if(o.type=="cardreader")return "B2 / CARD READER";if(o.type=="powerpanel")return "B2 / BACKUP POWER";if(o.type=="mentor")return "354 / KAMILA";if(o.type=="serum")return "354 / BLENDING DESK";if(o.type=="vent")return "354 / VENTILATION";
 int i=o.props.value("component",0);return std::string(i==0?"B3 LAB / ":i==1?"B2 LAB / ":"B1 ARCHIVE / ")+(o.type=="labnote"?"PROTOCOL":i==0?"CULTURE":i==1?"FILTER":"SCANNER");
}
void refreshGuidance(){const auto* target=goalTarget();if(!target){guidancePath.clear();guidanceID=-1;return;}if(guidanceID==target->id&&guidanceAge>0&&dist(guidanceStart,player)<12)return;guidanceID=target->id;guidanceStart=player;guidanceAge=.45f;guidancePath=map.path(player,target->pos(),true);}
void arrow(V p,V direction,glm::vec4 color,float size=6){V d=unit(direction);if(glm::length(d)<.1f)d=V(0,-1);V side(-d.y,d.x);r.line(p-d*size,p+d*size,color);r.line(p+d*size,p+side*size*.65f,color);r.line(p+d*size,p-side*size*.65f,color);}
void drawGuidance(){
 if(screen!=Screen::Play||cured)return;refreshGuidance();auto target=goalTarget();if(!target)return;glm::vec4 yellow(1,.86,.28,1);V waypoint=target->pos();bool openDoor=false;
 if(!guidancePath.empty()){
  waypoint=guidancePath.front();for(auto p:guidancePath){if(dist(player,p)>150||!map.ray(player,p,true))break;waypoint=p;}
  for(auto& o:map.objects)if(o.type=="door"&&!o.open){bool crosses=false;for(auto p:guidancePath)if(o.b.contains(p,3)){crosses=true;break;}if(crosses&&map.ray(player,o.pos()-unit(o.pos()-player)*18.f,true)){waypoint=o.pos();openDoor=true;break;}}
  for(size_t i=2;i+1<guidancePath.size()&&i<22;i+=4){V p=guidancePath[i]-cam;if(p.x<18||p.x>622||p.y<106||p.y>294||dist(player,guidancePath[i])>220||!map.ray(player,guidancePath[i],true))continue;arrow(p,guidancePath[i+1]-guidancePath[i-1],glm::vec4(1,.84,.25,.62),3);}
 }
 V pos=waypoint-cam;bool offscreen=pos.x<25||pos.x>615||pos.y<111||pos.y>284;V marker(glm::clamp(pos.x,25.f,615.f),glm::clamp(pos.y,111.f,284.f));
 if(dist(player,waypoint)>24){r.box(marker.x-10,marker.y-10,21,21,glm::vec4(.07,.09,.10,.94));r.outline(marker.x-10,marker.y-10,21,21,yellow);arrow(marker,waypoint-player,yellow,6);}
 V actual=target->pos()-cam;
 if(!offscreen&&map.ray(player,target->pos(),true)&&actual.x>25&&actual.x<615&&actual.y>115&&actual.y<283){float bob=std::sin(anim*3)*2;V p=actual+V(0,-36+bob);arrow(p,V(0,1),yellow,6);float width=std::min(218.f,8.f+targetName(*target).size()*4.8f);float x=std::clamp(p.x-width/2,8.f,632-width);r.box(x,p.y-20,width,14,glm::vec4(.08,.10,.12,.96));r.text(targetName(*target),x+4,p.y-18,yellow,.6f);}
 std::string next=openDoor?"OPEN THE DOOR [E]":targetName(*target);r.text("FOLLOW YELLOW ARROWS  >  "+next,12,59,yellow,.65f);
}
void roomSigns(){
 for(auto& o:map.objects)if(o.type=="roomsign"){
  V p=V(o.b.x,o.b.y)-cam;float w=o.b.w;if(p.x+w<0||p.x>640||p.y<-30||p.y>370)continue;
  auto accent=o.props.value("category",std::string(""))=="lab"?glm::vec4(.99,.82,.27,1):CYAN;
  std::string name=o.name;if(name.rfind("CAMPUS DETAIL / ",0)==0)name.erase(0,std::string("CAMPUS DETAIL / ").size());float scale=std::min(.85f,(w-14)/(8*float(name.size())));
  r.box(p.x,p.y,w,27,glm::vec4(.035,.09,.13,1));r.box(p.x,p.y,3,27,accent);r.outline(p.x,p.y,w,27,glm::vec4(.27,.43,.49,1));r.text(name,p.x+8,p.y+3,accent,scale);r.text(o.props.value("subtitle",std::string("ASTANA IT UNIVERSITY")),p.x+8,p.y+17,MUTED,.5f);
 }
}
std::string roomTitle()const{
 if(auto room=occupiedRoomAt(player))for(auto& o:map.objects)if(o.type=="roomsign"&&o.b.x>=room->x&&o.b.x<room->x+room->w&&o.b.y>=room->y-32&&o.b.y<room->y+room->h){std::string name=o.name;if(name.rfind("CAMPUS DETAIL / ",0)==0)name.erase(0,std::string("CAMPUS DETAIL / ").size());return name;}
 return "BLOCK "+std::to_string(currentBlock())+" / FLOOR 3";
}
void lockerNumbers(){
 int n=7;for(int x=map.w-1;x>=0;x--){int f=map.furniture[20*map.w+x];if(f!=45&&f!=49&&f!=50)continue;bool mine=x==151;std::string text=n<10?"0"+std::to_string(n):std::to_string(n);n++;V p=V(x*T,20*T)-cam;if(p.x<-16||p.x>650)continue;
  r.box(p.x+1,p.y-12,14,9,glm::vec4(.045,.10,.15,1));r.outline(p.x+1,p.y-12,14,9,mine?glm::vec4(1,.85,.24,1):glm::vec4(.37,.59,.67,1));r.text(text,p.x+3,p.y-13,mine?glm::vec4(1,.87,.3,1):WHITE,.65f);
  if(mine){r.outline(p.x-1,p.y-18,18,35,glm::vec4(1,.84,.25,1));r.text("YOURS",p.x-3,p.y-21,glm::vec4(1,.84,.25,1),.5f);}
 }
}
void campusDressing(){
 auto at=[&](float x,float y){return V(x*T,y*T)-cam;};
 // A guard's dual CCTV monitor, radio and incident clipboard.
 V p=at(168,29);r.box(p.x-2,p.y-13,28,18,glm::vec4(.07,.12,.17,1));r.outline(p.x-2,p.y-13,28,18,MUTED);
 for(int i=0;i<2;i++){r.box(p.x+i*13,p.y-10,10,11,glm::vec4(.08,.25,.24,1));r.line(p+V(i*13.f+1,-5),p+V(i*13.f+8,-5),CYAN);r.box(p.x+i*13+2+std::fmod(anim*2+i*4,6.f),p.y-8,2,3,glm::vec4(.66,.85,.63,1));}r.text("CCTV",p.x+3,p.y-20,CYAN,.5f);
 V radio=at(166,29);r.box(radio.x+4,radio.y-6,8,10,glm::vec4(.17,.20,.25,1));r.line(radio+V(5,-6),radio+V(6,-14),MUTED);r.box(radio.x+6,radio.y-3,4,2,CYAN);
 // Research shelf labels, catalogue drawer and scanner workflow placard.
 for(int i=0;i<3;i++){V q=at(5.f+i*4,28);r.box(q.x,q.y-13,31,10,glm::vec4(.13,.23,.29,1));r.text(i==0?"COURSES":i==1?"RESEARCH":"CAT-03",q.x+2,q.y-13,i==2?glm::vec4(1,.85,.3,1):CYAN,.5f);}
 V q=at(18,36);r.box(q.x,q.y,40,30,glm::vec4(.77,.75,.62,1));r.outline(q.x,q.y,40,30,glm::vec4(.35,.45,.44,1));r.text("CAT-03",q.x+3,q.y+2,glm::vec4(.12,.22,.27,1),.65f);r.text("3 LOCKS",q.x+3,q.y+12,glm::vec4(.12,.22,.27,1),.5f);r.box(q.x+5,q.y+23,30,3,glm::vec4(.22,.60,.39,1));
}
