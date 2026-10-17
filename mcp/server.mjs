// Server MCP RANCANG: menghubungkan Claude dengan aplikasi desktop RANCANG.
// Saat aplikasi berjalan, semua alat lewat jembatan HTTP lokal (127.0.0.1 + token).
// Saat aplikasi tertutup, alat baca dan terapkan_perubahan bekerja langsung pada berkas proyek terakhir;
// alat gambar, RAB, dan tangkap layar menjalankan aplikasi lebih dulu.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {Server} from '@modelcontextprotocol/sdk/server/index.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {CallToolRequestSchema, ListToolsRequestSchema} from '@modelcontextprotocol/sdk/types.js';
import PANDUAN from './panduan-data.md';

export const VERSI = '__VERSI__';
const POLA_ID = /^[A-Z]\d+$/;
const KOLEKSI_DARI = id => (id[0] === 'G' ? 'grup' : id[0] === 'K' ? 'komponen' : id[0] === 'T' ? 'kusen' : 'elemen');

/* ============ Lokasi data aplikasi ============ */
export function folderData() {
  if (process.env.RANCANG_DATA_DIR) return process.env.RANCANG_DATA_DIR;
  if (process.platform === 'win32') return path.join(process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'), 'RANCANG');
  if (process.platform === 'darwin') return path.join(os.homedir(), 'Library', 'Application Support', 'RANCANG');
  return path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'), 'RANCANG');
}
const berkasInfo = () => path.join(folderData(), 'mcp-jembatan.json');
function bacaInfo() {
  try { return JSON.parse(fs.readFileSync(berkasInfo(), 'utf8')); } catch { return null; }
}

/* ============ Jembatan ke aplikasi ============ */
async function rpc(info, metode, param = {}, batasMs = 120000) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), batasMs);
  try {
    const res = await fetch(`http://127.0.0.1:${info.port}/rpc`, {
      method: 'POST', signal: ctl.signal,
      headers: {'Content-Type': 'application/json', Authorization: 'Bearer ' + info.token},
      body: JSON.stringify({metode, param})
    });
    const j = await res.json();
    if (!j.ok) throw new Error(j.galat || 'Aplikasi menolak permintaan.');
    return j.hasil;
  } finally { clearTimeout(t); }
}
// Aplikasi dianggap berjalan bila jembatannya menjawab
async function aplikasi() {
  const info = bacaInfo();
  if (!info || !info.port || !info.token) return null;
  try { await rpc(info, 'info', {}, 15000); return info; } catch { return null; }
}
async function pastikanAplikasi() {
  const ada = await aplikasi();
  if (ada) return ada;
  const info = bacaInfo();
  if (!info || !info.exe || !fs.existsSync(info.exe)) {
    throw new Error('Aplikasi RANCANG belum berjalan dan lokasinya belum diketahui. Buka RANCANG sekali secara manual, lalu coba lagi.');
  }
  const anak = spawn(info.exe, info.argv || [], {detached: true, stdio: 'ignore', windowsHide: false});
  anak.unref();
  for (let i = 0; i < 120; i++) {
    await new Promise(r => setTimeout(r, 500));
    const siap = await aplikasi();
    if (siap) return siap;
  }
  throw new Error('RANCANG sudah dijalankan tetapi belum siap dalam 60 detik. Periksa jendela aplikasi.');
}

