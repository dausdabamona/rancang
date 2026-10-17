# RANCANG: Ringkasan Program dari Awal sampai Sekarang

*Disusun 17 Oktober 2026 · posisi terakhir: rilis exe v0.29.1, artifact versi 67*

RANCANG adalah aplikasi gambar bangunan ala SketchUp untuk kebutuhan PPK Poltek KP Sorong. Bangunan digambar sebagai model 3D. Dari model yang sama aplikasi menghasilkan gambar kerja 2D dan volume RAB. Claude bisa membaca, menggambar, dan merevisi model itu bersama pengguna.

---

## 1. Tujuan dan keputusan inti

**Tujuan.** Menggambar bangunan sederhana yang sering ditangani PPK, misalnya ruang kelas, laboratorium, asrama, gudang, bengkel, dan renovasi. Hasilnya dua:

- gambar kerja 2D siap kop: denah, tampak, potongan, daftar kusen, dan detail;
- volume yang bisa ditarik ke RAB.

**Keputusan inti (16 Oktober 2026).** Cara menggambarnya meniru SketchUp: Persegi, Garis, Push/Pull, dan ukuran diketik. Bedanya, hasilnya disimpan sebagai **elemen bangunan** (dinding, kolom, atap, dan seterusnya), bukan sekadar garis dan bidang. Ada tiga akibatnya:

- Claude mudah memahami dan mengubah model, misalnya dengan perintah "tinggikan semua dinding jadi 4 m".
- Denah, tampak, potongan, dan volume RAB dihitung dari data yang sama. Satu sumber, jadi selalu cocok.
- Ukuran dihitung dari data elemen, bukan dari jaring segitiga 3D, sehingga hasilnya tepat.

**Harga dari keputusan ini:** aplikasi kurang bebas dibanding SketchUp untuk bentuk sembarang. Celah ini kemudian ditutup bertahap lewat bidang 3D bebas, batang, pecah atap, Sapuan (Follow Me), dan Bidang 3D.

**Di luar cakupan:** render foto-realistis, perhitungan struktur dan beban, serta MEP detail.

---

## 2. Bentuk program

| Bentuk | Isi | Penyimpanan |
|---|---|---|
| **Artifact Claude** (versi web) | Satu halaman HTML yang diterbitkan di claude.ai. Dipakai untuk mencoba fitur baru lebih dulu. | Database artifact. Perubahan dari Claude langsung tampil. |
| **Aplikasi desktop (.exe)** | Electron untuk Windows, versi Setup dan Portable. Berjalan luring penuh. | Berkas `.rancang` (JSON) dengan simpan otomatis dan cadangan `.bak`. |
| **Ekstensi MCP** (`RANCANG.mcpb`) | Menghubungkan Claude desktop dengan aplikasi desktop: baca model, terapkan perubahan, gambar 2D, RAB, tangkap layar. | Jembatan lokal 127.0.0.1 dengan token acak. |
| **Panel Claude** (v0.27, hanya artifact) | Obrolan dengan Claude di dalam aplikasi, memakai akun Claude pengguna. Hapus elemen menunggu izin. | Riwayat hanya selama sesi. |

**Sumber tunggal:** semua fitur ditulis di satu berkas, `app/rancang.html` (sekitar 11.300 baris). Versi desktop disusun otomatis dari berkas itu. CDN dan huruf diganti salinan lokal.

**Teknologi:** Three.js r149, polygon-clipping 0.15.7, xlsx 0.18.5, Electron 44, server MCP dari @modelcontextprotocol/sdk, dan build otomatis lewat GitHub Actions.

---

## 3. Perjalanan versi

