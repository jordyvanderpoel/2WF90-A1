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
        return flip_neg(do_multiplication(flip_neg(x), y, r))
    if(y[0] == '-'):
        # x * y = -(x * -y)
        return flip_neg(do_multiplication(x, flip_neg(y), r))
        
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

# Simple mod reduce method
def do_reduce(x,m,r):
    m3 = m
    m2 = m
    while larger_than(x, m2, r):
        m3 = m2
        m2 = m2+'0'

    diff = do_subtraction(x, m3, r)

    # If m > diff, diff is the remainder
    if larger_than(m, diff, r):
        return {
            'answer': diff
        }
    # Else, recurse
    else:
        return do_reduce(diff, m, r)

# Return `True` if `x > y`
def larger_than(x,y,r):

    # If only one is negative, the
    # positive value is larger
    if(x[0] == '-' and y[0] != '-'):
        return False
    elif(x[0] != '-' and y[0] == '-'):
        return True

    # if `-x > -y`, than `x < y`
    if(x[0] == '-' and y[0] == '-'):
        z = y
        y = x[1:]
        x = z[1:]

    # If there is a difference in length after removing the sign,
    # on of the two is larger
    if len(x) > len(y):
        return True
    elif len(x) < len(y):
        return False
    
    # Iterate over the values to find a larger or smaller value
    for i in range(len(x)):
        diff = do_subtraction(x[i], y[i], r)
        if diff[0] == '-':
            return False
        if diff != '0':
            return True

    # Both values are equal
    return False


# Strictly for positive integers and very slow
# TODO: do long division
def do_division(x,y,r):
    return

# Extended Euclidian division,
# still figuring out the extended part
def do_euclid(x,y,r):

    if y == '0':
        return {
            'answ-d': x,
            'answ-a': '0',
            'answ-b': '1'
        }

    # Get the remainder of x%y 
    remainder = do_reduce(x,y,r)['answer']

    # Recursive loop until `y` == `0`
    result = do_euclid(y, remainder, r)

    # a0 = do_division(result['answ-b'], result['answ-a'], r)

    # a0 = result['answ-a']

    # a1 = do_multiplication(a0, result['answ-a'], r)['answer']

    # a = do_subtraction(result['answ-b'], a1, r)

    # b = result['answ-a']

    return {
        'answ-d': result['answ-d'],
        'answ-a': '',
        'answ-b': ''
    }

# TODO
def do_inverse(x,m,r):

    return {
        'answer': ''
    }
    

