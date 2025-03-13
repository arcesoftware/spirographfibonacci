import turtle
from random import randint
import math

# Set up the screen
turtle.screensize(canvwidth=10000, canvheight=10000, bg="white")
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Armadillo")

# Set up the turtle
skk = turtle.Turtle()
skk.speed(0)  # Fastest drawing speed
turtle.colormode(255)  # Enable RGB color mode
skk.width(1)  # Set the pen width
skk.goto(-150, -150)

# Memoization for Fibonacci
memo = {}

def fibonacci(n):
    if n in memo:
        return memo[n]
    if n <= 2:
        f = 1
    else:
        f = fibonacci(n-3) + fibonacci(n-5) + fibonacci(n-9) + fibonacci(n-7)
    memo[n] = f
    return f

# Number of sides and length of the star
n = 37
l = 59
s = math.sqrt(2)

# Function to draw the first star with more complex angles
def star1(fib_num):
    for i in range(n):
        # Using Fibonacci number to modify the pen color
        skk.color(randint(0, 255), randint(0, 255), randint(0, 255))
        # Draw forward with modified length
        skk.forward(fib_num * s)
        
        # More intricate turn with sin and cos to create complex angle
        angle = (fib_num + math.sin(i * math.pi / 4) * 50)  # Apply sine to vary the angle
        skk.left(angle)

# Function to draw the second star with a more complex rotation
def star2(fib_num):
    for i in range(n):
        skk.color(randint(0, 255), randint(0, 255), randint(0, 255))
        skk.forward(fib_num * s)
        
        # Adding more mathematical complexity to the angle with cosine and powers of Fibonacci
        angle = (fib_num + math.cos(i * math.pi / 5) * 30)  # Apply cosine to vary the angle
        skk.right(angle)

# Function to draw a complex pattern with enhanced rotation logic
def draw_pattern():
    for i in range(10, n, 5):  # Loop to create multiple patterns with different Fibonacci numbers
        fib_num = fibonacci(i)
        
        # Draw the first star with more complex rotation
        star1(fib_num)
        
        # Add a slight rotation to give variety to the pattern
        skk.right(fib_num * 2)  # Rotate by Fibonacci number
        
        # Draw the second star with more complex rotation
        star2(fib_num)
        
        # Adjust angle between patterns for a more complex structure
        skk.left(fib_num * 3)

# Start the drawing
draw_pattern()

# Hide the turtle and finish drawing
skk.hideturtle()
turtle.done()

