# Rencana RANCANG v0.50.2 — Aturan snap, alat Garis, perbaikan Putar

*Disepakati dengan pengguna 23 Oktober 2026 malam. Dikerjakan hari Minggu setelah kuota pulih. Status: **menunggu dikerjakan** (belum ada kode). Mulai dari `main` (sesudah v0.50.1 / PR #54), cabang baru `snap-garis-v0.50.2`.*

## Latar

Pengguna kesulitan membuat atap datar/dak:
- titik awal sulit ditentukan;
- snap jatuh di titik yang tidak diinginkan, sampai bidang menjadi miring;
- Putar tidak tepat: titik pusat tidak berada di benda yang diklik.

Konsep pengguna: menggambar garis sesuai titik → bidang datar → diberi material → elemen dak → dak beton. Garis, bidang, dan material dikerjakan di v0.51; v0.50.2 menyiapkan dasarnya.

## A. Aturan snap (prinsip pengguna, wajib)

> "Apa yang terlihat di layar itulah acuan snap. Software ini digambar manusia, bukan mesin."

1. **Urutan tangkap**
   1. **Utama: node (ujung/sudut), garis (titik mana pun di rusuk), dan titik tengah rusuk.** Node didahulukan. Kelonggaran jarak layar hanya berlaku untuk tiga jenis ini, dan dihitung dari node, garis, atau titik tengah itu sendiri.
   2. **Kedua: muka (face).** Dipakai hanya bila tidak ada node, garis, atau titik tengah dalam jangkauan kursor. Titiknya selalu titik pertama yang terkena sinar di permukaan terdepan, tepat di bawah kursor.
   3. **Grid atau bidang kerja: hanya bila tombol F9 menyala.** Tidak pernah otomatis.
2. **Tanpa snap** (F9 mati, kursor di ruang kosong): titik jatuh **bebas tepat di bawah kursor** di bidang kerja, tanpa dibulatkan ke grid. Ukuran pasti diketik.
3. **LARANGAN KERAS: tidak boleh ada titik tangkap di belakang benda yang terlihat.**
   - Berlaku untuk semua jenis: node, garis, titik tengah, muka, grid, garis bantu, dan titik milik benda itu sendiri.
   - Setiap calon titik diuji dengan sinar dari kamera. Ada benda apa pun di depannya, termasuk badan benda itu sendiri → **ditolak**.
   - Kelonggaran kedalaman cukup 1–2 cm, hanya untuk pembulatan hitungan titik yang memang di permukaan tampak. Kelonggaran 30 cm sekarang dihapus.
   - Grid di belakang dinding atau atap tidak pernah dipakai.
   - Titik yang tidak sempat diuji keterlihatannya **ditolak, bukan ditebak**.
   - Satu-satunya pengecualian: **Tembus (H)** yang dinyalakan pengguna sendiri.
4. **Penanda titik tangkap** selalu tepat di titik yang akan dipakai. Di sebelahnya tertulis jenis titik, benda, dan ketinggian, contoh *Ujung · Dinding D3 · +3,50*. Bila alat butuh bidang datar (lantai/dak), posisi akhirnya ditunjukkan dengan garis tegak putus-putus, supaya yang terlihat sama dengan yang terjadi.
5. **Tombol Grid di bilah bawah** menyala saat F9 aktif. Status F9 diingat per peramban.

## B. Alat Garis (baru) dan pintasan

- **L = Garis** (seperti Line di SketchUp). **W = Dinding** (pindah dari L, seperti Wall). W belum dipakai sebagai pintasan; di palet sudah ada alias `w: 'dinding'`.
- Pertama kali L ditekan setelah pembaruan, muncul pesan sekali: "L sekarang Garis; Dinding pindah ke W."
- Ubah semua petunjuk:
  - tooltip tombol Dinding (`title="Dinding (L)"`, ±baris 668);
  - layar kosong `<kbd>L</kbd> Dinding` (±737);
  - daftar pintasan di Menu (±13501);
  - `PETA_PINTASAN` (±12144: `l: 'dinding'` → `l: 'garis', w: 'dinding'`);
  - palet;
  - catatan rilis.
- Perilaku Garis:
  - Klik titik demi titik → rusuk lurus ke arah X, Y, maupun Z.
  - Ketik panjang per ruas. Panah → ← ↑ mengunci sumbu X/Y/Z.
  - Klik 2× atau Esc = selesai; klik titik pertama = tutup.
- **Bidang otomatis:**
  - Garis yang menutup di satu bidang rata (datar, tegak, atau miring) langsung menjadi **bidang** (face), seperti SketchUp.
  - Garis yang memotong bidang membaginya menjadi dua.
- **Penyimpanan:** jenis elemen baru untuk rusuk (usul awalan id yang belum terpakai). Bidang memakai jenis `bidang` (H) tanpa peran/material dulu.
- Rusuk dan bidang bisa diolah dengan Node & rusuk, Pindah, Putar, dan Push/Pull.
- **Belum masuk RAB.** Material menyusul di v0.51: Dak beton → plat W, Lantai, Atap datar, Rabat, Paving, dan lainnya.

## C. Perbaikan Putar

Urutan yang dipahami pengguna: pilih benda → klik titik pusat → klik titik awal → putar atau ketik derajat.

1. **Pilihan tidak berganti.** Bila sudah ada pilihan, klik titik pusat di mana pun (termasuk di benda lain) tidak mengganti pilihan. Sekarang `alatPutar.down` (±6890) menjalankan `S.sel.clear(); S.sel.add(t)` bila benda di bawah kursor berbeda; ini harus diubah seperti `alatPindah.down`, yang mempertahankan pilihan.
2. **Titik pusat mengikuti aturan snap A** (node, garis, titik tengah, lalu muka), tanpa pembulatan grid. Sekarang ada `snapG(h.point…)`, dan tepi tidak ikut ditangkap.
3. **Sudut bebas untuk atap.** Sekarang `kunci90` (±2939) membatasi atap selain denah, kolom, dan pondasi ke kelipatan 90°. Usulan: atap pelana/limas/sandar/datar yang diputar bukan kelipatan 90° otomatis diubah menjadi atap denah. Kolom dan pondasi tetap 90°, kecuali pengguna meminta lain.
4. Titik pusat ditandai jelas, dan koordinat X/Y/Z-nya tampil di bilah bawah.

## D. Catatan kode (temuan pemeriksaan 23 Okt)

| Masalah | Letak (±baris di `app/rancang.html`, main sesudah v0.50.1) |
|---|---|
| Titik milik benda sendiri dianggap tidak tertutup badannya (`idSendiri` dikecualikan) | `terlihatSnap` ±4933, baris `g.userData.elemId !== idSendiri` |
| Kelonggaran kedalaman `Math.max(0.3, 0.001 * jarak)` = 30 cm | `terlihatSnap` |
| Batas 8 uji keterlihatan: pastikan sisa calon **ditolak**, bukan dipakai | `pilihTerlihat` dalam `titikSnap` ±4988 |
| Perpotongan garis bantu (`potonganBantu`) dan titik bantu dilewatkan dari uji keterlihatan (`adalahBantu`) | `titikSnap`, `pilihTerlihat` |
| Grid jatuh di belakang benda: langkah 5 `intersectPlane` tanpa memeriksa benda di depan; `snapG` otomatis | akhir `titikSnap` |
| Muka hanya dipakai bila `opsi.bidang`; jadikan urutan kedua untuk semua alat | `titikSnap` langkah 4 |
| `RADIUS_SNAP = {ujung: 12, tengah: 10, tepi: 10}` px | ±4986 |
| Atap 2 titik: klik pertama tanpa snap *ujung* menjadi atap otomatis (`batasRuang`); snap tengah/tepi/grid tidak bisa jadi sudut pertama | `alatAtap.move` ±7862 |
| Putar mengganti pilihan; pusat `snapG` | `alatPutar.down` ±6971 |

**Waspada:** alat Dinding di 3D saat ini menyambung lewat titik as bawah, yang berada di dalam badan dinding. Sesudah larangan berlaku, sambungan di 3D memakai titik as di puncak dinding yang terlihat (`opsi.atas`). Tampilan atas tidak terpengaruh. Uji alat Dinding wajib dijalankan.

## E. Uji (file baru sederhana, bukan masjid)

Playwright + Electron, pola `/tmp/claude-0/uji/*.mjs` (buat ulang bila hilang; contoh susunan ada di uji-lantai/uji-got). Proyek uji: satu ruang 4 × 4 m (dinding 15 cm, z0 0,3, tinggi 3), dak 12 cm di atasnya, satu dinding pendek di depan.

1. Sudut belakang dak (tertutup dak) → tidak tertangkap; dengan Tembus (H) → tertangkap.
2. Titik ujung dinding di balik dinding 15 cm → tidak tertangkap.
3. Kursor di atas atap/dinding tanpa node, garis, atau titik tengah dekat → titik di muka terdepan, bukan grid di belakang.
4. F9 mati: titik di ruang kosong tidak dibulatkan ke 5 cm. F9 menyala: dibulatkan; grid di balik benda tetap tidak tertangkap.
5. Node mengalahkan titik tengah dan garis; garis dan titik tengah mengalahkan muka.
6. Putar: dak terpilih, pusat diklik di sudut dinding (benda lain) → pilihan tetap dak, pusat tepat di sudut, putar 30° berhasil.
7. Garis: L, gambar persegi 3 × 2 di ketinggian +3,30, tutup → satu bidang; garis diagonal → dua bidang; garis tegak (Z) bisa.
8. W membuat dinding; L menampilkan pesan pindah satu kali.
9. Semua uji lama: `RANCANG_UJI_ELECTRON=1 npm test`, uji asap, outliner, node, kerangka, atap, keterangan, tata, lantai, got. `npm run periksa-tipe` tetap 430.

## F. Langkah kerja hari Minggu

1. `git checkout main && git pull`, lalu cabang `snap-garis-v0.50.2`.
2. Catat keputusan ringkas di `docs/ringkasan-program.md` (rujuk dokumen ini).
3. Kerjakan berurutan: A (snap) → C (Putar) → B (Garis + pintasan L/W).
4. Uji (E), catatan rilis 0.50.2, versi `package.json` 0.50.2 + `npm install --package-lock-only --ignore-scripts`.
5. PR → CI hijau → merge squash → tunggu Release v0.50.2 (exe Setup, Portable, mcpb).
6. Perbarui artifact uji: RANCANG Uji v0.50 dan RANCANG Uji Pos Jaga. Terbitkan ulang dari `app/rancang.html` dengan judul masing-masing; data pengguna di sana tetap.
7. Sesudah v0.50.2: v0.51 Garis → bidang + material → elemen (Dak beton pertama), union per material.
