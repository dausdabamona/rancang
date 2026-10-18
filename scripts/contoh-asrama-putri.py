#!/usr/bin/env python3
"""Membangkitkan proyek contoh RANCANG: Asrama Putri Poltek KP Sorong (renovasi 2015, CV. Awal Rahmat Konsultan).

Sumber: PDF gambar kerja (denah eksisting, denah lantai 1–2 setelah renovasi, rencana pondasi/sloof/balok lantai/ring balok/atap,
potongan S.01 & S.04, tipe kusen). Dua sayap dua lantai yang saling berhadapan mengapit taman, disambung blok ruang tamu/tangga
di ujung timur:
- Sayap selatan (direnovasi): as 350·350·450·450·450·300·450·450·450 = 37,00 m, 9 kamar + KM per lantai.
- Sayap utara (eksisting): as 350·350·500·500·500·500·500·500 = 37,00 m, 8 kamar + KM per lantai, teras menghadap selatan.
Kedalaman tiap sayap 200·424·189 (KM · kamar · teras) + tempat jemur 3,00 di belakang (lt.1) / balkon 1,25 (lt.2).
Lantai 2 di +4,00, plafon +3,50 / +7,35, ring balk atas +7,75, atap limas 35° seng multiroof rangka kayu.

Pakai: python3 scripts/contoh-asrama-putri.py  → app/contoh/asrama-putri.json
"""
import json, os, datetime

Z2, Z_RB = 4.0, 7.75                 # lantai 2, puncak ring balk
TEBAL = 0.15
VA, VB, VC, VD = 0.0, 2.0, 6.24, 8.13   # kedalaman lokal sayap: A belakang KM · B KM/kamar · C depan kamar · D kolom teras
Y_SEL = 0.0                           # sayap selatan: dinding belakang A di y = 0, depan ke arah +y
Y_UT = 2 * VD + 6.38                  # sayap utara: dinding belakang A di y = 22,64, depan ke arah −y (celah blok/taman 6,38 m)
BLOK = (28.0, 37.0, VC, VD + 2.70)    # blok ruang tamu/tangga (denah lt.1 renovasi): x 28–37, dari dinding depan kamar 6,24 sampai 10,83 (teras + 2,70)
X_JOG = 21.5                          # batas atap barat (ridge +11,00) dan atap timur yang lebih dalam menutup blok (ridge +11,51)
TERAS_MASUK = (37.0, 39.25)           # entrance 2,25 m di timur blok

# ---------- sayap ----------
SAYAP = {
    'selatan': {'xs': [0, 3.5, 7.0, 11.5, 16.0, 20.5, 23.5, 28.0, 32.5, 37.0], 's': 1, 'yA': Y_SEL, 'nama': 'Sayap selatan (renovasi)',
                # (x0, x1, sisi KM): rangkaian ukuran 150|200 · 200|150 · 200|250 ×3 · 150|150 · 250|200 ×3
                'kamar': [(0, 3.5, 'timur'), (3.5, 7.0, 'barat'), (7.0, 11.5, 'barat'), (11.5, 16.0, 'barat'), (16.0, 20.5, 'barat'),
                          (20.5, 23.5, 'barat'), (23.5, 28.0, 'timur'), (28.0, 32.5, 'timur'), (32.5, 37.0, 'timur')]},
    'utara': {'xs': [0, 3.5, 7.0, 12.0, 17.0, 22.0, 27.0, 32.0, 37.0], 's': -1, 'yA': Y_UT, 'nama': 'Sayap utara (eksisting)',
              # rangkaian ukuran 150|200 · 200|150 · 200|300 ×3 · 300|200 ×3
              'kamar': [(0, 3.5, 'timur'), (3.5, 7.0, 'barat'), (7.0, 12.0, 'barat'), (12.0, 17.0, 'barat'), (17.0, 22.0, 'barat'),
                        (22.0, 27.0, 'timur'), (27.0, 32.0, 'timur'), (32.0, 37.0, 'timur')]},
}

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

# ---------- level ----------
tambah('M', {'jenis': 'level', 'nama': 'Lantai 1', 'z': 0})
tambah('M', {'jenis': 'level', 'nama': 'Lantai 2', 'z': Z2})
tambah('M', {'jenis': 'level', 'nama': 'Ring balk', 'z': Z_RB})

