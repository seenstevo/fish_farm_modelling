# Prelim function for calcualting the probability distribution for how many times fish are moved across the full batch process
# so loop through and store the probabilities for each event
probs = [0, 0, 0.5, 0, 0.33, 0.25, 0.2, 0.17, 0.14, 0, 0.125, 0.11, 0.1, 0.091, 0.083, 0.077]

def convolve_binomial(probabilities):
    # p is a list of probabilities of Bernoulli distributions.
    # The convolution of these distributions is returned as a list
    # `z` where z[i] is the probability of i-1, i=1, 2, ..., len(p)+1.
    n = len(probabilities) + 1
    z = [1] + [0] * (n - 1)
    for p in probabilities:
        z = [(1 - p) * z[i] + p * z[i - 1] for i in range(n)]
    return z

z = convolve_binomial(probs)