| Versi | Pokok perubahan |
|---|---|
| v0.1–v0.3 | Menggambar (Persegi, Dinding, Push/Pull, Pindah, ukuran diketik, Undo), panel properti (panjang, luas, volume), tampak 2D dan ekspor SVG/PNG, grup dan komponen, Claude menggambar lewat database |
| v0.4 | Pintu dan jendela menempel di dinding, kode kusen otomatis (P1, J1, …) |
| v0.5 | Atap pelana, limas, dak, sandar; denah atap |
| v0.6–v0.6.1 | Kolom praktis/struktur, slof, pondasi batu kali, foot plat, umpak, penulangan dan berat besi; sambungan dinding L/T rapi |
| v0.7–v0.9 | Garis potong dan gambar potongan, anotasi (teks, label, ukuran, peil) yang bisa disunting di gambar 2D |
| v0.10 | Lingkaran, busur, Offset |
| v0.11 | Plafon, rangka atap otomatis (baja ringan/kayu), pola penutup (spandek, gelombang, genteng) |
| v0.12 | Pindah dengan inferensi ala SketchUp: snap ujung/tengah/bidang, kunci sumbu |
| v0.13 | **Ekspor volume RAB ke Excel**: sheet RAB dengan VLOOKUP ke HSP MASTER, sheet backup volume |
| v0.14 | Simpan/buka berkas proyek .json |
| v0.15 | Tipe kusen (daun panil, kaca berkotak, bovenlicht, jalusi) dan lembar Daftar Kusen |
| v0.16 | Irisan 3D (section plane) tegak dan datar, pilih berurutan, pintu pindah dinding |
| v0.17–v0.20.4 | Kuda-kuda kayu sesuai gambar kerja, lisplang, susunan rangka sesuai detail, atap gabung (jurai dalam), lisplang per sisi, plafon miring dan tritisan |
| v0.21–v0.23 | Arah buka dan engsel pintu, alat Putar, jenis lantai dan pecah lantai per ruang |
| **v0.24** | **Aplikasi desktop (.exe) dan MCP**, rilis otomatis lewat GitHub |
| v0.25–v0.26 | Ruang Lembar (sampul, daftar gambar, kop 3 model, skala 1:150), PDF satu set, ukuran berantai dari as, ekspor DXF dan DAE, pustaka detail, simbol perabot, legenda, logo |
| v0.27 | Panel Claude di dalam artifact; seleksi dan klik kanan ala SketchUp; lubang lantai dan alat solid (Kurangi, Pangkas, Belah, Gabung); overstek per sisi |
| v0.28.0–v0.28.1 | **Pecah atap** jadi bidang (H) dan batang (J) yang bisa diedit satu per satu tanpa mengubah RAB; pilih/buang satu muka volume; as untuk tiang di luar dinding; kuda-kuda manual tampil di potongan |
| v0.28.2–v0.28.5 | Kusen tanpa daun, Push/Pull ujung dinding untuk panjang, edit di dalam grup, Push/Pull bidang menebalkan |
| v0.29.0 | **Sapuan** (Follow Me yang tetap bisa diedit): talang, lisplang, list plafon, plint, pipa, parit U |
| v0.29.1 | Pindah memakai titik acuan pada benda dan menempel ke bidang benda lain |
| *artifact v65–v67* | *Push/Pull untuk benda pejal, Push/Pull menempel ke titik benda lain, alat Bidang 3D (B), snap mengutamakan titik terdekat kamera. Masih diuji, belum masuk exe.* |

---

## 4. Fitur pokok yang sudah ada

**Menggambar dan mengedit 3D**
- Alat gambar: Persegi, Lingkaran, Busur, Dinding, Push/Pull, Offset, Pindah (dengan salin dan larik), Putar, Hapus, Bidang 3D, Sapuan.
- Ukuran bisa diketik dalam m atau cm.
- Snap: ujung, tengah, pada tepi, pada bidang, sumbu, dan garis lacak.
- Grup bersarang, komponen, Tembus pandang, irisan 3D, Undo/Redo.
- Perubahan dari Claude disorot oranye dan bisa dibatalkan dengan Ctrl+Z.

**Elemen bangunan**
- Dinding dengan pintu dan jendela (tipe kusen), lantai berjenis, plafon.
- Kolom, slof, ring balk, pondasi batu kali, foot plat, umpak.
- Atap parametrik dengan rangka, lisplang, dan plafon tritisan.
- Bidang dan batang bebas, sapuan.

**Gambar kerja 2D**
- Denah, denah atap, denah pondasi, tampak empat sisi, potongan, daftar kusen, detail penulangan, detail kuda-kuda dan sambungan.
- Ruang Lembar dengan kop, sampul, dan daftar gambar.
- Keluaran: PDF satu set, SVG/PNG, DXF, dan DAE untuk SketchUp.

**RAB**
- Volume per divisi: tanah dan pondasi, beton, besi per diameter, bekisting, dinding/plester/aci, kusen, atap, plafon, lantai.
- Ekspor ke Excel dengan kode HSP dan VLOOKUP.
- Sesuai keputusan terakhir pengguna, *pengembangan RAB ditunda dulu*; fokus sekarang gambar.

---

## 5. Model data (ringkas)

Satu elemen = satu dokumen dengan id tetap. Satuan meter. X ke timur, Y ke utara, Z ke atas.

| Awalan | Jenis | Awalan | Jenis |
|---|---|---|---|
| D | Dinding | A | Atap parametrik |
| B | Bukaan (pintu/jendela) | P | Plafon |
| V | Volume / lantai / bidang | H | Bidang 3D bebas |
| C | Kolom | J | Batang 3D (kayu, baja ringan, papan) |
| S | Slof | U | Sapuan (Follow Me) |
| R | Ring balk | X | Garis potong |
| F | Pondasi (batu kali, foot plat, umpak) | N | Anotasi |
| G | Grup | K / I | Definisi komponen / salinannya |
| T | Tipe kusen | | |

Setiap perubahan dari luar membawa `diubahOleh` dan `diubahPada`. Lewat MCP, satu panggilan `terapkan_perubahan` sama dengan satu langkah Undo.

