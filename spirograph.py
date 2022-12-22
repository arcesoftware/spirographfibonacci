from turtle import * 
screensize(canvwidth=7680, canvheight=4800, bg='black')
def fibonacci(n):
    fibo = []
    for i in range(n): 
        if i == 0 or i == 1:
            fibo.append(i)
        else:
            f = fibo.append(fibo[i-1] + fibo[i-2])
    fibo[n] = f 
    return f
def sprirograph(fibonacci):     
    for i in range(13):
        color('red') 
        for i in range (37):
            if i==13 or i == 55:
                forward(13) 
            forward(55)
            left(13)
        left(55)
while True: 
    sprirograph(fibonacci)
