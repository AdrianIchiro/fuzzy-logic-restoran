import pandas as pd

# fungsi segitiga

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)
    
def fuzzify_pelayanan(value):
    return {
        'rendah': triangular(value, 0, 25, 50),
        'sedang': triangular(value, 25, 50, 75),
        'tinggi': triangular(value, 50, 75, 100)
    }

def fuzzify_harga(value):
    return {
        'murah': triangular(value, 25000, 30000, 40000),
        'sedang': triangular(value, 35000, 42500, 50000),
        'mahal': triangular(value, 45000, 50000, 55000)
    }

