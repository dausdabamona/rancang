# RANCANG: Ringkasan Program dari Awal sampai Sekarang

*Disusun 17 Oktober 2026, diperbarui 18 Oktober 2026 · posisi terakhir: rilis exe v0.31.1; PR #20 (v0.32.0) menunggu uji di artifact*

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

**Keputusan platform (18 Oktober 2026).** Usul menulis ulang RANCANG dengan Python **ditolak**. Alasannya: hampir seluruh kemampuan ada di `app/rancang.html` (±13.000 baris) yang sekaligus menjadi versi artifact dan versi desktop; Python tidak bisa berjalan sebagai artifact, dan keluhan yang ada (seleksi, grup, memperluas bidang) adalah soal rancangan interaksi, bukan soal bahasa. Python boleh dipakai belakangan sebagai alat pendamping yang membaca/menulis berkas `.rancang`, misalnya DXF tingkat CAD dengan `ezdxf`, bila diperlukan.

**Di luar cakupan:** render foto-realistis, perhitungan struktur dan beban, serta MEP detail.

---

## 2. Bentuk program

| Bentuk | Isi | Penyimpanan |
|---|---|---|
| **Artifact Claude** (versi web) | Satu halaman HTML yang diterbitkan di claude.ai. Dipakai untuk mencoba fitur baru lebih dulu. | Database artifact. Perubahan dari Claude langsung tampil. |
| **Aplikasi desktop (.exe)** | Electron untuk Windows, versi Setup dan Portable. Berjalan luring penuh. | Berkas `.rancang` (JSON) dengan simpan otomatis dan cadangan `.bak`. |
| **Ekstensi MCP** (`RANCANG.mcpb`) | Menghubungkan Claude desktop dengan aplikasi desktop: baca model, terapkan perubahan, gambar 2D, RAB, tangkap layar. | Jembatan lokal 127.0.0.1 dengan token acak. |
| **Panel Claude** (v0.27, hanya artifact) | Obrolan dengan Claude di dalam aplikasi, memakai akun Claude pengguna. Hapus elemen menunggu izin. | Riwayat hanya selama sesi. |

