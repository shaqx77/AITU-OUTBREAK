#version 330 core
in vec3 worldPosition;
in vec3 worldNormal;
in vec3 albedo;
uniform vec3 eye;
uniform vec3 lightPosition;
uniform bool lightingEnabled;
out vec4 fragment;
void main() {
    vec3 N = normalize(worldNormal);
    vec3 toLight = lightPosition - worldPosition;
    float d = length(toLight);
    vec3 L = normalize(toLight);
    vec3 V = normalize(eye - worldPosition);
    vec3 H = normalize(L + V);
    float diffuse = max(dot(N, L), 0.0);
    // Specular energy is rejected on the unlit side of the surface.
    float specular = diffuse > 0.0 ? pow(max(dot(N, H), 0.0), 32.0) : 0.0;
    float attenuation = 1.0 / (1.0 + 0.025*d + 0.002*d*d);
    float fill = 0.22 + 0.20*max(dot(N, normalize(vec3(-0.3,1.0,0.4))),0.0);
    vec3 linearColor = lightingEnabled
        ? albedo*fill + attenuation*(albedo*diffuse*2.8 + vec3(1.0,0.83,0.58)*specular*0.55)
        : albedo*0.65;
    // Tone mapping and gamma conversion avoid clipping the bright moving light.
    vec3 mapped = linearColor / (linearColor + vec3(1.0));
    fragment = vec4(pow(mapped, vec3(1.0/2.2)),1.0);
}
