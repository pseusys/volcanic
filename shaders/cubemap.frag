#version 330 core

// global color variable
uniform samplerCube diffuse_map;
in vec3 texCoords;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    out_color = texture(diffuse_map, texCoords);
}