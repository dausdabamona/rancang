## Yang baru di 0.33.0

Tahap 1 dari rencana perbaikan interaksi (keputusan 18 Oktober 2026): seleksi yang pasti, dan Claude tahu apa yang Anda tunjuk.

- **Sorotan saat kursor lewat di alat Pilih.** Muka di bawah kursor disorot, dan info kursor di sudut kanvas menyebut benda yang *akan* terpilih bila diklik (termasuk grupnya). Hanya satu muka yang disorot supaya grup besar tetap ringan.
- **Bilah bawah menyebut sasaran kursor**: nama, id, dan jalurnya (`Pintu P2 · di Dinding D7 · Grup Kamar 1`), plus berapa benda lagi di belakangnya (Alt+klik). Saat kursor tidak di atas benda, bilah menampilkan ringkasan pilihan sekarang.
- **Alat MCP baru `pilihan_pengguna`**: Claude desktop bisa membaca benda yang sedang Anda pilih, muka yang terpilih, dan grup yang sedang dibuka. `info_proyek` ikut menyertakan ringkasannya.
- **Ukuran alas di panel Properti** untuk plafon dan lantai: ketik **Lebar arah X** atau **Panjang arah Y** yang baru (alas diskalakan dari sisi yang Anda pilih tetap: barat/tengah/timur, selatan/tengah/utara), atau **Perluas semua sisi** (plus keluar, minus ke dalam). Tidak perlu Push/Pull untuk ukuran pasti.
- **Garis potong lebih mudah dipilih**: penandanya digambar di atas pelat lantai (tidak lagi tertimbun), pita kliknya lebih lebar, dan panel ringkasan (saat tidak ada yang dipilih) menampilkan daftar garis potong dengan tombol *Pilih*.
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
