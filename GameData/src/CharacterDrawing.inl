// Pixel characters are drawn on the same grid as the campus sprites.
struct Appearance {
 int gender=0,skin=1,hair=0,outfit=0;
 void clamp(){gender=std::clamp(gender,0,1);skin=std::clamp(skin,0,4);hair=std::clamp(hair,0,3);outfit=std::clamp(outfit,0,3);}
 json data()const{return {{"gender",gender},{"skin",skin},{"hair",hair},{"outfit",outfit}};}
};
Appearance avatar;
glm::vec4 skinColor(int index){static const glm::vec4 c[]={{.98,.81,.66,1},{.85,.65,.45,1},{.66,.44,.29,1},{.44,.27,.19,1},{.27,.16,.12,1}};return c[std::clamp(index,0,4)];}
glm::vec4 outfitColor(int index){static const glm::vec4 c[]={{.18,.65,.70,1},{.60,.38,.85,1},{.86,.48,.27,1},{.27,.51,.80,1}};return c[std::clamp(index,0,3)];}
glm::vec4 hairColor(int index){static const glm::vec4 c[]={{.10,.10,.14,1},{.25,.15,.10,1},{.72,.49,.24,1},{.40,.23,.43,1}};return c[std::clamp(index,0,3)];}
void student(V p,int direction,int frame,bool bag,float zoom=1){
 auto a=avatar;auto skin=skinColor(a.skin),coat=outfitColor(a.outfit),hair=hairColor(a.hair);
 auto ink=glm::vec4(.055,.08,.13,1),pants=glm::vec4(.17,.22,.32,1);
 auto rect=[&](auto x,auto y,auto w,auto h,glm::vec4 color){box(std::round(p.x+float(x)*zoom),std::round(p.y+float(y)*zoom),float(w)*zoom,float(h)*zoom,color);};
 bool side=direction==1||direction==2,back=direction==3;float flip=direction==2?-1.f:1.f;float stride=frame==0?0.f:frame==1?1.f:-1.f;
 rect(-8,-1,16,4,glm::vec4(.01,.02,.04,.45));
 if(a.gender){rect(-7,-30,14,15,hair);rect(-8,-22,4,12,hair);rect(4,-22,4,12,hair);}
 rect(-5,-10,10,11,pants);rect(-5,-1+stride,4,3,ink);rect(2,-1-stride,4,3,ink);rect(-1,-6,2,7,ink);
 rect(-7,-20,14,13,coat);rect(-8,-18+stride,3,11,coat*.82f);rect(5,-18-stride,3,11,coat*.82f);
 rect(-8,-8+stride,3,3,skin);rect(5,-8-stride,3,3,skin);rect(-5,-19,10,1,coat*1.2f);
 rect(-2,-22,4,3,skin);rect(-5,-29,10,10,skin);rect(-6,-30,12,5,hair);rect(-6,-26,2,5,hair);
 if(!back){rect(side?flip*3-1:-3,-24,2,2,ink);if(!side)rect(2,-24,2,2,ink);rect(side?flip*4:-1,-21,2,1,skin*.65f);rect(-1,-18,1,7,glm::vec4(.94,.86,.62,1));rect(-2,-11,4,3,glm::vec4(.89,.94,.93,1));rect(-1,-10,2,1,coat);}
 else {rect(-5,-27,10,8,hair);rect(-3,-18,6,1,coat*.7f);}
 if(a.gender){rect(-6,-28,2,11,hair);rect(4,-28,2,11,hair);if(a.hair==3)rect(-3,-32,7,4,hair);}
 else if(a.hair==1){rect(-6,-31,12,3,hair);rect(3,-28,3,7,hair);}else if(a.hair==2)rect(-4,-32,8,4,hair);
 if(bag){float bx=back?-5:side?-flip*6-3:-7;rect(bx,-18,side?6:back?11:3,12,glm::vec4(.62,.43,.25,1));rect(bx+1,-17,side?4:back?9:1,2,glm::vec4(.83,.65,.39,1));if(back){rect(bx+2,-11,7,4,glm::vec4(.44,.31,.22,1));rect(bx+3,-10,5,1,glm::vec4(.91,.76,.48,1));}}
}
void studentPortrait(float x,float y,float size){
 float z=size/64;auto rect=[&](auto xx,auto yy,auto w,auto h,glm::vec4 c){box(x+float(xx)*z,y+float(yy)*z,float(w)*z,float(h)*z,c);};
 auto a=avatar;auto skin=skinColor(a.skin),hair=hairColor(a.hair),coat=outfitColor(a.outfit),ink=glm::vec4(.07,.09,.14,1);
 rect(0,0,64,64,glm::vec4(.09,.12,.23,1));for(int i=0;i<7;i++)rect(i*11-8,0,2,64,glm::vec4(.12,.19,.29,1));
 rect(10,49,45,15,coat);rect(17,43,31,13,coat*.8f);rect(26,37,12,12,skin*.82f);
 if(a.gender)rect(13,10,39,43,hair);
 rect(19,13,28,29,skin);rect(16,24,4,9,skin*.85f);rect(46,24,4,9,skin*.85f);
 rect(17,8,32,12,hair);rect(16,16,6,12,hair);rect(21,12,21,6,hair);rect(41,17,7,a.gender?31:8,hair);
 rect(23,25,7,2,hair);rect(36,25,7,2,hair);rect(24,29,5,3,ink);rect(37,29,5,3,ink);rect(25,29,1,1,WHITE);rect(38,29,1,1,WHITE);
 rect(31,31,3,6,skin*.72f);rect(28,39,11,2,skin*.58f);rect(25,47,3,17,glm::vec4(.95,.85,.55,1));rect(39,47,3,17,glm::vec4(.95,.85,.55,1));rect(28,58,12,6,WHITE);rect(30,60,8,2,coat);
 if(a.hair==2)rect(22,5,23,5,hair);if(a.gender&&a.hair==3)rect(36,3,12,8,hair);
}
