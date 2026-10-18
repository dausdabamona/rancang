## Yang baru di 0.34.1

- **Plafon miring berhenti di lisplang.** Alat Plafon mode *Miring* kini memotong plafon di sisi dalam papan lisplang, bukan di ujung seng. Seng tetap menjorok sejauh *Mundur dari ujung seng* (bawaan 20 cm pada rangka kayu; 0 pada baja ringan), yang bisa diatur per sisi di panel atap → Lisplang. Atap tanpa lisplang tetap memakai tepi penutup.
- **Papan lisplang bisa jadi batas Perpanjang/Pangkas** (Shift+H): klik plafon yang sudah ada, lalu klik papan lisplang; sisi plafon dipangkas/diperpanjang sampai sisi dalam papan. Berguna untuk merapikan plafon miring yang dibuat sebelum 0.34.1.

## Yang baru di 0.34.0

Tahap A desain ulang (mock-up *Desain Ulang RANCANG v0.34*, keputusan 18 Oktober 2026): lebih sedikit yang harus diingat, lebih banyak yang terlihat, ruang kerja lebih luas.

- **Pintasan hanya untuk alat yang sering dipakai**, mengikuti kebiasaan SketchUp/AutoCAD: Spasi Pilih · M Pindah · Q Putar · R Persegi · L Dinding · C Lingkaran · A Busur · P Push/Pull · F Offset · E Hapus · O Orbit · T Garis bantu · Z Zoom semua · H Tembus · Shift+H Perpanjang/Pangkas · Ctrl+G Grup. Yang berpindah dari 0.33: T (tadinya Atap), Q (tadinya Offset), F (tadinya Pondasi); G tanpa Ctrl tidak lagi membuat komponen. Huruf lain dilepas: alat itu dibuka dari bilah alat atau palet.
- **Palet perintah Ctrl+K** (tombol *Cari* di bilah atas): ketik sebagian nama untuk alat, elemen (nama/id), grup, lembar 2D, potongan, perintah tampilan, dan Claude. Singkatan AutoCAD dikenali: TR/EX Perpanjang-Pangkas, MI Cermin, RO Putar, CO Pindah, OF Offset, SEC Potongan, DIM Anotasi, REC Persegi.
- **Menu alat tiga keadaan** (Ctrl+B bergantian): penuh → ringkas (satu kolom, hanya alat sering dipakai, tombol *Alat lain* membuka palet) → tersembunyi.
- **Panel kanan dilipat menjadi rel tab** (Ctrl+J): tombol tegak *Properti* dan *Claude*; klik membuka lagi.
- **Mode fokus** (Ctrl+Shift+F, tombol *Fokus*): menu ringkas + panel jadi rel; keluar mengembalikan keadaan sebelumnya. Keadaan tata letak diingat per komputer.

## Yang baru di 0.33.0

Tahap 1 dari rencana perbaikan interaksi (keputusan 18 Oktober 2026): seleksi yang pasti, dan Claude tahu apa yang Anda tunjuk.