/* ============ Mode berkas (aplikasi tertutup) ============ */
function jalurProyekBerkas() {
  const info = bacaInfo();
  if (!info || !info.proyek) throw new Error('Belum ada proyek RANCANG yang pernah dibuka di komputer ini.');
  if (!fs.existsSync(info.proyek)) throw new Error('Berkas proyek terakhir tidak ditemukan: ' + info.proyek);
  return info.proyek;
}
function bacaProyekBerkas() {
  const jalur = jalurProyekBerkas();
  const d = JSON.parse(fs.readFileSync(jalur, 'utf8'));
  if (d.format !== 'rancang-proyek') throw new Error('Berkas proyek tidak dikenali: ' + jalur);
  for (const k of ['elemen', 'grup', 'komponen', 'kusen']) d[k] = d[k] || {};
  return {jalur, d};
}
export function terapkanKeData(d, perubahan) {
  const galat = [];
  const akhir = new Map();
  for (const [i, p] of perubahan.entries()) {
    const id = p && p.id;
    const data = p ? p.data : undefined;
    if (typeof id !== 'string' || !POLA_ID.test(id)) { galat.push(`#${i + 1}: id "${id}" tidak sah.`); continue; }
    if (data === null) { akhir.set(id, null); continue; }
    if (!data || typeof data !== 'object' || Array.isArray(data)) { galat.push(`${id}: data harus objek, atau null untuk menghapus.`); continue; }
    if (KOLEKSI_DARI(id) === 'elemen' && typeof data.jenis !== 'string') { galat.push(`${id}: isian "jenis" wajib ada.`); continue; }
    akhir.set(id, data);
  }
  const ada = id => (akhir.has(id) ? akhir.get(id) !== null : !!d[KOLEKSI_DARI(id)][id]);
  for (const [id, x] of akhir) {
    if (!x) continue;
    if (x.jenis === 'bukaan' && !ada(x.dinding)) galat.push(`${id}: dinding ${x.dinding} tidak ada.`);
    if (x.grup && !ada(x.grup)) galat.push(`${id}: grup ${x.grup} tidak ada.`);
  }
  if (galat.length) return {ok: false, galat};
  const waktu = new Date().toISOString();
  for (const [id, x] of akhir) {
    const k = KOLEKSI_DARI(id);
    if (x === null) delete d[k][id];
    else d[k][id] = {...x, diubahOleh: 'claude', diubahPada: waktu};
  }
  return {ok: true, diubah: [...akhir].filter(([, x]) => x).map(([id]) => id), dihapus: [...akhir].filter(([, x]) => !x).map(([id]) => id)};
}
function tulisProyekBerkas(jalur, d) {
  d.disimpan = new Date().toISOString();
  fs.writeFileSync(jalur + '.tmp', JSON.stringify(d, null, 1));
  fs.renameSync(jalur + '.tmp', jalur);
}

/* ============ Bantuan keluaran ============ */
const teks = isi => ({content: [{type: 'text', text: typeof isi === 'string' ? isi : JSON.stringify(isi, null, 1)}]});
const gambar = (dataURL, keterangan) => {
  const m = /^data:(image\/\w+);base64,(.*)$/.exec(dataURL || '');
  if (!m) throw new Error('Gambar tidak berhasil dibuat.');
  return {content: [{type: 'image', data: m[2], mimeType: m[1]}, ...(keterangan ? [{type: 'text', text: keterangan}] : [])]};
};
function ringkasElemen(id, x) {
  const r = {id, jenis: x.jenis || KOLEKSI_DARI(id), nama: x.nama || ''};
  if (x.tipe) r.tipe = x.tipe;
  if (x.bentuk) r.bentuk = x.bentuk;
  if (x.grup) r.grup = x.grup;
  if (x.kode) r.kode = x.kode;
  if (x.dinding) r.dinding = x.dinding;
  if (x.lantai) r.lantai = x.lantai;
  return r;
}
async function modelSekarang() {
  const info = await aplikasi();
  if (info) return {sumber: 'aplikasi', ...(await rpc(info, 'model'))};
  const {jalur, d} = bacaProyekBerkas();
  return {sumber: 'berkas (aplikasi tertutup)', proyek: jalur, setel: d.setel || {}, elemen: d.elemen, grup: d.grup, komponen: d.komponen, kusen: d.kusen};
}

