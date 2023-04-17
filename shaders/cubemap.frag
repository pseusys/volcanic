#version 330 core

// global color variable
uniform samplerCube day_sky, night_sky;
uniform float time;

in vec3 texCoords;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec4 day_color = texture(day_sky, texCoords);
    vec4 night_color = texture(night_sky, texCoords);
    out_color = vec4(day_color.rgb * time, day_color.a) + vec4(night_color.rgb * (1-time), night_color.a); //night_color * (1 - w_time); 
}