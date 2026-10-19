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
YT = -1.5                            # muka depan bagian tengah (menjorok 1,50 m)

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

# ---------- kusen ----------
def tipe_kusen(kode, untuk, daun, isi, kolom=1, baris=1, buka='kiri', boven=0, nama=None):
    i = idb('T')
    KUSEN[i] = {'kode': kode, 'untuk': untuk, 'nama': nama or ('Pintu ' if untuk == 'pintu' else 'Jendela ') + kode, 'profil': 0.06,
                'daun': daun, 'isi': isi, 'kolom': kolom, 'baris': baris, 'buka': buka, 'boven': {'tinggi': boven, 'kolom': 2, 'baris': 1} if boven else None, 'catatan': ''}
tipe_kusen('P1', 'pintu', 1, 'panil6', buka='kiri', boven=0.45, nama='Pintu P1 panil 90')
tipe_kusen('P2', 'pintu', 2, 'kaca', buka='kiri', nama='Pintu P2 dua daun kaca (entrance)')
tipe_kusen('P2', 'jendela', 1, 'kaca', buka='tetap', nama='Kaca mati samping pintu P2')
tipe_kusen('P4', 'pintu', 1, 'panil6', buka='kiri', nama='Pintu KM P4')
tipe_kusen('J3', 'jendela', 3, 'kaca', buka='kupu', nama='Jendela J3 (3 daun kaca)')
tipe_kusen('V1', 'jendela', 1, 'jalusi', buka='tetap', nama='Ventilasi kaca di atas jendela V1')
tipe_kusen('V2', 'jendela', 1, 'jalusi', buka='tetap', nama='Ventilasi KM V2')

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
for x, y in ((12.75, -2.25), (17.25, -2.25), (12.75, -7.2), (17.25, -7.2)): tiang_teras(x, y, g_ent)       # teras mobil
for x, y in ((-2.75, 5.0), (-2.75, 7.0), (L + 2.75, 5.0), (L + 2.75, 7.0)): tiang_teras(x, y, g_ent)       # pintu samping
for x in (13.31, 16.69): tiang_teras(x, D + 1.25, g_str, tinggi=Z_RB - 0.3)                                  # balkon belakang

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

# ---------- lantai tipikal: dinding & bukaan ----------
def segmen(x0, x1, skip):
    """pecah rentang [x0,x1] di sekitar rentang skip (a,b) yang dikosongkan."""
    a, b = skip
    return [(x0, min(x1, a)), (max(x0, b), x1)] if a is not None else [(x0, x1)]

def jendela_bay(wall, x_awal, bays, z_ambang, tinggi_j=1.5, vent=True):
    for bx in bays:
        pos = bx + 0.5 - x_awal
        bukaan(wall, 'jendela', 'J3', pos, 2.0, tinggi_j, z_ambang)
        if vent: bukaan(wall, 'jendela', 'V1', pos, 2.0, 0.55, z_ambang + tinggi_j + 0.15)

def lantai_tipikal(z0, g, h, no):
    ambang = 0.9
    bays = [3.0 * i for i in range(10)]
    # fasad depan y=0 (kecuali tengah 12–18 yang menjorok); belakang y=12 (kecuali inti tangga 12–18)
    for (a, b) in ((0.0, 12.0), (18.0, 30.0)):
        w = dinding((a, 0.0), (b, 0.0), z0, h, g, nama=f'Dinding depan lt.{no}')
        jendela_bay(w, a, [x for x in bays if a <= x < b], ambang)
    for (a, b) in ((0.0, 12.0), (18.0, 30.0)):
        w = dinding((a, D), (b, D), z0, h, g, nama=f'Dinding belakang lt.{no}')
        pakai = [x for x in bays if a <= x < b]
        if no == 1 and a == 18.0: pakai = [x for x in pakai if x < 27.0]
        if no == 2 and a == 18.0: pakai = [x for x in pakai if x < 27.0]
        jendela_bay(w, a, pakai, ambang)
        if a == 18.0:                                                              # ventilasi toilet 27–30
            for xv in (27.4, 28.9): bukaan(w, 'jendela', 'V2', xv - a, 0.8, 0.5, 2.2)
    # dinding samping x=0 dan x=30; pintu samping di ujung hall (y 5–7)
    for x, nm in ((0.0, 'barat'), (L, 'timur')):
        for (a, b) in ((0.0, 5.0), (7.0, D)):
            w = dinding((x, a), (x, b), z0, h, g, nama=f'Dinding samping {nm} lt.{no}')
            if b - a > 4.0: bukaan(w, 'jendela', 'J3', 1.5, 2.0, 1.5, ambang)
        if no == 1:
            w = dinding((x, 5.0), (x, 7.0), z0, h, g, nama=f'Dinding ujung hall {nm}')
            bukaan(w, 'pintu', 'P2', 0.1, 1.8, 2.4)
            bukaan(w, 'jendela', 'V1', 0.1, 1.8, 0.55, 2.7)
        else:
            w = dinding((x, 5.0), (x, 7.0), z0, h, g, nama=f'Dinding ujung hall {nm} lt.2')
            bukaan(w, 'jendela', 'J3', 0.15, 1.7, 1.8, 0.9)
    # dinding tepi hall (sekat kamar), ujung tengah terbuka ke inti tangga
    for y in (5.0, 7.0):
        for (a, b) in (((0.0, 12.0), (18.0, 30.0)) if y == 5.0 else ((0.0, 12.0), (18.0, 27.0))):
            dinding((a, y), (b, y), z0, h, g, tebal=0.12, nama=f'Dinding tepi hall lt.{no}')

