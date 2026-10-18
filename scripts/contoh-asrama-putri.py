#!/usr/bin/env python3
"""Membangkitkan proyek contoh RANCANG: Asrama Putri Poltek KP Sorong (renovasi 2015, CV. Awal Rahmat Konsultan).

Sumber: PDF gambar kerja (denah lantai 1 dan 2, rencana pondasi/sloof/balok lantai/ring balok/atap, potongan S.01 & S.04,
tipe kusen). Dua lantai, 37,00 × 8,13 m (as), teras depan 1,89 m, tempat jemur belakang 3,00 m (lantai 1) / balkon 1,25 m
(lantai 2), lantai 2 di +4,00, plafon +3,50 / +7,35, ring balk atas +7,75, atap limas seng multiroof rangka kayu.
Blok tangga/ruang tamu di ujung timur (sudah terbangun) digambar sederhana.

Pakai: python3 scripts/contoh-asrama-putri.py  → app/contoh/asrama-putri.json
"""
import json, os, datetime

# ---------- sumbu ----------
XS = [0, 3.5, 7.0, 11.5, 16.0, 20.5, 23.5, 28.0, 32.5, 37.0]          # as 1..10 (350·350·450·450·450·300·450·450·450)
YA, YB, YC, YD = 0.0, 2.0, 6.24, 8.13                                   # A belakang KM · B KM/kamar · C depan kamar · D kolom teras
Z2, Z_RB = 4.0, 7.75                                                    # lantai 2, puncak ring balk
TEBAL = 0.15
TB_BLOK = (28.0, 37.0, YD, 10.83)                                       # blok tangga/ruang tamu (x0, x1, y0, y1)

# kamar: (x0, x1, sisi KM 'barat'/'timur'); 9 kamar sesuai label denah asli — bay 20,5–23,5 (300) kamar kecil dengan KM 1,50 (dimensi 150|150)
# Sisi KM dari rangkaian ukuran denah asli: 150|200 · 200|150 · 200|250 ×3 · 150|150 · 250|200 ×3 (KM = bagian 200/150 berubin)
KAMAR = [(0, 3.5, 'timur'), (3.5, 7.0, 'barat'), (7.0, 11.5, 'barat'), (11.5, 16.0, 'barat'), (16.0, 20.5, 'barat'),
         (20.5, 23.5, 'barat'), (23.5, 28.0, 'timur'), (28.0, 32.5, 'timur'), (32.5, 37.0, 'timur')]
def batas_km(x0, x1, sisi):
    w = 1.5 if x1 - x0 <= 3.0 else 2.0
    return (x1 - w, x1) if sisi == 'timur' else (x0, x0 + w)

n = {}
def idb(aw):
    n[aw] = n.get(aw, 0) + 1
    return f'{aw}{n[aw]}'

E, GR, KUSEN = {}, {}, {}
def r2(v): return round(v + 1e-9, 3)
def P(x, y): return {'x': r2(x), 'y': r2(y)}
def tambah(aw, d, grup=None):
    i = idb(aw)
    if grup: d['grup'] = grup
    E[i] = d
    return i

def grup(nama):
    i = idb('G'); GR[i] = {'nama': nama}; return i

G_STRUKTUR = grup('Struktur')
G_L1 = grup('Lantai 1')
G_L2 = grup('Lantai 2')
G_ATAP = grup('Atap dan plafon')
G_BLOK = grup('Blok tangga (eksisting)')

# ---------- level ----------
tambah('M', {'jenis': 'level', 'nama': 'Lantai 1', 'z': 0})
tambah('M', {'jenis': 'level', 'nama': 'Lantai 2', 'z': Z2})
tambah('M', {'jenis': 'level', 'nama': 'Ring balk', 'z': Z_RB})

