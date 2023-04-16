#version 330 core

uniform float time;
uniform vec2 resolution;
uniform sampler2D tex;

// fragment position and normal of the fragment
in vec3 w_position, w_normal;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec2 cPos = -1.0 + 2.0 * w_position.xy / resolution.xy;
    float cLength = length(cPos);

    vec2 uv = w_position.xy / resolution.xy + (cPos / cLength) * cos(cLength * 12.0 - time * 4.0) * 0.03;
    vec3 col = texture2D(tex, uv).xyz;

    out_color = vec4(col, 1.0);
}
