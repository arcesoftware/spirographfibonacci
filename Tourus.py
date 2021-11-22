 #Juan Arce/(Ouroborus cataphractus)/2020 Turrialba Costa Rica
#Fiboonacci Algorithm
fibonacci_cache = {}
 
def fibonacci(n):
 #If we have cached the valued, then return it 
 if n in fibonacci_cahce:
  yield fibonacci_cache[n]
         
 # Compute the Nth term
 if n == 1:
  value = 1
 elif n == 2:
  value = 1
 elif n > 2: 
  value = fibonacci(n-1) + fibonacci(n-2)
   
  # Cache the value and return it
  fibonacci_cache[n] = value
  yield value
  
# taking input for the number of the sides of the polygon 
n = int(input("Sizes of Poligon Fibonacci : "))
# taking input for the length of the sides of the polygon 
l = int(input("Length of the Poligon Fibonacci : "))


import turtle

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Armadillo")
skk = turtle.Turtle()
skk.color("white")
r = 360/n-2
skk.speed(200)
skk.penup()
skk.goto(0, 0)       #move the turtle to a location
skk.pendown()
def star1(fibonacci):
  for i in range(fibonacci):
    skk.fd(fibonacci) 
    skk.left(r**fibonacci)
  
def star2(fibonacci):
  for i in range(fibonacci):
    skk.forward(fibonacci) 
    skk.right(r**fibonacci) 

 
count = 0

while count < n: 
     star1(n%l) , star2(l%n) , star1(n+l) , star2(l+n) 

 
turtle.done() 