/* ============ Daftar alat ============ */
const objek = (props, wajib = []) => ({type: 'object', properties: props, required: wajib, additionalProperties: false});
const daftarId = {type: 'array', items: {type: 'string'}, description: 'Id elemen atau grup (kosong = seluruh model)'};
export const ALAT = [
  {name: 'panduan_data', description: 'Panduan isian data setiap jenis elemen RANCANG (dinding, pintu, lantai, kolom, atap, dll.) beserta contoh JSON. Baca sebelum membuat atau mengubah elemen.',
    inputSchema: objek({})},
  {name: 'info_proyek', description: 'Info proyek yang terbuka: nama berkas, jumlah elemen/grup/komponen/kusen, pengaturan, jenis gambar 2D yang tersedia, dan apakah aplikasi sedang berjalan.',
    inputSchema: objek({})},
  {name: 'daftar_elemen', description: 'Daftar ringkas elemen (id, jenis, nama, grup, tipe). Bisa disaring.',
    inputSchema: objek({jenis: {type: 'string', description: 'Saring per jenis, mis. dinding, bukaan, volume, atap'}, grup: {type: 'string', description: 'Saring per id grup'},
      cari: {type: 'string', description: 'Saring per potongan nama (tidak peka huruf besar)'}, batas: {type: 'integer', minimum: 1, maximum: 2000, description: 'Jumlah maksimum (bawaan 300)'}})},
  {name: 'ambil_elemen', description: 'Ambil data lengkap elemen, grup (G), komponen (K), atau tipe kusen (T) berdasarkan id.',
    inputSchema: objek({ids: {type: 'array', items: {type: 'string'}, minItems: 1}}, ['ids'])},
  {name: 'terapkan_perubahan', description: 'Tambah, ubah, atau hapus beberapa dokumen sekaligus. Data menimpa seluruh dokumen; data null = hapus. Semua diperiksa dulu dan ditolak utuh bila ada yang tidak sah. Di aplikasi, perubahan disorot dan bisa di-Undo (Ctrl+Z).',
    inputSchema: objek({perubahan: {type: 'array', minItems: 1, items: objek({id: {type: 'string', description: 'mis. D12, B3, V4, G1, T2'}, data: {type: ['object', 'null'], description: 'Data lengkap dokumen, atau null untuk menghapus'}}, ['id', 'data'])}}, ['perubahan'])},
  {name: 'ringkasan_ukuran', description: 'Ringkasan ukuran: panjang dan luas dinding, bukaan, luas lantai, atap, volume beton dan besi, dsb.',
    inputSchema: objek({ids: daftarId})},
  {name: 'volume_rab', description: 'Volume pekerjaan RAB per divisi (kode HSP, uraian, satuan, volume) seperti ekspor Excel di aplikasi.',
    inputSchema: objek({ids: daftarId})},
  {name: 'gambar_2d', description: 'Buat gambar kerja 2D (denah, denah atap, denah pondasi, detail penulangan, daftar kusen, tampak, potongan). Format png (bawaan) untuk dilihat, svg untuk teks.',
    inputSchema: objek({jenis: {type: 'string', description: 'denah, atap, pondasi, detail, kusen, depan, belakang, kanan, kiri, atau potongan:X3 (lihat info_proyek)'},
      skala: {type: 'integer', minimum: 0, maximum: 5000, description: 'Angka penyebut skala, mis. 100 untuk 1:100 atau 150; 0 = otomatis'}, kertas: {type: 'string', enum: ['A4', 'A3']},
      dimensi: {type: 'boolean', description: 'Tampilkan garis ukuran (bawaan ya)'}, format: {type: 'string', enum: ['png', 'svg']}}, ['jenis'])},
  {name: 'tangkap_layar_3d', description: 'Tangkapan layar tampilan 3D aplikasi.',
    inputSchema: objek({tampilan: {type: 'string', enum: ['iso', 'atas', 'depan', 'belakang', 'kanan', 'kiri'], description: 'Arah pandang; kosong = tampilan sekarang'}})},
  {name: 'buka_proyek', description: 'Buka berkas proyek .rancang lain di aplikasi (berkas dibuat bila belum ada).',
    inputSchema: objek({jalur: {type: 'string', description: 'Jalur lengkap berkas .rancang'}}, ['jalur'])},
  {name: 'simpan_proyek_sebagai', description: 'Simpan proyek yang terbuka ke berkas .rancang baru dan lanjut bekerja di berkas itu.',
    inputSchema: objek({jalur: {type: 'string', description: 'Jalur lengkap berkas .rancang tujuan'}}, ['jalur'])}
];

