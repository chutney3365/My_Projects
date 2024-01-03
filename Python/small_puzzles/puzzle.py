# # sum has to be odd
# # product has to be even
# # both can't be prime

# import math

# def is_prime(num):
#     for i in range(2, int(num/2)+1):
#         if (num % i) == 0:
#             return False
#     else:
#         return True

# def num_sum_odd(product):
#     count = 0
#     for i in range(2, int(product/2) + 1):
#         if ((product % i) == 0 and ((product / i) + i) % 2 != 0):
#             count += 1
#     return int(count / 2)

# # for i in range (2, 801):
# #     for j in range(2, 801):
# #         if (is_prime(i) and is_prime(j)):
# #             continue
# #         sum = i + j
# #         if (sum % 2 == 0):
# #             continue
# #         seq = list(range(2, sum - 1))
# #         correct_pair = True
# #         for index in range(math.ceil(len(seq) / 2)):
# #             a = seq[index]
# #             b = seq[len(seq) - index -1]
# #             if (is_prime(a) and  is_prime(b)):
# #                 correct_pair = False
# #                 break
# #             product = a * b
# #             if (num_sum_odd(product) != 1):
# #                 correct_pair = False
# #                 break
# #         if (correct_pair == True):
# #                 print(i, j)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from collections import defaultdict

# The Riddle:
# Polly and Sam are visited by a friend. The friend, having though of two
# integers between 2 and 800 inclusive, whispers their product to Polly and
# their sum to Sam. The following dialogue results:
#   1. Polly: I don't know the two numbers
#   2. Sam: I know that and neither do I.
#   3. Polly: I know the two numbers.
#   4. Sam: So do I.
# What are the two numbers?


def generate_guesses(l=2, u=800):
    sums = defaultdict(list)
    prods = defaultdict(list)
    for p in range(l, u + 1):
        for q in range(p, u + 1):
            sums[p + q].append((p, q))
            prods[p * q].append((p, q))

    # Cannot be product of two primes, otherwise Polly would know
    def polly_does_not_know(n):
        return len(prods[n]) > 1

    # Cannot sum to something expressible by the sum of two primes
    #   By Goldbach's conjecture, this means that it at least is odd
    # Also Sam knows that Polly cannot know
    def sam_does_not_know(n):
        return (
            n % 2 == 1
            and len(sums[n]) > 1
            and all(polly_does_not_know(x * y) for (x, y) in sums[n])
        )

    # If Polly now knows, then there can only be one number such that
    # for all possible factorizations x * y of n, Sam does not know
    def now_polly_knows(n):
        count = 0
        for (x, y) in prods[n]:
            if sam_does_not_know(x + y):
                count += 1
            if count > 1:
                return False

        return count == 1

    # If Sam now knows, then for all x, y such that x + y = n
    # there should be only one such x * y where Polly knows
    def now_sam_knows(n):
        count = 0
        for (x, y) in sums[n]:
            if now_polly_knows(x * y):
                count += 1
            if count > 1:
                return False

        return count == 1

    guesses = [
        (p, q)
        for p in (range(l, u + 1)) for q in range(p, u + 1)
        if (
            polly_does_not_know(p * q)
            and sam_does_not_know(p + q)
            and now_polly_knows(p * q)
            and now_sam_knows(p + q)
        )
    ]
    return guesses


print(generate_guesses())