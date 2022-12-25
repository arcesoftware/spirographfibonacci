import pandas as pd
import turtle
#number of sides
n = 13
#lenght of the sizes
l = 55
turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')
def fibonacci(n):
    fibo = []
    for i in range(n):
        if i == 0 or i == 1:
            fibo.append(i)
        else:
            f = fibo[i-1] + fibo[i-2]
            fibo.append(f)
    return fibo

fibonacci_numbers = fibonacci(n)
df = pd.DataFrame(fibonacci_numbers, columns=['Fibonacci Number'])
print(df)

def sprirograph(fibonacci_sequence):
    for f in fibonacci_sequence:
        turtle.color('red')
        turtle.speed(0)
        for i in range(f):
            if i == n or i == l:
                turtle.forward(f)
            turtle.forward(f)
            turtle.left(f)
        turtle.left(f)

i = 0
while i < 10: 
    sprirograph(fibonacci(1000))
    i += 1
