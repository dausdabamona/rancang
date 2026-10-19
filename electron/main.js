// Proses utama RANCANG desktop: jendela aplikasi, berkas proyek .rancang, menu, dan jembatan MCP.
'use strict';
const {app, BrowserWindow, ipcMain, dialog, Menu, shell} = require('electron');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {Proyek} = require('./penyimpanan');
const {mulaiJembatan} = require('./jembatan');

const UJI_ASAP = process.argv.includes('--uji-asap');
const EKSTENSI = '.rancang';
const VERSI = app.getVersion();

// RANCANG_DATA_DIR: folder data lain (dipakai uji otomatis dan server MCP yang sama)
if (process.env.RANCANG_DATA_DIR) app.setPath('userData', process.env.RANCANG_DATA_DIR);
else if (UJI_ASAP) app.setPath('userData', fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-uji-')));
// WebGL: bila kartu grafis tidak didukung (laptop kantor lama, mesin CI), Chromium memakai SwiftShader (perangkat lunak)
app.commandLine.appendSwitch('enable-unsafe-swiftshader');
if (UJI_ASAP) { app.commandLine.appendSwitch('use-angle', 'swiftshader'); app.commandLine.appendSwitch('ignore-gpu-blocklist'); }
const dataApp = () => app.getPath('userData');
const berkasSetelan = () => path.join(dataApp(), 'pengaturan-desktop.json');
const berkasJembatan = () => path.join(dataApp(), 'mcp-jembatan.json');

const proyek = new Proyek();
let jendela = null;
let jembatan = null;
let siapHalaman = null; // Promise yang selesai saat halaman memuat rancangAPI

/* ============ Setelan desktop ============ */
function bacaSetelan() {
  try { return JSON.parse(fs.readFileSync(berkasSetelan(), 'utf8')); } catch { return {}; }
}
function tulisSetelan(ubah) {
  const s = {...bacaSetelan(), ...ubah};
  try {
    fs.mkdirSync(dataApp(), {recursive: true});
    fs.writeFileSync(berkasSetelan(), JSON.stringify(s, null, 1));
  } catch (err) { console.error('[setelan] gagal menulis', err); }
}
function berkasDariArgv(argv) {
  return argv.slice(1).find(a => a.toLowerCase().endsWith(EKSTENSI) && fs.existsSync(a)) || null;
}
function proyekAwal() {
  const dariArgv = berkasDariArgv(process.argv);
  if (dariArgv) return dariArgv;
  const s = bacaSetelan();
  if (s.terakhir && fs.existsSync(s.terakhir)) return s.terakhir;
  const folder = UJI_ASAP ? dataApp() : path.join(app.getPath('documents'), 'RANCANG');
  return path.join(folder, 'Proyek baru' + EKSTENSI);
}

/* ============ Jendela ============ */
function judul() {
  return `${proyek.jalur ? path.basename(proyek.jalur, EKSTENSI) : 'Tanpa nama'} — RANCANG ${VERSI}`;
}
function muatHalaman() {
  siapHalaman = new Promise((ok, gagal) => {
    const batas = setTimeout(() => gagal(new Error('Halaman RANCANG tidak siap dalam 60 detik.')), 60000);
    const cek = async () => {
      if (!jendela || jendela.isDestroyed()) return;
      try {
        const siap = await jendela.webContents.executeJavaScript('!!(window.rancangAPI && window.rancangAPI.siap())');
        if (siap) { clearTimeout(batas); ok(); return; }
      } catch (_) { /* halaman masih memuat */ }
      setTimeout(cek, 150);
    };
    jendela.webContents.once('did-finish-load', cek);
  });
  siapHalaman.catch(err => console.error('[halaman]', err.message));
  jendela.loadFile(path.join(__dirname, '..', 'build', 'renderer', 'index.html'));
  jendela.setTitle(judul());
  return siapHalaman;
}
function buatJendela() {
  jendela = new BrowserWindow({
    width: 1440, height: 900, minWidth: 960, minHeight: 600,
    title: judul(), show: !UJI_ASAP, backgroundColor: '#ECEEEC',
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    webPreferences: {preload: path.join(__dirname, 'preload.js'), contextIsolation: true, sandbox: true, nodeIntegration: false, spellcheck: false}
  });
  // tautan luar dibuka di browser; halaman tidak boleh berpindah ke alamat lain
  jendela.webContents.setWindowOpenHandler(({url}) => {
    if (/^https?:\/\//.test(url)) shell.openExternal(url);
    return {action: 'deny'};
  });
  jendela.webContents.on('will-navigate', e => e.preventDefault());
  // uji asap: teruskan pesan galat halaman ke log CI
  if (UJI_ASAP) {
    jendela.webContents.on('console-message', (e, ...lama) => { const lv = e.level ?? lama[0], msg = e.message ?? lama[1]; if (lv === 'error' || lv === 'warning' || lv >= 2) console.log('[halaman]', msg); });
    jendela.webContents.on('preload-error', (_e, p, err) => console.log('[preload]', p, err && err.message));
  }
  jendela.on('page-title-updated', e => { e.preventDefault(); jendela.setTitle(judul()); });
  jendela.on('closed', () => { jendela = null; });
  return muatHalaman();
}

/* ============ Proyek ============ */
function bukaProyek(jalur) {
  const abs = proyek.buka(jalur);
  tulisSetelan({terakhir: abs});
  app.addRecentDocument?.(abs);
  if (jembatan) jembatan.perbaruiInfo();
  return jendela ? muatHalaman() : Promise.resolve();
}
async function dialogBuka() {
  const r = await dialog.showOpenDialog(jendela, {title: 'Buka proyek RANCANG', properties: ['openFile'],
    filters: [{name: 'Proyek RANCANG', extensions: ['rancang']}, {name: 'Proyek .json (dari artifact)', extensions: ['json']}]});
  if (r.canceled || !r.filePaths[0]) return;
  const pilih = r.filePaths[0];
  try {
    if (pilih.toLowerCase().endsWith('.json')) {
      // berkas Simpan proyek dari versi artifact: disalin menjadi .rancang di sebelahnya
      const tujuan = pilih.replace(/\.json$/i, EKSTENSI);
      if (fs.existsSync(tujuan)) {
        const t = await dialog.showMessageBox(jendela, {type: 'question', buttons: ['Timpa', 'Batal'], defaultId: 1, cancelId: 1,
          message: `${path.basename(tujuan)} sudah ada.`, detail: 'Timpa dengan isi berkas .json yang dipilih?'});
        if (t.response !== 0) return;
      }
      fs.copyFileSync(pilih, tujuan);
      await bukaProyek(tujuan);
    } else await bukaProyek(pilih);
  } catch (err) {
    dialog.showErrorBox('Proyek gagal dibuka', err.message);
  }
}
async function dialogBaru() {
  const r = await dialog.showSaveDialog(jendela, {title: 'Proyek baru', buttonLabel: 'Buat',
    defaultPath: path.join(path.dirname(proyek.jalur || app.getPath('documents')), 'Proyek baru' + EKSTENSI),
    filters: [{name: 'Proyek RANCANG', extensions: ['rancang']}]});
  if (r.canceled || !r.filePath) return;
  if (fs.existsSync(r.filePath)) fs.rmSync(r.filePath);
  await bukaProyek(r.filePath);
}
async function dialogSimpanSebagai() {
  const r = await dialog.showSaveDialog(jendela, {title: 'Simpan proyek sebagai', defaultPath: proyek.jalur,
    filters: [{name: 'Proyek RANCANG', extensions: ['rancang']}]});
  if (r.canceled || !r.filePath) return;
  simpanSebagai(r.filePath);
}
function simpanSebagai(jalur) {
  const abs = proyek.simpanSebagai(jalur);
  tulisSetelan({terakhir: abs});
  if (jembatan) jembatan.perbaruiInfo();
  if (jendela) jendela.setTitle(judul());
  return abs;
}

proyek.on('ubahLuar', selisih => {
  if (!jendela) return;
  for (const [koleksi, perubahan] of Object.entries(selisih.koleksi)) jendela.webContents.send('db:ubah', {koleksi, perubahan});
  if (selisih.setel) jendela.webContents.send('db:setel', selisih.setel);
});
proyek.on('galat', err => { if (jendela) dialog.showErrorBox('RANCANG', err.message); });

/* ============ IPC ============ */
ipcMain.handle('db:awal', () => proyek.awal());
ipcMain.handle('db:set', (_e, koleksi, id, data) => { proyek.set(koleksi, id, data); return true; });
ipcMain.handle('db:setel', (_e, data) => { proyek.setel(data); return true; });
ipcMain.handle('unduh:simpan', async (_e, {filename, data}) => {
  const nama = path.basename(String(filename || 'berkas'));
  const r = await dialog.showSaveDialog(jendela, {title: 'Simpan berkas', defaultPath: path.join(app.getPath('documents'), nama)});
  if (r.canceled || !r.filePath) return {ok: false, code: 'declined'};
  try {
    fs.writeFileSync(r.filePath, typeof data === 'string' ? data : Buffer.from(data));
    return {ok: true};
  } catch (err) {
    return {ok: false, code: 'gagal', pesan: err.message};
  }
});

/* ============ Metode jembatan MCP ============ */
async function halaman(ekspresi) {
  if (!jendela) throw new Error('Jendela RANCANG tidak terbuka.');
  await siapHalaman;
  const teks = await jendela.webContents.executeJavaScript(`(async () => JSON.stringify(await (${ekspresi})))()`);
  return teks === undefined ? null : JSON.parse(teks);
}
const arg = x => JSON.stringify(x ?? null);
const metode = {
  info: async () => {
    const d = proyek.data;
    return {aplikasi: 'RANCANG', versi: VERSI, proyek: proyek.jalur, setel: d.setel,
      jumlah: {elemen: Object.keys(d.elemen).length, grup: Object.keys(d.grup).length, komponen: Object.keys(d.komponen).length, kusen: Object.keys(d.kusen).length},
      jenisGambar: await halaman('window.rancangAPI.jenisGambar2D()')};
  },
  model: async () => ({proyek: proyek.jalur, ...proyek.awal()}),
  pilihan: () => halaman('window.rancangAPI.pilihan()'),
  terapkan: async ({perubahan, oleh}) => {
    const r = await halaman(`window.rancangAPI.terapkanLuar(${arg(perubahan)}, ${arg(oleh || 'claude')})`);
    if (r && r.ok) proyek.simpanSekarang();
    return r;
  },
  gambar2D: ({format, ...opsi}) => halaman(format === 'png' ? `window.rancangAPI.gambar2DPng(${arg(opsi)})` : `window.rancangAPI.gambar2D(${arg(opsi)})`),
  rab: ({ids}) => halaman(`window.rancangAPI.rab(${arg(ids)})`),
  ringkasan: ({ids}) => halaman(`window.rancangAPI.ringkasan(${arg(ids)})`),
  ukur: ({id}) => halaman(`window.rancangAPI.ukurElemen(${arg(id)})`),
  pecahAtap: async ({id}) => {
    const r = await halaman(`window.rancangAPI.pecahAtap(${arg(id)})`);
    if (r && r.ok) proyek.simpanSekarang();
    return r;
  },
  tangkap3D: async ({tampilan}) => {
    if (jendela && !jendela.isVisible() && !UJI_ASAP) jendela.show();
    return halaman(`window.rancangAPI.tangkap3D(${arg({tampilan, semua: !!tampilan})})`);
  },
  buka: async ({jalur}) => {
    if (!jalur || !String(jalur).toLowerCase().endsWith(EKSTENSI)) throw new Error('Jalur harus berkas .rancang');
    await bukaProyek(jalur);
    return {proyek: proyek.jalur};
  },
  simpanSebagai: async ({jalur}) => {
    if (!jalur || !String(jalur).toLowerCase().endsWith(EKSTENSI)) throw new Error('Jalur harus berkas .rancang');
    return {proyek: simpanSebagai(jalur)};
  }
};

/* ============ Menu ============ */
function pasangMenu() {
  const tpl = [
    {label: 'Berkas', submenu: [
      {label: 'Proyek baru…', accelerator: 'CmdOrCtrl+N', click: dialogBaru},
      {label: 'Buka proyek…', accelerator: 'CmdOrCtrl+Shift+O', click: dialogBuka},
      {label: 'Simpan sebagai…', accelerator: 'CmdOrCtrl+Shift+S', click: dialogSimpanSebagai},
      {type: 'separator'},
      {label: 'Tampilkan berkas proyek di folder', click: () => proyek.jalur && shell.showItemInFolder(proyek.jalur)},
      {type: 'separator'},
      {label: 'Keluar', role: 'quit'}
    ]},
    {label: 'Tampilan', submenu: [
      {label: 'Muat ulang', accelerator: 'F5', click: () => jendela && muatHalaman()},
      {label: 'Layar penuh', role: 'togglefullscreen'},
      {label: 'Perbesar', role: 'zoomIn'}, {label: 'Perkecil', role: 'zoomOut'}, {label: 'Ukuran normal', role: 'resetZoom'},
      {type: 'separator'},
      {label: 'Alat pengembang', role: 'toggleDevTools'}
    ]},
    {label: 'Bantuan', submenu: [
      {label: 'Panduan dan unduhan (GitHub)', click: () => shell.openExternal('https://github.com/dausdabamona/rancang#readme')},
      {label: 'Folder data aplikasi (jembatan MCP)', click: () => shell.openPath(dataApp())},
      {label: `Tentang RANCANG ${VERSI}`, click: () => dialog.showMessageBox(jendela, {type: 'info', title: 'Tentang RANCANG',
        message: `RANCANG ${VERSI}`, detail: 'Aplikasi gambar bangunan, gambar kerja 2D, dan volume RAB.\nBerkolaborasi dengan Claude lewat MCP.\n\nFirdaus Dabamona'})}
    ]}
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(tpl));
}

/* ============ Uji asap (CI) ============ */
async function ujiAsap() {
  const hasil = {ok: false, langkah: []};
  const catat = (nama, ok, isi) => { hasil.langkah.push({nama, ok, ...(isi || {})}); if (!ok) throw new Error('Gagal: ' + nama); };
  try {
    await siapHalaman;
    catat('halaman siap', true);
    const r = await metode.terapkan({perubahan: [
      {id: 'D1', data: {jenis: 'dinding', nama: 'Dinding uji', awal: {x: 0, y: 0}, akhir: {x: 4, y: 0}, tebal: 0.15, tinggi: 3, z0: 0}},
      {id: 'D2', data: {jenis: 'dinding', nama: 'Dinding uji 2', awal: {x: 4, y: 0}, akhir: {x: 4, y: 3}, tebal: 0.15, tinggi: 3, z0: 0}},
      {id: 'B1', data: {jenis: 'bukaan', tipe: 'pintu', kode: 'P1', nama: 'Pintu uji', dinding: 'D1', jarak: 1, lebar: 0.8, tinggi: 2.1, ambang: 0}}
    ]});
    catat('terapkan perubahan', r && r.ok, {r});
    const tolak = await metode.terapkan({perubahan: [{id: 'D9', data: {jenis: 'dinding'}}]});
    catat('tolak data tidak sah', tolak && tolak.ok === false);
    const isi = JSON.parse(fs.readFileSync(proyek.jalur, 'utf8'));
    catat('tersimpan ke berkas', !!(isi.elemen.D1 && isi.elemen.B1 && isi.elemen.D1.diubahOleh === 'claude'));
    const g = await metode.gambar2D({jenis: 'denah'});
    catat('gambar denah', !!(g && g.svg && g.svg.length > 1000), {panjang: g && g.svg.length});
    const png = await metode.gambar2D({jenis: 'denah', format: 'png'});
    catat('gambar denah PNG', !!(png && /^data:image\/png;base64,/.test(png.png)));
    const rab = await metode.rab({});
    catat('volume RAB', Array.isArray(rab) && rab.length > 0, {divisi: rab.length});
    const t3 = await metode.tangkap3D({tampilan: 'iso'});
    catat('tangkap layar 3D', /^data:image\/png;base64,/.test(t3 || ''));
    // jembatan HTTP dengan token dari berkas info
    const info = JSON.parse(fs.readFileSync(berkasJembatan(), 'utf8'));
    const res = await fetch(`http://127.0.0.1:${info.port}/rpc`, {method: 'POST', headers: {'Content-Type': 'application/json', Authorization: 'Bearer ' + info.token}, body: JSON.stringify({metode: 'info'})});
    const j = await res.json();
    catat('jembatan MCP', j.ok && j.hasil.jumlah.elemen === 3, {jumlah: j.hasil && j.hasil.jumlah});
    const salah = await fetch(`http://127.0.0.1:${info.port}/rpc`, {method: 'POST', headers: {Authorization: 'Bearer salah'}, body: '{}'});
    catat('jembatan menolak token salah', salah.status === 401);
    // perubahan dari luar berkas dimuat ulang
    const luar = JSON.parse(fs.readFileSync(proyek.jalur, 'utf8'));
    luar.elemen.D2 = {...luar.elemen.D2, tinggi: 2.5, diubahOleh: 'claude'};
    fs.writeFileSync(proyek.jalur, JSON.stringify(luar));
    let tinggi = null;
    for (let i = 0; i < 40 && tinggi !== 2.5; i++) {
      await new Promise(r2 => setTimeout(r2, 250));
      tinggi = (await halaman('window.rancangAPI.model()')).elemen.D2.tinggi;
    }
    catat('muat ulang perubahan berkas dari luar', tinggi === 2.5);
    // v0.33: pilihan pengguna terbaca lewat rancangAPI dan tampil di bilah bawah
    const pil = await halaman(`(() => ({info: window.rancangUji.pilih(['D1']), pilihan: window.rancangAPI.pilihan()}))()`);
    catat('pilihan pengguna', pil.pilihan.terpilih.length === 1 && pil.pilihan.terpilih[0].id === 'D1' && /Dinding D1/.test(pil.info), {info: pil.info});
    // v0.33: kursor lewat di atas sudut dinding D1/D2 pada alat Pilih: dinding terdepan disorot, disebut di bilah bawah, lalu bersih lagi
    await halaman(`window.rancangUji.pilih([])`);
    const sorot = await halaman(`window.rancangUji.lewat(4, 1.5, 1.5)`);
    catat('sorotan kursor alat Pilih', /^D[12]$/.test(sorot.kunci) && sorot.jumlahMesh > 0 && new RegExp('Dinding ' + sorot.kunci).test(sorot.info) && sorot.bersih && sorot.kanvasTetap, sorot);
    // v0.33: panel Properti plafon: lebar X diketik → alas diskalakan dari sisi barat; perluas 0,2 → semua sisi keluar 0,2
    const rp = await metode.terapkan({perubahan: [{id: 'P1', data: {jenis: 'plafon', nama: 'Plafon uji', alas: [{x: 0, y: 0}, {x: 4, y: 0}, {x: 4, y: 3}, {x: 0, y: 3}], z0: 3, bahan: 'grc', rangka: 'hollow'}}]});
    catat('buat plafon uji', rp && rp.ok, {r: rp});
    await halaman(`window.rancangUji.pilih(['P1'])`);
    const u1 = await halaman(`window.rancangUji.isiMedan('l-lebarx', '6')`);
    const xs1 = u1.data && u1.data.alas.map(q => q.x);
    catat('ukuran alas: lebar X diketik', !!xs1 && Math.min(...xs1) === 0 && Math.max(...xs1) === 6, {alas: u1.data && u1.data.alas});
    const u2 = await halaman(`window.rancangUji.isiMedan('l-perluas', '0,2')`);
    const xs2 = u2.data && u2.data.alas.map(q => q.x), ys2 = u2.data && u2.data.alas.map(q => q.y);
    catat('ukuran alas: perluas semua sisi', !!xs2 && Math.min(...xs2) === -0.2 && Math.max(...xs2) === 6.2 && Math.min(...ys2) === -0.2 && Math.max(...ys2) === 3.2, {alas: u2.data && u2.data.alas});
    // v0.33: plafon miring bawaan atap memakai bahan/rangka pilihan dan masuk baris RAB yang sama dengan plafon datar (PL-007 PVC, PL-012 hollow), tanpa PL-004
    const ra = await metode.terapkan({perubahan: [{id: 'A1', data: {jenis: 'atap', bentuk: 'pelana', x0: 0, y0: 0, x1: 4, y1: 3, z0: 3, kemiringan: 30, overstek: 0.6, arah: 'x', rangka: 'bajaringan', plafonMiring: 'penuh', plafonBahan: 'pvc', plafonRangka: 'hollow'}}]});
    catat('buat atap berplafon miring PVC', ra && ra.ok, {r: ra});
    const rab2 = await metode.rab({});
    const baris = rab2.flatMap(dv => dv.baris), pvc = baris.find(b => b.kode === 'PL-007'), hollow = baris.find(b => b.kode === 'PL-012'), lama = baris.find(b => b.kode === 'PL-004');
    // v0.34: palet perintah mengenali alat, singkatan AutoCAD, elemen, dan lembar; tata letak ringkas/rel/fokus
    const pal1 = await halaman(`window.rancangUji.palet('tr')`), pal2 = await halaman(`window.rancangUji.palet('plaf')`), pal3 = await halaman(`window.rancangUji.palet('elemen D1')`);
    catat('palet perintah', pal1[0] && /Perpanjang/.test(pal1[0]) && pal2.some(x => x === 'Alat: Plafon') && pal2.some(x => /Elemen: Plafon P1/.test(x)) && pal3.some(x => /Elemen: Dinding D1/.test(x)), {pal1: pal1.slice(0, 2), pal2: pal2.slice(0, 4), pal3: pal3.slice(0, 2)});
    const tt1 = await halaman(`window.rancangUji.tata('ringkas', false)`), tt2 = await halaman(`window.rancangUji.tata(undefined, undefined, true)`), tt3 = await halaman(`window.rancangUji.tata(undefined, undefined, false)`);
    catat('tata letak ringkas, rel panel, mode fokus', /rail-ringkas/.test(tt1.kelas) && /panel-tutup/.test(tt1.kelas) && tt1.relTampak && tt1.panelW === '44px' && /fokus/.test(tt2.kelas) && !/fokus/.test(tt3.kelas) && /rail-ringkas/.test(tt3.kelas), {tt1, tt2, tt3});
    // v0.35: alat Tangga dua klik (pangkal di lantai 1, naik ke level +4,00 → 22 anak, optrede ≈18 cm); plat lantai beton masuk RAB; denah per level
    const rl = await metode.terapkan({perubahan: [{id: 'M1', data: {jenis: 'level', nama: 'Lantai 2', z: 4}}, {id: 'W1', data: {jenis: 'plat', alas: [{x: 0, y: 0}, {x: 4, y: 0}, {x: 4, y: 3}, {x: 0, y: 3}], z0: 3.88, tebal: 0.12}}]});
    catat('buat level dan plat lantai', rl && rl.ok, {r: rl});
    const tg = await halaman(`window.rancangUji.tangga({x: 6, y: 0, z: 0}, {x: 6, y: 5})`);
    catat('alat Tangga dua klik', !!tg.id && tg.data.jenis === 'tangga' && tg.data.jumlahAnak === 23 && tg.data.tinggi === 4 && tg.data.arah === 90 && tg.ukur.volume > 0, {id: tg.id, n: tg.data && tg.data.jumlahAnak, arah: tg.data && tg.data.arah, ukur: tg.ukur});
    const tg2 = await halaman(`window.rancangUji.isiMedan('tg-jumlahAnak', '22')`);
    catat('panel Tangga: jumlah anak diubah', tg2.data && tg2.data.jumlahAnak === 22, {n: tg2.data && tg2.data.jumlahAnak});
    const rab3 = await metode.rab({}), baris3 = rab3.flatMap(dv => dv.baris), betonPlat = baris3.find(b => b.kode === 'ST-030'), betonTangga = baris3.find(b => b.kode === 'ST-031');
    catat('RAB plat lantai dan tangga', !!betonPlat && betonPlat.vol > 0 && !!betonTangga && betonTangga.vol > 0, {plat: betonPlat && betonPlat.vol, tangga: betonTangga && betonTangga.vol});
    const dl1 = await metode.gambar2D({jenis: 'denah', level: 0}), dl2 = await metode.gambar2D({jenis: 'denah', level: 4});
    catat('denah per level', dl1.svg.length > 1000 && dl2.svg.length > 500 && /NAIK/.test(dl1.svg) && dl1.svg !== dl2.svg, {l1: dl1.svg.length, l2: dl2.svg.length});
    // v0.35: proyek contoh Asrama Putri terbaca dari build/renderer/contoh (file://) dan dimuat utuh
    const ct = await halaman(`window.rancangUji.contoh('asrama-putri', 'ganti')`);
    catat('buka contoh Asrama Putri', ct && ct.elemen > 300 && ct.kusen >= 9 && /Asrama/.test(ct.nama), {elemen: ct.elemen, kusen: ct.kusen, proyek: ct.nama});
    const dl3 = await metode.gambar2D({jenis: 'denah', level: 4});
    catat('denah lantai 2 contoh', dl3.svg.length > 20000 && /TURUN/.test(dl3.svg), {panjang: dl3.svg.length});
    // v0.36: Meteran (tanpa elemen) dan Dimensi (anotasi ukuran bergeser, tampil di denah)
    const mt = await halaman(`window.rancangUji.meteran({x: 0, y: 0, z: 0}, {x: 3, y: 4, z: 0})`);
    catat('alat Meteran', /5,00|500/.test(mt.hasil) && /ΔZ/.test(mt.hasil) && mt.elemenBaru === 0, mt);
    const mz = await halaman(`window.rancangUji.sumbuMeteran({x: 1, y: 1, z: 0}, {x: 1, y: 1, z: 2.5})`);
    const mtp = await halaman(`window.rancangUji.meteranTepi({x: 0, y: 0, z: 0}, {x: 1, y: 0, z: 0}, {x: 2, y: 1.5, z: 0})`);
    catat('Meteran: kunci sumbu Z dan garis bantu sejajar tepi', mz && mz.kunci === 'z' && Math.abs(mz.p[2] - 2.5) < 0.05 && mtp.elemenBaru === 1 && mtp.bantu && mtp.bantu.jenis === 'bantu' && Math.abs(mtp.bantu.awal.y - 1.5) < 0.01 && Math.abs(mtp.bantu.akhir.y - 1.5) < 0.01, {mz, bantu: mtp.bantu});
    const dm = await halaman(`window.rancangUji.dimensi({x: 0, y: 0, z: 0}, {x: 6, y: 0, z: 0}, 0.8)`);
    const dmSvg = await metode.gambar2D({jenis: 'denah'});
    catat('alat Dimensi', !!dm.id && dm.data && dm.data.tipe === 'ukuran' && Math.abs(Math.hypot(dm.data.geser.x, dm.data.geser.y) - 0.8) < 0.01 && dmSvg.svg.includes('data-anot="' + dm.id + '"'), {id: dm.id, geser: dm.data && dm.data.geser});
    // lembar denah per lantai: contoh Kantor Utama → Denah Lantai 1 dan Denah Lantai 2 sebagai lembar sendiri (level Ring balk dilewati)
    const ku = await halaman(`window.rancangUji.contoh('kantor-utama', 'ganti')`);
    const lbr = await halaman(`window.rancangAPI.daftarLembar().filter(l => l.jenis.startsWith('denah')).map(l => l.jenis + '|' + l.nama)`);
    const dk2 = await metode.gambar2D({jenis: 'denah:4'});
    catat('lembar denah per lantai', ku.elemen > 400 && lbr.join() === 'denah:0|Denah Lantai 1,denah:4|Denah Lantai 2' && /DENAH LANTAI 2/.test(dk2.svg), {elemen: ku.elemen, lembar: lbr});
    // v0.36: DXF semua lembar dalam satu berkas, disusun matriks
    const dg = await halaman(`window.rancangAPI.dxf({semua: true}).then(r => ({jumlah: r.jumlah, kolom: r.kolom, baris: r.baris, panjang: r.dxf.length, judul: (r.dxf.match(/LEMBAR-JUDUL/g) || []).length, eof: r.dxf.trim().endsWith('EOF')}))`);
    catat('DXF gabungan satu berkas', dg.jumlah > 5 && dg.kolom === Math.ceil(Math.sqrt(dg.jumlah)) && dg.judul >= dg.jumlah && dg.eof, dg);
    catat('RAB plafon miring menyatu dengan plafon datar', !!pvc && pvc.vol > 0 && !!hollow && hollow.vol > 0 && !lama, {pvc: pvc && pvc.vol, hollow: hollow && hollow.vol});
    hasil.ok = true;
  } catch (err) {
    hasil.galat = err.message;
  }
  const teks = JSON.stringify(hasil, null, 1);
  console.log(teks);
  if (process.env.RANCANG_UJI_HASIL) fs.writeFileSync(process.env.RANCANG_UJI_HASIL, teks);
  if (!hasil.ok && process.env.GITHUB_ACTIONS) console.log(`::error title=uji-asap::${hasil.galat}`);
  app.exit(hasil.ok ? 0 : 1);
}

/* ============ Mulai ============ */
if (!UJI_ASAP && !app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', (_e, argv) => {
    const f = berkasDariArgv(argv);
    if (f) bukaProyek(f);
    if (jendela) { if (jendela.isMinimized()) jendela.restore(); jendela.focus(); }
  });
  app.whenReady().then(async () => {
    pasangMenu();
    try { bukaProyek(proyekAwal()); } catch (err) {
      dialog.showErrorBox('Proyek gagal dibuka', err.message + '\n\nProyek baru dibuat sebagai gantinya.');
      bukaProyek(path.join(app.getPath('documents'), 'RANCANG', `Proyek baru ${Date.now()}${EKSTENSI}`));
    }
    try {
      jembatan = await mulaiJembatan({metode, berkasInfo: berkasJembatan(),
        infoTambahan: () => ({exe: process.env.PORTABLE_EXECUTABLE_FILE || process.execPath, argv: app.isPackaged ? [] : [app.getAppPath()], proyek: proyek.jalur, versi: VERSI})});
    } catch (err) { console.error('[jembatan] gagal dimulai', err); }
    await buatJendela().catch(() => {});
    if (UJI_ASAP) ujiAsap();
  });
  app.on('window-all-closed', () => app.quit());
  app.on('before-quit', () => {
    proyek.simpanSekarang();
    proyek.hentikanPantau();
    if (jembatan) jembatan.tutup();
  });
}