- **Sorotan saat kursor lewat di alat Pilih.** Muka di bawah kursor disorot, dan info kursor di sudut kanvas menyebut benda yang *akan* terpilih bila diklik (termasuk grupnya). Hanya satu muka yang disorot supaya grup besar tetap ringan.
- **Bilah bawah menyebut sasaran kursor**: nama, id, dan jalurnya (`Pintu P2 · di Dinding D7 · Grup Kamar 1`), plus berapa benda lagi di belakangnya (Alt+klik). Saat kursor tidak di atas benda, bilah menampilkan ringkasan pilihan sekarang.
- **Alat MCP baru `pilihan_pengguna`**: Claude desktop bisa membaca benda yang sedang Anda pilih, muka yang terpilih, dan grup yang sedang dibuka. `info_proyek` ikut menyertakan ringkasannya.
- **Ukuran alas di panel Properti** untuk plafon dan lantai: ketik **Lebar arah X** atau **Panjang arah Y** yang baru (alas diskalakan dari sisi yang Anda pilih tetap: barat/tengah/timur, selatan/tengah/utara), atau **Perluas semua sisi** (plus keluar, minus ke dalam). Tidak perlu Push/Pull untuk ukuran pasti.
- **Garis potong lebih mudah dipilih**: penandanya digambar di atas pelat lantai (tidak lagi tertimbun), pita kliknya lebih lebar, dan panel ringkasan (saat tidak ada yang dipilih) menampilkan daftar garis potong dengan tombol *Pilih*.
- **Pintasan Perpanjang/Pangkas menjadi Shift+H** (H tetap untuk Tembus pandang; sebelumnya bentrok sehingga H selalu membuka Tembus).
- **Panel Claude menerima tangkapan layar lewat Ctrl+V** dan seret-lepas gambar ke panel, selain tombol *Lampirkan gambar*.
- **Pengaturan plafon miring disatukan, tanpa menu baru**: alat Plafon menampilkan pemilih mode *Per ruang · Gabungan · Miring* di bilah petunjuk (Tab tetap bekerja); plafon miring bebas (bidang) mendapat bahan, rangka, lis, dan *jarak di bawah penutup atap* yang bisa diketik ulang; plafon miring bawaan atap bisa dipilih bahan dan rangkanya. RAB plafon miring kini masuk baris yang sama dengan plafon datar (PL-002…PL-007, rangka PL-011…PL-016); baris PL-004 ditiadakan.
- **Pola kerja baru dengan Claude: tunjuk dulu, baru perintah pendek.** Kata *ini / itu / yang dipilih* kini selalu mengacu ke pilihan Anda, baik lewat MCP maupun Panel Claude di artifact. Bila tidak ada yang dipilih, Claude bertanya, bukan menebak.

## Yang baru di 0.26.0

- **Simbol perabot dan sanitair** ukuran nyata di denah (alat Simbol, tekan R untuk memutar): kasur, lemari, meja, sofa, kloset, wastafel, shower, bak mandi, kitchen set, pohon.
- **Legenda otomatis** dari isi lembar (alat Legenda).
- **Unggah logo** untuk kop semua lembar.
- **Pustaka detail sendiri**: gambar di petak Detail bebas, simpan ke pustaka, pakai lagi di lembar atau proyek lain.
- **Perbaikan klos penahan gording**: kini di sisi bawah gording (3D, potongan, detail kuda-kuda).
- Claude lewat MCP bisa membuat gambar lembar detail (det:1, det:2, …).

## Yang baru di 0.25.0

- **Zoom gambar 2D** dan **Ruang Lembar**: daftar lembar, sampul, daftar gambar, kop di kanan (3 model), urutan lembar bisa diseret.
- **PDF semua lembar sekaligus** dengan sampul.
- **Alat gambar 2D** sendiri: garis, polyline, persegi, lingkaran, busur, teks, arsir, tanda rujukan.
- **Ukuran berantai dari as dinding**, gelembung as, skala 1 : 150 dan skala bebas, peil bisa digeser dan disembunyikan.
- **Pustaka detail**: pondasi batu kali, foot plat, umpak, **kuda-kuda**, dan **sambungan kayu** (tumpuan, puncak, kaki makelar, sokong, perpanjangan) di lembar detail; keterangan dibagi kiri-kanan.
- **Ekspor DXF** (per lembar atau semua lembar dalam ZIP) untuk AutoCAD/BricsCAD/LibreCAD, dan **model 3D DAE** untuk SketchUp (File → Import).
- Daftar kusen kini selalu muat di kertas (skala menyesuaikan).

## Unduhan

| Berkas | Untuk |
|---|---|
| `RANCANG-Setup-x.y.z.exe` | Pasang di Windows 10/11: ada shortcut Start Menu dan desktop, berkas `.rancang` terbuka dengan klik dua kali. Tidak perlu hak admin. |
| `RANCANG-Portable-x.y.z.exe` | Langsung jalan tanpa instalasi (cocok untuk laptop kantor yang membatasi pemasangan program). |
| `RANCANG.mcpb` | Ekstensi Claude desktop: klik dua kali untuk menyambungkan Claude dengan RANCANG. |

**Windows SmartScreen:** aplikasi belum bertanda tangan digital, jadi saat pertama dijalankan Windows menampilkan "Windows protected your PC". Klik **More info → Run anyway**.

Panduan lengkap: lihat [README](https://github.com/dausdabamona/rancang#readme).