# ---------- pondasi & kolom ----------
TUL16 = {'n': 8, 'd': 16, 'ulir': False}
def footplat(x, y, tipe):
    if tipe == 'R1':
        return {'jenis': 'pondasi', 'tipe': 'footplat', 'nama': f'Foot plat R1', 'x': x, 'y': y, 'p': 1.7, 'l': 1.7, 'tebal': 0.3,
                'tulPlat': {'d': 16, 's': 0.15, 'ulir': False}, 'pedestal': {'b': 0.35, 'h': 0.35}, 'puncakPedestal': -0.45,
                'tul': {'n': 12, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.04, 'z0': -1.55}
    return {'jenis': 'pondasi', 'tipe': 'footplat', 'nama': f'Foot plat R2', 'x': x, 'y': y, 'p': 1.25, 'l': 1.25, 'tebal': 0.3,
            'tulPlat': {'d': 16, 's': 0.15, 'ulir': False}, 'pedestal': {'b': 0.3, 'h': 0.3}, 'puncakPedestal': -0.35,
            'tul': {'n': 8, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.04, 'z0': -1.6}

def kolom(x, y, b, z0, tinggi, nama, tul_n, tul_d):
    return {'jenis': 'kolom', 'tipe': 'struktur', 'nama': nama, 'x': x, 'y': y, 'b': b, 'h': b, 'tinggi': tinggi, 'z0': z0,
            'tul': {'n': tul_n, 'd': tul_d, 'ulir': False}, 'sengkang': {'d': 10 if b >= 0.35 else 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.03}

TITIK_R1 = [(x, y) for x in XS for y in (YA, YC)]
TITIK_R2 = [(x, YD) for x in XS] + [(3.5, YB), (7.0, YB)]
for x, y in TITIK_R1:
    tambah('F', footplat(x, y, 'R1'), G_STRUKTUR)
    tambah('C', kolom(x, y, 0.35, -0.45, Z2 + 0.45, 'Kolom R1 35/35', 12, 16), G_STRUKTUR)    # lantai 1 (dari puncak pedestal)
    tambah('C', kolom(x, y, 0.30, Z2, Z_RB - Z2, 'Kolom R2 30/30 lt.2', 8, 16), G_STRUKTUR)
for x, y in TITIK_R2:
    tambah('F', footplat(x, y, 'R2'), G_STRUKTUR)
    tambah('C', kolom(x, y, 0.30, -0.35, Z2 + 0.35, 'Kolom R2 30/30', 8, 16), G_STRUKTUR)
    tambah('C', kolom(x, y, 0.30, Z2, Z_RB - Z2, 'Kolom R2 30/30 lt.2', 8, 16), G_STRUKTUR)

# ---------- sloof, balok lantai, ring balk ----------
def balok(jenis, a, b, lebar, tinggi, z0, nama, tul_n=6, tul_d=16, sk=0.12):
    return {'jenis': jenis, 'nama': nama, 'awal': P(*a), 'akhir': P(*b), 'b': lebar, 'h': tinggi, 'z0': z0,
            'tul': {'n': tul_n, 'd': tul_d, 'ulir': False}, 'sengkang': {'d': 8, 's': sk}, 'fc': 18.7, 'selimut': 0.03}

def jalur_memanjang(y): return (0, y), (37.0, y)
# sloof: SL1 25/40 (baris A, C, semua as melintang A–C), SL2 20/30 (baris D teras, as melintang C–D, baris B di bay 350)
for y in (YA, YC):
    tambah('S', balok('slof', *jalur_memanjang(y), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), G_STRUKTUR)
tambah('S', balok('slof', *jalur_memanjang(YD), 0.20, 0.30, -0.35, 'Sloof SL2 20/30', 6, 16), G_STRUKTUR)
tambah('S', balok('slof', (3.5, YB), (7.0, YB), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), G_STRUKTUR)
for x in XS:
    tambah('S', balok('slof', (x, YA), (x, YC), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), G_STRUKTUR)
    tambah('S', balok('slof', (x, YC), (x, YD), 0.20, 0.30, -0.35, 'Sloof SL2 20/30', 6, 16), G_STRUKTUR)
# balok lantai 2 (puncak +4,00): BL1 30/60 baris A, C dan as melintang; BL2 20/30 baris B, D dan balkon belakang
for y in (YA, YC):
    tambah('R', balok('ringbalk', *jalur_memanjang(y), 0.30, 0.60, Z2 - 0.60, 'Balok lantai BL1 30/60', 8, 16), G_STRUKTUR)
for y in (YB, YD, -1.25):
    tambah('R', balok('ringbalk', *jalur_memanjang(y), 0.20, 0.30, Z2 - 0.30, 'Balok lantai BL2 20/30', 6, 16), G_STRUKTUR)
for x in XS:
    tambah('R', balok('ringbalk', (x, -1.25), (x, YD), 0.30, 0.60, Z2 - 0.60, 'Balok lantai BL1 30/60', 8, 16), G_STRUKTUR)
# ring balk (puncak +7,75): RB3 25/35 baris A, C, as melintang; RB1 20/30 baris D; RB2 15/20 baris B
for y in (YA, YC):
    tambah('R', balok('ringbalk', *jalur_memanjang(y), 0.25, 0.35, Z_RB - 0.35, 'Ring balk RB3 25/35'), G_STRUKTUR)
tambah('R', balok('ringbalk', *jalur_memanjang(YD), 0.20, 0.30, Z_RB - 0.30, 'Ring balk RB1 20/30'), G_STRUKTUR)
tambah('R', balok('ringbalk', *jalur_memanjang(YB), 0.15, 0.20, Z_RB - 0.20, 'Ring balk RB2 15/20', 4, 12), G_STRUKTUR)
for x in XS:
    tambah('R', balok('ringbalk', (x, YA), (x, YD), 0.25, 0.35, Z_RB - 0.35, 'Ring balk RB3 25/35'), G_STRUKTUR)

# ---------- kusen (tipe) ----------
def tipe_kusen(kode, untuk, daun, isi, kolom=2, baris=1, buka='kiri', boven=0.45, nama=None):
    i = idb('T')
    KUSEN[i] = {'kode': kode, 'untuk': untuk, 'nama': nama or ('Pintu ' if untuk == 'pintu' else 'Jendela ') + kode, 'profil': 0.06,
                'daun': daun, 'isi': isi, 'kolom': kolom, 'baris': baris, 'buka': buka, 'boven': {'tinggi': boven, 'kolom': 2, 'baris': 1} if boven else None, 'catatan': ''}
tipe_kusen('P1', 'pintu', 1, 'panil6', buka='kiri')                                # 80
tipe_kusen('P2', 'pintu', 2, 'panil6', buka='kiri', nama='Pintu P2 (60+90)')        # 60 + 90
tipe_kusen('P4', 'pintu', 1, 'panil6', buka='kiri', boven=0)                         # 70, KM
tipe_kusen('PJ2', 'pintu', 1, 'panil6', buka='kanan')                               # daun pintu 70 dari PJ2
tipe_kusen('PJ2', 'jendela', 1, 'kaca', kolom=1, baris=1, buka='tetap')             # kaca mati 75 dari PJ2
tipe_kusen('J1', 'jendela', 2, 'kaca', kolom=1, baris=1, buka='kupu')               # 2 × 75
tipe_kusen('J3', 'jendela', 3, 'kaca', kolom=1, baris=1, buka='kupu')               # 3 × 75
tipe_kusen('V1', 'jendela', 2, 'jalusi', kolom=1, baris=1, buka='tetap', boven=0)   # ventilasi 2 × 75 × 45
tipe_kusen('PJ1', 'pintu', 1, 'kaca', kolom=1, baris=1, buka='kiri', boven=0, nama='Pintu kaca PJ1')  # kaca tinggi 5,80 di blok tangga

def bukaan(dinding, tipe, kode, x_abs, lebar, tinggi, ambang=0, buka_ke=None):
    """x_abs = koordinat X mutlak tepi bukaan (untuk dinding memanjang sumbu X); jarak dihitung dari ujung awal dinding."""
    w = E[dinding]; jarak = x_abs - w['awal']['x'] if abs(w['akhir']['y'] - w['awal']['y']) < 1e-6 else x_abs
    assert 0 <= jarak and jarak + lebar <= abs(w['akhir']['x'] - w['awal']['x']) + 1e-6 or abs(w['akhir']['y'] - w['awal']['y']) > 1e-6, (dinding, x_abs, lebar)
    d = {'jenis': 'bukaan', 'tipe': tipe, 'kode': kode, 'dinding': dinding, 'jarak': r2(jarak), 'lebar': lebar, 'tinggi': tinggi, 'ambang': ambang}
    if buka_ke: d['bukaKe'] = buka_ke
    return tambah('B', d)

# ---------- dinding per lantai ----------
def dinding(a, b, z0, tinggi, g, tebal=TEBAL, nama=None, bahan=None):
    d = {'jenis': 'dinding', 'awal': P(*a), 'akhir': P(*b), 'tebal': tebal, 'tinggi': tinggi, 'z0': z0}
    if nama: d['nama'] = nama
    if bahan: d['bahan'] = bahan
    return tambah('D', d, g)

def lantai_tipikal(z0, g, h_balok_ac, h_balok_b, h_sekat, lantai_no):
    """Dinding + bukaan satu lantai. h_* = TINGGI dinding (bukan elevasi puncak): sampai bawah balok lantai (lt.1) atau bawah ring balk (lt.2)."""
    # dinding memanjang A (belakang KM/ceruk), B (KM–kamar), C (depan kamar), menerus 0–37
    for y, h, nama in ((YA, h_balok_ac, 'Dinding belakang'), (YB, h_balok_b, 'Dinding KM–kamar'), (YC, h_balok_ac, 'Dinding depan')):
        dinding((0, y), (37.0, y), z0, h, g, nama=f'{nama} lt.{lantai_no}')
    # dinding melintang di tiap as (A–C)
    for x in XS:
        dinding((x, YA), (x, YC), z0, h_balok_ac, g, nama=f'Dinding as x={x:g} lt.{lantai_no}')
    # sekat KM (A–B) dan bukaan tiap kamar
    for x0, x1, sisi in KAMAR:
        kx0, kx1 = batas_km(x0, x1, sisi)          # KM 2,00 lebar (1,50 di bay 300)
        cx0, cx1 = (x0, kx0) if sisi == 'timur' else (kx1, x1)                    # ceruk (sisa bay) di belakang kamar
        xsekat = kx0 if sisi == 'timur' else kx1
        dinding((xsekat, YA), (xsekat, YB), z0, h_sekat, g, tebal=0.10, nama=f'Sekat KM lt.{lantai_no}')
        # bukaan: cari dinding yang memuat x
        dB = dind_memuat(YB, x0, x1); dA = dind_memuat(YA, x0, x1); dC = dind_memuat(YC, x0, x1)
        tengah_km, tengah_ceruk = (kx0 + kx1) / 2, (cx0 + cx1) / 2
        bukaan(dB, 'pintu', 'P4', tengah_km - 0.35 - min(0.6, (kx1 - kx0) / 2 - 0.5) * (1 if sisi == 'timur' else -1), 0.70, 2.10)    # pintu KM, digeser dari tengah
        bukaan(dB, 'pintu', 'P4', tengah_ceruk - 0.35, 0.70, 2.10)                                        # pintu ceruk/gudang kecil
        bukaan(dA, 'jendela', 'V1', tengah_km - (0.80 if kx1 - kx0 >= 2.0 else 0.55), 1.60 if kx1 - kx0 >= 2.0 else 1.10, 0.45, 1.80)                                   # ventilasi KM
        if cx1 - cx0 >= 2.0: bukaan(dA, 'jendela', 'J1', tengah_ceruk - 0.80, 1.60, 1.20, 0.90)           # jendela ceruk ke belakang (ceruk 1,5 m tanpa jendela)
        # depan: PJ2 = pintu 70 + kaca mati 75 (pintu di dekat tengah), J1 di sisi lain
        # PJ2 (pintu 70 + kaca mati 75) di sisi KM, J1 (2 × 75) di sisi lain bila bay cukup lebar (≥ 4,5 m)
        if sisi == 'timur':
            xp = x1 - 0.40 - 1.45
            bukaan(dC, 'pintu', 'PJ2', xp + 0.75, 0.70, 2.10); bukaan(dC, 'jendela', 'PJ2', xp, 0.75, 2.10, 0)
            if x1 - x0 >= 4.5: bukaan(dC, 'jendela', 'J1', x0 + 0.50, 1.60, 1.20, 0.90)
        else:
            xp = x0 + 0.40
            bukaan(dC, 'pintu', 'PJ2', xp, 0.70, 2.10); bukaan(dC, 'jendela', 'PJ2', xp + 0.70, 0.75, 2.10, 0)
            if x1 - x0 >= 4.5: bukaan(dC, 'jendela', 'J1', x1 - 0.50 - 1.60, 1.60, 1.20, 0.90)

def dind_memuat(y, x0, x1):
    for i, d in E.items():
        if d['jenis'] == 'dinding' and abs(d['awal']['y'] - y) < 1e-6 and abs(d['akhir']['y'] - y) < 1e-6 and d.get('grup') == LANTAI_AKTIF \
                and d['awal']['x'] <= x0 + 1e-6 and d['akhir']['x'] >= x1 - 1e-6:
            return i
    raise SystemExit(f'dinding y={y} memuat {x0}–{x1} tidak ada')

# lantai 1: dinding dari 0 sampai bawah balok lantai (BL1 bawah 3,40; BL2 bawah 3,70; sekat sampai plat 3,88)
LANTAI_AKTIF = G_L1
lantai_tipikal(0, G_L1, Z2 - 0.60, Z2 - 0.30, Z2 - 0.12, 1)
# lantai 2: dari +4,00 sampai bawah ring balk (RB3 7,40; RB2 7,55; sekat 7,55)
LANTAI_AKTIF = G_L2
lantai_tipikal(Z2, G_L2, Z_RB - 0.35 - Z2, Z_RB - 0.20 - Z2, Z_RB - 0.20 - Z2, 2)

# ---------- lantai (volume) ----------
def lantai(nama, alas, z0, tinggi, jenis, penutup, g, lubang=None):
    d = {'jenis': 'volume', 'nama': nama, 'alas': [P(*q) for q in alas], 'z0': z0, 'tinggi': tinggi, 'lantai': jenis, 'penutupLantai': penutup}
    if lubang: d['lubang'] = [[P(*q) for q in c] for c in lubang]
    return tambah('V', d, g)

for i, (x0, x1, sisi) in enumerate(KAMAR, 1):
    kx0, kx1 = batas_km(x0, x1, sisi)
    lantai(f'Lantai Kamar {i}', [(x0, YB), (x1, YB), (x1, YC), (x0, YC)], -0.10, 0.10, 'ruang', 'k40', G_L1)
    lantai(f'Lantai KM {i}', [(kx0, YA), (kx1, YA), (kx1, YB), (kx0, YB)], -0.12, 0.10, 'km', 'k20', G_L1)
    cx0, cx1 = (x0, kx0) if sisi == 'timur' else (kx1, x1)
    lantai(f'Lantai ceruk {i}', [(cx0, YA), (cx1, YA), (cx1, YB), (cx0, YB)], -0.10, 0.10, 'ruang', 'k40', G_L1)
lantai('Lantai teras depan', [(-0.2, YC), (37.2, YC), (37.2, YD + 0.3), (-0.2, YD + 0.3)], -0.12, 0.10, 'teras', 'k30', G_L1)
lantai('Tempat jemur belakang', [(-2.0, -3.0), (37.2, -3.0), (37.2, YA), (-2.0, YA)], -0.15, 0.10, 'teras', 'plester', G_L1)

# plat lantai 2: L (badan + blok tangga), void tangga di blok
bx0, bx1, by0, by1 = TB_BLOK
V_TANGGA = [(29.2, 8.6), (35.0, 8.6), (35.0, 9.8), (29.2, 9.8)]
tambah('W', {'jenis': 'plat', 'nama': 'Plat lantai 2 (PL1, 12 cm K-250)', 'z0': Z2 - 0.12, 'tebal': 0.12, 'fc': 20.75, 'tul': {'d': 10, 's': 0.12},
             'alas': [P(0, -1.25), P(37.0, -1.25), P(37.0, by1), P(bx0, by1), P(bx0, YD + 0.15), P(0, YD + 0.15)],
             'lubang': [[P(*q) for q in V_TANGGA]]}, G_STRUKTUR)
# penutup lantai 2 (keramik tipis) per ruang: satu volume tipis di atas plat
lantai('Keramik lantai 2', [(0, -1.25), (37.0, -1.25), (37.0, YD + 0.15), (0, YD + 0.15)], Z2, 0.02, 'ruang', 'k40', G_L2)
# railing balkon depan dan belakang lantai 2: dinding rendah 1,00 m tebal 0,10
dinding((-0.0, YD + 0.1), (bx0, YD + 0.1), Z2, 1.0, G_L2, tebal=0.10, nama='Railing balkon depan lt.2')
dinding((0, -1.2), (37.0, -1.2), Z2, 1.0, G_L2, tebal=0.10, nama='Railing balkon belakang lt.2')
dinding((0, -1.2), (0, YA), Z2, 1.0, G_L2, tebal=0.10, nama='Railing balkon belakang barat')
dinding((37.0, -1.2), (37.0, YA), Z2, 1.0, G_L2, tebal=0.10, nama='Railing balkon belakang timur')
dinding((0, YC), (0, YD + 0.1), Z2, 1.0, G_L2, tebal=0.10, nama='Railing balkon depan barat')

# ---------- plafon ----------
for z, g, lt in ((3.50, G_ATAP, 1), (7.35, G_ATAP, 2)):
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon kamar lt.{lt}', 'alas': [P(0, YA), P(37.0, YA), P(37.0, YC), P(0, YC)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g)
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon teras lt.{lt}', 'alas': [P(0, YC), P(37.0, YC), P(37.0, YD), P(0, YD)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g)

# ---------- atap ----------
KUDA = {'kaki': [0.05, 0.10], 'tarik': [0.05, 0.10], 'makelar': [0.05, 0.10], 'tiang': [0.05, 0.10], 'sokong': [0.025, 0.10], 'skor': [0.025, 0.10],
        'gording': [0.05, 0.10], 'bubungan': [0.05, 0.10], 'klos': [0.05, 0.05], 'lisMundur': 0.20, 'jarakGording': 0.8}
tambah('A', {'jenis': 'atap', 'nama': 'Atap limas utama (kuda-kuda K1/K3 kayu besi 5/10)', 'bentuk': 'limas', 'x0': 0, 'y0': YA, 'x1': 37.0, 'y1': YD, 'z0': Z_RB, 'kemiringan': 35, 'overstek': 1.2,
             'arah': 'x', 'penutup': 'spandek', 'rangka': 'kayu', 'jarakKuda': 3.3, 'tebal': 0.1, 'lisplang': 'papan', 'kuda': KUDA}, G_ATAP)

# ---------- blok tangga / ruang tamu (eksisting, disederhanakan) ----------
dinding((bx0, YD), (bx0, by1), 0, Z_RB + 0.6, G_BLOK, nama='Dinding barat blok tangga')
dinding((bx1, YD), (bx1, by1), 0, Z_RB + 0.6, G_BLOK, nama='Dinding timur blok tangga')
dU = dinding((bx0, by1), (bx1, by1), 0, Z_RB + 0.6, G_BLOK, nama='Dinding depan blok tangga')
bukaan(dU, 'pintu', 'P2', bx0 + 5.5, 1.50, 2.10)                # pintu masuk 60+90
bukaan(dU, 'jendela', 'PJ1', bx0 + 0.9, 1.10, 5.80, 0.10)       # kaca tinggi 5,80 (bukaan tinggi)
bukaan(dU, 'jendela', 'J3', bx0 + 2.6, 2.35, 1.20, 0.90)
bukaan(dU, 'jendela', 'J3', bx0 + 2.6, 2.35, 1.20, Z2 + 0.90)
lantai('Lantai ruang tamu', [(bx0, YD), (bx1, YD), (bx1, by1), (bx0, by1)], -0.10, 0.10, 'ruang', 'k40', G_BLOK)
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga ke lantai 2', 'awal': P(29.3, 8.65), 'arah': 0, 'lebar': 1.1, 'tinggi': Z2, 'jumlahAnak': 22, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, G_BLOK)
for x in (bx0, (bx0 + bx1) / 2, bx1):
    tambah('C', kolom(x, by1, 0.30, -0.35, Z_RB + 0.6 + 0.35, 'Kolom R2 30/30 blok', 8, 16), G_BLOK)
tambah('A', {'jenis': 'atap', 'nama': 'Atap blok tangga', 'bentuk': 'limas', 'x0': bx0, 'y0': YD, 'x1': bx1, 'y1': by1, 'z0': Z_RB + 0.6, 'kemiringan': 40, 'overstek': 0.8,
             'arah': 'x', 'penutup': 'spandek', 'rangka': 'kayu', 'jarakKuda': 3.0, 'tebal': 0.1, 'lisplang': 'papan'}, G_BLOK)

# ---------- simbol perabot & sanitair di denah ----------
def simbol(nama, x, y, rot=0):
    tambah('L', {'jenis': 'gambar2d', 'bentuk': 'simbol', 'simbol': nama, 'lembar': 'denah', 'tempel': 'gambar', 'titik': [{'x': r2(x), 'y': r2(y), 'z': 0}], 'rotasi': rot})
for x0, x1, sisi in KAMAR:
    kx0, kx1 = batas_km(x0, x1, sisi)
    simbol('kasur1', x0 + 0.75 if sisi == 'timur' else x1 - 0.75, 5.1, 0)       # tempat tidur di sudut depan, jauh dari KM
    simbol('kasur1', x1 - 0.75 if sisi == 'timur' else x0 + 0.75, 5.1, 0)
    simbol('lemari', (x0 + x1) / 2, 2.45, 0)
    simbol('klosetJongkok', kx0 + 0.5, 0.6, 0)
    if kx1 - kx0 >= 2.0: simbol('bakMandi', kx1 - 0.45, 0.5, 0)
tambah('L', {'jenis': 'gambar2d', 'bentuk': 'legenda', 'lembar': 'denah', 'tempel': 'kertas', 'titik': [{'x': 22, 'y': 22}]})

# ---------- garis potong & anotasi ----------
tambah('X', {'jenis': 'potong', 'nama': 'A', 'awal': P(-3, 4.0), 'akhir': P(40, 4.0), 'pandang': -1})
tambah('X', {'jenis': 'potong', 'nama': 'B', 'awal': P(9.25, -4.5), 'akhir': P(9.25, 11.5), 'pandang': 1})
for i, (x0, x1, sisi) in enumerate(KAMAR, 1):
    tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'Kamar Tidur', 'titik': {'x': (x0 + x1) / 2, 'y': 4.4, 'z': 0}, 'pada': 'denah'})
    kx0, kx1 = batas_km(x0, x1, sisi)
    tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'KM/WC', 'titik': {'x': (kx0 + kx1) / 2, 'y': 1.0, 'z': 0}, 'pada': 'denah'})
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'Teras', 'titik': {'x': 18.5, 'y': 7.2, 'z': 0}, 'pada': 'denah'})
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'Tempat jemur', 'titik': {'x': 18.5, 'y': -1.6, 'z': 0}, 'pada': 'denah'})
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'Ruang tamu', 'titik': {'x': 36.0, 'y': 10.2, 'z': 0}, 'pada': 'denah'})

proyek = {'format': 'rancang-proyek', 'versi': 1, 'aplikasi': 'RANCANG', 'disimpan': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'setel': {'nama': 'Asrama Putri Poltek KP Sorong', 'tebalDinding': 0.15, 'tinggiDinding': 3.4, 'kemiringanAtap': 35, 'overstekAtap': 1.2},
          'elemen': E, 'grup': GR, 'komponen': {}, 'kusen': KUSEN}
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'app', 'contoh'), exist_ok=True)
out = os.path.join(os.path.dirname(__file__), '..', 'app', 'contoh', 'asrama-putri.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(proyek, f, ensure_ascii=False, separators=(',', ':'))
print(out, len(E), 'elemen', len(GR), 'grup', len(KUSEN), 'tipe kusen')
