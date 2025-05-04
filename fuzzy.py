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


def inferensi(servis, harga):
    rules = []

    rules.append(('rendah', 'mahal', 'tidak_layak'))
    rules.append(('tinggi', 'murah', 'sangat_layak'))
    rules.append(('sedang', 'sedang', 'layak'))
    rules.append(('tinggi', 'sedang', 'layak'))
    rules.append(('sedang', 'murah', 'layak'))
    rules.append(('rendah', 'murah', 'layak'))
    rules.append(('tinggi', 'mahal', 'layak'))
    rules.append(('rendah', 'sedang', 'tidak_layak'))
    rules.append(('sedang', 'mahal', 'tidak_layak'))

    hasil = {'tidak_layak': 0.0, 'layak': 0.0, 'sangat_layak': 0.0}

    for rule in rules:
        s, h, o = rule
        nilai = min(servis[s], harga[h])
        hasil[o] = max(hasil[o], nilai)

    return hasil


def defuzzifikasi(output):
    bobot = {
        'tidak_layak': 25,
        'layak': 60,
        'sangat_layak': 90
    }
    atas = sum(output[label] * bobot[label] for label in output)
    bawah = sum(output[label] for label in output)
    return atas / bawah if bawah != 0 else 0

