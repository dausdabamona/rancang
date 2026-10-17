# RANCANG

Aplikasi gambar bangunan ala SketchUp: gambar model 3D (dinding, pintu/jendela, lantai, kolom, sloof, ring balk, pondasi, atap dengan kuda-kuda kayu atau baja ringan, plafon), lalu hasilkan **gambar kerja 2D** (denah, tampak, potongan, daftar kusen, detail penulangan) dan **volume RAB** yang bisa diekspor ke Excel.

RANCANG bisa **berkolaborasi dengan Claude**: Claude membaca model, menggambar atau mengubah elemen, membuat gambar 2D, dan menghitung volume langsung di aplikasi Anda. Setiap perubahan dari Claude disorot oranye dan bisa dibatalkan dengan Ctrl+Z.

## Unduh dan pasang (Windows 10/11)

1. Buka halaman **[Releases](https://github.com/dausdabamona/rancang/releases)** dan unduh salah satu:
   - `RANCANG-Setup-x.y.z.exe`: dipasang (shortcut Start Menu dan desktop, berkas `.rancang` terbuka dengan klik dua kali). Tidak perlu hak admin.
   - `RANCANG-Portable-x.y.z.exe`: langsung jalan tanpa instalasi.
2. Saat pertama dijalankan, Windows SmartScreen menampilkan **"Windows protected your PC"** karena aplikasi belum bertanda tangan digital. Klik **More info → Run anyway**.
3. Proyek pertama otomatis dibuat di `Dokumen\RANCANG\Proyek baru.rancang`. Semua perubahan **tersimpan otomatis**.

Aplikasi berjalan **luring penuh**: Three.js, pustaka poligon, pembuat Excel, dan huruf sudah ada di dalam aplikasi.

### Berkas proyek

- Menu **Berkas**: Proyek baru (Ctrl+N), Buka proyek (Ctrl+Shift+O), Simpan sebagai (Ctrl+Shift+S), Tampilkan berkas proyek di folder.
- Format `.rancang` adalah JSON. Berkas **Simpan proyek (.json)** dari versi web (artifact) bisa dibuka lewat Buka proyek, dan sebaliknya.
- Saat proyek dibuka, salinan cadangan `nama.rancang.bak` dibuat di sebelahnya.
- Bila berkas proyek diubah dari luar (misalnya oleh Claude lewat folder yang tersambung), aplikasi memuat ulang dan menyorot perubahannya.

## Sambungkan dengan Claude (MCP)

1. Pastikan **Claude desktop** terpasang dan RANCANG sudah pernah dibuka sekali.
2. Unduh `RANCANG.mcpb` dari Releases, lalu **klik dua kali**. Claude desktop membuka jendela pemasangan ekstensi; klik **Install**. (Atau: Claude desktop → Settings → Extensions → Install Extension… → pilih `RANCANG.mcpb`.)
3. Di percakapan Claude, minta misalnya: *"Lihat proyek RANCANG saya dan buatkan dinding sekat di as 3 dengan pintu P2"*.

Alat yang tersedia untuk Claude:

| Alat | Fungsi |
|---|---|
| `panduan_data` | Panduan isian data setiap jenis elemen |
| `info_proyek` | Nama berkas, jumlah elemen, jenis gambar yang tersedia |
| `daftar_elemen`, `ambil_elemen` | Membaca model |
| `terapkan_perubahan` | Menambah, mengubah, menghapus elemen (diperiksa dulu, ditolak utuh bila ada yang salah) |
| `ringkasan_ukuran`, `volume_rab` | Ukuran dan volume RAB |
| `gambar_2d` | Denah, tampak, potongan, daftar kusen (PNG atau SVG) |
| `tangkap_layar_3d` | Tangkapan layar tampilan 3D |
| `buka_proyek`, `simpan_proyek_sebagai` | Berpindah atau menyimpan berkas proyek |

Keamanan: jembatan antara Claude dan aplikasi hanya terbuka di komputer ini (`127.0.0.1`) dan dikunci token acak yang dibuat ulang setiap aplikasi dibuka. Claude desktop meminta izin Anda sebelum menjalankan alat.

Bila aplikasi tertutup, Claude tetap bisa membaca dan mengubah berkas proyek terakhir. Untuk gambar, RAB, dan tangkap layar, aplikasi dijalankan otomatis.

## Pengembangan

Sumber aplikasi hanya satu: **`app/rancang.html`**. Versi web (artifact Claude) diterbitkan langsung dari berkas itu; versi desktop disusun darinya.

```
app/rancang.html          sumber aplikasi (versi artifact dan desktop)
electron/main.js          proses utama: jendela, menu, berkas proyek, jembatan MCP
electron/penyimpanan.js   berkas .rancang: simpan otomatis, cadangan, pantau perubahan luar
electron/jembatan.js      HTTP lokal 127.0.0.1 + token untuk server MCP
electron/preload.js       API kecil ke halaman (sandbox)
electron/renderer/claude-shim.js   pengganti window.claude (db, user, downloads) di desktop
mcp/server.mjs            server MCP (dibundel esbuild), mcp/manifest.json, mcp/panduan-data.md
scripts/build-renderer.mjs  halaman luring: CDN dan Google Fonts diganti salinan lokal
scripts/build-mcp.mjs     paket build/mcp → RANCANG.mcpb
test/                     uji unit penyimpanan dan uji MCP (mode berkas dan mode aplikasi)
.github/workflows/build.yml  build Windows, uji, artefak, Release saat tag v*
```

Perintah:

| Perintah | Fungsi |
|---|---|
| `npm ci` | Pasang dependensi |
| `npm start` | Susun renderer lalu jalankan aplikasi |
| `npm run build` | Susun renderer luring dan server MCP |
| `npm test` | Uji unit + MCP mode berkas (`RANCANG_UJI_ELECTRON=1` untuk menguji MCP terhadap aplikasi yang berjalan) |
| `npm run uji-asap` | Jalankan aplikasi tersembunyi, uji alur utama, lalu keluar |
| `npm run dist:win` | Build Setup.exe dan Portable.exe (di Windows) |
| `npm run pack:mcpb` | Paketkan `build/RANCANG.mcpb` |

### Merilis versi baru

1. Naikkan `version` di `package.json` (misalnya `0.25.0`) lewat pull request.
2. Setelah digabung ke `main`, buat tag yang sama: `git tag v0.25.0 && git push origin v0.25.0`.
3. GitHub Actions menguji, membangun, dan menerbitkan Release berisi Setup.exe, Portable.exe, dan RANCANG.mcpb.

Setiap push ke `main` dan setiap pull request juga dibangun; hasilnya bisa diunduh dari tab **Actions** → run terakhir → **Artifacts**.
