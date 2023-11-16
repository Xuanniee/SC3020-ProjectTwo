from explore import db


def assert_test(op):
    print(op['Query']) 
    n = len(db.queryDirect(op['Query']))
    
    ar = op['Actual Rows']
    al = op['Actual Loops']
    
    print()
    print('Actual Rows:', ar)
    print('Actual Loops:', al)
    print('Actual R*L:', ar*al)
    print('Query Rows:', n)
    print()

    assert abs(ar*al - n) <= al
