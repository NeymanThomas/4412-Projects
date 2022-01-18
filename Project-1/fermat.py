import random


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)

def mod_exp(x, y, N):
    # This function handles calculating (a^N-1) % N 
    #
    # <PSEUDO CODE>
    # function modexp(x, y, N)
    # Input: Two n-bit integers x and N, an integer exponent y
    # Output: x^y % N
    #
    # if y = 0: return 1
    # z = modexp(x, |y/2|, N)
    # if y is even:
    #   return z^2 % N
    # else:
    #   return x * z^2 % N

    if y == 0:
        return 1
    
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return (z ** 2) % N
    else:
        return x * (z ** 2) % N
    
    # why can't it simply be this?
    #return (x ** y) % N
	

def fprobability(k):
    # You will need to implement this function and change the return value.   
    return 0.0


def mprobability(k):
    # You will need to implement this function and change the return value.   
    return 0.0

def fermat(N,k):
    # This function uses the Fermat algorithm to determine if a number is prime or composite.
    # k represents the amount of iterations when testing if the input 'N' is
    # prime or not. The larger k, the more precise the algorithm. the 'a' value is chosen
    # at random with the random.randint() method. this is done k number of iterations.
    # If the algorithm finds a case where a^(N-1)%1 != 1 it will return composite
    # early, otherwise it will return prime.
    #
    # <PSEUDO CODE>
    # function primality(N)
    # Input: Positive integer N
    # Output: yes/no
    #
    # Pick a positive integer a < N at random
    # if a^(N-1) % N = 1:
    #   return yes
    # else:
    #   return no

    # the algorithm doesn't work for numbers 1 - 4, so we have to just check
    # those values manually
    if N == 1 or N == 4:
        return 'composite'
    elif N == 2 or N == 3:
        return 'prime'
    else:
        for i in range(k):
            # it doesn't make sense to mod by 1, so start at 2
            a = random.randint(2, N - 1)

            if mod_exp(a, N - 1, N) != 1:
                return 'composite'
    return 'prime'



def miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
	#
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
	return 'composite'
