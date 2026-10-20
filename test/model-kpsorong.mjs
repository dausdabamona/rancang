// Model 3D Dermaga Poltek KP Sorong (TA 2020) dari "Gambar Desain Dermaga KP Sorong_Rev" (CV Bias Monarchy Konsultan).
// Sumbu: x memanjang dari pantai (x = 0) ke laut; y melintang, as A di y = 0, as B di y = 3.
// Causeway x 0–30, trestle x 30–59 (as 10…3), kepala dermaga x 59–64 (as 2 dan 1), lebar kepala y −1…16 (as A…E).
// Ukuran yang tidak terbaca di gambar (tebal pipa, tulangan balok, kemiringan tiang) diberi tanda "asumsi" di catatan.

const ZD = 3.5, TP = 0.25, ZBP = ZD - TP;              // elevasi dermaga, tebal pelat, dasar pelat
const HB = 0.45, ZBB = ZBP - HB;                         // balok 70 cm termasuk pelat → 45 cm di bawah pelat
const HPC = 0.7, ZPC = ZBB - HPC, ZK = ZPC + 0.1;        // pile cap 70 cm di bawah balok, kepala tiang masuk 10 cm
const AS = {10: 31, 9: 35, 8: 39, 7: 43, 6: 47, 5: 51, 4: 55, 3: 58, 2: 60, 1: 63};
const ASY = {A: 0, B: 3, C: 7, D: 11, E: 15};
const N_MIRING = 18;                                     // terbaca ±1:18 di tampak samping (asumsi, perlu konfirmasi)

/** Ujung tiang: −16,00 untuk as 10–7, −22,00 untuk as 6–1 dan kepala dermaga (tampak samping). */
const ujung = x => (x <= AS[7] + 0.01 ? -16 : -22);

