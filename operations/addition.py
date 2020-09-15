def do_addition(x,y,r):
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

    return result