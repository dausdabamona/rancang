# Pemeriksaan Tipe RANCANG (@ts-check)

*18 Oktober 2026 · skrip utama `app/rancang.html` · tsc 5.9 + @types/three 0.149*

Perintah: `npm run periksa-tipe` (tanpa langkah build; skrip diekstrak ke `build/tipe/` lalu diperiksa `tsc --noEmit --allowJs --checkJs`). Typedef ada di blok `/* ===== TIPE ===== */` di awal skrip; deklarasi global (THREE, polygonClipping, XLSX, window.claude) di `tipe/global.d.ts`.

Hasil pertama: **442 kesalahan tipe**, 396 di antaranya `TS2339` (akses properti pada union `ElemenRancang` tanpa penyempitan `jenis`). Yang penting bukan jumlahnya, tetapi beberapa kesalahan yang menunjukkan bug nyata. Semua perbaikan **diusulkan terpisah**; commit tipe ini tidak mengubah perilaku.

## Risiko tinggi: bug nyata yang mengubah hasil

| # | Lokasi | Temuan | Dampak |
|---|---|---|---|
| T1 | `pecahLantai`, baris ±7117: `const top = r2(atas - turun)` | `atas` **tidak terdefinisi** di fungsi itu. Sejak commit 6b561ff (v0.28) deklarasinya pindah ke `pemotongLantai`. Diuji headless: `ReferenceError: atas is not defined`. | Tombol **Pecah per ruang** gagal total sejak v0.28.0. |
| T2 | `total()`, baris ±7042: `t.nV++; t.luasAlas += u.luasAlas` | Sapuan jatuh ke cabang volume; `ukurSapuan` tidak punya `luasAlas`. | `luasAlas` menjadi **NaN** bila model memuat sapuan; sapuan juga belum masuk `dataRAB`. |
| T3 | `sah()` untuk dinding, volume, kolom, slof, pondasi, atap, instance | `z0` dan `tinggi` tidak diperiksa tipenya (hanya `>= 0` yang lolos untuk string angka). | Data MCP `z0:"0.1"` lolos; `(b.z0 \|\| 0) + dz` menjadi penggabungan string, geometri rusak diam-diam. |
| T4 | `buatGrup()` saat Tembus aktif | `targetDariKlik` memindah `S.konteks` ke subgrup elemen yang diklik; Ctrl+G dengan pilihan campuran bisa membuat `induk` bersiklus. Tidak ada pemeriksaan siklus di `buatGrup` maupun `terapkanLuar`. | Grup hilang dari daftar teratas dan dari RAB (`semuaId`), `leluhur` berputar sampai batas 50. |

## Risiko sedang: data atau id bisa salah

| # | Lokasi | Temuan |
|---|---|---|
| S1 | `ringkasProyek`, awalan `'DBVCSRFAPXNGTLE'` | Tanpa **H, J, U, I, K**; Claude lewat MCP tidak diberi nomor id terbesar untuk bidang, batang, sapuan, dan komponen, sehingga id baru bisa bentrok. |
| S2 | `AWALAN` (baris ±668) dan `pemberiId` (`'DVBACSRPFXNHJU'`) | `gambar2d`→L dan `detail`→E tidak ada; `dariDefinisi` jatuh ke `'V'`; mode edit komponen tanpa L/E/I. |
| S3 | `muatProyek` mode "tambah" | Rujukan `grup` ke G yang tidak ada di berkas tidak dipetakan ulang; elemen bisa menempel ke G lain bernomor sama. |
| S4 | `terapkanLuar` | Elemen tanpa `grup` diterima (keluar dari grup), G dihapus lewat `data:null` tanpa memperbarui anaknya, G tanpa `induk` menjadi teratas. |
| S5 | `sahData` G mewajibkan `nama` string; `langgananKoleksi` dan `bacaProyek` melewati G yang gagal | Elemen menjadi yatim: tidak bisa diedit, dan dikecualikan dari RAB. |
| S6 | Pintasan **G** tanpa Ctrl = `jadikanKomponen` | Menghapus grup terpilih beserta subgrupnya, diganti satu komponen; `pecahKomponen` tidak memulihkan grup. Salah tekan saat bermaksud Ctrl+G. |
| S7 | Alat Hapus dan Delete saat Tembus mati | `targetKlik` memilih grup terluar; `hapusPilihan` menghapus seluruh isinya. Klik satu umpak bisa menghapus satu bangunan (Ctrl+Z menolong). |
| S8 | `buatSVG` / `gambar2D` | `skala` kadang angka, kadang `'-'` atau `'TERTERA'`; pemanggil (`#m-info`, DXF, PDF) membandingkan string dengan angka. Perlu satu bentuk. |

