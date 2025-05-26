largest = None
smallest = None
while True:
    try:
        num_str = input("Enter a number or 'done'")
        if num_str == 'done':
            break

        num = int(num_str)
        if largest == None and smallest == None:
            largest = num
            smallest = num
        elif num > largest:
            largest = num
        elif num < smallest:
            smallest = num
    except ValueError:
            print("Invalid input")



print('Maximum is', largest)
print('Minimum is', smallest)








#

#largest = None
#smallest = None
#while True:
    #   num = input("Enter a number: ")
    #if num == "done":
    #   break
    #print(num)

#print("Maximum", largest)