export function modelKPSorong() {
  const el = {}, n = {};
  const id = h => h + (n[h] = (n[h] || 0) + 1);
  const tambah = (h, data) => { el[id(h)] = data; };
  const grup = {
    G1: {nama: 'Dermaga Poltek KP Sorong', induk: null, zona: {profil: 'dermaga'}},
    G2: {nama: 'Causeway', induk: 'G1'},
    G3: {nama: 'Trestle', induk: 'G1'},
    G4: {nama: 'Kepala dermaga', induk: 'G1'},
    G5: {nama: 'Perlengkapan dermaga', induk: 'G1'}
  };

  // ---- tiang + pile cap
  const tiang = (g, x, y, miring) => {
    const zu = ujung(x), tegak = ZK - zu;
    const panjang = miring ? +(tegak * Math.sqrt(1 + N_MIRING ** 2) / N_MIRING).toFixed(2) : +tegak.toFixed(2);
    tambah('Z', {jenis: 'tiang', nama: 'Tiang pancang', grup: g, bahan: 'baja', x, y, dLuar: 406.4, tebal: 12, panjang, zKepala: ZK, panjangSegmen: 12, coating: false,
      ...(miring ? {miring: {n: N_MIRING, arah: miring}} : {}),
      selimut: {atas: ZPC, bawah: -0.3, tebal: 0.075, fc: 24.9},
      catatan: `Ujung tiang ${zu.toFixed(2)} m (gambar). Tebal pipa 12 mm asumsi`});
  };
  const pc = (g, x, y, tipe) => tambah('F', {jenis: 'pondasi', tipe: 'pilecap', nama: tipe === 1 ? 'Pile cap PC-1 130×80×70' : 'Pile cap PC-2 80×80×70', grup: g, x, y,
    p: 0.8, l: tipe === 1 ? 1.3 : 0.8, tebal: HPC, z0: ZPC, tulPlat: {d: 16, s: 0.15, ulir: true}, fc: 29, selimut: 0.075});
  // PC-1 memanjang Y (pasangan tiang di y dan y+0,5, tiang miring condong ke +y)
  const pasanganY = (g, x, y) => { tiang(g, x, y); tiang(g, x, y + 0.5, 90); pc(g, x, y + 0.25, 1); };
  // PC-1 memanjang X di as 1 (tiang miring condong ke darat)
  const pasanganX = (g, x, y) => {
    tiang(g, x, y); tiang(g, x - 0.5, y, 180);
    tambah('F', {jenis: 'pondasi', tipe: 'pilecap', nama: 'Pile cap PC-1 130×80×70', grup: g, x: x - 0.25, y, p: 1.3, l: 0.8, tebal: HPC, z0: ZPC, tulPlat: {d: 16, s: 0.15, ulir: true}, fc: 29, selimut: 0.075});
  };
  const tunggal = (g, x, y) => { tiang(g, x, y); pc(g, x, y, 2); };

  // trestle: as 10…3, garis A dan B; pasangan miring di A pada as 9, 7, 5, 3
  for (const a of [10, 9, 8, 7, 6, 5, 4, 3]) {
    const x = AS[a];
    if ([9, 7, 5, 3].includes(a)) pasanganY('G3', x, ASY.A); else tunggal('G3', x, ASY.A);
    tunggal('G3', x, ASY.B);
  }
  // kepala: as 2 → A pasangan-Y, B…E tunggal; as 1 → A, C, E pasangan-X, B, D tunggal
  pasanganY('G4', AS[2], ASY.A);
  for (const k of ['B', 'C', 'D', 'E']) tunggal('G4', AS[2], ASY[k]);
  for (const k of ['A', 'B', 'C', 'D', 'E']) (['A', 'C', 'E'].includes(k) ? pasanganX : tunggal)('G4', AS[1], ASY[k]);

  // ---- balok (ringbalk peran balok: z0 = dasar balok)
  const balok = (g, nama, a, b, lebar, tul) => tambah('R', {jenis: 'ringbalk', peran: 'balok', nama, grup: g, awal: {x: a[0], y: a[1]}, akhir: {x: b[0], y: b[1]},
    b: lebar, h: HB, z0: ZBB, tul: {...tul, ulir: true}, sengkang: {d: 10, s: 0.15}, fc: 29, selimut: 0.05});
  const UT = {n: 8, d: 19}, TP_ = {n: 6, d: 16};
  // trestle: utama 40/70 di A dan B serta melintang di tiap as; tepi 25/70 di y −1, y 4 dan pangkal x 30
  balok('G3', 'Balok utama 40/70 as A', [30, 0], [59, 0], 0.4, UT);
  balok('G3', 'Balok utama 40/70 as B', [30, 3], [59, 3], 0.4, UT);
  for (const a of [10, 9, 8, 7, 6, 5, 4, 3]) balok('G3', `Balok utama 40/70 as ${a}`, [AS[a], -1], [AS[a], 4], 0.4, UT);
  balok('G3', 'Balok tepi 25/70 sisi A', [30, -0.875], [59, -0.875], 0.25, TP_);
  balok('G3', 'Balok tepi 25/70 sisi B', [30, 3.875], [58, 3.875], 0.25, TP_);
  balok('G3', 'Balok tepi 25/70 pangkal', [30.125, -1], [30.125, 4], 0.25, TP_);
  // balok dudukan tiang lampu 40/45 di luar sisi B (jalur utilitas)
  tambah('R', {jenis: 'ringbalk', peran: 'balok', nama: 'Balok dudukan tiang lampu 40/45', grup: 'G3', awal: {x: 30, y: 4.2}, akhir: {x: 58, y: 4.2},
    b: 0.4, h: 0.45, z0: ZD - 0.4 - 0.45, tul: {n: 6, d: 16, ulir: true}, sengkang: {d: 10, s: 0.15}, fc: 29, selimut: 0.05});
  // kepala: utama di as 2 dan 1 (memanjang Y) dan di A…E (melintang X); tepi keliling
  balok('G4', 'Balok utama 40/70 as 2', [AS[2], -1], [AS[2], 16], 0.4, UT);
  balok('G4', 'Balok utama 40/70 as 1', [AS[1], -1], [AS[1], 16], 0.4, UT);
  for (const k of ['A', 'B', 'C', 'D', 'E']) balok('G4', `Balok utama 40/70 as ${k}`, [59, ASY[k]], [64, ASY[k]], 0.4, UT);
  balok('G4', 'Balok tepi 25/70 sisi laut', [63.875, -1], [63.875, 16], 0.25, TP_);
  balok('G4', 'Balok tepi 25/70 sisi darat', [59.125, -1], [59.125, 16], 0.25, TP_);
  balok('G4', 'Balok tepi 25/70 ujung A', [59, -0.875], [64, -0.875], 0.25, TP_);
  balok('G4', 'Balok tepi 25/70 ujung E', [59, 15.875], [64, 15.875], 0.25, TP_);

  // ---- pelat lantai (z0 = dasar pelat), tulangan D16-150 (lembar 06)
  tambah('W', {jenis: 'plat', nama: 'Pelat lantai trestle t.25', grup: 'G3', alas: [{x: 30, y: -1}, {x: 58.97, y: -1}, {x: 58.97, y: 4}, {x: 30, y: 4}], z0: ZBP, tebal: TP, fc: 29, tul: {d: 16, s: 0.15, ulir: true}});
  tambah('W', {jenis: 'plat', nama: 'Pelat lantai kepala t.25', grup: 'G4', alas: [{x: 59, y: -1}, {x: 64, y: -1}, {x: 64, y: 16}, {x: 59, y: 16}, {x: 59, y: 5}, {x: 58.97, y: 4.97}, {x: 58.97, y: 4}, {x: 59, y: 4}], z0: ZBP, tebal: TP, fc: 29, tul: {d: 16, s: 0.15, ulir: true},
    catatan: 'Celah dilatasi ±3 cm di pertemuan trestle'});

  // ---- causeway: puncak 5,0 m + kansten 2×0,2 m, talud 1:2, elevasi +3,50
  tambah('U', {jenis: 'timbunan', nama: 'Causeway', grup: 'G2', awal: {x: 0, y: 1.5}, akhir: {x: 30, y: 1.5}, lebarAtas: 5.4, zAtas: ZD, talud: 2,
    catatan: 'Lantai beton t.15 + sirtu t.25 di atas timbunan pilihan; talud pasangan batu (lembar 13)'});

  // ---- perlengkapan
  const zL = ZD;
  const bolder = (x, y, rotasi) => tambah('O', {jenis: 'perlengkapan', tipe: 'bolder', nama: 'Bollard', grup: 'G5', kapasitas: 15, x, y, z0: zL, rotasi});
  bolder(AS[9], -0.6, 0); bolder(AS[5], -0.6, 0);
  bolder(AS[1], ASY.A, 270); bolder(AS[1], ASY.D, 270); bolder(AS[1], ASY.E, 270);
  for (const k of ['A', 'C', 'E']) tambah('O', {jenis: 'perlengkapan', tipe: 'fender', nama: 'Fender V 600H', grup: 'G5', model: 'V 600H', panjang: 1.5, x: 64, y: ASY[k], z0: zL, rotasi: 270});
  tambah('O', {jenis: 'perlengkapan', tipe: 'fender', nama: 'Fender V 600H', grup: 'G5', model: 'V 600H', panjang: 1.5, x: AS[2], y: -1, z0: zL, rotasi: 0});
  for (const x of [35, 43, 51]) tambah('O', {jenis: 'perlengkapan', tipe: 'pju', nama: 'PJU', grup: 'G5', tinggi: 6, x, y: 4.2, z0: zL, rotasi: 180});

  // ---- elevasi muka air dan profil dasar laut (stasiun tampak samping, lembar 04)
  tambah('M', {jenis: 'level', nama: 'HWS', datum: 'hwl', z: 2.18});
  tambah('M', {jenis: 'level', nama: 'MSL', datum: 'msl', z: 1.09});
  tambah('M', {jenis: 'level', nama: 'LWS', datum: 'lwl', z: 0});
  tambah('M', {jenis: 'level', nama: 'Dasar laut', datum: 'dasar', z: -10.1, profil: {awal: {x: 0, y: 0}, akhir: {x: 70, y: 0},
    titik: [[0, 0.5], [25, -0.436], [35, -2.211], [45, -4.572], [55, -6.935], [65, -9.074], [70, -10.108]]}});
  // ---- garis potong
  tambah('X', {jenis: 'potong', nama: 'A', awal: {x: 41, y: 6}, akhir: {x: 41, y: -3}, pandang: 1, dalam: 2});
  tambah('X', {jenis: 'potong', nama: 'B', awal: {x: -3, y: 0.25}, akhir: {x: 67, y: 0.25}, pandang: -1});
  tambah('X', {jenis: 'potong', nama: 'C', awal: {x: 61.5, y: 18}, akhir: {x: 61.5, y: -3}, pandang: 1, dalam: 2});
  tambah('X', {jenis: 'potong', nama: 'D', awal: {x: 15, y: 8}, akhir: {x: 15, y: -5}, pandang: 1, dalam: 2});

  const setel = {nama: 'Dermaga Politeknik KP Sorong (model ulang dari gambar TA 2020)', faktorBesi: 5,
    sampul: {lokasi: 'Politeknik Kelautan dan Perikanan Sorong', pemilik: 'Politeknik KP Sorong', tahun: '2020', penggambar: 'Firdaus Dabamona'}, kop: {kodeLembar: 'PKP'}};
  return {setel, grup, elemen: el};
}
