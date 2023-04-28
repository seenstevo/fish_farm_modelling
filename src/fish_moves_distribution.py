# Prelim function for calcualting the probability distribution for how many times fish are moved across the full batch process

def convolve_binomial(probabilities):
    # p is a list of probabilities of Bernoulli distributions.
    # The convolution of these distributions is returned as a list
    # `z` where z[i] is the probability of i-1, i=1, 2, ..., len(p)+1.
    n = len(probabilities) + 1
    z = [1] + [0] * (n - 1)
    for p in probabilities:
        z = [(1 - p) * z[i] + p * z[i - 1] for i in range(n)]
    return z