**Sumber tunggal:** semua fitur ditulis di satu berkas, `app/rancang.html` (sekitar 13.000 baris). Versi desktop disusun otomatis dari berkas itu. CDN dan huruf diganti salinan lokal.

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
| v0.30 | Push/Pull benda pejal dan menempel ke titik benda lain; alat Bidang 3D; **cache snap** per elemen (sebelumnya semua geometri dihitung ulang tiap gerak kursor, ±28 ms di model 592 elemen); snap mengabaikan titik yang tertutup benda lain |
| v0.33.0 | Rilis 18 Okt 2026 malam: PR #20 + #21 (seleksi dengan sorotan dan info kursor, `pilihan_pengguna`, ukuran alas, plafon miring disatukan, garis potong mudah dipilih, Shift+H, Ctrl+V gambar di Panel Claude) |
| v0.34.0 | Tahap A desain ulang: pintasan ala SketchUp/AutoCAD, palet Ctrl+K, menu tiga keadaan, rel panel, mode fokus |
| v0.34.1 (PR #24) | Plafon miring berhenti di lisplang; mundur seng 20 cm semua rangka; isian jarak tepi plafon dari ujung seng |
| v0.31–v0.31.1 | Antarmuka Broadsheet, Plafon terpisah (miring, per ruang, gabungan); menu alat dan panel properti bisa dilipat |
| v0.32.0 (PR #20, cabang `menu-potongan`, menunggu uji pengguna) | Menu Potongan A–A/B–B di bar tampilan; plafon: Pecah per ruang / Gabungkan, bahan tripleks dan PVC, rangka dan lis plafon digambar 3D + lembar "Rencana plafon dan rangka" + RAB; ukuran gording/bubungan/klos dapat dipilih; Pustaka Sanitair (alat Z); skor kayu antar tiang kuda-kuda; lisplang diperpanjang/dipangkas per sisi; dinding bertepi atas bertangga/miring (`profilAtas`); **alat Perpanjang/Pangkas (Shift+H)**: ujung papan lisplang dan sisi plafon sampai batas benda lain; bahan dinding (bata, tripleks, GRC, gypsum) dengan rangka |
| v0.33.0 | Tahap 1 interaksi: sorotan kursor, bilah bawah menyebut sasaran, `pilihan_pengguna`, Ukuran alas di Properti, Shift+H Perpanjang, pengaturan plafon miring disatukan |
| v0.34.0 | Tahap A desain ulang: pintasan ala SketchUp/AutoCAD, palet Ctrl+K, menu tiga keadaan, rel panel, mode fokus |
| v0.34.1 (PR #24) | Plafon miring berhenti di lisplang; `mundurSeng` (jarak spandek menjorok, bawaan 20 cm) di Properti |
| v0.35.0 | **Bangunan bertingkat**: alat Tangga (Y), plat lantai beton (W) dengan void, denah per level (`level` di gambar 2D dan MCP), RAB tangga dan plat |
| v0.36.0 | **Ukur dan gambar**: alat Meteran (Shift+T) dan Dimensi (D) ala SketchUp (anotasi `ukuran` + `geser`), lembar denah per lantai (`denah:<elevasi>`), kusen gabung satu rangka, boven jalusi, proyek contoh Kantor Utama |

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
| T | Tipe kusen | Y | Tangga beton lurus |
| W | Plat lantai beton | | |

Setiap perubahan dari luar membawa `diubahOleh` dan `diubahPada`. Lewat MCP, satu panggilan `terapkan_perubahan` sama dengan satu langkah Undo.

---

## 6. Cara kerja yang disepakati

1. **Dokumentasi dulu.** Setiap keputusan dicatat di *Dokumen Keputusan: Aplikasi Gambar Bangunan v1* sebelum atau bersama kodenya.
2. **Bertahap.** Untuk perubahan besar: usulan, tunggu "LANJUT" atau "OK", baru dikerjakan. Masalah kecil langsung diperbaiki.
3. **Usulan model dibahas dalam 2D dulu**, baru dibangun 3D.
4. **Uji di artifact dulu, baru exe.** Fitur baru diterbitkan ke artifact. Setelah pengguna memastikan berhasil, baru digabung ke main dan dibuatkan exe.
5. **Rilis.** Versi di `package.json` dinaikkan lewat pull request. Setelah merge ke main, GitHub Actions membuat Release `vX.Y.Z` berisi Setup.exe, Portable.exe, dan RANCANG.mcpb.
6. **Bahasa.** Antarmuka, komentar kode, dan pesan memakai Bahasa Indonesia. Commit memakai format Conventional Commits.
7. **Pola kerja dengan Claude (18 Oktober 2026): tunjuk dulu, baru perintah pendek.** Pengguna memilih benda di kanvas, lalu memberi perintah singkat ("geser 20 cm ke utara"). Kata *ini / itu / yang dipilih* selalu mengacu ke pilihan pengguna; bila pilihan kosong, Claude bertanya, bukan menebak.

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
- **Asrama Putri Poltek KP Sorong** (renovasi 2015, PDF CV. Awal Rahmat Konsultan; v0.35, proyek contoh `app/contoh/asrama-putri.json`, dibangkitkan `scripts/contoh-asrama-putri.py`), 375 elemen:
  - As 1–10 (350·350·450·450·450·300·450·450·450 = 37,00 m) × A–D (200·424·189); 2 lantai × 8 kamar tidur dengan KM/WC 2,00 m dan ceruk; selasar tembus 3,00 m; teras depan 1,89 m; tempat jemur belakang 3,00 m (lt.1) / balkon 1,25 m (lt.2).
  - Struktur: foot plat R1 170×170 (kolom 35/35, 12Ø16) dan R2 125×125 (kolom 30/30, 8Ø16); sloof SL1 25/40, SL2 20/30; balok lantai BL1 30/60, BL2 20/30 (puncak +4,00); ring balk RB1 20/30, RB2 15/20, RB3 25/35 (puncak +7,75); plat lantai 12 cm Ø10-120 K-250 dengan void tangga.
  - Tangga beton lurus 22 × 18/26 di blok ruang tamu timur (eksisting, disederhanakan), railing kiri.
  - Plafon tripleks 4 mm rangka kayu +3,50 dan +7,35; atap limas 35° seng multiroof, kuda-kuda kayu besi 5/10 jarak 3,30 m, overstek 1,20 m, lisplang papan, spandek menjorok 20 cm; atap limas tersendiri di blok tangga.
  - Kusen: P1 80, P2 60+90, P4 70 (KM, tanpa bovenlicht), PJ2 = pintu 70 + kaca mati 75 (bovenlicht 45), J1 2×75, J3 3×75, V1 2×75×45 (ambang 1,80), PJ1 kaca tinggi 5,80 di blok tangga.
  - Dibuka di aplikasi lewat palet Ctrl+K → *Buka contoh: Asrama Putri 2 lantai* atau panel Proyek → *Contoh*. Pemilih *Level* di Gambar 2D memberi denah lantai 1 (NAIK) dan lantai 2 (TURUN).

---

## 8. Keputusan 18 Oktober 2026: rencana perbaikan interaksi

**Keluhan pengguna** (berlaku di artifact maupun desktop):
1. Seleksi, grup, dan komponen sulit dioperasikan, sehingga pekerjaan kecil sulit dilakukan sendiri.
2. Semua akhirnya lewat prompt, dan prompt sering salah paham dengan maksud yang disampaikan.
3. Memperluas bidang seperti plafon sangat sulit.

**Diagnosis dari kode (v0.31.1):**
- Alat Pilih tidak menyorot benda di bawah kursor; sorotan (`soroti`) hanya dipakai Push/Pull, Hapus, dan Offset. Pengguna baru tahu yang terpilih setelah klik.
- Grup/komponen hanya dicapai lewat klik dua kali bertingkat dan Alt+klik; tidak ada daftar objek (outliner).
- Panel Properti tipis: pekerjaan kecil (geser pintu, ubah lebar jendela, putar komponen) tidak punya isian angka, jadi terpaksa lewat prompt.
- Server MCP tidak tahu pilihan pengguna dan grup yang sedang dibuka; hanya Panel Claude di artifact yang mengirimnya. Inilah sumber utama salah paham.
- Plafon dibuat per ruang dari batas dinding; mode gabungan hanya membuat selubung persegi panjang. Setelah jadi, bentuknya hanya bisa diubah lewat Push/Pull tepi (dan, sejak v0.32 di PR #20, alat Perpanjang/Pangkas H untuk menarik satu sisi ke batas benda lain); Offset menolak plafon; tidak ada cara menyeret sudut, menambah titik, atau mengetik koordinat alas. Berlaku juga untuk lantai (`volume`) dan lubang.

**Rencana yang disepakati** (tiap tahap satu PR, diuji di artifact dulu, lalu rilis exe):

| Tahap | Isi | Rilis |
|---|---|---|
| 1 | Sorotan saat kursor lewat di alat Pilih + nama dan jalur benda di bilah status (`Pintu P2 · Dinding D7 · Grup Kamar 1`); alat MCP `pilihan_pengguna` (id terpilih, grup dibuka, muka terpilih); instruksi Claude untuk pola "tunjuk dulu, baru perintah pendek" | v0.33 |
| 2 | **Sunting alas** untuk plafon/lantai/lubang: klik dua kali masuk mode sunting, seret sudut dengan snap, klik tepi menambah titik, Delete membuang titik, Esc selesai; Offset menerima plafon dan lubang; plafon gabungan memakai gabungan poligon sungguhan (polygon-clipping); tombol "Pas ke ruang" di Properti; melanjutkan alat Perpanjang/Pangkas (Shift+H) dari v0.32 yang sudah bisa menarik sisi plafon ke batas benda lain | v0.34 |
| 3 | Outliner di panel kiri: pohon grup → komponen → elemen; klik memilih, klik dua kali masuk, ikon mata menyembunyikan, menu klik kanan sama dengan kanvas; sinkron dengan pilihan kanvas | v0.35 |
| 4 | Properti per jenis dengan isian angka langsung diterapkan: bukaan (jarak dari ujung, lebar, tinggi, ambang, tipe kusen), instance (posisi, rotasi, elevasi), kolom (penampang, posisi), dinding (ujung awal/akhir), daftar titik alas | v0.36 |
| 5 | Pegangan langsung lainnya: seret ujung dinding, seret pintu sepanjang dinding, panah pindah pada benda terpilih | dinilai lagi setelah 1–4 dipakai |

Sunting Alas ditempatkan di tahap 2 karena disebut langsung sebagai hambatan nyata dan mekanisme peganganannya dipakai lagi di tahap 5.

**Keputusan tambahan 18 Oktober 2026 (malam), dikerjakan di PR #21 / v0.33:**
- *Plafon miring tidak mendapat menu/alat sendiri.* Alasan: bilah alat sudah 23 tombol dan semua huruf A–Z terpakai; plafon datar dan miring sama bahan/rangka/lis-nya, hanya bidangnya yang miring; prinsip RANCANG: pengaturan ada di panel Properti benda yang dipilih. Yang dilakukan: pemilih mode *Per ruang · Gabungan · Miring* terlihat di bilah petunjuk alat Plafon; satu komponen isian plafon (`medanSetelPlafon`) dipakai untuk P, bidang H peran plafon, dan atap (`plafonBahan`, `plafonRangka`); bidang plafon menyimpan `turun` dan bisa diketik ulang; RAB plafon miring menyatu dengan plafon datar (PL-004 ditiadakan).
- *Ukuran alas plafon/lantai bisa diketik* (lebar X, panjang Y dengan sisi tetap, perluas semua sisi) sebagai pengganti Push/Pull untuk ukuran pasti.
- Perbaikan kecil atas laporan uji: info kursor dipindah ke lapisan kanvas (gambar goyang), sorotan hanya muka di bawah kursor (grup besar berat), garis potong di atas pelat lantai + daftar Pilih, Extend/Trim = Shift+H (bentrok Tembus), Panel Claude menerima Ctrl+V tangkapan layar.

**Desain ulang v0.34 (mock-up disetujui 18 Oktober 2026 malam, artifact *Desain Ulang RANCANG v0.34*).** Aturan pengguna: menu bisa dilipat agar ruang kerja luas; informatif tapi tidak berlebihan (tiga tingkat: selalu tampak → saat ada pilihan → hanya bila diminta); pintasan hanya untuk alat yang sering dipakai, mengikuti SketchUp/AutoCAD.
- Tahap A (v0.34.0): peta pintasan baru, palet perintah Ctrl+K, menu alat tiga keadaan, panel jadi rel tab, mode fokus.
- Tahap B (berikutnya): panel bertab Properti · Objek (outliner) · Claude, kartu properti ringkas mengambang di mode fokus.
- Tahap C: tab Claude di desktop lewat API key Anthropic (berbayar per pakai) di samping jalur MCP.

**Bangunan bertingkat (v0.35.0, 18 Oktober 2026).** Untuk menggambar Asrama Putri 2 lantai (PDF gambar kerja, 37,0 × 8,75 m, lantai 2 di +4,00) diputuskan tiga alat dibuat dulu, baru modelnya: (1) **Tangga** beton lurus parametrik — dua klik, jumlah anak dari tinggi level, panel Properti, denah NAIK/TURUN, RAB; (2) **Plat lantai beton** (W) dengan lubang void, dikonversi dari lantai biasa, masuk RAB beton/besi/bekisting; (3) **Denah per level** — pemilih Level di bar Gambar 2D dan parameter `level` di MCP `gambar_2d`. Tangga bordes/putar belum ada: digambar sebagai dua tangga lurus + plat bordes.

**Perbaikan plafon miring (18 Oktober 2026 malam, PR #24 → v0.34.1).** Laporan pengguna: plafon miring ikut sepanjang spandek, padahal seharusnya berhenti di lisplang; spandek menjorok ±20 cm dan harus bisa diatur; pengaturannya harus ada di Properti atau terpotong otomatis saat dibuat. Yang dilakukan:
- Alat Plafon mode *Miring* memakai muka atap yang dimundurkan sampai sisi dalam papan lisplang (`susunTepiAtap(d).muka[].dalam`), bukan muka penutup; berlaku juga untuk atap yang sudah dipecah (tepi bidang H yang berpapan lisplang H sejajar dimundurkan, `mundurKeLisplang`).
- Bawaan *Mundur dari ujung seng* menjadi 20 cm untuk semua rangka (sebelumnya baja ringan 0, sehingga perbaikan tidak terlihat). Atap baja ringan lama ikut bergeser; tetap bisa diatur per sisi lisplang.
- Isian baru di Properti plafon miring: *Jarak tepi plafon dari ujung seng (m)* (`mundurSeng`, terisi otomatis = mundur + tebal papan, mis. 0,225); mengetik ulang menggeser tepi luar yang berhadapan dengan lisplang.
- Papan lisplang diterima sebagai batas alat Perpanjang/Pangkas (sisi dalam papan).
- Uji asap 26 langkah: kayu, baja ringan, atap terpecah, isian jarak (0,225 → 0,40 = geser 15 cm mendatar pada 30°).

**Keputusan 23 Oktober 2026: rencana "penyesuaian kecil" (v0.48 → v0.50).** Keluhan pengguna: memperbaiki hal kecil pada model buatan Claude (spandek kurang panjang beberapa cm, dinding kurang tinggi sampai gording, atap miring berbentuk segitiga, gording melewati lisplang, DXF yang garis tertutupnya tidak terpangkas) mudah di SketchUp/AutoCAD tetapi sulit di RANCANG; tanpa tampilan seperti Outliner pengguna tidak tahu yang diklik itu grup besar, pecahan grup, atau elemen. Diagnosis: (1) konteks pilihan tidak terlihat, (2) belum ada alat umum "X sampai/berhenti di Y" — Shift+H baru untuk lisplang dan plafon, (3) ekspor DXF tanpa penghapusan garis tersembunyi. Urutan baru (Outliner dinaikkan ke depan, sebelum Sunting Alas dan Properti per jenis; diperbarui malam 23 Oktober):

| Urutan | Versi | Isi |
|---|---|---|
| 1 | v0.48 | Outliner (tombol *Objek*, mengambang di kiri kanvas) + jalur konteks yang bisa diklik — **selesai, PR #51 digabung** |
| 2 | v0.49 | Node & rusuk X/Y/Z untuk semua elemen + Shift+H umum (lihat keputusan malam di bawah) — **selesai, PR menunggu uji artifact** |
| 3 | v0.50 | Kerangka proyek: jenis (gedung/jembatan/dermaga), elevasi dan tingkat di tampak samping, grid as |
| 4 | v0.51 | Garis → bidang, material, Push/Pull menjadi elemen sesuai material, union per material |
| 5 | v0.52 | Node & rusuk untuk pintu/jendela, kolom, pondasi footplat/umpak, tangga, tiang |
| 6 | v0.53 | DXF hidden-line |
| 7 | v0.54 | APK hanya untuk melihat (view-only) |

Outliner ditempatkan mengambang di kiri kanvas (bukan tab di panel kanan seperti Tahap B v0.34) supaya pohon dan panel Properti terlihat bersamaan, seperti Outliner + Entity Info di SketchUp; bisa ditutup kapan saja.

**Keputusan 23 Oktober 2026 (malam): v0.49 Node & rusuk — perubahan dari rencana Shift+H.** Pengguna menegaskan: Push/Pull sudah ada, yang belum ada adalah mengubah **rusuk, titik sudut, dan panjang garis** pada semua elemen (spandek, kayu, kaca, beton, dinding, dll.), termasuk bentuk 2D dan **sumbu Z** (sekarang hanya X/Y), serta **memecah satu garis menjadi beberapa node**. Pekerjaan kecil seperti geser 15 cm harus bisa dengan alat, tidak lewat Claude. Isi v0.49 (satu alat *Node & rusuk*, pintasan N):
- Sorotan node/rusuk di bawah kursor; klik node atau rusuk, geser X/Y/Z dengan inferensi dan kunci sumbu (panah), ketik jarak lalu Enter.
- Tambah node (klik 2× pada rusuk), bagi rusuk (ketik /n), hapus node (Delete); panjang rusuk dan koordinat node bisa diketik di Properti.
- Shift+H dengan node/rusuk terpilih: node bergerak sampai menyentuh benda yang diklik (dinding naik sampai gording, gording dipangkas di lisplang, spandek sampai lisplang).
- Berlaku untuk bidang 3D, lantai/plafon/plat, dinding (as bawah dan tepi atas), batang kayu/baja, balok/slof/ring balk, sapuan. Node baru pada as dinding, batang, atau balok memecah elemen menjadi dua (RAB tetap). Pintu/jendela, kolom, pondasi, tangga, tiang menyusul di v0.50.
- Plafon datar yang dimiringkan (Z) otomatis menjadi plafon miring (bidang H peran plafon, RAB menyatu). Lantai dan plat beton yang dimiringkan **ditolak dengan pesan** (RAB dihitung datar); bisa diubah bila pengguna memilih lain.
- Salinan komponen dibuka dulu; atap parametrik dipecah dulu (Pecah atap) agar rusuknya bisa dipegang.

**Keputusan 23 Oktober 2026 (malam): konsep menggambar diperbaiki — "material menentukan jenis elemen".** Usulan pengguna: menggambar dimulai dari bidang datar (garis, lengkung, lingkaran → bidang), diberi material, lalu dijadikan bidang ruang; material sama bisa digabung (union) dan diolah seperti bidang lain; membangun dimulai dari tampak samping (elevasi, jumlah tingkat; perlakuan serupa dengan nama berbeda untuk jembatan dan dermaga), dibantu grid as, lalu disusun dari elemen → grup → komponen → grup … sampai bangunan utuh. Pertimbangan: keputusan inti 16 Oktober (data = elemen bangunan, bukan garis/bidang bebas) dipertahankan karena gambar kerja 2D dan RAB rinci (beton, besi, bekisting) bergantung padanya. **Disetujui pengguna:** jalan tengah —
- Pengguna menggambar bebas: garis yang tertutup menjadi bidang; persegi, lingkaran, busur tetap.
- Bidang diberi **material** dari pustaka material. Saat bidang ditarik (Push/Pull), RANCANG menjadikannya elemen sesuai material dan arahnya: datar + beton bertulang → plat (W); datar + keramik/rabat → lantai (V); tegak + bata/GRC/kaca → dinding (D); penampang kecil + beton → kolom/balok menurut arah tarik; penampang + kayu/baja profil → batang (J); miring + spandek/genteng → bidang atap (H); material *bebas* → volume biasa dengan RAB m³/m² per material.
- **Union/Kurangi** berlaku antar-elemen bermaterial sama (diperluas dari alat solid v0.27 yang kini hanya untuk lantai/plafon).
- **Kerangka proyek** sebagai langkah pertama proyek baru: pilih jenis (gedung, jembatan, dermaga); atur elevasi dan jumlah tingkat pada gambar tampak samping dengan nama sesuai jenis (gedung: pondasi, lantai 1…n, ring balk, nok; dermaga: dasar laut, LWS, HWL, pile cap, lantai dermaga; jembatan: dasar sungai, muka air banjir, tumpuan, gelagar, lantai jembatan); lalu grid as. Hasilnya level dan as yang dipakai semua alat.
- Alur bertingkat dipandu bersama Outliner: elemen → grup → komponen → grup → bangunan.

Urutan baru: v0.50 Kerangka proyek · v0.51 Garis → bidang + material → elemen (+ union per material) · v0.52 Node untuk pintu/jendela, kolom, pondasi footplat/umpak, tangga, tiang · v0.53 DXF hidden-line · v0.54 APK view-only.

**Pertanyaan yang masih terbuka**
- Pekerjaan kecil yang paling sering dibutuhkan (menentukan urutan isi tahap 4).
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
4. **Pekerjaan sekarang adalah mutu alat edit manual.** Seleksi yang pasti, bidang yang bisa dibentuk ulang, outliner, dan properti yang bisa diketik, supaya pengguna mengerjakan sendiri hal-hal kecil dan menyerahkan pekerjaan besar ke Claude. Platform tetap HTML + Three.js; tidak ditulis ulang.
5. **Disiplin proses menjaga mutu.** Keputusan tertulis lebih dulu, tahapan dengan LANJUT, uji di artifact sebelum exe, dan satu sumber kode.
