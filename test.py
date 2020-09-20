import operations

print('----EUCLID-----')
print(operations.do_euclid('b22b5d17e57a41599185', '157f77a46f4c796bb774', 16))
print('should equal')
print({
    "answ-d": "19",
    "answ-a": "-74ba5fd6968445267",
    "answ-b": "3c769a8d705995e753"
})
print('')

print('----MOD INVERSE-----')
print(operations.do_inverse('c1b715933d2d1dcb0e23', '157f77a46f4c796bb774', 16))
print('should equal')
print({
    "answer": "8bb87443ec917fa3e87",
})
print('')

print('----MOD INVERSE-----')
print(operations.do_inverse('b22b5d17e57a41599185', '157f77a46f4c796bb774', 16))
print('should equal')
print({
    "answer": "ERROR - inverse does not exist",
})
print('')

print('mod-multiply:', operations.do_mod_multiply('93f76ca85dfdbf3f1790', 'c2a72e55e1956be991ca', '157f77a46f4c796bb774', 16)['answer'], '== dad2e63149941a790c4\n')