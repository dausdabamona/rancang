// Pengganti window.claude untuk versi desktop.
// Aplikasi memanggil window.claude.use('db' | 'user' | 'downloads') seperti di artifact;
// di sini semua diteruskan ke proses utama Electron lewat window.rancangDesktop (preload).
(() => {
  'use strict';
  const D = window.rancangDesktop;
  if (!D) return;
  const KOLEKSI = ['elemen', 'grup', 'komponen', 'kusen'];
  const pendengar = Object.fromEntries(KOLEKSI.map(k => [k, []]));
  const pendengarSetel = [];
  let awal = null;
  const muatAwal = () => awal || (awal = D.awal());

  // bentuk perubahan dokumen mengikuti API snapshot yang dipakai aplikasi
  const ubahan = (type, id, data) => ({type, doc: {id, data: () => data, metadata: {hasPendingWrites: false}}});
  const snapSetel = s => ({exists: !!s, data: () => s || {}});

  D.onUbah(({koleksi, perubahan}) => {
    const daftar = pendengar[koleksi];
    if (!daftar || !perubahan.length) return;
    const ch = perubahan.map(p => ubahan(p.data ? 'modified' : 'removed', p.id, p.data));
    for (const cb of daftar) cb({docChanges: () => ch});
  });
  D.onSetel(s => { for (const cb of pendengarSetel) cb(snapSetel(s)); });

  const db = {
    collection(nama) {
      if (!KOLEKSI.includes(nama)) throw new Error('Koleksi tidak dikenal: ' + nama);
      return {
        onSnapshot(cb, gagal) {
          muatAwal().then(d => {
            const ch = Object.entries(d[nama] || {}).map(([id, data]) => ubahan('added', id, data));
            cb({docChanges: () => ch});
            pendengar[nama].push(cb);
          }).catch(err => { console.error('[claude-shim] gagal memuat', err); if (gagal) gagal(err); });
          return () => { const i = pendengar[nama].indexOf(cb); if (i >= 0) pendengar[nama].splice(i, 1); };
        },
        doc(id) {
          return {
            set: data => D.set(nama, id, data),
            delete: () => D.hapus(nama, id)
          };
        }
      };
    },
    doc(jalur) {
      if (jalur !== 'pengaturan/proyek') throw new Error('Dokumen tidak dikenal: ' + jalur);
      return {
        set: data => D.setel(data),
        onSnapshot(cb) {
          muatAwal().then(d => { cb(snapSetel(d.setel)); pendengarSetel.push(cb); }).catch(() => {});
          return () => {};
        }
      };
    }
  };

  const user = {can: async () => true};

  const downloads = {
    async save({filename, data}) {
      let isi = data;
      if (data instanceof Blob) isi = new Uint8Array(await data.arrayBuffer());
      else if (data instanceof ArrayBuffer) isi = new Uint8Array(data);
      const r = await D.simpanUnduhan({filename, data: isi});
      if (!r || !r.ok) { const e = new Error((r && r.pesan) || 'Gagal menyimpan berkas'); e.code = (r && r.code) || 'gagal'; throw e; }
    }
  };

  const layanan = {db, user, downloads};
  window.claude = Object.freeze({
    use: async nama => { if (!layanan[nama]) throw new Error('Layanan tidak tersedia: ' + nama); return layanan[nama]; }
  });
})();
