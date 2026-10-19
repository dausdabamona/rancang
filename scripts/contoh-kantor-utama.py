#!/usr/bin/env python3
"""Membangkitkan proyek contoh RANCANG: Gedung Kantor Utama Poltek KP Sorong (pembangunan 2015, CV. Wahana Multikarya Consultan).

Sumber: PDF gambar kerja 55 lembar (site plan, kusen, denah lt.1–2, pondasi, kolom, sloof, balok, atap, plafon, potongan S.01/S.02,
tampak, perspektif). Gedung dua lantai 30,00 × 12,00 m, simetris, hall tengah 2,00 m diapit dua baris ruang 5,00 m (kisi kolom 3,00 m),
teras masuk mobil di depan (selatan), tangga dan balkon di belakang (utara), dua pintu samping di ujung hall.
Lantai 1 ±0,00 · lantai 2 +4,00 · plafon +3,25 / +7,40 · ring balk +8,00 · nok +12,80 (atap perisai seng galvalum, rangka kayu).

Pakai: python3 scripts/contoh-kantor-utama.py  → app/contoh/kantor-utama.json
"""
import json, os, datetime

L, D = 30.0, 12.0                    # panjang (x) dan lebar (y) bangunan, as ke as kolom luar
Z2, Z_RB = 4.0, 8.0                  # lantai 2, puncak ring balk (tepi atap)
TEBAL = 0.15
XS = [3.0 * i for i in range(11)]    # as kolom 0 … 30
YS = [0.0, 5.0, 7.0, 12.0]           # baris kolom: depan · tepi hall · tepi hall · belakang
XC0, XC1 = 12.0, 18.0                # lebar bagian tengah (teras/tangga)
YJ, YT = -1.5, -2.25                 # bagian tengah depan: sudut kaca JP sampai y = −1,50, muka depan (pintu P2) di y = −2,25

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

for nama, z in (('Lantai 1', 0), ('Lantai 2', Z2), ('Ring balk', Z_RB)):
    tambah('M', {'jenis': 'level', 'nama': nama, 'z': z})

