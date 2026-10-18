// Menyusun paket MCP: server dibundel jadi satu berkas (tanpa node_modules), manifest, dan ikon.
// Hasil di build/mcp; dipaketkan menjadi RANCANG.mcpb dengan `npm run pack:mcpb`.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {build} from 'esbuild';

const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const keluar = path.join(akar, 'build', 'mcp');
const {version} = JSON.parse(fs.readFileSync(path.join(akar, 'package.json'), 'utf8'));

fs.rmSync(keluar, {recursive: true, force: true});
fs.mkdirSync(path.join(keluar, 'server'), {recursive: true});

// panduan data bersumber tunggal di app/rancang.html (blok <script type="text/markdown" id="panduan-data">),
// dipakai juga oleh panel Claude di aplikasi
const panduanDariHtml = {name: 'panduan-data', setup(b) {
  b.onResolve({filter: /panduan-data\.md$/}, () => ({path: 'panduan-data', namespace: 'panduan'}));
  b.onLoad({filter: /.*/, namespace: 'panduan'}, () => {
    const html = fs.readFileSync(path.join(akar, 'app', 'rancang.html'), 'utf8').replace(/\r\n/g, '\n');
    const m = html.match(/<script type="text\/markdown" id="panduan-data">\n?([\s\S]*?)<\/script>/);
    if (!m) throw new Error('Blok panduan-data tidak ditemukan di app/rancang.html');
    return {contents: m[1].trim() + '\n', loader: 'text'};
  });
}};

try {
await build({
  entryPoints: [path.join(akar, 'mcp', 'server.mjs')],
  outfile: path.join(keluar, 'server', 'index.mjs'),
  bundle: true, platform: 'node', format: 'esm', target: 'node18',
  plugins: [panduanDariHtml],
  banner: {js: "import {createRequire as __buatRequire} from 'node:module'; const require = __buatRequire(import.meta.url);"},
  legalComments: 'none',
  logLevel: 'warning'
});
// sisipkan versi
const f = path.join(keluar, 'server', 'index.mjs');
fs.writeFileSync(f, fs.readFileSync(f, 'utf8').replace(/__VERSI__/g, version));
const manifest = fs.readFileSync(path.join(akar, 'mcp', 'manifest.json'), 'utf8').replace(/__VERSI__/g, version);
JSON.parse(manifest);
fs.writeFileSync(path.join(keluar, 'manifest.json'), manifest);
fs.copyFileSync(path.join(akar, 'assets', 'icon-512.png'), path.join(keluar, 'icon.png'));
} catch (err) {
  if (process.env.GITHUB_ACTIONS) console.log(`::error title=build-mcp::${String(err.message).split('\n')[0]}`);
  console.error(err);
  process.exit(1);
}
console.log('[build-mcp] selesai → build/mcp (versi ' + version + ')');
