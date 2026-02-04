#version 450 core

out vec4 FragColor;
uniform vec2 u_resolution;
uniform float u_time;

void main()
{
    // Map pixel to complex plane
    vec2 c;
    c.x = (gl_FragCoord.x / u_resolution.x) * 3.0 - 2.0;
    c.y = (gl_FragCoord.y / u_resolution.y) * 3.0 - 1.5;

    // Balanced subtle dynamic center and continuous zoom
    vec2 center = vec2(-0.74364388703 + 0.008 * sin(u_time * 0.03),
                       0.13182590421 + 0.008 * cos(u_time * 0.025));

    float zoom = pow(1.02, u_time * 30.0); // continuous zoom
    c = (c - center) / zoom + center;

    // Mandelbrot iteration
    vec2 z = vec2(0.0);
    int iter;
    const int max_iter = 400;

    for(iter = 0; iter < max_iter; ++iter) {
        float x = (z.x * z.x - z.y * z.y) + c.x;
        float y = (2.0 * z.x * z.y) + c.y;
        z = vec2(x, y);
        if(dot(z, z) > 4.0) break;
    }

    // Smooth dynamic color
    float t = float(iter) / float(max_iter);
    float r = 0.5 + 0.5 * cos(3.0 + t*10.0 + u_time*0.5);
    float g = 0.5 + 0.5 * cos(1.0 + t*10.0 + u_time*0.7);
    float b = 0.5 + 0.5 * cos(5.0 + t*10.0 + u_time*0.9);

    FragColor = vec4(r, g, b, 1.0);
}