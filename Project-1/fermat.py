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
	

def fprobability(k):  
    # Finding the probability for Fermat Algorithm is extremely simple. 
    # Because the function has a one-to-one relation with elements that
    # fail the test and elements that pass, this implies there is a 1/2
    # chance the test will fail. Increasing the amount of tests done
    # exponentially decreases this chance by changing the probability to
    # 1 / 2 * k where k is the number of tests run.
    return 1 - ( 1 / (2 * k))


def mprobability(k):
    # For this test, the more bases of a that are tried, the more accurate
    # the test will be. If N is composite, then at most 1/4 of the bases are
    # strong liars for N. So compounding this probability with k gives you
    # a probability of 1 / 4 * k error. This is superior to the Fermat test.
    return 1 - (1 / (4 * k))

def fermat(N,k):
    # This function uses the Fermat algorithm to determine if a number is prime or composite.
    # k represents the amount of iterations when testing if the input 'N' is
    # prime or not. The larger k, the more precise the algorithm. the 'a' value is chosen
    # at random with the random.randint() method. this is done k number of iterations.
    # If the algorithm finds a case where a^(N-1)%1 == 1 it will return prime
    # early, otherwise it will return composite.
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
            a = random.randint(2, N - 2)

            if mod_exp(a, N - 1, N) == 1:
                return 'prime'
    return 'composite'



def miller_rabin(N,k):
    # this function did not have any pseudo code provided in the text but it also
    # functions quite similarly to the Fermat test.

    # once again we need to check manually for values 4 or less
    if N == 1 or N == 4:
        return 'composite'
    elif N == 2 or N == 3:
        return 'prime'
    else:
        # integer 'a' will need to be 1 < a < N - 1
        # we are trying to achieve 
        # - a^d = 1 (mod N)     or
        # - a^(2^r)d = -1 (mod N) for some 0 <= r <= s
        # when N is an odd prime it will pass because of Fermat's little theorem where
        # - a^(n-1) = 1 (mod N)
        # the only only square roots of 1 mod N are 1 and -1

        # We need to factor out powers of 2 from N - 1 so that we end up with 2^r * d + 1
        d = N - 1
        while (d % 2 == 0):
            d //= 2

        # now we loop for k iterations
        for i in range(k):
            # a is once again our random value
            a = random.randint(2, N - 2)
            # x holds the value for a^d mod N
            x = mod_exp(a, d, N)
            # if x returned as 1 or N - 1, we can exit early and know it's prime
            if (x == 1 or x == N - 1):
                return 'prime'
            
            # loop an r number of times
            while (d != N - 1):
                # x = x^2 mod N
                x = (x * x) % N
                d *= 2

                if (x == 1):
                    return 'composite'
                if (x == N - 1):
                    return 'prime'
            
            return 'composite'
