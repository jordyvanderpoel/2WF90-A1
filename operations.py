rep = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9', 'a', 'b', 'c', 'd', 'e', 'f']

def flip_neg(x):
    return (x[1:] if x[0] == '-' else '-' + x)

def do_addition(x,y,r):
    # First handle negative numbers
    if(x[0] == '-' and y[0] == '-'):
        # x + y = -(-x + -y)
        return flip_neg(do_addition(flip_neg(x), flip_neg(y), r))
    if(x[0] == '-'):
        # x - y = y - -x
        return do_subtraction(y, flip_neg(x), r)
    if(y[0] == '-'):
        # x - y = x - -y
        return do_subtraction(x, flip_neg(y), r)

    # Ensure equal length
    maxlength = max(len(x),len(y))
    x = x.zfill(maxlength)
    y = y.zfill(maxlength)
    
    c = 0
    result = ''
    
    for i in range(maxlength-1, -1, -1): # From end to front
        sum = c + int(x[i],r) + int(y[i],r) # Calculate sum of current digits
        
        c = (sum//r if sum >= r else 0) # If we have a carry, get carry (floor division of sum over radix) else reset to 0
            
        result = rep[(sum%r)] + result # Add the sum without carries to the current result-string

    if (c > 0):
        result = rep[c] + result # Add final carry to result

    return result.lstrip('0').zfill(1)
    
def do_subtraction(x,y,r):
    # First handle negative numbers
    if(x[0] == '-' and y[0] == '-'):
        # x - y = -y - -x
        return do_subtraction(flip_neg(y), flip_neg(x), r)
    if(x[0] == '-'):
        # x - y = -(-x + y)
        return flip_neg(do_addition(flip_neg(x), y, r))
    if(y[0] == '-'):
        # x - y = x + -y
        return do_addition(x, flip_neg(y), r)
        
    # Handle y is longer x
    if len(y) > len(x):
        # x - y = -(y - x)
        return flip_neg(do_subtraction(y, x, r))

    # Handle y > x
    if len(x) == len(y):
        for i in range(len(x)):
            if int(y[i], r) > int(x[i], r):
                return flip_neg(do_subtraction(y, x, r))
            elif int(y[i], r) < int(x[i], r):
                break

    # Ensure equal length
    maxlength = max(len(x),len(y))
    x = x.zfill(maxlength)
    y = y.zfill(maxlength)
    
    c = 0
    result = ''
    
    for i in range(maxlength-1, -1, -1): # From end to front
        sum = int(x[i],r) - int(y[i],r) - c # Calculate subtraction of current digits
        
        c = (abs(sum//r) if sum < 0 else 0) # If we have a carry, get carry (floor division of sum over radix) else reset to 0
            
        result = rep[(sum%r)] + result # Add the sum without carries to the current result-string

    return result.lstrip('0').zfill(1)
    
def do_multiplication(x,y,r):    
    # First handle negative numbers
    if(x[0] == '-' and y[0] == '-'):
        # x * y = -x * -y
        return do_multiplication(flip_neg(x), flip_neg(y), r)
    if(x[0] == '-'):
        # x * y = -(-x * y)
        result = do_multiplication(flip_neg(x), y, r)
        result['answer'] = flip_neg(result['answer'])
        return result

    if(y[0] == '-'):
        # x * y = -(x * -y)
        result = do_multiplication(x, flip_neg(y), r)
        result['answer'] = flip_neg(result['answer'])
        return result
        
    # Ensure equal length
    maxlength = max(len(x),len(y))
    x = x.zfill(maxlength)
    y = y.zfill(maxlength)
    
    s = []
    result = {}
    result['answer'] = '0'
    result['count-mul'] = 0
    result['count-add'] = 0
    
    for i in range(maxlength-1, -1, -1): # X from end to front
        for j in range(maxlength-1, -1, -1): # Y from end to front            
            mul = int(x[i],r) * int(y[j],r)
            n = (maxlength - i - 1) + (maxlength - j -1)
            result['count-mul'] += 1
            
            if (mul > 0):
                s.append(rep[mul//r] + rep[mul%r] + ("0" * n))
    
    for k in s:
        result['answer'] = do_addition('0' + result['answer'], k, r).lstrip('0').zfill(1)
        result['count-add'] += 1
    
    return result

def do_karatsuba(x,y,r):
    # Base case for recursion
    if len(x) == 1 and len(y) == 1:
        return do_multiplication(x,y,r)

    # First handle negative numbers
    if(x[0] == '-' and y[0] == '-'):
        # x * y = -x * -y
        return do_karatsuba(flip_neg(x), flip_neg(y), r)
    if(x[0] == '-'):
        # x * y = -(-x * y)
        return flip_neg(do_karatsuba(flip_neg(x), y, r))
    if(y[0] == '-'):
        # x * y = -(x * -y)
        return flip_neg(do_karatsuba(x, flip_neg(y), r))

    # Ensure equal length
    maxlength = max(len(x),len(y))
    if maxlength%2 == 1:
        maxlength += 1
    y = y.zfill(maxlength)
    x = x.zfill(maxlength)
    
    s = []
    result = {}
    result['answer'] = '0'
    result['count-mul'] = 0
    result['count-add'] = 0
    
    # KARATSUBA MAGIC #
    halflength = maxlength/2
    xlo = x[0:(maxlength//2)]
    xhi = x[(maxlength//2):maxlength]
    ylo = y[0:(maxlength//2)]
    yhi = y[(maxlength//2):maxlength]
    
    # xhiylo + xloyhi = (xhi+xlo)(yhi+ylo)-xhiyhi-xloylo
    xhiyhi = do_karatsuba(xhi,yhi,r)
    xloylo = do_karatsuba(xlo,ylo,r)
    xhixloyhiylo = do_karatsuba(do_addition(xhi,xlo,r), do_addition(yhi, ylo,r),r) #(xhi+xlo)(yhi+ylo)
    xhiyloPxloyhi = do_subtraction(do_subtraction(xhixloyhiylo['answer'], xhiyhi['answer'],r), xloylo['answer'],r);
    
    result['count-mul'] += xhiyhi['count-mul'] + xloylo['count-mul'] + xhixloyhiylo['count-mul']
    result['count-add'] += xhiyhi['count-add'] + xloylo['count-add'] + xhixloyhiylo['count-add'] + 4
    
    outLo = xhiyhi['answer']
    outMe = xhiyloPxloyhi + ("0" * (maxlength//2))
    outHi = xloylo['answer'] + ("0" * (maxlength))
    
    result['answer'] = do_addition(do_addition(outLo, outMe, r), outHi, r)
    
    return result

# return the length of a string x in radix r
def get_len(x, r):
    k = '0'
    while len(x) > 0:
        x = x[1:]
        k = do_addition(k, '1', r)
    return k

# x^y with radix r
def do_pow(x, y, r):
    result = x

    if y == '0':
        return '1'

    while y != '1':
        result = do_multiplication(result, x, r)['answer']
        y = do_subtraction(y, '1', r)
    return result

# Cast a radix to a str digit with itself as radix
def do_radix_to_str(r):
    s = '0'
    k = r
    while k > 0:
        s = do_addition(s, '1', r)
        k = k - 1
    return s

# Implementation of algorithm 1.5
def do_division(x,y,b):

    # Dividing by zero resolves to 0
    if y == '0':
        return {
            'r': '0',
            'q': '0'
        }

    # Initialize result vars
    r = x
    q = '0'

    # Get the length of both digits
    m = get_len(x,b)
    n = get_len(y,b)

    # k = m - n + 1
    k = do_addition(do_subtraction(m,n,b), '1', b)

    # Loop over k-1, k-2, ..., 0
    i = do_subtraction(k, '1', b)
    while i[0] != '-':

        # (b^i)
        p = do_pow(do_radix_to_str(b), i, b)

        # (b^i)*y
        d = do_multiplication(p, y, b)['answer']

        # r//(b^i)
        q1 = rep[(int(r, b)//int(d, b))%b]

        # add q1 to q
        q = do_addition(q, do_multiplication(q1, p, b)['answer'], b)

        # r1 is q1*(b^i)*y
        r1 = do_multiplication(q1, d, b)['answer']

        # substract r1 from r
        r = do_subtraction(r, r1, b)

        # substract one from i to decrement the loop index
        i = do_subtraction(i, '1', b)
        
    return {
        'r': r.lstrip('0').zfill(1),
        'q': q.lstrip('0').zfill(1)
    }

# Modular reduction using long division
def do_reduce(x,m,r):
    return {
        'answer': do_division(x,m,r)['r']
    }

def do_mod_multiply(x,y,m,r):

    mul = do_multiplication(x,y,r)['answer']
    
    return do_reduce(mul,m,r)

# Implementation of Algorithm 2.2
def do_euclid(x,y,r):

    # Initialize variables
    xx = x
    yy = y
    x1 = '1'
    x2 = '0'
    y1 = '0'
    y2 = '1'

    # Loop while yy (b' in the Algorithm 2.2) > 0
    while yy != '0':

        # step 2.2
        res = do_division(xx,yy,r)

        # step 2.3
        xx = yy
        yy = res['r']

        # step 2.4
        x3 = do_subtraction(x1, do_multiplication(res['q'], x2, r)['answer'], r)
        y3 = do_subtraction(y1, do_multiplication(res['q'], y2, r)['answer'], r)

        # step 2.5 and 2.6
        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3
    
    # GCD
    d = xx

    # Flip signs
    if x[0] != '-' and x != '0':
        x = x1
    else:
        x = flip_neg(x1)

    if y[0] != '-' and y != '0':
        y = y1
    else:
        y = flip_neg(y1)
    
    return {
        'answ-d': d,
        'answ-a': x,
        'answ-b': y
    }

# TODO
def do_inverse(x,m,r):

    return {
        'answer': ''
    }
    

