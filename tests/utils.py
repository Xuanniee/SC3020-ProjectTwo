from explore import db


def assert_test(op):
    n = len(db.queryDirect(op['Query']))

    ar = op['Actual Rows']
    al = op['Actual Loops']
    
    print()
    print('Actual Rows:', ar)
    print('Actual Loops:', al)
    print('Actual R*L:', ar*al)
    print('Query Rows:', n)
    print()

    assert ar*al - n <= al
