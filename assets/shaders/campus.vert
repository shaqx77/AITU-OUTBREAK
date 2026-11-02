#version 330 core
layout(location=0) in vec3 position;
layout(location=1) in vec3 normal;
layout(location=2) in vec3 color;
uniform mat4 view;
uniform mat4 projection;
out vec3 worldPosition;
out vec3 worldNormal;
out vec3 albedo;
void main() {
    worldPosition = position;
    worldNormal = normal;
    albedo = color;
    gl_Position = projection * view * vec4(position, 1.0);
}
