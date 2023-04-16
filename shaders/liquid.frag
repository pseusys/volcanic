#version 330 core

// time elapsed
uniform float time;

// size of one texture image
uniform vec2 resolution;

// texture image
uniform sampler2D tex;

// waves insensitivity
uniform float amplitude;

// animation speed
uniform float speed;

// shift of wave center from the middle
uniform float center_shift;

// wave distortion factor
uniform float distortion;

// liquid transparency
uniform float transparency;

// fragment position and normal of the fragment
in vec3 w_position, w_normal;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec2 center_pos = w_position.xz / resolution.xy - center_shift;
    float center_len = length(center_pos);

    vec2 waving = (center_pos / center_len) * cos(center_len * distortion - time * speed) * amplitude;
    vec2 uv = w_position.xz / resolution.xy + waving;
    vec3 col = texture2D(tex, uv).xyz;

    out_color = vec4(col, transparency);
}
