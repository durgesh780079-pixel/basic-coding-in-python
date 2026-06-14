a="\nharry is good"
# file = open("harry.txt","w")
# file.write(a)

file=open("robot.txt","r")
# content=file.read()
content=file.readlines()
print(content)

file.close()