h1, h2 = Z2 - 0.50, Z_RB - 0.30 - Z2
lantai_tipikal(0.0, g_l1, h1, 1)
lantai_tipikal(Z2, g_l2, h2, 2)

def sekat_dan_pintu(z0, g, h, no, spec):
    """spec: daftar (jenis, (x0,y0), (x1,y1), pintu_pos|None). jenis 'd' dinding sekat 12 cm."""
    for a, b, pintu in spec:
        w = dinding(a, b, z0, h, g, tebal=0.12, nama=f'Sekat ruang lt.{no}')
        if pintu is not None: bukaan(w, 'pintu', 'P1', pintu, 0.9, 2.1)

# pintu ruang pada dinding tepi hall (lantai 1 dan 2) — dinding tepi hall dibuat di atas; bukaan menyusul di sini
def pintu_hall(g, z0, h, no, daftar):
    for y, a, b, xp, kode in daftar:
        w = [i for i, e in E.items() if e.get('jenis') == 'dinding' and e.get('nama') == f'Dinding tepi hall lt.{no}' and abs(e['awal']['y'] - y) < 1e-6 and e['awal']['x'] <= a + 1e-6 and e['akhir']['x'] >= b - 1e-6]
        assert w, (y, a, b)
        bukaan(w[0], 'pintu', kode, xp - E[w[0]]['awal']['x'], 0.9 if kode == 'P1' else 1.5, 2.1)

# lantai 1
pintu_hall(g_l1, 0, h1, 1, [(5.0, 0, 12, 2.55, 'P1'), (5.0, 0, 12, 8.55, 'P1'), (5.0, 18, 30, 22.05, 'P1'), (5.0, 18, 30, 28.05, 'P1'),
                            (7.0, 0, 12, 2.55, 'P1'), (7.0, 0, 12, 8.55, 'P1'), (7.0, 18, 27, 20.55, 'P1'), (7.0, 18, 27, 25.05, 'P1')])
sekat_dan_pintu(0, g_l1, h1, 1, [
    ((6, 0), (6, 5), None), ((12, 0), (12, 5), None), ((18, 0), (18, 5), None), ((27, 0), (27, 5), None),          # sekat ruang depan
    ((6, 7), (6, 12), None), ((12, 7), (12, 12), None), ((18, 7), (18, 12), None), ((24, 7), (24, 12), None), ((27, 7), (27, 12), None),   # sekat ruang belakang
    ((27, 8.25), (30, 8.25), None), ((28.5, 8.25), (28.5, 12), None)])
for xp in (27.4, 28.9):
    bukaan([i for i, e in E.items() if e.get('nama') == 'Sekat ruang lt.1' and e['awal']['y'] == 8.25][0], 'pintu', 'P4', xp - 27.0, 0.7, 2.1)
# gudang kotak di bawah tangga (lt.1) dan sekat inti tangga
dinding((13.31, 7.0), (13.31, D), 0, h1, g_l1, tebal=0.12, nama='Dinding inti tangga barat')
dinding((16.69, 7.0), (16.69, D), 0, h1, g_l1, tebal=0.12, nama='Dinding inti tangga timur')
# bagian tengah menjorok: dinding depan di y=-1.5 dengan pintu P2 + kaca samping
dk1 = dinding((XC0, 0.0), (XC0, YT), 0, h1, g_l1, nama='Dinding samping teras barat')
dk2 = dinding((XC1, 0.0), (XC1, YT), 0, h1, g_l1, nama='Dinding samping teras timur')
dk3 = dinding((XC0, YT), (XC1, YT), 0, h1, g_l1, nama='Dinding depan tengah lt.1')
bukaan(dk3, 'pintu', 'P2', 1.9, 2.2, 2.4)
bukaan(dk3, 'jendela', 'P2', 0.55, 1.2, 2.4)
bukaan(dk3, 'jendela', 'P2', 4.25, 1.2, 2.4)
bukaan(dk3, 'jendela', 'V1', 0.55, 4.9, 0.5, 2.55)
# lantai 2
pintu_hall(g_l2, Z2, h2, 2, [(5.0, 0, 12, 1.05, 'P1'), (5.0, 0, 12, 4.05, 'P1'), (5.0, 0, 12, 7.05, 'P1'), (5.0, 0, 12, 10.05, 'P1'), (5.0, 18, 30, 25.05, 'P1'), (5.0, 18, 30, 28.05, 'P1'),
                            (7.0, 0, 12, 3.9, 'P1'), (7.0, 0, 12, 10.05, 'P1'), (7.0, 18, 27, 22.05, 'P1')])
