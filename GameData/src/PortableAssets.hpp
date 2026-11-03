#pragma once
// Assets travel inside the Windows executable. They are materialized as normal
// files for the existing JSON, image, shader and audio loaders, without a network.
#ifdef _WIN32
namespace portable {
struct Entry {std::string name;uint32_t crc,compressed,size,offset;uint16_t method;};
struct Bundle {const unsigned char* bytes=nullptr;size_t size=0;std::vector<Entry> files;std::string id;};
uint16_t u16(const unsigned char* p){return uint16_t(p[0])|(uint16_t(p[1])<<8);}
uint32_t u32(const unsigned char* p){return uint32_t(p[0])|(uint32_t(p[1])<<8)|(uint32_t(p[2])<<16)|(uint32_t(p[3])<<24);}
uint32_t updateCRC(uint32_t crc,const unsigned char* data,size_t size){
 static const std::array<uint32_t,256> table=[](){std::array<uint32_t,256> t{};for(uint32_t n=0;n<256;n++){uint32_t c=n;for(int k=0;k<8;k++)c=(c&1)?0xedb88320u^(c>>1):c>>1;t[n]=c;}return t;}();
 for(size_t i=0;i<size;i++)crc=table[(crc^data[i])&255]^(crc>>8);return crc;
}
uint32_t crcOf(const std::vector<unsigned char>& data){return updateCRC(0xffffffffu,data.data(),data.size())^0xffffffffu;}
std::wstring environment(const wchar_t* name){DWORD n=GetEnvironmentVariableW(name,nullptr,0);if(!n)return {};std::wstring value(n,L'\0');DWORD actual=GetEnvironmentVariableW(name,value.data(),n);if(!actual||actual>=n)return {};value.resize(actual);return value;}
Bundle load(){
 HMODULE module=GetModuleHandleW(nullptr);HRSRC resource=FindResourceW(module,MAKEINTRESOURCEW(201),MAKEINTRESOURCEW(10));
 if(!resource)throw std::runtime_error("The executable has no embedded game data. Download the complete AITU-OUTBREAK.exe again.");
 HGLOBAL loaded=LoadResource(module,resource);Bundle b;b.size=SizeofResource(module,resource);b.bytes=static_cast<const unsigned char*>(LockResource(loaded));
 if(!b.bytes||b.size<22)throw std::runtime_error("Embedded game data is incomplete.");
 size_t end=b.size-22;bool found=false;size_t limit=b.size>65557?b.size-65557:0;
 for(;;){if(u32(b.bytes+end)==0x06054b50u&&end+22+u16(b.bytes+end+20)==b.size){found=true;break;}if(end==limit)break;end--;}
 if(!found)throw std::runtime_error("Embedded data directory is missing.");
 const auto* trailer=b.bytes+end;uint16_t count=u16(trailer+10);size_t cursor=u32(trailer+16);
 if(u16(trailer+4)||u16(trailer+6)||count!=u16(trailer+8)||count==65535)throw std::runtime_error("Unsupported embedded data archive.");
 for(unsigned int i=0;i<count;i++){
  if(cursor+46>b.size||u32(b.bytes+cursor)!=0x02014b50u)throw std::runtime_error("Embedded data directory is damaged.");
  auto p=b.bytes+cursor;size_t length=u16(p+28),extra=u16(p+30),comment=u16(p+32);
  if(cursor+46+length+extra+comment>b.size||(u16(p+8)&1))throw std::runtime_error("Invalid embedded data entry.");
  std::string name(reinterpret_cast<const char*>(p+46),length);while(name.rfind("./",0)==0)name.erase(0,2);
  if(!name.empty()&&name.back()!='/'){
   auto path=std::filesystem::u8path(name);if(path.is_absolute()||path.has_root_name()||name.find('\\')!=std::string::npos||name.find(':')!=std::string::npos||name.find('\0')!=std::string::npos)throw std::runtime_error("Invalid embedded resource path.");
   for(const auto& part:path)if(part=="..")throw std::runtime_error("Invalid embedded resource parent path.");
   Entry e{name,u32(p+16),u32(p+20),u32(p+24),u32(p+42),u16(p+10)};
   if(e.size>64u*1024u*1024u||(e.method!=0&&e.method!=8))throw std::runtime_error("Unsupported embedded resource.");b.files.push_back(e);
  }
  cursor+=46+length+extra+comment;
 }
 if(b.files.empty())throw std::runtime_error("Embedded game data is empty.");
 uint64_t hash=14695981039346656037ull;for(size_t i=0;i<b.size;i++){hash^=b.bytes[i];hash*=1099511628211ull;}
 std::ostringstream id;id<<std::hex<<hash;b.id=id.str();return b;
}
bool validFile(const std::filesystem::path& path,const Entry& e){
 std::error_code error;if(!std::filesystem::is_regular_file(path,error)||std::filesystem::file_size(path,error)!=e.size)return false;
 std::ifstream in(path,std::ios::binary);if(!in)return false;std::array<unsigned char,65536> buffer{};uint32_t crc=0xffffffffu;size_t total=0;
 while(in){in.read(reinterpret_cast<char*>(buffer.data()),buffer.size());size_t n=size_t(in.gcount());crc=updateCRC(crc,buffer.data(),n);total+=n;}
 return total==e.size&&(crc^0xffffffffu)==e.crc;
}
std::vector<unsigned char> inflate(const Bundle& b,const Entry& e){
 size_t start=e.offset;if(start+30>b.size||u32(b.bytes+start)!=0x04034b50u)throw std::runtime_error("Embedded resource header is damaged: "+e.name);
 start+=30+u16(b.bytes+start+26)+u16(b.bytes+start+28);
 if(start>b.size||e.compressed>b.size-start)throw std::runtime_error("Embedded resource is truncated: "+e.name);
 std::vector<unsigned char> output(e.size);
 if(e.method==0){if(e.compressed!=e.size)throw std::runtime_error("Invalid stored resource: "+e.name);std::copy_n(b.bytes+start,e.size,output.begin());}
 else {int n=stbi_zlib_decode_noheader_buffer(reinterpret_cast<char*>(output.data()),int(output.size()),reinterpret_cast<const char*>(b.bytes+start),int(e.compressed));if(n!=int(e.size))throw std::runtime_error("Cannot unpack resource: "+e.name);}
 if(crcOf(output)!=e.crc)throw std::runtime_error("Embedded resource checksum failed: "+e.name);return output;
}
std::filesystem::path prepare(const Bundle& b){
 auto home=environment(L"AITU_DATA_HOME");if(home.empty())home=environment(L"LOCALAPPDATA");
 auto base=home.empty()?std::filesystem::temp_directory_path():std::filesystem::path(home);
 auto directory=base/L"AITU-OUTBREAK"/L"Runtime"/b.id/L"assets";std::filesystem::create_directories(directory);
 for(const auto& e:b.files){
  auto path=directory/std::filesystem::u8path(e.name);if(validFile(path,e))continue;
  auto data=inflate(b,e);std::filesystem::create_directories(path.parent_path());auto temp=path;temp+=L".unpack-"+std::to_wstring(GetCurrentProcessId());
  {std::ofstream out(temp,std::ios::binary|std::ios::trunc);out.write(reinterpret_cast<const char*>(data.data()),std::streamsize(data.size()));out.flush();if(!out)throw std::runtime_error("Cannot save game resource: "+e.name);}
  if(!MoveFileExW(temp.c_str(),path.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Cannot finish preparing resource: "+e.name);
 }
 return directory;
}
void initialize(int argc,char** argv){
 bool useExternal=false;for(int i=1;i<argc;i++)if(std::string(argv[i])=="--external-assets")useExternal=true;
 wchar_t filename[32768]{};DWORD n=GetModuleFileNameW(nullptr,filename,32768);if(!n||n>=32768)throw std::runtime_error("Cannot resolve the game location.");auto parent=std::filesystem::path(filename).parent_path();
 if(useExternal){assets=std::filesystem::exists(parent/"GameData/assets")?parent/"GameData/assets":parent/"assets";diagnostics=std::filesystem::exists(parent/"GameData")?parent/"GameData/Logs":parent/"logs";}
 else {auto bundle=load();assets=prepare(bundle);diagnostics=assets.parent_path()/"Logs";}
 std::filesystem::create_directories(diagnostics);
}
}
#endif
