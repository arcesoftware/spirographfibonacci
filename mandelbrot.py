"""
Created on Tue Dec 27 23:22:20 2022

This code uses the turtle library to generate a graphical representation of the Mandelbrot set, which is a fractal that is defined by the behavior of a complex function known as the Mandelbrot function. The code starts by defining the maximum number of iterations and the escape time function, which is used to determine the number of iterations it takes for a given complex number, c, to escape the Mandelbrot set.

The turtle's screen size is set to 7680x4800 pixels, with a black background color. Then, the turtle's pen color is set to white and the pen size to 1 pixel. 

The turtle's speed is set to the maximum to ensure that the program runs as quickly as possible.

The code then iterates over the complex plane by using two nested for loops that range from -400 to 400. Within these loops, the code sets the value of c to be the current position on the complex plane divided by 200, and then passes this value to the escape time function. The returned value, i, is then used to determine whether or not the current point on the complex plane is a member of the Mandelbrot set.

If the point is a member of the set, the turtle's dot method is called at the current position, which will draw a point on the screen. 

If the point is not a member of the set, no dot is drawn. Once all points in the complex plane have been evaluated, the turtle is hidden and the screen is left open so that the user can view the final image.

The code uses the turtle library to generate an image of the Mandelbrot set, which is a fractal that is defined by the behavior of a complex function. 

The turtle's screen size and maximum number of iterations are set at the beginning of the code. The code then uses two nested for loops to iterate over the complex plane, and uses the escape time function to determine if each point on the complex plane is a member of the Mandelbrot set. Points that are members of the set are then plotted on the screen using the turtle's dot method.

One of the most interesting aspects of this code is the use of the turtle library to generate an image of the Mandelbrot set. 

The turtle library is traditionally used for drawing simple shapes and figures, but this code demonstrates how it can be used to create more complex and dynamic images, such as the Mandelbrot set.

Furthermore, the code uses the complex data type to represent the points on the complex plane, which allows for the use of complex arithmetic and operations. 

This is important as the Mandelbrot set is defined by the behavior of a complex function, and the use of the complex data type allows for a more accurate representation of the set.

Overall, this code provides a great example of how the turtle library can be used in an unexpected way, and how the complex data type can be used to represent mathematical concepts in a more accurate way. It also highlights the power of iteration and nested loops in generating dynamic images and exploring mathematical concepts.

@author: Arce
"""
import turtle

# Set the screen size and the maximum number of iterations
turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')
max_iterations = 256

# Define the escape time function
def escape_time(c):
    z = 0
    for i in range(max_iterations):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iterations

# Set the screen's background color
turtle.bgcolor("black")

# Set the turtle's pen color to white
turtle.pencolor("white")

# Set the turtle's pen size to 1 pixel
turtle.pensize(1)

# Set the turtle's speed to the maximum
turtle.speed(0)

# Iterate over the complex plane
for x in range(-400, 400):
    for y in range(-400, 400):
        c = complex(x/200, y/200)
        i = escape_time(c)
        if i == max_iterations:
            turtle.goto(x, y)
            turtle.dot()

# Hide the turtle and keep the screen open
turtle.hideturtle()
turtle.exitonclick()
