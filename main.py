import asn1tools as asn
import json
import operations

### AfS software assignment 1 - example code ###

# set file names
base_location = './'
ops_loc = base_location + 'operations.asn'
exs_loc = base_location + 'test_exercises_students_pretty_answers'
ans_loc = base_location + 'my_answers'

###### Creating an exercise list file ######

# How to create an exercise JSON file containing one addition exercise
#exercises = {'exercises' : []}                                     # initialize empty exercise list
#ex = {'add' : {'radix' : 10, 'x' : '3', 'y' : '4', 'answer' : ''}} # create add exercise
#exercises['exercises'].append(ex)                                  # add exercise to list

# Encode exercise list and print to file
#my_file = open(exs_loc, 'wb+')                                     # write to binary file
#my_file.write(json.dumps(exercises).encode())                      # add encoded exercise list
#my_file.close()

###### Using an exercise list file ######

# Compile specification
spec = asn.compile_files(ops_loc, codec = "jer")

# Read exercise list 
exercise_file = open(exs_loc, 'rb')                                # open binary file
file_data = exercise_file.read()                                   # read byte array
my_exercises = spec.decode('Exercises', file_data)                 # decode after specification
exercise_file.close()                                              

# Create answer JSON
my_answers = {'exercises': []}

# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    operation = exercise[0]                                        # get operation type
    params = exercise[1]                                           # get parameters

    original = params.copy()
    
    if operation == 'add':
        params['answer'] = operations.do_addition(params['x'], params['y'], params['radix'])
    
    if operation == 'mod-add':
        params['answer'] = operations.do_mod_addition(params['x'], params['y'], params['m'], params['radix'])
    
    if operation == 'subtract':
        params['answer'] = operations.do_subtraction(params['x'], params['y'], params['radix'])

    if operation == 'mod-subtract':
        params['answer'] = operations.do_mod_subtraction(params['x'], params['y'], params['m'], params['radix'])
    
    if operation == 'multiply':
        result = operations.do_multiplication(params['x'], params['y'], params['radix'])
        params['answer'] = result['answer']
        params['count-mul'] = result['count-mul']
        params['count-add'] = result['count-add']
    
    if operation == 'mod-multiply':
        result = operations.do_mod_multiply(params['x'], params['y'], params['m'], params['radix'])
        params['answer'] = result['answer']
    
    if operation == 'karatsuba':
        result = operations.do_karatsuba(params['x'], params['y'], params['radix'])
        params['answer'] = result['answer']
        params['count-mul'] = result['count-mul']
        params['count-add'] = result['count-add']
    
    if operation == 'reduce':
        result = operations.do_reduce(params['x'], params['m'], params['radix'])
        params['answer'] = result['answer']
    
    if operation == 'euclid':
        result = operations.do_euclid(params['x'], params['y'], params['radix'])
        params['answ-d'] = result['answ-d']
        params['answ-a'] = result['answ-a']
        params['answ-b'] = result['answ-b']
    
    if operation == 'inverse':
        result = operations.do_inverse(params['x'], params['m'], params['radix'])
        params['answer'] = result['answer']

    if original != params:
        print('{} not equal: \n\n {} \n\n {} \n\n'.format(operation, original, params))

    # Save answer
    my_answers['exercises'].append({operation: params})

###### Creating an answers list file ######

# Save exercises with answers to file
my_file = open(ans_loc, 'wb+')                                       # write to binary file
my_file.write(json.dumps(my_answers).encode())                       # add encoded exercise list
my_file.close()

