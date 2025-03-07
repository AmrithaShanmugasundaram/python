
high=5
low=1
n=3
arr=[10, 7, 8]
cnt=0
for i in arr:
    while i>0:
        cnt+=1
        i-=high
        if i>0:
            i+=low
print(cnt)