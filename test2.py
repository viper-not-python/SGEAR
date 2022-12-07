xyz = "1.35,-0.05,-0.22"
c1 = xyz.find(",")
c2 = xyz[c1 + 1:].find(",") + c1
#try:
print(c1)
print(c2)
x = xyz[0:c1]
y = xyz[c1+1:c2+1]
z = xyz[c2+2:]
print(x)
print(y)
print(z)