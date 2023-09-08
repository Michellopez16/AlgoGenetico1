l_sel= [[5, 0, 1], [4, 2, 1], [5, 1, 0], [1, 5, 4], [0, 1, 4], [2, 1, 0], [1, 5, 3], [3, 2, 5], [0, 5, 3], [0, 4, 5],
        [0, 2, 3], [4, 0, 3], [4, 3, 1], [5, 3, 4], [2, 4, 3], [0, 2, 3], [3, 4, 1], [4, 3, 5], [2, 4, 1], [2, 3, 1],
        [3, 1, 2], [2, 4, 0], [4, 0, 5], [4, 3, 2]]

l_rand= [0.59, 0.96, 0.64, 0.86, 0.44, 0.70, 0.78, 0.96, 0.67, 0.89, 0.46, 0.34, 0.24, 0.80, 0.77, 0.11, 0.91, 0.69,
         0.80, 0.50, 0.60, 0.18, 0.55, 0.39, 0.68, 0.21, 0.01, 0.91, 0.78, 0.35, 0.04, 0.49, 0.43, 0.13, 0.82, 0.66,
         0.40, 0.50, 0.93, 0.64, 0.75, 0.96, 0.13, 0.30, 0.63, 0.55, 0.46, 0.87, 0.03, 0.59, 0.87, 0.42, 0.34, 0.68,
         0.99, 0.32, 0.15, 0.69, 0.40, 0.49, 0.58, 0.48, 0.76, 0.22, 0.73, 0.50, 0.10, 0.21, 0.95, 0.64, 0.41, 0.13,
         0.69, 0.48, 0.41, 0.08, 0.34, 0.14, 0.62, 0.71, 0.01, 0.70, 0.05, 0.37, 0.96, 0.26, 0.58, 0.88, 0.95, 0.05,
         0.06, 0.51, 0.39, 0.61, 0.45, 0.42, 0.25, 0.69, 0.18, 0.66, 0.72, 0.33, 0.90, 0.78, 0.36, 0.37, 0.91, 0.15, ]

l_cross= [1, 2, 2, 1, 2, 2, 2, 1, 1, 1]



r_cross = 0.9
r_mut = 0.25

min_value = -1
max_value = 1

n_bits = 4 #bits

import numpy as np
f = lambda x: x**2



def mapping(decimal_values,min_value=-1,max_value=1):
    
    return min_value + decimal_values*(max_value - min_value)/(2**n_bits-1)

pop=[[0, 1, 0, 1], [1, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1]]
b = [0, 0, 0, 0] 
popn = []
for elem in pop:
    popn.append(b+elem)
popn
pop_int8 = np.packbits(popn)
pop_int8 # -> [-1,1]

#print(pop_int8)
pop_int8 = np.random.randint(0,15,6)

for num_m in range(4):


    decoded_values = mapping(pop_int8)
    fitnesses = f(decoded_values)
    #l_sel_tmp = np.array(l_sel[:6])
    l_sel_tmp = np.random.randint(0,6,(6,3) )
    tournaments = np.choose(l_sel_tmp,fitnesses )

    min_value = tournaments.min(axis=1)
    index_array_min_arg = tournaments.argmin(axis=1)
    ind_pop_int8 = np.take_along_axis(l_sel_tmp,index_array_min_arg.reshape( (-1,1) ),axis=1).reshape( (-1) )

    pop_elegida = pop_int8[ind_pop_int8]

    pop_a = pop_elegida[0::2]
    pop_b = pop_elegida[1::2]

    a = pop_a
    b = pop_b
    #a = np.array([10, 10,  9], dtype=np.uint8) #pop_a
    #b = np.array([ 9,  9, 10], dtype=np.uint8)  #pop_b

    #np.array([0.59,0.89,0.80])
    #np.array([1,1,1])
    #valor_de_alla = np.array([1, 2, 2])
    valor_de_alla = np.random.randint(1,3,3)

    m=n_bits-valor_de_alla

    mask_a= (-1 << m)
    mask_b= ~(-1 << m) 

    ab = (a & mask_a) | (b & mask_b) 
    ba = (b & mask_a) | (a & mask_b)

    n_pop = np.stack((ab,ba), axis = 1,dtype=np.int8).flatten()

    #mutaciones_4bits = np.array([ 0.96, 0.64, 0.86, 0.44, 0.70, 0.78, 0.96, 0.67,
    #0.46, 0.34, 0.24, 0.80, 0.77, 0.11, 0.91, 0.69,
    #0.50, 0.60, 0.18, 0.55, 0.39, 0.68, 0.21, 0.01,]) < r_mut
    mutaciones_4bits = np.random.random(24) < r_mut

    #b= np.zeros(len(a),dtype=np.uint8)
    #c = np.stack((b,a), axis = 1).flatten()

    tmp_zeros= np.zeros(len(mutaciones_4bits),dtype=np.uint8).reshape((-1,n_bits))

    mutaciones_4bits= mutaciones_4bits.reshape((-1,4))

    mutaciones_8bits = np.stack((tmp_zeros,mutaciones_4bits), axis = 1).flatten()
    mutaciones_int8 = np.packbits(mutaciones_8bits, axis=-1)

    pop_int8 = np.array( (n_pop | mutaciones_int8) & ~(n_pop & mutaciones_int8), dtype=np.int8)

fitnesses = f(mapping(pop_int8))
    
print(pop_int8)
print(fitnesses)

