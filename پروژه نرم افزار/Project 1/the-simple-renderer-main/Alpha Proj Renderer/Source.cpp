#include <sb7.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

class mandelbrot_app : public sb7::application
{
    GLuint shaderProgram;
    GLuint VAO;
    GLuint VBO;
    GLuint resLoc;
    GLuint timeLoc;
    std::string loadShaderFile(const std::string& path)
    {
        std::ifstream file(path);
        std::stringstream buffer;
        buffer << file.rdbuf();
        return buffer.str();
    }

    GLuint compileShader(GLenum type, const std::string& source)
    {
        GLuint shader = glCreateShader(type);
        const char* src = source.c_str();
        glShaderSource(shader, 1, &src, nullptr);
        glCompileShader(shader);

        GLint status;
        glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
        if (status != GL_TRUE)
        {
            char buffer[512];
            glGetShaderInfoLog(shader, 512, nullptr, buffer);
            std::cerr << "Shader compilation error: " << buffer << std::endl;
        }
        return shader;
    }

    GLuint createProgram(const std::string& vertFile, const std::string& fragFile)
    {
        GLuint vertShader = compileShader(GL_VERTEX_SHADER, loadShaderFile(vertFile));
        GLuint fragShader = compileShader(GL_FRAGMENT_SHADER, loadShaderFile(fragFile));
        GLuint program = glCreateProgram();
        glAttachShader(program, vertShader);
        glAttachShader(program, fragShader);
        glLinkProgram(program);

        GLint status;
        glGetProgramiv(program, GL_LINK_STATUS, &status);
        if (status != GL_TRUE)
        {
            char buffer[512];
            glGetProgramInfoLog(program, 512, nullptr, buffer);
            std::cerr << "Program link error: " << buffer << std::endl;
        }

        glDeleteShader(vertShader);
        glDeleteShader(fragShader);

        return program;
    }

public:
    void startup() override
    {
        shaderProgram = createProgram("shaders/vertexShaderInput.glsl", "shaders/fragmentShaderInput.glsl");
        resLoc = glGetUniformLocation(shaderProgram, "u_resolution");
        timeLoc = glGetUniformLocation(shaderProgram, "u_time");
        // Full-screen quad
        float quadVertices[] = {
            -1.0f, -1.0f,
             1.0f, -1.0f,
            -1.0f,  1.0f,
            -1.0f,  1.0f,
             1.0f, -1.0f,
             1.0f,  1.0f
        };

        glGenVertexArrays(1, &VAO);
        glGenBuffers(1, &VBO);
        glBindVertexArray(VAO);
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(quadVertices), quadVertices, GL_STATIC_DRAW);
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);
        glEnableVertexAttribArray(0);
    }

    void render(double currentTime) override
    {
        int width = info.windowWidth;
        int height = info.windowHeight;

        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(shaderProgram);
        glUniform2f(resLoc, (float)width, (float)height); 
            glUniform1f(timeLoc, (float)currentTime);


        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 6);
    }

    void shutdown() override
    {
        glDeleteProgram(shaderProgram);
        glDeleteVertexArrays(1, &VAO);
        glDeleteBuffers(1, &VBO);
    }
};

DECLARE_MAIN(mandelbrot_app);