---

## 6. Cara kerja yang disepakati

1. **Dokumentasi dulu.** Setiap keputusan dicatat di *Dokumen Keputusan: Aplikasi Gambar Bangunan v1* sebelum atau bersama kodenya.
2. **Bertahap.** Untuk perubahan besar: usulan, tunggu "LANJUT" atau "OK", baru dikerjakan. Masalah kecil langsung diperbaiki.
3. **Usulan model dibahas dalam 2D dulu**, baru dibangun 3D.
4. **Uji di artifact dulu, baru exe.** Fitur baru diterbitkan ke artifact. Setelah pengguna memastikan berhasil, baru digabung ke main dan dibuatkan exe.
5. **Rilis.** Versi di `package.json` dinaikkan lewat pull request. Setelah merge ke main, GitHub Actions membuat Release `vX.Y.Z` berisi Setup.exe, Portable.exe, dan RANCANG.mcpb.
6. **Bahasa.** Antarmuka, komentar kode, dan pesan memakai Bahasa Indonesia. Commit memakai format Conventional Commits.

---

## 7. Model yang sudah dikerjakan dengan RANCANG

- **Guest House:** kuda-kuda kayu 6/12, lisplang, plafon teras dan tritisan, daftar kusen PJ1/J2/V1/P1/P2. Model inilah yang membentuk sebagian besar aturan atap kayu.
- **Gedung Prodi 1:** parit, sambungan pipa, slof dan ring balk selasar.
- **KM/WC umum 2×2:** contoh ekspor volume RAB.
- **Gedung Instalasi Bengkel Poltek KP Sorong** (dari PDF CV. Patonro 2022), 592 elemen:
  - As 1–8 dan A–C, kolom 35/35, ring balk 30/35, poer plat, dan batu kali.
  - Atap pelana spandek 36° dengan atap ventilasi bubungan +10,95.
  - Kuda-kuda **rangka batang sejajar** digambar manual: 6 kuda-kuda, 58 batang per kuda-kuda. Balok atas dan bawah sejajar mengunci pada dinding, sesuai koreksi pengguna.
  - Gunung-gunung dan dinding angin-angin, 58 jalusi ventilasi.
  - **Kanopi kayu parkiran:** atap spandek 10°, tiang 12/12 di atas umpak, dengan posisi tiang yang disunting langsung oleh pengguna.

---

## 8. Posisi sekarang dan pekerjaan yang tertunda

**Menunggu uji pengguna di artifact (v67)**
- Push/Pull untuk benda pejal.
- Push/Pull yang menempel ke titik benda lain.
- Alat Bidang 3D.

Bila berhasil, perubahan ini dirilis sebagai exe v0.30.0.

**Keluhan terbaru: seleksi dan snap terasa tidak nyaman.** Temuan awal:
1. Snap menghitung ulang semua elemen setiap kali kursor bergerak, sekitar 30 ms per gerak pada model bengkel.
2. Snap bisa menempel ke titik yang tertutup benda lain.

Usulan perbaikannya menunggu persetujuan.

**Pertanyaan yang masih terbuka**
- Dinding mana yang seharusnya ada pintu ("bidang ini harusnya ada pintu").
- Pintu P4 tanpa daun, arah diagonal kuda-kuda, dan site plan kampus.
- Asumsi bengkel: pintu PU, kedalaman poer, arah utara, tinggi ventilasi.
- Ukuran balok kanopi: bentang sekitar 5,5 m cukup berat untuk 8/15.
- Grup G1 dan G10 terurai saat penyuntingan manual.

**Ditunda:** Sapuan tahap 2 dan 3, serta pengembangan RAB (termasuk RAB sapuan).

---

## 9. Kesimpulan pokok

1. **Arah program sudah terbukti.** Menyimpan gambar sebagai elemen bangunan membuat satu model menghasilkan 3D, gambar kerja 2D, dan volume RAB sekaligus, dan membuat Claude bisa ikut menggambar dengan aman.
2. **Gambar kerja sudah lengkap untuk bangunan sederhana.** Dari denah sampai PDF satu set ber-kop, plus DXF untuk CAD.
3. **Dua jalur kerja sudah jalan.** Artifact untuk mencoba cepat dan kolaborasi langsung; exe dan MCP untuk kerja harian luring di laptop dengan berkas sendiri.
4. **Pekerjaan sekarang adalah mutu alat edit manual.** Push/Pull benda pejal, Pindah, seleksi, dan snap harus terasa senyaman SketchUp, karena pengguna ingin mengerjakan sendiri hal-hal kecil dan menyerahkan pekerjaan besar ke Claude.
5. **Disiplin proses menjaga mutu.** Keputusan tertulis lebih dulu, tahapan dengan LANJUT, uji di artifact sebelum exe, dan satu sumber kode.
