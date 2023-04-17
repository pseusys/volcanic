#version 330 core

// input attribute variable, given per vertex
in vec3 position, normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// position and normal for the fragment shader
out vec3 w_position, w_normal;

in vec3 k_a, k_d, k_s;
in float s;

out vec3 w_k_a, w_k_d, w_k_s;
out float w_s;

void main() {
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model * vec4(position, 0)).xyz;

    w_k_a = k_a;
    w_k_d = k_d;
    w_k_s = k_s;
    w_s = s;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * model * vec4(position, 1);
}
