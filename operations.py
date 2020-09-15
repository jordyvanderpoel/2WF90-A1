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
            
        result = str((sum%r)) + result # Add the sum without carries to the current result-string

    if (c > 0):
        result = str(c) + result # Add final carry to result

    return result.lstrip('0')
    
def do_subtraction(x,y,r):
    # First handle negative numbers
    if(x[0] == '-' and y[0] == '-'):
        # x - y = -y - -x
        return do_subtraction(flip_neg(y), flip_neg(x), r)
    if(x[0] == '-'):
        # x - y = -(-x + b)
        return flip_neg(do_addition(flip_neg(x), y, r))
    if(y[0] == '-'):
        # x - y = x + -y
        return do_addition(x, flip_neg(y), r)
        
    # Handle b > a
    if(len(y) > len(x) or (len(x) == len(y) and int(y, r) > int(x, r))):
        # a - b = -(b - a)
        return flip_neg(do_subtraction(y, x, r))

    # Ensure equal length
    maxlength = max(len(x),len(y))
    x = x.zfill(maxlength)
    y = y.zfill(maxlength)
    
    c = 0
    result = ''
    
    for i in range(maxlength-1, -1, -1): # From end to front
        sum = int(x[i],r) - int(y[i],r) - c # Calculate subtraction of current digits
        
        c = (abs(sum//r) if sum < 0 else 0) # If we have a carry, get carry (floor division of sum over radix) else reset to 0
        #print(sum,(sum < 0),abs(sum),c)
            
        result = str((sum%r)) + result # Add the sum without carries to the current result-string

    return result.lstrip('0')