sekat_dan_pintu(Z2, g_l2, h2, 2, [
    ((3, 0), (3, 5), None), ((6, 0), (6, 5), None), ((9, 0), (9, 5), None), ((12, 0), (12, 5), None), ((24, 0), (24, 5), None), ((27, 0), (27, 5), None),
    ((9, 7), (9, 12), None), ((12, 7), (12, 12), None), ((18, 7), (18, 12), None), ((27, 7), (27, 12), None),
    ((27, 8.25), (30, 8.25), None), ((28.5, 8.25), (28.5, 12), None),
    ((22.25, 1.5), (22.25, 5), None), ((22.25, 1.5), (24, 1.5), None)])
for xp in (27.4, 28.9):
    bukaan([i for i, e in E.items() if e.get('nama') == 'Sekat ruang lt.2' and e['awal']['y'] == 8.25][0], 'pintu', 'P4', xp - 27.0, 0.7, 2.1)
dinding((13.31, 7.0), (13.31, D), Z2, h2, g_l2, tebal=0.12, nama='Dinding inti tangga barat lt.2')
dinding((16.69, 7.0), (16.69, D), Z2, h2, g_l2, tebal=0.12, nama='Dinding inti tangga timur lt.2')
dd = dinding((13.31, D), (16.69, D), Z2, h2, g_l2, nama='Dinding belakang inti tangga lt.2')
bukaan(dd, 'pintu', 'P2', 0.6, 1.5, 2.1)
bukaan(dd, 'jendela', 'P2', 0.0, 0.5, 2.1)
bukaan(dd, 'jendela', 'P2', 2.2, 0.5, 2.1)
# bagian tengah menjorok lt.2: ruang direktur menjorok 1,50 m, dinding depan berpanel papan nama
dd1 = dinding((XC0, 0.0), (XC0, YT), Z2, h2, g_l2, nama='Dinding samping direktur barat')
dd2 = dinding((XC1, 0.0), (XC1, YT), Z2, h2, g_l2, nama='Dinding samping direktur timur')
dd3 = dinding((XC0, YT), (XC1, YT), Z2, h2, g_l2, nama='Dinding depan direktur lt.2 (panel papan nama)')
bukaan(dd3, 'jendela', 'J3', 0.5, 1.4, 1.5, 0.9)
# dinding hiasan di belakang inti tangga (lt.1) setinggi atap
dinding((13.31, D + 1.25), (16.69, D + 1.25), 0, Z_RB - 0.3, g_ent, tebal=0.20, nama='Dinding hiasan belakang')
dinding((13.31, D), (13.31, D + 1.25), 0, Z2 - 0.5, g_ent, tebal=0.15, nama='Dinding samping hiasan barat')
dinding((16.69, D), (16.69, D + 1.25), 0, Z2 - 0.5, g_ent, tebal=0.15, nama='Dinding samping hiasan timur')

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
lantai('Lantai toilet pria', kotak(27, 28.5, 8.25, 12), -0.12, 0.10, 'km', 'k20', g_l1)
lantai('Lantai toilet wanita', kotak(28.5, 30, 8.25, 12), -0.12, 0.10, 'km', 'k20', g_l1)
lantai('Lantai vestibule toilet', kotak(27, 30, 7, 8.25), -0.10, 0.10, 'ruang', 'k40', g_l1)
lantai('Lantai teras depan tengah', kotak(XC0, XC1, YT, 0), -0.10, 0.10, 'ruang', 'k40', g_l1)
lantai('Lantai ramp teras mobil', kotak(12.3, 17.7, -8.5, YT), -0.12, 0.12, 'teras', 'k30', g_ent)
lantai('Teras samping barat', kotak(-2.75, 0, 4.6, 7.4), -0.12, 0.10, 'teras', 'k30', g_ent)
lantai('Teras samping timur', kotak(L, L + 2.75, 4.6, 7.4), -0.12, 0.10, 'teras', 'k30', g_ent)
simbol('klosetJongkok', 27.75, 11.0); simbol('klosetJongkok', 29.25, 11.0)
teks('Toilet', 27.75, 9.3); teks('Toilet', 29.25, 9.3)
teks('Dinding hiasan', 15.0, D + 1.6)

