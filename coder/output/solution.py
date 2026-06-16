Plan:
1. Define a variable sum to hold the total sum of the series. Initialize it to 0.
2. Define a loop that will iterate 10,000 times.
3. Each time in the loop, compute 1 divided by the current index value.
    * If index is even, add this result to the sum.
    * If index is odd, subtract this result from the sum.
4. Print out the total sum.

Here is the code for the series:

```python
def serie_sum(n): 
    sum = 0 
    negate = False

    for i in range(1, 2*n, 2):
        if not negate:
            sum += 1/i
            negate = True
        else:
            sum -= 1/i
            negate = False
     
    return sum

print(serie_sum(10000))
```
This will calculate 1 - 1/3 + 1/5 - 1/7 + 1/9 - ... up to 10000 terms.

To validate the program, we can test the function with different values and check if the results are as expected. We know that sum of infinite series is Pi/4, by considering first 10000 terms we can get the approximation.

```python
import math

result = serie_sum(10000)
print('Series sum is', result)

#Verify the result with Pi/4
print('Error :', abs(result - math.pi/4))
```

This will calculate error between value given by our function and Pi/4. If the code is correct, the error should be a very small number.