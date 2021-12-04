import turtle
from random import randint
turtle.colormode(255)
# Create Fibonacci Cache
fibonacci_cache = {}

def fibonacci(n):
#If we have cached the valued, then return it 
    if n in fibonacci_cache:
        return fibonacci_cache[n]
            
# Compute the Nth term
    if n == 1:
        value = 1
    elif n == 2:
        value = 1
    elif n > 2: 
        value = fibonacci(n-1) + fibonacci(n-2)
      
# Cache the value and return it
    fibonacci_cache[n] = value
    return value

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Arce")
wn.setup(width=600, height=500)
turtle.bgcolor("black")
turtle.reset()
turtle.hideturtle()
turtle.width()
turtle.speed(200)

def fib(fibonacci):
    for i in range(fibonacci):
        turtle.color(randint(0, 255), randint(0, 255), randint(0, 255))
        turtle.forward(i)
        turtle.right(90)



while True: 
        fib(fibonacci(50))
turtle.exitonclick()