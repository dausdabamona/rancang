// Jembatan lokal untuk server MCP: HTTP hanya di 127.0.0.1, port acak, wajib token acak.
// Lokasi port dan token dicatat di berkas mcp-jembatan.json pada folder data aplikasi.
'use strict';
const http = require('node:http');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const BATAS_BADAN = 25 * 1024 * 1024;

function bacaBadan(req) {
  return new Promise((ok, gagal) => {
    let n = 0;
    const bagian = [];
    req.on('data', c => {
      n += c.length;
      if (n > BATAS_BADAN) { gagal(Object.assign(new Error('Permintaan terlalu besar'), {status: 413})); req.destroy(); return; }
      bagian.push(c);
    });
    req.on('end', () => ok(Buffer.concat(bagian).toString('utf8')));
    req.on('error', gagal);
  });
}

function samaAman(a, b) {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

// metode: {nama: async (param) => hasil}
function mulaiJembatan({metode, berkasInfo, infoTambahan = () => ({})}) {
  const token = crypto.randomBytes(24).toString('hex');
  const server = http.createServer(async (req, res) => {
    const kirim = (status, isi) => {
      const teks = JSON.stringify(isi);
      res.writeHead(status, {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store'});
      res.end(teks);
    };
    try {
      // tolak permintaan dari halaman web (ada Origin) agar situs lain tidak bisa memanggil jembatan
      if (req.headers.origin) return kirim(403, {ok: false, galat: 'Asal permintaan tidak diizinkan.'});
      const auth = req.headers.authorization || '';
      if (!samaAman(auth, 'Bearer ' + token)) return kirim(401, {ok: false, galat: 'Token tidak sah.'});
      if (req.method !== 'POST' || req.url !== '/rpc') return kirim(404, {ok: false, galat: 'Tidak ditemukan.'});
      const badan = JSON.parse(await bacaBadan(req) || '{}');
      const f = metode[badan.metode];
      if (!f) return kirim(400, {ok: false, galat: `Metode "${badan.metode}" tidak dikenal.`});
      const hasil = await f(badan.param || {});
      kirim(200, {ok: true, hasil});
    } catch (err) {
      console.error('[jembatan]', err);
      kirim(err.status || 500, {ok: false, galat: err.message || String(err)});
    }
  });
  return new Promise((ok, gagal) => {
    server.on('error', gagal);
    server.listen(0, '127.0.0.1', () => {
      const {port} = server.address();
      const tulisInfo = () => {
        const isi = {port, token, pid: process.pid, mulai: new Date().toISOString(), ...infoTambahan()};
        fs.mkdirSync(path.dirname(berkasInfo), {recursive: true});
        fs.writeFileSync(berkasInfo + '.tmp', JSON.stringify(isi, null, 1), {mode: 0o600});
        fs.renameSync(berkasInfo + '.tmp', berkasInfo);
      };
      tulisInfo();
      ok({
        port, token, server, perbaruiInfo: tulisInfo,
        // saat aplikasi ditutup: port dan token dihapus, path exe dan proyek tetap untuk mode berkas MCP
        tutup() {
          try {
            const lama = JSON.parse(fs.readFileSync(berkasInfo, 'utf8'));
            if (lama.pid === process.pid) {
              delete lama.port; delete lama.token; delete lama.pid;
              fs.writeFileSync(berkasInfo, JSON.stringify({...lama, ...infoTambahan(), ditutup: new Date().toISOString()}, null, 1));
            }
          } catch (_) { /* berkas info sudah tidak ada */ }
          server.close();
        }
      });
    });
  });
}

module.exports = {mulaiJembatan};
