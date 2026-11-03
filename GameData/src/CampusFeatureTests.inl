// Regression coverage for the character flow and the new navigation UI.
auto originalAppearance=g.r.avatar;
g.menuAction(0);require(g.screen==Screen::Character&&!g.hasGame,"new game opens character creation before intro");
g.creatorRow=0;g.changeAppearance(1);require(g.r.avatar.gender!=originalAppearance.gender,"character choice changes body style");
g.pressed[GLFW_KEY_ESCAPE]=true;g.tick(0);g.pressed.fill(false);require(g.screen==Screen::Menu&&g.r.avatar.data()==originalAppearance.data(),"cancel restores appearance without starting a run");
g.openCreator();g.r.avatar.gender=0;g.r.avatar.skin=1;g.creatorRow=0;g.changeAppearance(1);g.creatorRow=1;g.changeAppearance(3);g.creatorRow=2;g.changeAppearance(1);g.creatorRow=3;g.changeAppearance(1);
auto selectedAppearance=g.r.avatar;g.confirmCharacter();require(g.screen==Screen::Intro&&g.r.avatar.gender==1&&g.r.avatar.skin==4,"chosen female survivor and dark skin reach opening scene");
g.r.avatar={};g.loadAppearance();require(g.r.avatar.data()==selectedAppearance.data(),"appearance loads from persistent player profile");g.savePoint();g.retry();require(g.r.avatar.data()==selectedAppearance.data(),"appearance survives checkpoint retry");
g.openCreator();g.render(1280,720);require(glGetError()==GL_NO_ERROR,"creator renders at widescreen aspect");g.render(900,900);require(glGetError()==GL_NO_ERROR,"creator renders at square aspect");g.r.avatar=originalAppearance;g.saveAppearance();
int signs=0;for(auto& object:g.map.objects)signs+=object.type=="roomsign";require(signs>=9,"labs and security have readable room signage");
require(g.map.type("batonweapon")&&g.map.type("batonweapon")->pos().x>165*T,"security baton replaces cleaning weapon");
require(g.map.type("mopweapon")==nullptr,"no obsolete cleaning-weapon interaction");
g.start(false,false);require(g.goalTarget()&&g.goalTarget()->type=="laptop","first navigation target is classroom computer");g.refreshGuidance();require(!g.guidancePath.empty(),"initial computer navigation has a walkable route");
g.laptopUnlocked=true;g.syncGates();require(g.goalTarget()->type=="locker","computer unlock switches navigation to locker 08");g.refreshGuidance();require(!g.guidancePath.empty(),"locker navigation leaves through classroom doorway");for(auto point:g.guidancePath)require(!g.map.hit(point,4),"guidance never routes through solid furniture or walls");
g.hasPhone=true;require(g.goalTarget()->type=="keyrack","phone pickup switches target to physical service keys");g.lectureKey=true;require(g.goalTarget()->type=="projector","lecture key switches target to recording");
g.notesRecorded=true;require(g.goalTarget()->type=="labnote","recording points to lab protocol before equipment");g.protocolSeen[0]=true;require(g.goalTarget()->type=="antidote","reading protocol changes target to culture bench");
g.antidoteParts[0]=true;require(g.goalTarget()->type=="keycard","culture secured points to local access card");g.keycard=true;require(g.goalTarget()->type=="cardreader","card pickup points to block-2 reader");g.cardSwiped=true;g.syncGates();require(g.goalTarget()->type=="powerpanel","block-3 clearance points to backup power");
