xyz = "1,1,1"
c1 = xyz.find(",")
c2 = xyz[c1 + 2:].find(",") + 2
#try:
x = xyz[0:c1]
y = xyz[c1+1:c2+1]
z = xyz[c2+2:]
print(x)
print(y)
print(z)