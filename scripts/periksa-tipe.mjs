// Periksa tipe skrip utama app/rancang.html dengan tsc (JSDoc + // @ts-check), tanpa langkah build.
// Pakai: npm run periksa-tipe  (perlu devDependencies typescript dan @types/three)
// Keluaran: daftar kesalahan dengan nomor baris app/rancang.html, dan ringkasan per kode kesalahan.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {execSync} from 'node:child_process';
import {join} from 'node:path';

const akar = new URL('..', import.meta.url).pathname;
const html = readFileSync(join(akar, 'app/rancang.html'), 'utf8');
const blok = html.split('<script>').slice(1).map(b => b.split('</script>')[0]);
const utama = blok.find(b => b.includes('@ts-check'));
if (!utama) { console.error('Skrip utama dengan // @ts-check tidak ditemukan.'); process.exit(2); }
const awal = html.slice(0, html.indexOf(utama)).split('\n').length; // baris HTML tempat baris 1 skrip berada

const dir = join(akar, 'build/tipe');
mkdirSync(dir, {recursive: true});
writeFileSync(join(dir, 'rancang.js'), utama);
writeFileSync(join(dir, 'tsconfig.json'), JSON.stringify({
  compilerOptions: {allowJs: true, checkJs: true, noEmit: true, target: 'es2022', lib: ['dom', 'es2022', 'dom.iterable'], strict: false, noImplicitAny: false, skipLibCheck: true, types: [], typeRoots: [join(akar, 'node_modules/@types')]},
  files: ['rancang.js', join(akar, 'tipe/global.d.ts')]
}));
let keluaran = '';
try { execSync(`"${join(akar, 'node_modules/.bin/tsc')}" -p "${join(dir, 'tsconfig.json')}"`, {encoding: 'utf8'}); }
catch (e) { keluaran = e.stdout || ''; }
const baris = keluaran.split('\n').filter(l => l.includes('error TS'));
const ringkas = new Map();
for (const l of baris) {
  const m = l.match(/rancang\.js\((\d+),(\d+)\): error (TS\d+): (.*)/);
  if (!m) continue;
  ringkas.set(m[3], (ringkas.get(m[3]) || 0) + 1);
  console.log(`app/rancang.html:${+m[1] + awal - 1}:${m[2]} ${m[3]} ${m[4]}`);
}
console.log(`\n${baris.length} kesalahan tipe.`);
for (const [k, n] of [...ringkas].sort((a, b) => b[1] - a[1])) console.log(`  ${k}: ${n}`);
