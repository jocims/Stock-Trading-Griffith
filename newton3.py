current = 6 # The algorithm starts at x=6
precision = 0.00001
previous_step_size = 1
max_iters = 10000 # maximum number of iterations
iters = 0 #iteration counter

df = lambda x: 4 * x**3 - 9 * x**2
df2 = lambda x: 12 * x**2 - 18  * x

while (previous_step_size > precision) & (iters < max_iters):
    previous = current
    current -= df(previous) / df2(previous)
    previous_step_size = abs(current - previous)
    iters+=1

if iters >= max_iters:
    print("local minimum not found")
    print("value found after max iterations: ", current)
else:
    print("The local minimum occurs at:", current)
    print("Number of iterations used:", iters)
