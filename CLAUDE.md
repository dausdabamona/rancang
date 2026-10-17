# RANCANG

Aplikasi gambar bangunan ala SketchUp (model 3D → gambar kerja 2D + volume RAB) yang dikendalikan bersama Claude.

## Stack
- Satu halaman HTML + Three.js r149 + polygon-clipping 0.15.7 + xlsx 0.18.5 (`app/rancang.html`)
- Desktop: Electron 44 + electron-builder (NSIS + portable, Windows x64)
- MCP: @modelcontextprotocol/sdk, dibundel esbuild, dipaketkan @anthropic-ai/mcpb
- Build: GitHub Actions windows-latest

## Konvensi
- Ikuti firdaus-dev conventions; Bahasa UI, komentar logika, dan pesan: Indonesia
- Dokumentasi dulu: setiap keputusan dicatat di Dokumen Keputusan (Claude Doc "Dokumen Keputusan: Aplikasi Gambar Bangunan v1") sebelum kode
- Bertahap: usulan → tunggu "LANJUT" dari pengguna → kerjakan
- Sumber tunggal: ubah fitur di `app/rancang.html`; jangan menyunting `build/renderer` (hasil susun)
- Commit Conventional Commits, subjek Bahasa Indonesia; perubahan lewat cabang + pull request

## Struktur
Lihat bagian Pengembangan di README.md.

## Perintah Penting
- dev: `npm start`
- uji: `npm test` (tambahkan `RANCANG_UJI_ELECTRON=1` untuk uji MCP ↔ aplikasi; di Linux jalankan dengan `xvfb-run -a`)
- uji asap: `npm run uji-asap` (Linux: `xvfb-run -a npx electron . --uji-asap --no-sandbox`)
- build: `npm run build`, `npm run dist:win`, `npm run pack:mcpb`
- rilis: tag `vX.Y.Z` sama dengan `version` di package.json

## Catatan Khusus
- Versi artifact menyimpan ke database artifact (`window.claude.use('db')`); versi desktop memakai `electron/renderer/claude-shim.js` yang meniru API yang sama di atas berkas `.rancang`.
- `window.rancangAPI` di `app/rancang.html` adalah antarmuka untuk jembatan desktop dan MCP; perubahan dari luar ditandai `diubahOleh: 'claude'`.
- Jembatan MCP: HTTP 127.0.0.1 port acak + token; info di `<userData>/mcp-jembatan.json`. `RANCANG_DATA_DIR` mengganti folder data (uji).
- WebGL: `enable-unsafe-swiftshader` aktif agar tetap jalan di laptop tanpa dukungan GPU.