## Risiko rendah: ketidakkonsistenan yang menyulitkan tipe, tidak merusak data

- Arti `z0` berbeda per jenis: dasar (dinding, volume, kolom, slof, foot plat), puncak (batu kali, umpak), muka bawah (plafon), dudukan (atap). Bawaan beragam: `|| 0`, `?? -h`, `?? -0.2`, `?? -1.2`, `?? 0.1`.
- `dinding` dipakai untuk dua tipe: id string pada bukaan, persegi `{x0,y0,x1,y1}` pada bidang.
- `batang.atas` berupa larik `[x,y,z]`; semua titik lain objek `{x,y,z}`.
- `ukuran` tiga arti: objek profil (sapuan), mm (gambar 2D), `[b,h]` (batang rangka internal). `b`/`h` lebar X/Y pada kolom, lebar/tinggi penampang pada batang dan balok.
- `susunTepiAtap` dideklarasikan `function` lalu ditimpa (`susunTepiAtap = function …`) untuk cache: sah di JS, ditolak tsc (TS2630). Sebaiknya `let`.
- Fungsi dipanggil dengan argumen yang tidak dideklarasikan: `garisBatuKali.dbl(e)`, `lapor(i, n, nama)` dengan bawaan `() => {}` (TS2554). Tidak berbahaya.
- Pengurutan kunci objek dengan `sort((a, b) => a - b)` pada string (`r.beton`), mengandalkan koersi implisit.
- Panduan data MCP menyebut `putar` pada J (tidak ada di kode), `mukaHapus` pada atap (hanya volume), tidak menyebut `G.pecahan`, dan `pada` anotasi hanya `'denah'` (kode: `semua|denah|tampak|potongan`).
- `peran` sapuan dan `tebalGunung` atap tidak divalidasi dan tidak punya UI.

## Kesalahan yang bukan bug (bising)

- 396 × TS2339: properti diakses pada `ElemenRancang` tanpa `if (d.jenis === …)`. Akan berkurang sendiri saat fungsi-fungsi per jenis diberi `@param {Dinding}` dsb.
- Akses DOM generik (`dataset`, `closest`, `matches` pada `Element`/`EventTarget`), `material`/`geometry` pada `Object3D`, `camera` union perspektif/ortografik, `jspdf`/`svg2pdf` di `window`.
- Tuple campuran `[string, number]` yang dipakai dalam aritmetika (kop gambar, DXF, sisi atap).

## Usulan perbaikan (menunggu persetujuan satu per satu)

1. **T1** `pecahLantai`: hitung ulang `const atas = (d.z0 || 0) + (d.tinggi || 0)` di dalam fungsi. Satu baris; uji headless sudah disiapkan.
2. **T2** `total()`: cabang khusus sapuan (panjang, volume) dan baris RAB sapuan per profil.
3. **S1 + S2**: lengkapi `ringkasProyek`, `AWALAN`, `pemberiId`.
4. **T3**: `sah` memeriksa `Number.isFinite` untuk `z0`/`tinggi` yang ada.
5. **T4 + S4**: pemeriksaan siklus `induk` di `buatGrup` dan `terapkanLuar`; `terapkanLuar` memperbarui anak saat G dihapus.
6. **S6 + S7**: pintasan G diberi konfirmasi atau dipindah; alat Hapus pada grup terluar meminta konfirmasi bila isinya > 1.
7. **S8**: `skala` selalu angka, label `'-'`/`'TERTERA'` dipindah ke medan `skalaTeks`.