# ---------- struktur ----------
def footplat(x, y, tipe):
    if tipe == 'R1':
        return {'jenis': 'pondasi', 'tipe': 'footplat', 'nama': 'Foot plat R1', 'x': r2(x), 'y': r2(y), 'p': 1.7, 'l': 1.7, 'tebal': 0.3,
                'tulPlat': {'d': 16, 's': 0.15, 'ulir': False}, 'pedestal': {'b': 0.35, 'h': 0.35}, 'puncakPedestal': -0.45,
                'tul': {'n': 12, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.04, 'z0': -1.55}
    return {'jenis': 'pondasi', 'tipe': 'footplat', 'nama': 'Foot plat R2', 'x': r2(x), 'y': r2(y), 'p': 1.25, 'l': 1.25, 'tebal': 0.3,
            'tulPlat': {'d': 16, 's': 0.15, 'ulir': False}, 'pedestal': {'b': 0.3, 'h': 0.3}, 'puncakPedestal': -0.35,
            'tul': {'n': 8, 'd': 16, 'ulir': False}, 'sengkang': {'d': 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.04, 'z0': -1.6}

def kolom(x, y, b, z0, tinggi, nama, tul_n, tul_d):
    return {'jenis': 'kolom', 'tipe': 'struktur', 'nama': nama, 'x': r2(x), 'y': r2(y), 'b': b, 'h': b, 'tinggi': r2(tinggi), 'z0': r2(z0),
            'tul': {'n': tul_n, 'd': tul_d, 'ulir': False}, 'sengkang': {'d': 10 if b >= 0.35 else 8, 's': 0.2}, 'fc': 18.7, 'selimut': 0.03}

def balok(jenis, a, b, lebar, tinggi, z0, nama, tul_n=6, tul_d=16, sk=0.12):
    return {'jenis': jenis, 'nama': nama, 'awal': P(*a), 'akhir': P(*b), 'b': lebar, 'h': tinggi, 'z0': r2(z0),
            'tul': {'n': tul_n, 'd': tul_d, 'ulir': False}, 'sengkang': {'d': 8, 's': sk}, 'fc': 18.7, 'selimut': 0.03}

def kolom_lengkap(x, y, tipe, g, puncak=Z_RB):
    if tipe == 'R1':
        tambah('F', footplat(x, y, 'R1'), g)
        tambah('C', kolom(x, y, 0.35, -0.45, Z2 + 0.45, 'Kolom R1 35/35', 12, 16), g)
    else:
        tambah('F', footplat(x, y, 'R2'), g)
        tambah('C', kolom(x, y, 0.30, -0.35, Z2 + 0.35, 'Kolom R2 30/30', 8, 16), g)
    tambah('C', kolom(x, y, 0.30, Z2, puncak - Z2, 'Kolom R2 30/30 lt.2', 8, 16), g)

# ---------- kusen (tipe) ----------
def tipe_kusen(kode, untuk, daun, isi, kolom=2, baris=1, buka='kiri', boven=0.45, nama=None):
    i = idb('T')
    KUSEN[i] = {'kode': kode, 'untuk': untuk, 'nama': nama or ('Pintu ' if untuk == 'pintu' else 'Jendela ') + kode, 'profil': 0.06,
                'daun': daun, 'isi': isi, 'kolom': kolom, 'baris': baris, 'buka': buka, 'boven': {'tinggi': boven, 'kolom': 2, 'baris': 1} if boven else None, 'catatan': ''}
tipe_kusen('P1', 'pintu', 1, 'panil6', buka='kiri')
tipe_kusen('P2', 'pintu', 2, 'panil6', buka='kiri', nama='Pintu P2 dua daun')
tipe_kusen('P2', 'jendela', 1, 'kaca', kolom=1, baris=1, buka='tetap', nama='Kaca mati samping pintu P2')   # jendela besar di kedua sisi pintu depan, satu unit kusen
tipe_kusen('P4', 'pintu', 1, 'panil6', buka='kiri', boven=0)
tipe_kusen('PJ2', 'pintu', 1, 'panil6', buka='kanan')
tipe_kusen('PJ2', 'jendela', 1, 'kaca', kolom=1, baris=1, buka='tetap')
tipe_kusen('J1', 'jendela', 2, 'kaca', kolom=1, baris=1, buka='kupu')
tipe_kusen('J3', 'jendela', 3, 'kaca', kolom=1, baris=1, buka='kupu')
tipe_kusen('V1', 'jendela', 2, 'jalusi', kolom=1, baris=1, buka='tetap', boven=0)
tipe_kusen('V2', 'jendela', 1, 'jalusi', kolom=1, baris=1, buka='tetap', boven=0, nama='Ventilasi V2 (KM 1,50)')
tipe_kusen('V3', 'jendela', 1, 'kaca', kolom=1, baris=1, buka='tetap', boven=0, nama='Celah kaca V3 fasad entrance')
tipe_kusen('PJ1', 'jendela', 1, 'kaca', kolom=1, baris=6, buka='tetap', boven=0, nama='Kaca mati tinggi PJ1 (6 kotak)')   # 110 × 580, 6 kotak kaca bersusun

def bukaan(dinding, tipe, kode, x_abs, lebar, tinggi, ambang=0):
    """x_abs = koordinat X mutlak tepi bukaan (dinding sejajar X); jarak dihitung dari ujung awal dinding."""
    w = E[dinding]
    datar = abs(w['akhir']['y'] - w['awal']['y']) < 1e-6
    jarak = x_abs - w['awal']['x'] if datar else x_abs
    if datar: assert -1e-6 <= jarak and jarak + lebar <= abs(w['akhir']['x'] - w['awal']['x']) + 1e-6, (dinding, x_abs, lebar)
    return tambah('B', {'jenis': 'bukaan', 'tipe': tipe, 'kode': kode, 'dinding': dinding, 'jarak': r2(max(0, jarak)), 'lebar': lebar, 'tinggi': tinggi, 'ambang': ambang})

def dinding(a, b, z0, tinggi, g, tebal=TEBAL, nama=None):
    d = {'jenis': 'dinding', 'awal': P(*a), 'akhir': P(*b), 'tebal': tebal, 'tinggi': r2(tinggi), 'z0': r2(z0)}
    if nama: d['nama'] = nama
    return tambah('D', d, g)

def lantai(nama, alas, z0, tinggi, jenis, penutup, g, lubang=None):
    d = {'jenis': 'volume', 'nama': nama, 'alas': [P(*q) for q in alas], 'z0': r2(z0), 'tinggi': tinggi, 'lantai': jenis, 'penutupLantai': penutup}
    if lubang: d['lubang'] = [[P(*q) for q in c] for c in lubang]
    return tambah('V', d, g)

def simbol(nama, x, y, rot=0):
    tambah('L', {'jenis': 'gambar2d', 'bentuk': 'simbol', 'simbol': nama, 'lembar': 'denah', 'tempel': 'gambar', 'titik': [{'x': r2(x), 'y': r2(y), 'z': 0}], 'rotasi': rot})

def teks(t, x, y):
    tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': t, 'titik': {'x': r2(x), 'y': r2(y), 'z': 0}, 'pada': 'denah'})

# ---------- satu sayap ----------
def sayap(kunci):
    W = SAYAP[kunci]; XS, s, yA, KAMAR = W['xs'], W['s'], W['yA'], W['kamar']
    Y = lambda v: yA + s * v                       # kedalaman lokal → y dunia
    YA, YB, YC, YD = Y(VA), Y(VB), Y(VC), Y(VD)
    g_str = grup(f'Struktur {W["nama"]}'); g_l1 = grup(f'Lantai 1 {W["nama"]}'); g_l2 = grup(f'Lantai 2 {W["nama"]}'); g_atap = grup(f'Atap {W["nama"]}')
    rect = lambda x0, x1, v0, v1: [(x0, Y(v0)), (x1, Y(v0)), (x1, Y(v1)), (x0, Y(v1))]

    # kolom + pondasi: R1 baris A dan C, R2 baris D (teras) dan B di bay 350
    for x in XS:
        kolom_lengkap(x, YA, 'R1', g_str); kolom_lengkap(x, YC, 'R1', g_str); kolom_lengkap(x, YD, 'R2', g_str)
    for x in (3.5, 7.0): kolom_lengkap(x, YB, 'R2', g_str)
    # sloof
    for y in (YA, YC): tambah('S', balok('slof', (0, y), (37.0, y), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), g_str)
    tambah('S', balok('slof', (0, YD), (37.0, YD), 0.20, 0.30, -0.35, 'Sloof SL2 20/30'), g_str)
    tambah('S', balok('slof', (3.5, YB), (7.0, YB), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), g_str)
    for x in XS:
        tambah('S', balok('slof', (x, YA), (x, YC), 0.25, 0.40, -0.45, 'Sloof SL1 25/40'), g_str)
        tambah('S', balok('slof', (x, YC), (x, YD), 0.20, 0.30, -0.35, 'Sloof SL2 20/30'), g_str)
    # balok lantai 2 (puncak +4,00) dan ring balk (puncak +7,75)
    for y in (YA, YC):
        tambah('R', balok('ringbalk', (0, y), (37.0, y), 0.30, 0.60, Z2 - 0.60, 'Balok lantai BL1 30/60', 8, 16), g_str)
        tambah('R', balok('ringbalk', (0, y), (37.0, y), 0.25, 0.35, Z_RB - 0.35, 'Ring balk RB3 25/35'), g_str)
    for y in (YB, YD, Y(-1.25)):
        tambah('R', balok('ringbalk', (0, y), (37.0, y), 0.20, 0.30, Z2 - 0.30, 'Balok lantai BL2 20/30', 6, 16), g_str)
    tambah('R', balok('ringbalk', (0, YD), (37.0, YD), 0.20, 0.30, Z_RB - 0.30, 'Ring balk RB1 20/30'), g_str)
    tambah('R', balok('ringbalk', (0, YB), (37.0, YB), 0.15, 0.20, Z_RB - 0.20, 'Ring balk RB2 15/20', 4, 12), g_str)
    for x in XS:
        tambah('R', balok('ringbalk', (x, Y(-1.25)), (x, YD), 0.30, 0.60, Z2 - 0.60, 'Balok lantai BL1 30/60', 8, 16), g_str)
        tambah('R', balok('ringbalk', (x, YA), (x, YD), 0.25, 0.35, Z_RB - 0.35, 'Ring balk RB3 25/35'), g_str)

    # dinding dan bukaan per lantai; h_* = TINGGI dinding sampai bawah balok (lt.1) atau bawah ring balk (lt.2)
    def lantai_tipikal(z0, g, h_ac, h_b, h_sekat, no):
        dA = dinding((0, YA), (37.0, YA), z0, h_ac, g, nama=f'Dinding belakang lt.{no}')
        dB = dinding((0, YB), (37.0, YB), z0, h_b, g, nama=f'Dinding KM–kamar lt.{no}')
        dC = dinding((0, YC), (37.0, YC), z0, h_ac, g, nama=f'Dinding depan lt.{no}')
        for x in XS: dinding((x, YA), (x, YC), z0, h_ac, g, nama=f'Dinding as x={x:g} lt.{no}')
        for x0, x1, sisi in KAMAR:
            kx0, kx1 = batas_km(x0, x1, sisi)
            cx0, cx1 = (x0, kx0) if sisi == 'timur' else (kx1, x1)
            xsekat = kx0 if sisi == 'timur' else kx1
            dinding((xsekat, YA), (xsekat, YB), z0, h_sekat, g, tebal=0.10, nama=f'Sekat KM lt.{no}')
            tkm, tcr, wkm = (kx0 + kx1) / 2, (cx0 + cx1) / 2, kx1 - kx0
            bukaan(dB, 'pintu', 'P4', tkm - 0.35 - min(0.6, wkm / 2 - 0.5) * (1 if sisi == 'timur' else -1), 0.70, 2.10)   # pintu KM
            bukaan(dB, 'pintu', 'P4', tcr - 0.35, 0.70, 2.10)                                                           # pintu ceruk
            bukaan(dA, 'jendela', 'V1' if wkm >= 2 else 'V2', tkm - (0.80 if wkm >= 2 else 0.55), 1.60 if wkm >= 2 else 1.10, 0.45, 1.80)      # ventilasi KM
            bukaan(dA, 'pintu', 'P4', tcr - 0.35, 0.70, 2.10)                                                           # pintu ceruk ke tempat jemur
            # depan: PJ2 (pintu 70 + kaca mati 75) di sisi KM, J1 (2 × 75) di sisi lain bila bay ≥ 4,5 m
            if sisi == 'timur':
                xp = x1 - 0.40 - 1.45
                bukaan(dC, 'pintu', 'PJ2', xp + 0.75, 0.70, 2.10); bukaan(dC, 'jendela', 'PJ2', xp, 0.75, 2.10)
                if x1 - x0 >= 4.5: bukaan(dC, 'jendela', 'J1', x0 + 0.50, 1.60, 1.20, 0.90)
            else:
                xp = x0 + 0.40
                bukaan(dC, 'pintu', 'PJ2', xp, 0.70, 2.10); bukaan(dC, 'jendela', 'PJ2', xp + 0.70, 0.75, 2.10)
                if x1 - x0 >= 4.5: bukaan(dC, 'jendela', 'J1', x1 - 0.50 - 1.60, 1.60, 1.20, 0.90)
    lantai_tipikal(0, g_l1, Z2 - 0.60, Z2 - 0.30, Z2 - 0.12, 1)
    lantai_tipikal(Z2, g_l2, Z_RB - 0.35 - Z2, Z_RB - 0.20 - Z2, Z_RB - 0.20 - Z2, 2)

    # lantai
    for i, (x0, x1, sisi) in enumerate(KAMAR, 1):
        kx0, kx1 = batas_km(x0, x1, sisi); cx0, cx1 = (x0, kx0) if sisi == 'timur' else (kx1, x1)
        lantai(f'Lantai Kamar {i}', rect(x0, x1, VB, VC), -0.10, 0.10, 'ruang', 'k40', g_l1)
        lantai(f'Lantai KM {i}', rect(kx0, kx1, VA, VB), -0.12, 0.10, 'km', 'k20', g_l1)
        lantai(f'Lantai ceruk {i}', rect(cx0, cx1, VA, VB), -0.10, 0.10, 'ruang', 'k40', g_l1)
        simbol('kasur1', x0 + 0.75 if sisi == 'timur' else x1 - 0.75, Y(5.1))
        simbol('kasur1', x1 - 0.75 if sisi == 'timur' else x0 + 0.75, Y(5.1))
        simbol('lemari', (x0 + x1) / 2, Y(2.45))
        simbol('klosetJongkok', kx0 + 0.5, Y(0.6))
        if kx1 - kx0 >= 2.0: simbol('bakMandi', kx1 - 0.45, Y(0.5))
        teks('Kamar Tidur', (x0 + x1) / 2, Y(4.4)); teks('KM/WC', (kx0 + kx1) / 2, Y(1.0))
    lantai('Lantai teras', rect(-0.2, BLOK[0] if kunci == 'selatan' else 37.2, VC, VD + 0.3), -0.12, 0.10, 'teras', 'k30', g_l1)
    lantai('Tempat jemur', rect(-2.0, 37.2, -3.0, VA), -0.15, 0.10, 'teras', 'plester', g_l1)
    teks('Teras', 18.5, Y(7.2)); teks('Tempat jemur', 18.5, Y(-1.6))
    # plat lantai 2, keramik, railing balkon
    tambah('W', {'jenis': 'plat', 'nama': f'Plat lantai 2 {W["nama"]} (12 cm K-250)', 'z0': Z2 - 0.12, 'tebal': 0.12, 'fc': 20.75, 'tul': {'d': 10, 's': 0.12},
                 'alas': [P(*q) for q in (rect(0, 37.0, -1.25, VD + 0.15) if kunci == 'utara' else [(0, Y(-1.25)), (37.0, Y(-1.25)), (37.0, YC), (BLOK[0], YC), (BLOK[0], Y(VD + 0.15)), (0, Y(VD + 0.15))])]}, g_str)
    lantai('Keramik lantai 2', rect(0, 37.0, -1.25, VD + 0.15) if kunci == 'utara' else [(0, Y(-1.25)), (37.0, Y(-1.25)), (37.0, YC), (BLOK[0], YC), (BLOK[0], Y(VD + 0.15)), (0, Y(VD + 0.15))], Z2, 0.02, 'ruang', 'k40', g_l2)
    dinding((0, Y(VD + 0.1)), (BLOK[0] if kunci == 'selatan' else 37.0, Y(VD + 0.1)), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon depan lt.2')
    dinding((0, Y(-1.2)), (37.0, Y(-1.2)), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon belakang lt.2')
    for x in (0, 37.0): dinding((x, Y(-1.2)), (x, YA), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon belakang')
    dinding((0, YC), (0, Y(VD + 0.1)), Z2, 1.0, g_l2, tebal=0.10, nama='Railing balkon depan barat')
    # plafon dan atap
    for z, lt in ((3.50, 1), (7.35, 2)):
        tambah('P', {'jenis': 'plafon', 'nama': f'Plafon kamar lt.{lt}', 'alas': [P(*q) for q in rect(0, 37.0, VA, VC)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g_atap)
        tambah('P', {'jenis': 'plafon', 'nama': f'Plafon teras lt.{lt}', 'alas': [P(*q) for q in rect(0, BLOK[0] if kunci == 'selatan' else 37.0, VC, VD)], 'z0': z, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g_atap)
    KUDA = {'kaki': [0.05, 0.10], 'tarik': [0.05, 0.10], 'makelar': [0.05, 0.10], 'tiang': [0.05, 0.10], 'sokong': [0.025, 0.10], 'skor': [0.025, 0.10],
            'gording': [0.05, 0.10], 'bubungan': [0.05, 0.10], 'klos': [0.05, 0.05], 'lisMundur': 0.20, 'jarakGording': 0.8}
    def atap(nama, x0, x1, v0, v1, jarak, miring=35):
        y0, y1 = sorted((Y(v0), Y(v1)))
        tambah('A', {'jenis': 'atap', 'nama': nama, 'bentuk': 'limas', 'x0': x0, 'y0': r2(y0), 'x1': x1, 'y1': r2(y1), 'z0': Z_RB, 'kemiringan': miring, 'overstek': 1.2,
                     'arah': 'x', 'penutup': 'spandek', 'rangka': 'kayu', 'jarakKuda': jarak, 'tebal': 0.1, 'lisplang': 'papan', 'kuda': KUDA}, g_atap)
    if kunci == 'selatan':
        atap('Atap limas barat K1 (nok +11,00)', 0, X_JOG, VA, VD, 3.3)                 # Rencana Konstruksi Atap: K1 jarak 330
        atap('Atap limas timur K3 (nok ±11,5, menutup blok)', X_JOG, 37.0, VA, BLOK[3], 2.92, 30)   # lebih landai agar nok ±11,5 seperti potongan S.01   # K3 jarak 292, lebih dalam 2,70 ke utara
    else:
        atap(f'Atap limas {W["nama"]}', 0, 37.0, VA, VD, 3.3)

sayap('selatan')
sayap('utara')

# ---------- blok ruang tamu / tangga (lt.1: teras + 2,70 di depan dua kamar timur; lt.2: ruang rekreasi) ----------
bx0, bx1, by0, by1 = BLOK
g_blok = grup('Blok ruang tamu & tangga')
H_BLOK = Z_RB - 0.35                                   # dinding sampai bawah ring balk, atap limas timur menutup blok
dW = dinding((bx0, VD, ), (bx0, by1), 0, H_BLOK, g_blok, nama='Dinding barat blok (sisi lorong)')          # dari kolom teras ke utara
dT = dinding((bx1, VD), (bx1, by1), 0, H_BLOK, g_blok, nama='Dinding timur blok (entrance)')
dU = dinding((bx0, by1), (bx1, by1), 0, H_BLOK, g_blok, nama='Dinding utara blok (sisi lorong)')
dT1 = dinding((bx1, VC), (bx1, VD), 0, H_BLOK, g_blok, nama='Dinding timur blok bagian teras')
dinding((bx0, VC), (bx0, VD), 0, H_BLOK, g_blok, nama='Dinding barat blok bagian teras')
# KM/WC blok 2,30 × 2,00 di sudut barat laut
dinding((bx0 + 2.3, by1 - 2.0), (bx0 + 2.3, by1), 0, Z2 - 0.12, g_blok, tebal=0.10, nama='Sekat KM blok')
dKM = dinding((bx0, by1 - 2.0), (bx0 + 2.3, by1 - 2.0), 0, Z2 - 0.12, g_blok, tebal=0.10, nama='Sekat KM blok')
bukaan(dKM, 'pintu', 'P4', bx0 + 1.3, 0.70, 2.10)
# fasad timur (Tampak Depan): kaca tinggi PJ1 + kisi di atasnya di bagian selatan; pintu P2 + kaca samping; 3 celah kaca; papan nama
ye = by1 - 1.35                                        # as pintu masuk (entrance 2,25 → pintu 1,50 + kaca 2 × 0,60 = 2,70 dipusatkan)
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'PJ1', 'dinding': dT, 'jarak': r2(VD + 0.4 - VD), 'lebar': 1.10, 'tinggi': 5.80, 'ambang': 0.10})
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'V1', 'dinding': dT, 'jarak': r2(0.15), 'lebar': 1.60, 'tinggi': 0.45, 'ambang': 6.40})
tambah('B', {'jenis': 'bukaan', 'tipe': 'pintu', 'kode': 'P2', 'dinding': dT, 'jarak': r2(ye - VD - 0.75), 'lebar': 1.50, 'tinggi': 2.10, 'ambang': 0})
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'P2', 'dinding': dT, 'jarak': r2(ye - VD - 1.35), 'lebar': 0.60, 'tinggi': 2.10, 'ambang': 0})
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'P2', 'dinding': dT, 'jarak': r2(ye - VD + 0.75), 'lebar': 0.60, 'tinggi': 2.10, 'ambang': 0})
for dy in (-0.9, 0.0, 0.9):
    tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'V3', 'dinding': dT, 'jarak': r2(ye - VD + dy - 0.125), 'lebar': 0.25, 'tinggi': 0.80, 'ambang': 3.05})
