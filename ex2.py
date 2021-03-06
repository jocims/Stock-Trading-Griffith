cur_x = 6 # The algorithm starts at x=6
gamma = 0.01 # step size multiplier
precision = 0.00001
previous_step_size = 1
max_iters = 10000 # maximum number of iterations
iters = 0 #iteration counter
momentum = 0.5
velocity = 0
df = lambda x: 4 * x**3 - 9 * x**2
while (previous_step_size > precision) & (iters < max_iters):
	prev_x = cur_x
	velocity = momentum * velocity + df(prev_x)
	cur_x -= gamma * velocity
	previous_step_size = abs(cur_x - prev_x)
	iters+=1