/* ============ Pelaksana alat ============ */
export async function jalankanAlat(nama, a = {}) {
  switch (nama) {
    case 'panduan_data': return teks(PANDUAN);
    case 'info_proyek': {
      const info = await aplikasi();
      if (info) return teks({aplikasiBerjalan: true, ...(await rpc(info, 'info'))});
      const {jalur, d} = bacaProyekBerkas();
      return teks({aplikasiBerjalan: false, catatan: 'Aplikasi tertutup: baca dan terapkan_perubahan bekerja pada berkas; gambar/RAB/tangkap layar akan menjalankan aplikasi.',
        proyek: jalur, setel: d.setel || {}, jumlah: Object.fromEntries(['elemen', 'grup', 'komponen', 'kusen'].map(k => [k, Object.keys(d[k]).length]))});
    }
    case 'daftar_elemen': {
      const m = await modelSekarang();
      const cari = (a.cari || '').toLowerCase(), batas = a.batas || 300;
      const semua = Object.entries(m.elemen).filter(([, x]) => (!a.jenis || x.jenis === a.jenis) && (!a.grup || x.grup === a.grup) && (!cari || String(x.nama || '').toLowerCase().includes(cari)));
      semua.sort(([p], [q]) => p.localeCompare(q, 'en', {numeric: true}));
      return teks({sumber: m.sumber, total: semua.length, ditampilkan: Math.min(batas, semua.length),
        grup: Object.entries(m.grup).map(([id, g]) => ({id, nama: g.nama, induk: g.induk || null})),
        elemen: semua.slice(0, batas).map(([id, x]) => ringkasElemen(id, x))});
    }
    case 'ambil_elemen': {
      const m = await modelSekarang();
      const hasil = {};
      for (const id of a.ids || []) hasil[id] = POLA_ID.test(id) ? (m[KOLEKSI_DARI(id)][id] ?? null) : null;
      return teks(hasil);
    }
    case 'terapkan_perubahan': {
      const info = await aplikasi();
      if (info) return teks(await rpc(info, 'terapkan', {perubahan: a.perubahan, oleh: 'claude'}));
      const {jalur, d} = bacaProyekBerkas();
      const r = terapkanKeData(d, a.perubahan || []);
      if (r.ok) tulisProyekBerkas(jalur, d);
      return teks({...r, catatan: 'Aplikasi tertutup: perubahan ditulis ke berkas dan diperiksa lengkap saat aplikasi dibuka.'});
    }
    case 'ringkasan_ukuran': return teks(await rpc(await pastikanAplikasi(), 'ringkasan', {ids: a.ids || []}));
    case 'volume_rab': return teks(await rpc(await pastikanAplikasi(), 'rab', {ids: a.ids || []}));
    case 'gambar_2d': {
      const info = await pastikanAplikasi();
      const opsi = {jenis: a.jenis, skala: a.skala || 0, kertas: a.kertas || 'A3', dimensi: a.dimensi !== false};
      if (a.format === 'svg') {
        const h = await rpc(info, 'gambar2D', opsi);
        return teks(`<!-- ${opsi.jenis}, skala 1:${h.skala}, kertas ${h.kertas}${h.info ? ', ' + h.info : ''} -->\n${h.svg}`);
      }
      const h = await rpc(info, 'gambar2D', {...opsi, format: 'png'});
      return gambar(h.png, `${opsi.jenis}, skala 1:${h.skala}, kertas ${h.kertas}${h.info ? '. ' + h.info : ''}`);
    }
    case 'tangkap_layar_3d': return gambar(await rpc(await pastikanAplikasi(), 'tangkap3D', {tampilan: a.tampilan}));
    case 'buka_proyek': return teks(await rpc(await pastikanAplikasi(), 'buka', {jalur: a.jalur}));
    case 'simpan_proyek_sebagai': return teks(await rpc(await pastikanAplikasi(), 'simpanSebagai', {jalur: a.jalur}));
    default: throw new Error('Alat tidak dikenal: ' + nama);
  }
}

/* ============ Mulai ============ */
export async function mulai() {
  const server = new Server({name: 'rancang', version: VERSI}, {capabilities: {tools: {}},
    instructions: 'RANCANG adalah aplikasi gambar bangunan (Bahasa Indonesia). Baca panduan_data sebelum membuat elemen. Satuan meter. Periksa hasil dengan gambar_2d atau tangkap_layar_3d.'});
  server.setRequestHandler(ListToolsRequestSchema, async () => ({tools: ALAT}));
  server.setRequestHandler(CallToolRequestSchema, async req => {
    try {
      return await jalankanAlat(req.params.name, req.params.arguments || {});
    } catch (err) {
      return {isError: true, content: [{type: 'text', text: err && err.message ? err.message : String(err)}]};
    }
  });
  await server.connect(new StdioServerTransport());
}

if (process.argv[1] && /index\.mjs$|server\.mjs$/.test(process.argv[1]) && !process.env.RANCANG_MCP_TANPA_MULAI) {
  mulai().catch(err => { console.error('[rancang-mcp]', err); process.exit(1); });
}