# sisi lorong (utara): kaca tinggi PJ1 yang sama + kisi
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'PJ1', 'dinding': dU, 'jarak': r2(bx1 - 0.4 - 1.10 - bx0), 'lebar': 1.10, 'tinggi': 5.80, 'ambang': 0.10})
tambah('B', {'jenis': 'bukaan', 'tipe': 'jendela', 'kode': 'J3', 'dinding': dU, 'jarak': r2(3.0), 'lebar': 2.35, 'tinggi': 1.20, 'ambang': Z2 + 0.90})
# kanopi dak +4,00 (tebal 12, menjorok 1,20) dengan band tepi 50 cm, dan papan nama ASRAMA PUTRI (panel tipis di dinding timur lt.2)
tambah('W', {'jenis': 'plat', 'nama': 'Kanopi dak entrance (12 cm)', 'z0': Z2 - 0.12, 'tebal': 0.12, 'fc': 18.7, 'tul': {'d': 8, 's': 0.15},
             'alas': [P(bx1, VD + 1.9), P(bx1 + 1.2, VD + 1.9), P(bx1 + 1.2, by1 + 0.15), P(bx1, by1 + 0.15)]}, g_blok)
dinding((bx1 + 1.14, VD + 1.9), (bx1 + 1.14, by1 + 0.15), Z2 - 0.50, 0.50, g_blok, tebal=0.12, nama='Band kanopi')
dinding((bx1 + 0.08, VD + 1.9), (bx1 + 0.08, by1 - 0.3), Z2 + 0.5, 2.6, g_blok, tebal=0.06, nama='Papan nama ASRAMA PUTRI (panel)')
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'ASRAMA PUTRI', 'titik': {'x': bx1 + 0.15, 'y': r2((VD + 1.9 + by1) / 2), 'z': 5.9}, 'pada': 'tampak'})
lantai('Lantai ruang tamu', [(bx0, VC), (bx1, VC), (bx1, by1), (bx0, by1)], -0.10, 0.10, 'ruang', 'k40', g_blok)
lantai('Lantai KM blok', [(bx0, by1 - 2.0), (bx0 + 2.3, by1 - 2.0), (bx0 + 2.3, by1), (bx0, by1)], -0.12, 0.10, 'km', 'k20', g_blok)
lantai('Teras entrance', [(bx1, VD + 1.9), (TERAS_MASUK[1], VD + 1.9), (TERAS_MASUK[1], by1), (bx1, by1)], -0.12, 0.10, 'teras', 'k30', g_blok)
# tangga lurus sejajar dinding kamar (dari barat naik ke timur), void di plat
YT0 = VC + 0.5
tambah('Y', {'jenis': 'tangga', 'nama': 'Tangga ke lantai 2', 'awal': P(bx0 + 1.2, YT0), 'arah': 0, 'lebar': 1.2, 'tinggi': Z2, 'jumlahAnak': 22, 'antrede': 0.26,
             'tebalPlat': 0.12, 'z0': 0, 'fc': 18.7, 'tul': {'d': 10, 's': 0.15}, 'railing': 'kiri'}, g_blok)
