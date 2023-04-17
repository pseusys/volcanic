#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// position and normal for the fragment shader
out vec3 w_position, w_normal;

void main() {
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model * vec4(position, 0)).xyz;

    gl_Position = projection * view * model * vec4(position, 1);
}
