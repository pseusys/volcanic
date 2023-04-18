#version 330 core

// input attribute variable, given per vertex
in vec3 position;

// global matrix variables
uniform mat4 view, projection;

out vec3 tex_coords;

void main() {
    // initialize interpolated colors at vertices
    tex_coords = position;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * vec4(position, 1);
}
