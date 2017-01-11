#
# Simple non-recursive Fibonacci
#
# Created for Concurrent Python presentation
#
# Based on examples/code from a blog/YouTube video
# * Apologies but I don't remember which one...
#
def fibonacci(n, verbose=False):
    values = []
    count = 0
    #
    if n < 0:
        sys.exit('Error:  Fibonacci term must be >= 0')
    #
    while count <= n:
        if count == 0:
            values = [0, 0]
            loop = False
        elif count == 1:
            values = [0, 1]
            loop = False
        else:
            values = [values[-1], values[-1] + values[-2]]
        #
        count += 1
        #
        if verbose:
            print('values = {}'.format(values))
    print('Fibonacci term {} = {}'.format(n, values[1]))

