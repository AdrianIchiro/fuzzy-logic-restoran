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

df = pd.read_excel("restoran.xlsx")

hasil = []

for index, row in df.iterrows():
    pelayanan = row['Pelayanan']
    harga = row['harga']
    id_pelanggan = row['id Pelanggan']
    
    fuzzy_pelayanan = fuzzify_pelayanan(pelayanan)
    fuzzy_harga = fuzzify_harga(harga)
    hasil_inferensi = inferensi(fuzzy_pelayanan, fuzzy_harga)
    skor = defuzzifikasi(hasil_inferensi)

    hasil.append({
        'ID Restoran': id_pelanggan,
        'Pelayanan': pelayanan,
        'Harga': harga,
        'Skor Kelayakan': round(skor, 2)
    })

# ambil 5 yang terbaik

peringkat = sorted(hasil, key=lambda x: x['Skor Kelayakan'], reverse=True)[:5]
peringkat_df = pd.DataFrame(peringkat)
peringkat_df.to_excel("peringkat.xlsx", index=False)

print(peringkat_df)