// Menyusun halaman desktop (luring) dari sumber tunggal app/rancang.html.
// CDN dan Google Fonts diganti salinan lokal; shim window.claude disisipkan sebelum skrip aplikasi.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const keluar = path.join(akar, 'build', 'renderer');
const nm = p => path.join(akar, 'node_modules', p);

// Ganti tepat satu kali; build gagal bila sumber berubah dan pola tidak ditemukan
function ganti(teks, cari, baru, label) {
  const n = teks.split(cari).length - 1;
  if (n !== 1) throw new Error(`[build-renderer] pola "${label}" ditemukan ${n} kali, seharusnya 1. Periksa app/rancang.html.`);
  return teks.replace(cari, () => baru);
}

const CSP = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline'",
  "font-src 'self'",
  "img-src 'self' data: blob:",
  "connect-src 'self' data: blob:",
  "worker-src 'self' blob:",
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'"
].join('; ');

const FONT = [
  ['archivo', 'Archivo', [600, 700]],
  ['ibm-plex-sans', 'IBM Plex Sans', [400, 500, 600]],
  ['ibm-plex-mono', 'IBM Plex Mono', [400, 500]]
];

function susun() {
  // akhir baris disamakan (checkout Windows bisa memakai CRLF)
  let html = fs.readFileSync(path.join(akar, 'app', 'rancang.html'), 'utf8').replace(/\r\n/g, '\n');
  html = ganti(html, '<link rel="preconnect" href="https://fonts.googleapis.com">\n', '', 'preconnect googleapis');
  html = ganti(html, '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n', '', 'preconnect gstatic');
  html = html.replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2[^"]*">/, m => {
    if (!m) throw new Error('[build-renderer] tautan Google Fonts tidak ditemukan');
    return `<meta http-equiv="Content-Security-Policy" content="${CSP}">\n<link rel="stylesheet" href="fonts/fonts.css">`;
  });
  if (!html.includes('fonts/fonts.css')) throw new Error('[build-renderer] tautan Google Fonts tidak ditemukan');
  html = ganti(html, '<script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>',
    '<script src="claude-shim.js"></script>\n<script src="vendor/three.min.js"></script>', 'three CDN');
  html = ganti(html, '<script src="https://cdn.jsdelivr.net/npm/polygon-clipping@0.15.7/dist/polygon-clipping.umd.min.js"></script>',
    '<script src="vendor/polygon-clipping.umd.min.js"></script>', 'polygon-clipping CDN');
  html = ganti(html, "'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js'", "'vendor/xlsx.full.min.js'", 'xlsx CDN');
  const sisa = html.match(/https:\/\/(cdn|fonts)[^\s"'`)]*/g);
  if (sisa) throw new Error('[build-renderer] masih ada sumber luar: ' + sisa.join(', '));

  fs.rmSync(keluar, {recursive: true, force: true});
  fs.mkdirSync(path.join(keluar, 'vendor'), {recursive: true});
  fs.mkdirSync(path.join(keluar, 'fonts'), {recursive: true});
  fs.writeFileSync(path.join(keluar, 'index.html'), html);
  fs.copyFileSync(path.join(akar, 'electron', 'renderer', 'claude-shim.js'), path.join(keluar, 'claude-shim.js'));
  fs.copyFileSync(nm('three/build/three.min.js'), path.join(keluar, 'vendor', 'three.min.js'));
  fs.copyFileSync(nm('polygon-clipping/dist/polygon-clipping.umd.min.js'), path.join(keluar, 'vendor', 'polygon-clipping.umd.min.js'));
  fs.copyFileSync(nm('xlsx/dist/xlsx.full.min.js'), path.join(keluar, 'vendor', 'xlsx.full.min.js'));

  const css = [];
  for (const [paket, keluarga, bobot] of FONT) {
    for (const w of bobot) for (const sub of ['latin', 'latin-ext']) {
      const nama = `${paket}-${sub}-${w}-normal.woff2`, asal = nm(`@fontsource/${paket}/files/${nama}`);
      if (!fs.existsSync(asal)) throw new Error('[build-renderer] berkas huruf tidak ada: ' + nama);
      fs.copyFileSync(asal, path.join(keluar, 'fonts', nama));
      const rentang = sub === 'latin'
        ? 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
        : 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
      css.push(`@font-face{font-family:'${keluarga}';font-style:normal;font-weight:${w};font-display:swap;src:url(${nama}) format('woff2');unicode-range:${rentang}}`);
    }
  }
  fs.writeFileSync(path.join(keluar, 'fonts', 'fonts.css'), css.join('\n') + '\n');
  console.log('[build-renderer] selesai →', path.relative(akar, keluar));
}

try {
  susun();
} catch (err) {
  // anotasi GitHub Actions agar pesan terlihat di ringkasan run
  if (process.env.GITHUB_ACTIONS) console.log(`::error title=build-renderer::${err.message}`);
  console.error(err);
  process.exit(1);
}