void = [(bx0 + 1.1, YT0 - 0.05), (bx0 + 1.2 + 0.26 * 21 + 0.3, YT0 - 0.05), (bx0 + 1.2 + 0.26 * 21 + 0.3, YT0 + 1.25), (bx0 + 1.1, YT0 + 1.25)]
tambah('W', {'jenis': 'plat', 'nama': 'Plat lantai 2 blok (12 cm K-250)', 'z0': Z2 - 0.12, 'tebal': 0.12, 'fc': 20.75, 'tul': {'d': 10, 's': 0.12},
             'alas': [P(bx0, VC), P(bx1, VC), P(bx1, by1), P(bx0, by1)], 'lubang': [[P(*q) for q in void]]}, g_blok)
dinding((bx0 + 1.1, YT0 + 1.3), (bx0 + 1.2 + 0.26 * 21 + 0.3, YT0 + 1.3), Z2, 1.0, g_blok, tebal=0.10, nama='Railing void tangga')
dinding((bx0 + 1.1, YT0 - 0.1), (bx0 + 1.1, YT0 + 1.3), Z2, 1.0, g_blok, tebal=0.10, nama='Railing void tangga')
for x in (bx0, (bx0 + bx1) / 2, bx1): kolom_lengkap(x, by1, 'R2', g_blok)
for x in (bx0, (bx0 + bx1) / 2, bx1):
    tambah('R', balok('ringbalk', (x, VD), (x, by1), 0.20, 0.30, Z2 - 0.30, 'Balok lantai blok BL2 20/30', 6, 16), g_blok)
    tambah('R', balok('ringbalk', (x, VD), (x, by1), 0.20, 0.30, Z_RB - 0.30, 'Ring balk blok RB1 20/30', 6, 16), g_blok)