# ---------- komponen struktur ----------
def footplat(x, y, p=1.6, nama='Foot plat K1 160×160'):
    return {'jenis': 'pondasi', 'tipe': 'footplat', 'nama': nama, 'x': r2(x), 'y': r2(y), 'p': p, 'l': p, 'tebal': 0.3,
            'tulPlat': {'d': 16, 's': 0.15, 'ulir': False}, 'pedestal': {'b': 0.35, 'h': 0.35}, 'puncakPedestal': -1.14,
            'tul': {'n': 12, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.04, 'z0': -2.67}

def kolom(x, y, b, h, z0, tinggi, nama, tul_n=12):
    return {'jenis': 'kolom', 'tipe': 'struktur', 'nama': nama, 'x': r2(x), 'y': r2(y), 'b': b, 'h': h, 'tinggi': r2(tinggi), 'z0': r2(z0),
            'tul': {'n': tul_n, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.03}

def balok(jenis, a, b, lebar, tinggi, z0, nama, tul_n=8, tul_d=16, sk=0.15):
    return {'jenis': jenis, 'nama': nama, 'awal': P(*a), 'akhir': P(*b), 'b': lebar, 'h': tinggi, 'z0': r2(z0),
            'tul': {'n': tul_n, 'd': tul_d, 'ulir': False}, 'sengkang': {'d': 8, 's': sk}, 'fc': 18.7, 'selimut': 0.03}

def tiang(x, y, g, p=1.6, puncak=Z_RB):
    """Satu as kolom lengkap: foot plat, kolom K1 35/35 sampai lantai 2, kolom K2 25/35 sampai ring balk."""
    tambah('F', footplat(x, y, p, 'Foot plat K1 160×160' if p >= 1.6 else 'Foot plat 120×120'), g)
    tambah('C', kolom(x, y, 0.35, 0.35, -1.14, Z2 + 1.14, 'Kolom K1 35/35'), g)
    tambah('C', kolom(x, y, 0.25, 0.35, Z2, puncak - Z2, 'Kolom K2 25/35 lt.2', 8), g)

def tiang_teras(x, y, g, tinggi=Z2 - 0.12):
    tambah('F', footplat(x, y, 1.2, 'Foot plat 120×120'), g)
    tambah('C', kolom(x, y, 0.35, 0.35, -1.14, tinggi + 1.14, 'Kolom teras 35/35'), g)

# ---------- kusen (lembar Tipe Kusen & Rencana Penempatan Kusen lt.I/II) ----------
def tipe_kusen(kode, untuk, daun, isi, kolom=1, baris=1, buka='kiri', boven=0, boven_kolom=1, nama=None, profil=0.05):
    i = idb('T')
    KUSEN[i] = {'kode': kode, 'untuk': untuk, 'nama': nama or ('Pintu ' if untuk == 'pintu' else 'Jendela ') + kode, 'profil': profil,
                'daun': daun, 'isi': isi, 'kolom': kolom, 'baris': baris, 'buka': buka,
                'boven': {'tinggi': boven, 'kolom': boven_kolom, 'baris': 1} if boven else None, 'catatan': 'Kusen kayu besi 5/10, kaca riben 5 mm'}
tipe_kusen('P1', 'pintu', 1, 'kaca', baris=2, boven=0.60, nama='Pintu P1: 1 daun kaca riben 80/210 + ventilasi kaca di atas pintu')
tipe_kusen('P2', 'pintu', 2, 'kaca', baris=2, buka='kiri', nama='Pintu P2: 2 daun kaca riben 2 × 80/210')
tipe_kusen('PK', 'pintu', 1, 'jalusi', boven=0.60, nama='Pintu PK kamar mandi: panil kayu besi 60/210 + ventilasi kaca di atas')
tipe_kusen('J1', 'jendela', 3, 'kaca', buka='kupu', boven=0.60, boven_kolom=1, nama='Jendela J1: 3 daun kaca riben 70/145 + boven kaca mati 3 kotak')
tipe_kusen('JK', 'jendela', 1, 'kaca', kolom=2, baris=5, buka='tetap', nama='Jendela JK: kaca mati 2 × 5 kotak (48/277)')
tipe_kusen('PL', 'jendela', 1, 'kaca', kolom=2, baris=5, buka='tetap', nama='Jendela PL: kaca mati 2 × 5 kotak (77/282), ujung hall lt.2')
tipe_kusen('JP', 'jendela', 1, 'kaca', kolom=1, baris=5, buka='tetap', nama='Jendela JP: kaca sudut riben setinggi 6,32 m (kotak 50 + rangka 12)')
tipe_kusen('V1', 'jendela', 1, 'jalusi', buka='tetap', nama='Ventilasi KM/WC V1: jalusi papan kayu besi 80/45')
tipe_kusen('VP', 'jendela', 1, 'kaca', kolom=4, buka='tetap', nama='Ventilasi kaca di atas dinding partisi (lebar dinding 3 m)')
tipe_kusen('VP5', 'jendela', 1, 'kaca', kolom=7, buka='tetap', nama='Ventilasi kaca di atas dinding partisi (lebar dinding 5 m)')
tipe_kusen('VPD', 'jendela', 1, 'kaca', kolom=3, buka='tetap', nama='Ventilasi kaca di atas dinding partisi (daerah pintu double)')
tipe_kusen('VT', 'jendela', 1, 'kaca', kolom=3, buka='tetap', nama='Ventilasi kaca di atas tangga')
tipe_kusen('LK', 'jendela', 2, 'kaca', buka='tetap', nama='Loket kaca (R. Bagian Administrasi Umum)')

# ukuran kusen (lebar × tinggi termasuk rangka 5 cm)
U = {'P1': (0.90, 2.15 + 0.60), 'P2': (1.70, 2.15), 'PK': (0.70, 2.15 + 0.60), 'J1': (2.30, 1.55 + 0.60), 'JK': (1.11, 2.87), 'PL': (1.69, 2.92),
     'V1': (0.90, 0.55), 'LK': (1.00, 1.00)}

def dinding(a, b, z0, tinggi, g, tebal=TEBAL, nama=None):
    d = {'jenis': 'dinding', 'awal': P(*a), 'akhir': P(*b), 'tebal': tebal, 'tinggi': r2(tinggi), 'z0': r2(z0)}
    if nama: d['nama'] = nama
    return tambah('D', d, g)

def bukaan(wall, tipe, kode, pos, lebar, tinggi, ambang=0):
    """pos = jarak tepi bukaan dari ujung awal dinding."""
    w = E[wall]
    panjang = abs(w['akhir']['x'] - w['awal']['x']) + abs(w['akhir']['y'] - w['awal']['y'])
    assert -1e-6 <= pos and pos + lebar <= panjang + 1e-6, (wall, pos, lebar, panjang)
    return tambah('B', {'jenis': 'bukaan', 'tipe': tipe, 'kode': kode, 'dinding': wall, 'jarak': r2(max(0, pos)), 'lebar': lebar, 'tinggi': tinggi, 'ambang': ambang})

def lantai(nama, alas, z0, tinggi, jenis, penutup, g, lubang=None):
    d = {'jenis': 'volume', 'nama': nama, 'alas': [P(*q) for q in alas], 'z0': r2(z0), 'tinggi': tinggi, 'lantai': jenis, 'penutupLantai': penutup}
    if lubang: d['lubang'] = [[P(*q) for q in c] for c in lubang]
    return tambah('V', d, g)

def plat(nama, alas, z0, tebal, g, lubang=None, fc=20.75):
    d = {'jenis': 'plat', 'nama': nama, 'z0': r2(z0), 'tebal': tebal, 'fc': fc, 'tul': {'d': 10, 's': 0.12}, 'alas': [P(*q) for q in alas]}
    if lubang: d['lubang'] = [[P(*q) for q in c] for c in lubang]
    return tambah('W', d, g)

def simbol(nama, x, y, rot=0):
    tambah('L', {'jenis': 'gambar2d', 'bentuk': 'simbol', 'simbol': nama, 'lembar': 'denah', 'tempel': 'gambar', 'titik': [{'x': r2(x), 'y': r2(y), 'z': 0}], 'rotasi': rot})

def teks(t, x, y, z=0, pada='denah'):
    tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': t, 'titik': {'x': r2(x), 'y': r2(y), 'z': z}, 'pada': pada})

def kotak(x0, x1, y0, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

g_str = grup('Struktur'); g_l1 = grup('Lantai 1'); g_l2 = grup('Lantai 2'); g_atap = grup('Atap & plafon')
g_ent = grup('Entrance & kanopi'); g_tg = grup('Tangga'); g_tapak = grup('Tapak')

# ---------- kolom dan pondasi ----------
for x in XS:
    for y in YS: tiang(x, y, g_str)
for x in (12.75, 17.25): tiang(x, YT, g_ent, p=1.2)                                                          # sudut muka depan tengah
for x in (12.75, 17.25): tiang_teras(x, -7.2, g_ent)                                                        # teras mobil
for x, y in ((-2.75, 5.0), (-2.75, 7.0), (L + 2.75, 5.0), (L + 2.75, 7.0)): tiang_teras(x, y, g_ent)       # pintu samping
for x in (XC0, XC1): tiang_teras(x, D + 1.25, g_str, tinggi=Z2 - 0.12)                                       # balkon belakang (selasar lt.1)

# ---------- sloof, balok lantai, ring balk ----------
for y in YS:
    tambah('S', balok('slof', (0, y), (L, y), 0.25, 0.40, -0.40, 'Sloof SL1 25/40'), g_str)
    tambah('R', balok('ringbalk', (0, y), (L, y), 0.25, 0.50, Z2 - 0.50, 'Balok lantai BL1 25/50'), g_str)
    tambah('R', balok('ringbalk', (0, y), (L, y), 0.20, 0.30, Z_RB - 0.30, 'Ring balk RB1 20/30', 6, 16), g_str)
for x in XS:
    tambah('S', balok('slof', (x, 0), (x, D), 0.25, 0.40, -0.40, 'Sloof SL1 25/40'), g_str)
    tambah('R', balok('ringbalk', (x, 0), (x, D), 0.25, 0.50, Z2 - 0.50, 'Balok lantai BL1 25/50'), g_str)
    tambah('R', balok('ringbalk', (x, 0), (x, D), 0.20, 0.30, Z_RB - 0.30, 'Ring balk RB1 20/30', 6, 16), g_str)
for x in (12.75, 17.25):
    tambah('S', balok('slof', (x, -7.2), (x, 0), 0.15, 0.20, -0.30, 'Sloof SL2 15/20', 4, 12), g_ent)
    tambah('R', balok('ringbalk', (x, -7.2), (x, 0), 0.25, 0.50, Z2 - 0.50, 'Balok lantai teras 25/50'), g_ent)
for y in (-2.25, -7.2): tambah('R', balok('ringbalk', (12.75, y), (17.25, y), 0.25, 0.50, Z2 - 0.50, 'Balok lantai teras 25/50'), g_ent)

# ---------- dinding & bukaan per lantai ----------
h1, h2 = Z2 - 0.50, Z_RB - 0.30 - Z2          # tinggi dinding sampai bawah balok lantai / ring balk
AMB_J = 0.95                                   # ambang jendela J1 (puncak boven +3,10 di bawah plafon)
VENT = {1: 2.80, 2: 2.90}                      # ambang ventilasi kaca di atas partisi (tinggi 45 cm, rapat ke plafon)

def B(wall, tipe, kode, pos, lebar=None, tinggi=None, ambang=0):
    lb, tg = U.get(kode, (lebar, tinggi))
    return bukaan(wall, tipe, kode, pos, lebar or lb, tinggi or tg, ambang)

def j1_per_bay(wall, x_awal, bays):
    for bx in bays: B(wall, 'jendela', 'J1', bx + 0.35 - x_awal, ambang=AMB_J)

def hall(no, z0, g, h, y, rentang, pintu):
    """dinding tepi hall dengan pintu (x tepi kiri, kode) dan ventilasi kaca di atas partisi per bay 3 m."""
    for a, b in rentang:
        w = dinding((a, y), (b, y), z0, h, g, tebal=0.12, nama=f'Dinding partisi hall lt.{no}')
        for xp, kode in pintu:
            if a <= xp and xp + U[kode][0] <= b + 1e-6: B(w, 'pintu', kode, xp - a)
        for bx in [x for x in XS[:-1] if a <= x and x + 3.0 <= b + 1e-6]:
            dobel = any(k == 'P2' and bx <= xp < bx + 3.0 for xp, k in pintu)
            B(w, 'jendela', 'VPD' if dobel else 'VP', bx + 0.2 - a, 2.60, 0.45, VENT[no])

def partisi(no, z0, g, h, a, b, pintu=None, vent=True):
    w = dinding(a, b, z0, h, g, tebal=0.12, nama=f'Dinding partisi lt.{no}')
    L_ = abs(b[0] - a[0]) + abs(b[1] - a[1])
    if pintu: B(w, 'pintu', pintu[1], pintu[0])
    if vent and L_ >= 4.9: B(w, 'jendela', 'VP5', 0.2, 4.59, 0.45, VENT[no])
    return w

bays_depan = [x for x in XS[:-1] if x < 12 or x >= 18]
for no, z0, g, h in ((1, 0.0, g_l1, h1), (2, Z2, g_l2, h2)):
    # fasad depan dan belakang: J1 tiap bay, V1 di dua toilet belakang
    for a, b in ((0.0, 12.0), (18.0, 30.0)):
        w = dinding((a, 0.0), (b, 0.0), z0, h, g, nama=f'Dinding depan lt.{no}')
        j1_per_bay(w, a, [x for x in bays_depan if a <= x < b])
        w = dinding((a, D), (b, D), z0, h, g, nama=f'Dinding belakang lt.{no}')
        j1_per_bay(w, a, [x for x in bays_depan if a <= x < b and x < 27.0])
        if a == 18.0:
            for xv in (27.3, 28.8): B(w, 'jendela', 'V1', xv - a, ambang=2.20)
    # samping: polos, ujung hall lt.1 pintu P2, lt.2 kaca PL; loket di dinding barat R. Adm. Umum
    for x, nm in ((0.0, 'barat'), (L, 'timur')):
        ws = dinding((x, 0.0), (x, 5.0), z0, h, g, nama=f'Dinding samping {nm} lt.{no}')
        if no == 1 and x == 0.0:
            B(ws, 'jendela', 'LK', 0.85, ambang=0.95); B(ws, 'jendela', 'LK', 3.30, ambang=0.95)
        dinding((x, 7.0), (x, D), z0, h, g, nama=f'Dinding samping {nm} lt.{no}')
        we = dinding((x, 5.0), (x, 7.0), z0, h, g, nama=f'Dinding ujung hall {nm} lt.{no}')
        if no == 1: B(we, 'pintu', 'P2', 0.15)
        else: B(we, 'jendela', 'PL', 0.155, ambang=0.25)

# lantai 1 — partisi hall (Rencana Penempatan Kusen Lantai I)
hall(1, 0.0, g_l1, h1, 7.0, ((0.0, 12.0), (18.0, 27.0)), [(4.2, 'P2'), (10.15, 'P2'), (18.2, 'P2'), (24.15, 'P1')])
hall(1, 0.0, g_l1, h1, 5.0, ((0.0, 12.0), (18.0, 30.0)), [(4.2, 'P2'), (10.15, 'P2'), (18.2, 'P2'), (27.1, 'P1')])
dinding((13.31, 5.0), (16.69, 5.0), 0.0, h1, g_l1, tebal=0.12, nama='Dinding pendek ruang tunggu lt.1')
for x in (6, 12, 18, 27): partisi(1, 0.0, g_l1, h1, (x, 0), (x, 5))
for x in (6, 12, 18, 24): partisi(1, 0.0, g_l1, h1, (x, 7), (x, D))
# toilet lt.1 (27–30 × 7–12): PK dari hall, wastafel, PK ke WC
dinding((27, 7), (27, D), 0.0, h1, g_l1, tebal=0.12, nama='Dinding toilet lt.1')
wt = dinding((27, 7), (30, 7), 0.0, h1, g_l1, tebal=0.12, nama='Dinding toilet sisi hall lt.1')
for xp in (27.4, 28.9): B(wt, 'pintu', 'PK', xp - 27)
dinding((28.5, 7), (28.5, D), 0.0, h1, g_l1, tebal=0.10, nama='Sekat toilet pria/wanita lt.1')
wc = dinding((27, 10.0), (30, 10.0), 0.0, h1, g_l1, tebal=0.10, nama='Dinding WC lt.1')
for xp in (27.4, 28.9): B(wc, 'pintu', 'PK', xp - 27)
# inti tangga lt.1: dinding samping, belakang JK–P2–JK, gudang di bawah bordes (pintu PK)
dinding((13.31, 7.0), (13.31, D), 0, h1, g_l1, tebal=0.12, nama='Dinding inti tangga barat lt.1')
dinding((16.69, 7.0), (16.69, D), 0, h1, g_l1, tebal=0.12, nama='Dinding inti tangga timur lt.1')
wb = dinding((12.0, D), (18.0, D), 0, h1, g_l1, nama='Dinding belakang inti tangga lt.1')
B(wb, 'jendela', 'JK', 0.2, ambang=0.30); B(wb, 'pintu', 'P2', 2.15); B(wb, 'jendela', 'JK', 4.69, ambang=0.30)
wg = dinding((13.31, 10.0), (16.69, 10.0), 0, 1.80, g_l1, tebal=0.12, nama='Dinding gudang bawah bordes')
B(wg, 'pintu', 'PK', 2.40, 0.70, 1.70)
# bagian tengah depan: muka di y = −2,25, sudut kaca JP setinggi dua lantai, pintu P2
for no, z0, g, h in ((1, 0.0, g_l1, h1), (2, Z2, g_l2, h2)):
    amb = 0.30 if no == 1 else 0.0
    tj = 3.20 if no == 1 else 3.12
    for xs_, xj, nm in ((XC0, XC0 + 0.75, 'barat'), (XC1, XC1 - 0.75, 'timur')):
        w1 = dinding((xs_, 0.0), (xs_, YJ), z0, h, g, nama=f'Dinding sudut kaca JP {nm} lt.{no}')
        B(w1, 'jendela', 'JP', 0.12, 1.27, tj, amb)
        w2 = dinding((xs_, YJ), (xj, YJ), z0, h, g, nama=f'Dinding sudut kaca JP {nm} (muka) lt.{no}')
        B(w2, 'jendela', 'JP', 0.0, 0.64, tj, amb)
        dinding((xj, YJ), (xj, YT), z0, h, g, nama=f'Dinding jorokan {nm} lt.{no}')
    wf = dinding((XC0 + 0.75, YT), (XC1 - 0.75, YT), z0, h, g, nama=f'Dinding depan tengah lt.{no}' + (' (panel papan nama)' if no == 2 else ''))
    if no == 1: B(wf, 'pintu', 'P2', 1.40)

# lantai 2 — partisi hall (Rencana Penempatan Kusen Lantai II)
hall(2, Z2, g_l2, h2, 7.0, ((0.0, 12.0), (18.0, 27.0)), [(7.3, 'P2'), (18.3, 'P2')])
hall(2, Z2, g_l2, h2, 5.0, ((0.0, 30.0),), [(2.0, 'P1'), (5.0, 'P1'), (8.0, 'P1'), (9.15, 'P1'), (21.3, 'P1'), (26.05, 'P1'), (27.15, 'P1')])
for x in (3, 6, 9, 24, 27): partisi(2, Z2, g_l2, h2, (x, 0), (x, 5))
partisi(2, Z2, g_l2, h2, (12, 0), (12, 5), pintu=(3.2, 'P1'))
for x in (9, 12, 18): partisi(2, Z2, g_l2, h2, (x, 7), (x, D))
dinding((27, 7), (27, D), Z2, h2, g_l2, tebal=0.12, nama='Dinding toilet lt.2')
wt = dinding((27, 7), (30, 7), Z2, h2, g_l2, tebal=0.12, nama='Dinding toilet sisi hall lt.2')
for xp in (27.4, 28.9): B(wt, 'pintu', 'PK', xp - 27)
dinding((28.5, 7), (28.5, D), Z2, h2, g_l2, tebal=0.10, nama='Sekat toilet pria/wanita lt.2')
wc = dinding((27, 10.0), (30, 10.0), Z2, h2, g_l2, tebal=0.10, nama='Dinding WC lt.2')
for xp in (27.4, 28.9): B(wc, 'pintu', 'PK', xp - 27)
# toilet direktur
wtd = dinding((22.25, 1.5), (22.25, 5.0), Z2, h2, g_l2, tebal=0.10, nama='Dinding toilet direktur')
B(wtd, 'pintu', 'PK', 1.6)
dinding((22.25, 1.5), (24.0, 1.5), Z2, h2, g_l2, tebal=0.10, nama='Dinding toilet direktur')
# inti tangga lt.2: dinding samping + ventilasi kaca di atas tangga, belakang P1–JK–JK–P1 ke balkon
for x, nm in ((13.31, 'barat'), (16.69, 'timur')):
    w = dinding((x, 7.0), (x, D), Z2, h2, g_l2, tebal=0.12, nama=f'Dinding inti tangga {nm} lt.2')
    B(w, 'jendela', 'VT', 0.8, 3.24, 0.55, 2.80)
wb = dinding((12.0, D), (18.0, D), Z2, h2, g_l2, nama='Dinding belakang inti tangga lt.2')
B(wb, 'pintu', 'P1', 0.25); B(wb, 'jendela', 'JK', 1.55, ambang=0.20); B(wb, 'jendela', 'JK', 3.34, ambang=0.20); B(wb, 'pintu', 'P1', 4.85)

# dinding hiasan batu di belakang selasar
dinding((13.1, D + 2.2), (16.9, D + 2.2), 0, 3.6, g_ent, tebal=0.25, nama='Dinding hiasan belakang')
teks('Dinding hiasan', 15.0, D + 2.6); teks('Selasar', 15.0, D + 1.0)

# ---------- lantai 1: finishing ----------
ruang1 = [('Ruang Tata Usaha', 0, 6, 7, 12), ('R. Kepegawaian', 6, 12, 7, 12), ('Ruang Arsip', 18, 24, 7, 12), ('Pantry', 24, 27, 7, 12),
          ('R. Bagian Administrasi Umum', 0, 6, 0, 5), ('R. Perlengkapan', 6, 12, 0, 5), ('Ruang Tunggu/Tamu', 12, 18, 0, 5),
          ('R. Administrasi Kemahasiswaan', 18, 27, 0, 5), ('Gudang Peralatan', 27, 30, 0, 5)]
for nm, a, b, c, d in ruang1:
    lantai(f'Lantai {nm}', kotak(a, b, c, d), -0.10, 0.10, 'ruang', 'k40', g_l1)
    teks(nm, (a + b) / 2, (c + d) / 2 + 1.2)
lantai('Lantai hall (kiri)', kotak(0, 12, 5, 7), -0.10, 0.10, 'ruang', 'k40', g_l1); teks('Hall (keramik 40/40)', 6, 6.0)
lantai('Lantai hall (kanan)', kotak(18, 30, 5, 7), -0.10, 0.10, 'ruang', 'k40', g_l1); teks('Hall (keramik 40/40)', 24, 6.0)
lantai('Lantai inti tangga lt.1', kotak(12, 18, 5, 12), -0.10, 0.10, 'ruang', 'k40', g_l1)
lantai('Lantai toilet pria', kotak(27, 28.5, 7, 12), -0.12, 0.10, 'km', 'k20', g_l1)
lantai('Lantai toilet wanita', kotak(28.5, 30, 7, 12), -0.12, 0.10, 'km', 'k20', g_l1)
lantai('Lantai selasar belakang', kotak(XC0, XC1, D, D + 1.6), -0.12, 0.10, 'teras', 'k30', g_ent)
TENGAH = [(XC0, 0), (XC0, YJ), (XC0 + 0.75, YJ), (XC0 + 0.75, YT), (XC1 - 0.75, YT), (XC1 - 0.75, YJ), (XC1, YJ), (XC1, 0)]
lantai('Lantai lobi depan tengah', TENGAH, -0.10, 0.10, 'ruang', 'k40', g_l1)
lantai('Lantai ramp teras mobil', kotak(12.3, 17.7, -8.5, YT), -0.12, 0.12, 'teras', 'k30', g_ent)
lantai('Teras samping barat', kotak(-2.75, 0, 4.6, 7.4), -0.12, 0.10, 'teras', 'k30', g_ent)
lantai('Teras samping timur', kotak(L, L + 2.75, 4.6, 7.4), -0.12, 0.10, 'teras', 'k30', g_ent)
simbol('klosetJongkok', 27.75, 11.0); simbol('klosetJongkok', 29.25, 11.0)
teks('Toilet', 27.75, 9.3); teks('Toilet', 29.25, 9.3)

# ---------- lantai 2: plat + finishing ----------
void = kotak(13.4, 16.6, 7.5, 11.7)
alas2 = [(0, 0)] + TENGAH + [(L, 0), (L, D), (XC1, D), (XC1, D + 1.25), (XC0, D + 1.25), (XC0, D), (0, D)]
plat('Plat lantai 2 (12 cm K-250)', alas2, Z2 - 0.12, 0.12, g_str, lubang=[void])
lantai('Keramik lantai 2', alas2, Z2, 0.02, 'ruang', 'k40', g_l2, lubang=[void])
ruang2 = [('Ruang Dosen', 0, 9, 7, 12), ('Ruang Tunggu/Tamu', 9, 12, 7, 12), ('R. Rapat Umum', 18, 27, 7, 12),
          ('R. Pudir II', 0, 3, 0, 5), ('R. Pudir III', 3, 6, 0, 5), ('R. Pudir I', 6, 9, 0, 5), ('R. Sekretaris', 9, 12, 0, 5),
          ('R. Direktur', 12, 22.25, 0, 5), ('R.U. Keuangan', 24, 27, 0, 5), ('Ruang Istirahat', 27, 30, 0, 5)]
for nm, a, b, c, d in ruang2:
    teks(nm, (a + b) / 2, (c + d) / 2 + 1.0, Z2)
teks('Hall (keramik 40/40)', 6, 6.0, Z2); teks('Hall (keramik 40/40)', 24, 6.0, Z2)
teks('Toilet', 23.1, 3.2, Z2); teks('Toilet', 27.75, 9.3, Z2); teks('Toilet', 29.25, 9.3, Z2); teks('Balkon', 15.0, D + 0.6, Z2)
simbol('klosetJongkok', 27.75, 11.0); simbol('klosetJongkok', 29.25, 11.0)
# pagar balkon belakang
dinding((XC0, D + 1.25), (XC1, D + 1.25), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon belakang')
for x in (XC0, XC1): dinding((x, D), (x, D + 1.25), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon belakang')
# railing void tangga
for a, b in (((13.4, 7.5), (13.4, 11.7)), ((16.6, 7.5), (16.6, 11.7)), ((13.4, 11.7), (16.6, 11.7)), ((15.1, 7.5), (16.6, 7.5))):
    dinding(a, b, Z2, 1.0, g_tg, tebal=0.08, nama='Railing void tangga')

# ---------- tangga dogleg di inti tangga (22 anak: 2 × 11, tinggi naik 2,00 per bordes) ----------
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga lantai 1 → bordes', 'awal': P(16.5, 7.5), 'arah': 90, 'lebar': 1.4, 'tinggi': 2.0, 'jumlahAnak': 11, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, g_tg)
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga bordes → lantai 2', 'awal': P(13.5, 10.1), 'arah': 270, 'lebar': 1.4, 'tinggi': 2.0, 'jumlahAnak': 11, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 2.0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, g_tg)
plat('Bordes tangga (12 cm K-250)', kotak(13.5, 16.5, 10.1, 11.8), 1.88, 0.12, g_tg)
teks('Naik', 15.8, 8.8); teks('Bordes', 15.0, 10.9, 2.0)

# ---------- plafon ----------
for z, lt in ((3.25, 1), (7.40, 2)):
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon lt.{lt}', 'alas': [P(*q) for q in kotak(0, L, 0, D)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'hollow', 'lis': 'kayu'}, g_atap)
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon bagian tengah lt.{lt}', 'alas': [P(*q) for q in TENGAH], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'hollow', 'lis': 'kayu'}, g_atap)

# ---------- atap: perisai seng galvalum ±36,7° (nok +12,80), gable bagian tengah ----------
KUDA = {'kaki': [0.05, 0.10], 'tarik': [0.05, 0.10], 'makelar': [0.05, 0.10], 'tiang': [0.05, 0.10], 'sokong': [0.05, 0.10], 'skor': [0.05, 0.10],
        'gording': [0.05, 0.10], 'bubungan': [0.05, 0.10], 'klos': [0.05, 0.05], 'lisMundur': 0.20, 'jarakGording': 0.8}
def atap(nama, x0, y0, x1, y1, miring, jarak=3.0, z0=Z_RB):
    tambah('A', {'jenis': 'atap', 'nama': nama, 'bentuk': 'limas', 'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'z0': z0, 'kemiringan': miring, 'overstek': 0.6,
                 'arah': 'x', 'penutup': 'spandek', 'rangka': 'kayu', 'jarakKuda': jarak, 'tebal': 0.1, 'lisplang': 'papan', 'kuda': KUDA}, g_atap)
atap('Atap perisai utama K1 (nok +12,80)', 0, 0, L, D, 36.65)
atap('Atap gable bagian tengah K2 (nok +10,95)', 11.35, YT, 18.65, 8.0, 35.7)

# ---------- kanopi dak, entrance ----------
for a, b in ((-0.3, 12.0), (18.0, L + 0.3)):
    plat('Kanopi dak lt.1 depan', kotak(a, b, -1.2, 0), Z2 - 0.12, 0.12, g_ent, fc=18.7)
    plat('Kanopi dak lt.1 belakang', kotak(a, b, D, D + 1.2), Z2 - 0.12, 0.12, g_ent, fc=18.7)
plat('Kanopi dak teras mobil (12 cm)', kotak(12.2, 17.8, -7.7, YT), Z2 - 0.12, 0.12, g_ent, fc=18.7)
dinding((12.2, -7.7), (17.8, -7.7), Z2 - 0.50, 0.50, g_ent, tebal=0.12, nama='Band kanopi teras mobil')
dinding((12.2, -7.7), (12.2, YT), Z2 - 0.50, 0.50, g_ent, tebal=0.12, nama='Band kanopi teras mobil')
dinding((17.8, -7.7), (17.8, YT), Z2 - 0.50, 0.50, g_ent, tebal=0.12, nama='Band kanopi teras mobil')
plat('Kanopi dak pintu samping barat', kotak(-2.95, 0.2, 4.4, 7.6), Z2 - 0.12, 0.12, g_ent, fc=18.7)
plat('Kanopi dak pintu samping timur', kotak(L - 0.2, L + 2.95, 4.4, 7.6), Z2 - 0.12, 0.12, g_ent, fc=18.7)
# panel papan nama bergaris + tiang abu-abu dua sisi (Tampak Depan)
dinding((13.4, YT - 0.06), (16.6, YT - 0.06), Z2 + 0.6, 2.8, g_ent, tebal=0.06, nama='Panel papan nama (dinding bergaris)')
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'POLTEK KP SORONG', 'titik': {'x': 15.0, 'y': YT - 0.2, 'z': 6.0}, 'pada': 'tampak'})
# lantai tangga masuk: tiga anak tangga
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga teras masuk', 'awal': P(17.7, -9.3), 'arah': 90, 'lebar': 5.4, 'tinggi': 0.45, 'jumlahAnak': 3, 'antrede': 0.4,
             'tebalPlat': 0.12, 'z0': -0.45, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'tanpa'}, g_ent)

# ---------- tapak: halaman, palem, jalan ----------
lantai('Halaman paving depan', kotak(-4.0, L + 4.0, -16.0, -9.3), -0.15, 0.10, 'lain', 'plester', g_tapak)
lantai('Lantai teras depan sayap', kotak(0.0, 12.0, -1.2, 0), -0.12, 0.10, 'teras', 'k30', g_tapak)
lantai('Lantai teras depan sayap timur', kotak(18.0, L, -1.2, 0), -0.12, 0.10, 'teras', 'k30', g_tapak)
for x in (4.5, 10.5, 19.5, 25.5): simbol('pohon', x, -2.4)
teks('Teras mobil (ramp)', 15.0, -5.0); teks('Entrance', 15.0, YT + 0.3)

# ---------- legenda dan garis potong ----------
tambah('L', {'jenis': 'gambar2d', 'bentuk': 'legenda', 'lembar': 'denah', 'tempel': 'kertas', 'titik': [{'x': 22, 'y': 215}]})
tambah('X', {'jenis': 'potong', 'nama': 'S.01', 'awal': P(-4.0, 6.0), 'akhir': P(L + 4.0, 6.0), 'pandang': 1})
tambah('X', {'jenis': 'potong', 'nama': 'S.02', 'awal': P(15.0, -10.0), 'akhir': P(15.0, D + 3.0), 'pandang': 1})

proyek = {'format': 'rancang-proyek', 'versi': 1, 'aplikasi': 'RANCANG', 'disimpan': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'setel': {'nama': 'Kantor Utama Poltek KP Sorong', 'tebalDinding': 0.15, 'tinggiDinding': 3.5, 'kemiringanAtap': 36.65, 'overstekAtap': 0.6, 'contohVersi': 2},
          'elemen': E, 'grup': GR, 'komponen': {}, 'kusen': KUSEN}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'contoh', 'kantor-utama.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(proyek, f, ensure_ascii=False, separators=(',', ':'))
print(out, len(E), 'elemen', len(GR), 'grup', len(KUSEN), 'tipe kusen')
