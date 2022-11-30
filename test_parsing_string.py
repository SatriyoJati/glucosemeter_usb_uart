import re

'''
raw_data  = [[a,b],[]]
raw_data[0] = [a,b]
raw_data[0][0] = a

for i in range(len(raw_data))
    if raw_data[i] is not []:
        for j in range(len(raw_data)):
            raw_data[i][j].decode("utf-8")
'''

my_string = [[b'alice',b'/x00 /x00/x00/x00/x00/x00/x00/x00 /x00/x00/x00 /x00/x00/x00 theodora  1231415 205'],[]]

parsed_string = []

for i in range(len(my_string)):
    if my_string[i] is not []:
        for j in range(len(my_string[i])):
            parsed_string.append(my_string[i][j].decode("utf-8"))

for i in range(len(parsed_string)):
    print(parsed_string[i])

for i in range(len(parsed_string)):
    if 'theodora' in parsed_string[i]:
        output = re.findall(r'theodora.*', parsed_string[i])
        # list_output = output.split(' ')
final_output = output[0].split(' ')

print(final_output[3])

mylist = [0,1,3,4,5,6,8]
for i in range(len(mylist)):
    print(i)