tambah('R', balok('ringbalk', (bx0, by1), (bx1, by1), 0.20, 0.30, Z2 - 0.30, 'Balok lantai blok BL2 20/30', 6, 16), g_blok)
tambah('R', balok('ringbalk', (bx0, by1), (bx1, by1), 0.20, 0.30, Z_RB - 0.30, 'Ring balk blok RB1 20/30', 6, 16), g_blok)
tambah('P', {'jenis': 'plafon', 'nama': 'Plafon ruang tamu lt.1', 'alas': [P(bx0, VC), P(bx1, VC), P(bx1, by1), P(bx0, by1)], 'z0': 3.50, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g_blok)
tambah('P', {'jenis': 'plafon', 'nama': 'Plafon ruang rekreasi lt.2', 'alas': [P(bx0, VC), P(bx1, VC), P(bx1, by1), P(bx0, by1)], 'z0': 7.35, 'bahan': 'tripleks4', 'rangka': 'kayu', 'lis': 'kayu'}, g_blok)
simbol('klosetJongkok', bx0 + 0.5, by1 - 0.6); simbol('bakMandi', bx0 + 1.8, by1 - 1.5)
simbol('sofa', bx0 + 6.0, by1 - 1.0, 0)
teks('Ruang tamu', bx0 + 5.5, by1 - 2.2); teks('Entrance', TERAS_MASUK[1] - 0.9, ye)
tambah('N', {'jenis': 'anotasi', 'tipe': 'teks', 'teks': 'Ruang rekreasi', 'titik': {'x': bx0 + 5.5, 'y': r2(by1 - 2.2), 'z': Z2}, 'pada': 'denah'})

# ---------- lorong di sisi utara blok menuju teras sayap utara ----------
lantai('Lorong penghubung', [(bx0, by1), (TERAS_MASUK[1], by1), (TERAS_MASUK[1], Y_UT - VD - 0.3), (bx0, Y_UT - VD - 0.3)], -0.12, 0.10, 'teras', 'k30', g_blok)
teks('Lorong', bx0 + 4.5, (by1 + Y_UT - VD) / 2)

# ---------- taman di antara dua teras ----------
g_taman = grup('Taman')
lantai('Taman', [(0.5, VD + 0.9), (bx0 - 0.6, VD + 0.9), (bx0 - 0.6, Y_UT - VD - 0.9), (0.5, Y_UT - VD - 0.9)], -0.15, 0.10, 'lain', 'plester', g_taman)
for x in (4.5, 11.0, 17.5, 24.0): simbol('pohon', x, Y_UT / 2)
lantai('Jalan setapak', [(0.5, Y_UT / 2 - 0.75), (bx0 - 0.6, Y_UT / 2 - 0.75), (bx0 - 0.6, Y_UT / 2 + 0.75), (0.5, Y_UT / 2 + 0.75)], -0.12, 0.08, 'teras', 'plester', g_taman)
teks('Taman', 14.0, VD + 1.4)

# ---------- legenda, garis potong ----------
tambah('L', {'jenis': 'gambar2d', 'bentuk': 'legenda', 'lembar': 'denah', 'tempel': 'kertas', 'titik': [{'x': 22, 'y': 215}]})
tambah('X', {'jenis': 'potong', 'nama': 'A', 'awal': P(-3, 4.0), 'akhir': P(42, 4.0), 'pandang': -1})
tambah('X', {'jenis': 'potong', 'nama': 'B', 'awal': P(9.25, -4.5), 'akhir': P(9.25, Y_UT + 4.5), 'pandang': 1})

proyek = {'format': 'rancang-proyek', 'versi': 1, 'aplikasi': 'RANCANG', 'disimpan': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'setel': {'nama': 'Asrama Putri Poltek KP Sorong', 'tebalDinding': 0.15, 'tinggiDinding': 3.4, 'kemiringanAtap': 35, 'overstekAtap': 1.2},
          'elemen': E, 'grup': GR, 'komponen': {}, 'kusen': KUSEN}
out = os.path.join(os.path.dirname(__file__), '..', 'app', 'contoh', 'asrama-putri.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(proyek, f, ensure_ascii=False, separators=(',', ':'))
print(out, len(E), 'elemen', len(GR), 'grup', len(KUSEN), 'tipe kusen')
