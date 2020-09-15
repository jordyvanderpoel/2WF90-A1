import asn1tools as asn
import json
import operations

### AfS software assignment 1 - example code ###

# set file names
base_location = './'
ops_loc = base_location + 'operations.asn'
exs_loc = base_location + 'my_pretty_exercises'
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
    
    if operation == 'add':
        params['answer'] = operations.do_addition(params['x'], params['y'], params['radix'])
    
    if operation == 'mod-add':
        ### TODO: Do modular addition ###
        params['answer'] = '1234'
    
    if operation == 'subtract':
        params['answer'] = operations.do_subtraction(params['x'], params['y'], params['radix'])

    if operation == 'mod-subtract':
        ### TODO: Do modular subtraction ###
        params['answer'] = '1234'
    
    if operation == 'multiply':
        ### TODO: Do multiplication ###
        params['answer'] = '66'
        params['count-mul'] = '1'
        params['count-add'] = '2'
    
    if operation == 'mod-multiply':
        ### TODO: Do modular multiplication ###
        params['answer'] = '1234'
    
    if operation == 'karatsuba':
        ### TODO: Do karatsuba algorithm ###
        params['answer'] = ''
        params['count-mul'] = 0
        params['count-add'] = 0
    
    if operation == 'reduce':
        ### TODO: Do modular reduction ###
        params['answer'] = ''
    
    if operation == 'euclid':
        ### TODO: Do euclidean algorithm ###
        params['answ-d'] = '1'
        params['answ-a'] = '0'
        params['answ-b'] = '0'
    
    if operation == 'inverse':
        ### TODO: Do modular inversion ###
        params['answer'] = ''

    # Save answer
    my_answers['exercises'].append({operation: params})

###### Creating an answers list file ######

# Save exercises with answers to file
my_file = open(ans_loc, 'wb+')                                       # write to binary file
my_file.write(json.dumps(my_answers).encode())                       # add encoded exercise list
my_file.close()

