#code here
import demoFeature1


while (True):
    inp = input("Enter 1 to select demoFeature1 or press q to quit")
    if inp =="q":
        break
    if inp == "1":
        demoFeature1.hello()
