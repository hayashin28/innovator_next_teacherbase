'''
print(3)
print(2)
print(1)
print('GO!!')
'''
num = 4
for i in range(num):
    if num - i - 1 == 0:
        print(str(num) + ' - ' + str(i) + ' - 1 = '  + 'GO!!')
    else:      
        print(str(num) + ' - ' + str(i) + ' - 1 = ' + str(num - i - 1))