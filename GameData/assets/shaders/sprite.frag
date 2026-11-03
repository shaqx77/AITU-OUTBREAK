#version 330 core
in vec2 U;in vec4 C;uniform sampler2D tex;out vec4 o;void main(){o=texture(tex,U)*C;}