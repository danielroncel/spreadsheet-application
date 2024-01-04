x = '=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12;MIN(A13:A20))'
y = '=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12;MIN(A13:A20))'

assert len(x) == len(y)

for i in range(len(x)):
    if x[i] != y[i]:
        print(i)