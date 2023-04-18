#version 330 core

// input attribute variable, given per vertex
in vec3 position;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;

out vec3 texCoords;

void main() {
    // initialize interpolated colors at vertices
    texCoords = position;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * vec4(position, 1);
}