# ---------- lantai 2: plat + finishing ----------
void = kotak(13.4, 16.6, 7.5, 11.7)
alas2 = [(0, 0), (XC0, 0), (XC0, YT), (XC1, YT), (XC1, 0), (L, 0), (L, D), (16.69, D), (16.69, D + 1.25), (13.31, D + 1.25), (13.31, D), (0, D)]
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
dinding((13.31, D + 1.25), (16.69, D + 1.25), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon belakang')
# railing void tangga
for a, b in (((13.4, 7.5), (13.4, 11.7)), ((16.6, 7.5), (16.6, 11.7)), ((13.4, 11.7), (16.6, 11.7)), ((13.4, 7.5), (14.9, 7.5))):
    dinding(a, b, Z2, 1.0, g_tg, tebal=0.08, nama='Railing void tangga')

# ---------- tangga dogleg di inti tangga (22 anak: 2 × 11, tinggi naik 2,00 per bordes) ----------
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga lantai 1 → bordes', 'awal': P(14.9, 7.5), 'arah': 90, 'lebar': 1.4, 'tinggi': 2.0, 'jumlahAnak': 11, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, g_tg)
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga bordes → lantai 2', 'awal': P(15.1, 10.1), 'arah': 270, 'lebar': 1.4, 'tinggi': 2.0, 'jumlahAnak': 11, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 2.0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, g_tg)
plat('Bordes tangga (12 cm K-250)', kotak(13.5, 16.5, 10.1, 11.8), 1.88, 0.12, g_tg)
teks('Naik', 14.2, 8.8); teks('Bordes', 15.0, 10.9, 2.0)

# ---------- plafon ----------
for z, lt in ((3.25, 1), (7.40, 2)):
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon lt.{lt}', 'alas': [P(*q) for q in kotak(0, L, 0, D)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'hollow', 'lis': 'kayu'}, g_atap)
    tambah('P', {'jenis': 'plafon', 'nama': f'Plafon bagian tengah lt.{lt}', 'alas': [P(*q) for q in kotak(XC0, XC1, YT, 0)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'hollow', 'lis': 'kayu'}, g_atap)

# ---------- atap: perisai seng galvalum ±36,7° (nok +12,80), gable bagian tengah ----------
KUDA = {'kaki': [0.05, 0.10], 'tarik': [0.05, 0.10], 'makelar': [0.05, 0.10], 'tiang': [0.05, 0.10], 'sokong': [0.05, 0.10], 'skor': [0.05, 0.10],
        'gording': [0.05, 0.10], 'bubungan': [0.05, 0.10], 'klos': [0.05, 0.05], 'lisMundur': 0.20, 'jarakGording': 0.8}
def atap(nama, x0, y0, x1, y1, miring, jarak=3.0, z0=Z_RB):
    tambah('A', {'jenis': 'atap', 'nama': nama, 'bentuk': 'limas', 'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'z0': z0, 'kemiringan': miring, 'overstek': 0.6,
                 'arah': 'x', 'penutup': 'spandek', 'rangka': 'kayu', 'jarakKuda': jarak, 'tebal': 0.1, 'lisplang': 'papan', 'kuda': KUDA}, g_atap)
atap('Atap perisai utama K1 (nok +12,80)', 0, 0, L, D, 36.65)
atap('Atap gable bagian tengah K2 (nok +10,95)', 11.35, -2.0, 18.65, 8.0, 35.7)

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
dinding((12.0, YT - 0.10), (13.3, YT - 0.10), Z2, 3.8, g_ent, tebal=0.15, nama='Tiang abu-abu depan barat')
dinding((16.7, YT - 0.10), (18.0, YT - 0.10), Z2, 3.8, g_ent, tebal=0.15, nama='Tiang abu-abu depan timur')
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'POLITEKNIK KELAUTAN DAN PERIKANAN SORONG', 'titik': {'x': 15.0, 'y': YT - 0.2, 'z': 6.0}, 'pada': 'tampak'})
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
          'setel': {'nama': 'Kantor Utama Poltek KP Sorong', 'tebalDinding': 0.15, 'tinggiDinding': 3.5, 'kemiringanAtap': 36.65, 'overstekAtap': 0.6},
          'elemen': E, 'grup': GR, 'komponen': {}, 'kusen': KUSEN}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'contoh', 'kantor-utama.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(proyek, f, ensure_ascii=False, separators=(',', ':'))
print(out, len(E), 'elemen', len(GR), 'grup', len(KUSEN), 'tipe kusen')
