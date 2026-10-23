# Rencana RANCANG v0.53 — Pipeline gambar kerja 2D (makna garis, garis tersembunyi, garis bertumpuk)

*Disepakati dengan pengguna 24 Oktober 2026 (LANJUT). Dikerjakan sesudah v0.50.2 (dan v0.51/v0.52 bila urutan tidak diubah). Status: **menunggu**.*

## Latar

Keluhan pengguna:
- DXF tampak dan potongan masih memuat garis yang seharusnya tertutup ("harusnya di-trim dan dihapus").
- Garis yang berhimpit tergambar dua kali.

Prinsip yang disepakati:
- **Model 3D ≠ gambar 2D.** Gambar adalah representasi grafis dengan bahasa teknis sendiri (skala, konvensi, pembaca).
- **Tebal dan jenis garis menyampaikan makna**: dipotong, tampak, tersembunyi, as.

## Keadaan sekarang (24 Okt)

| Konsep | Sudah | Belum |
|---|---|---|
| Model → gambar | Gambar 2D dihitung dari elemen parametrik per jenis lembar | — |
| Tebal garis | Pena 0,13 / 0,18 / 0,25 / 0,35 / 0,5 / 0,7 mm (`TEBAL_2D`); layer DXF dipilah menurut tebal | Tebal ditentukan per jenis gambar, belum per makna garis |
| Bidang potong denah | `POTONG_DENAH = 1.2`, `potongDenah()`; overstek atap di atas bidang potong putus-putus | Kasus setengah terpotong belum diperiksa satu per satu |
| Jenis garis | Penuh, putus-putus, as, titik (`GARIS_2D`); dimensi berantai | — |
| Arsir | Arsir beton (`arsirBetonKertas`); alat arsir di Ruang Lembar | Belum lengkap per material; kerapatan kertas belum dipastikan |
| Garis bertumpuk | — | **Belum ada** |
| Garis tersembunyi (tampak/potongan, DXF) | — | **Belum ada** |
| Detail menurut skala | Simbol pintu, kusen, sanitair | Belum ada aturan baku |

## Pipeline (urutan kerja disepakati)

1. **Tahap 1 — Makna garis + metadata (fondasi).**
   - Setiap elemen, saat diminta gambar 2D, mengembalikan garis beserta metadata:
     - `makna`: potong | tampakDekat | tampakJauh | tersembunyi | arsir | bantu | as;
     - `elemenAsal` (id);
     - `jarak` ke pengamat atau ke bidang potong;
     - `konteksLembar`: denah | tampak | potongan | atap | pondasi | plafon | detail.
   - Fungsi gambar per elemen menerima **jenis lembar** sebagai masukan, bukan hanya bidang potong dan arah pandang. Satu elemen bisa menghasilkan garis berbeda per lembar. Contoh overstek atap:
     - denah → putus-putus;
     - tampak → utuh;
     - potongan → utuh bila terpotong, tampak sesuai jarak bila tidak.
   - Tebal dan jenis garis ditentukan dari `makna` (tahap 5 di bawah), tidak lagi per jenis gambar.
2. **Tahap 2 — Garis tersembunyi** (dikerjakan **sebelum** garis bertumpuk, supaya jumlah garis berkurang dulu).
   - Bawaan: garis yang tertutup elemen lain **dibuang**.
   - **Pengecualian, digambar putus-putus** (makna `tersembunyi`):
     1. Bovenlicht dan jendela tinggi di denah: bagian bukaan di atas bidang potong 1,20 m, misalnya kusen atas atau bovenlicht di atas ±1,50 m.
     2. Anak tangga di atas bidang potong denah. Yang terpotong digambar utuh dengan panah arah naik.
     3. Tepi mezzanine, balkon, dan bordes di denah lantai bawah: tepi lantai atas yang melayang di atas ruang.
     4. Ring balk dan lintel di atas bukaan tinggi (jendela ±2,0 m, pintu garasi).
     5. Balok, ring balk, dan balok anak di atas plafon atau di bawah plat yang tidak terekspos. Muncul di denah plafon dan denah lantai atas; penting untuk koordinasi ME dan posisi lampu.
     6. Overstek atap di denah (sudah berjalan).
     7. Kuda-kuda, gording, dan jurai pada denah atap (rangka di bawah penutup).
     8. Pondasi di bawah lantai pada denah pondasi.
     9. **Sloof di bawah dinding pada denah lantai 1: opsi per lembar** (bawaan mati), karena tergantung konvensi konsultan.
   - **Garis as tidak pernah dipotong benda apa pun.** Aturan ini ditanam di tahap ini. As adalah anotasi referensi, bukan benda yang bisa tertutup. Dimensi dan teks juga tidak ikut uji tertutup.
   - Metode: uji tertutup per segmen garis terhadap elemen di depannya. Bisa pakai depth buffer atau raycasting; three-mesh-bvh dari v0.50.2 dipakai ulang bila sudah ada. Segmen yang tertutup sebagian dipecah, bukan dibuang utuh.
3. **Tahap 3 — Garis bertumpuk** (pembersih akhir).
   - Garis yang berhimpit dalam toleransi **0,1 mm di kertas** digabung menjadi satu.
   - Yang menang adalah prioritas tertinggi: potong > tampak dekat > tampak jauh > tersembunyi > arsir > bantu/dimensi.
   - Segmen yang bertumpuk sebagian dipecah, supaya tidak ada celah saat diperbesar.
4. **Tahap 4 — Detail menurut skala.**
   - 1:200: kotak dan simbol.
   - 1:100: garis tepi, bukaan, simbol standar; profil baja sebagai garis tunggal.
   - 1:50: kusen, tebal material, profil.
   - 1:20: profil lengkap dan sambungan.
   - Garis lebih pendek dari ±1 mm di kertas disederhanakan atau dibuang.
5. **Tahap 5 — Tebal dan jenis garis dari makna.**
   - potong 0,5–0,7 mm + arsir;
   - tampak dekat 0,35;
   - tampak jauh 0,18–0,25;
   - tersembunyi putus-putus 0,18;
   - arsir 0,13;
   - bantu/dimensi 0,13–0,18;
   - as titik-strip 0,13.
   - Layer DXF per makna: POTONG, TAMPAK, TERSEMBUNYI, ARSIR, AS, DIMENSI, TEKS.
6. **Tahap 6 — Arsir dan anotasi.**
   - Arsir per material (bata, beton, kayu, tanah, pasir, batu kali). Kerapatannya tetap dalam mm kertas, dan arsir terbatas di dalam batas elemen yang terpotong.
   - Anotasi tidak tumpang tindih (melanjutkan aturan keterangan v0.50).

Tahap 4–6 lebih bersifat tampilan dan tidak mengubah kebenaran baca gambar, jadi dikerjakan sesudah tahap 1–3. **Setiap tahap adalah modul terpisah yang diuji sendiri.** Kalau gambar keluar kotor, kelihatan di tahap mana masalahnya.

## Pertanyaan konsep (dari tulisan yang dibawa pengguna) dan jawabannya

1. **Elemen setengah terpotong** (pintu 2,1 m, bidang potong 1,2 m): bagian yang terpotong digambar sebagai potong; bagian di atas bidang potong (kusen atas, bovenlicht) digambar putus-putus (pengecualian 1).
2. **Garis imajiner (as):** tidak pernah dipotong (tahap 2).
3. **Overhang dan recess:** satu elemen, garis berbeda per `konteksLembar` (tahap 1).
4. **Arsir material:** tahap 6.
5. **Dimensi berantai:** sudah ada. Pembaruan otomatis saat dinding digeser dan larangan tumpang tindih diperiksa di tahap 6.

## Uji (file baru sederhana)

Satu rumah dua lantai kecil berisi:
- tangga;
- jendela tinggi dengan bovenlicht;
- balok di atas plafon;
- atap pelana dengan overstek;
- satu kolom yang berhimpit dengan dinding.

Yang diuji:
- denah lantai 1: pengecualian 1, 2, 4, 6 putus-putus; as utuh melewati dinding;
- denah atap: rangka putus-putus;
- tampak: tidak ada garis di belakang dinding; overstek utuh;
- potongan: dinding dan plat terpotong tebal + arsir; rangka di balik plafon putus-putus;
- DXF:
  - tidak ada segmen ganda; dihitung dari jumlah segmen sebelum dan sesudah tahap 3, ditambah pemeriksaan pasangan berhimpit;
  - layer sesuai makna.
EOF
python3 - <<'E'
p='docs/ringkasan-program.md'; s=open(p).read()
a="Rincian: `docs/rencana-v0.50.2.md` bagian C2."
assert a in s
s=s.replace(a,a+"""

**Keputusan 24 Oktober 2026: v0.53 menjadi pipeline gambar kerja 2D.** Disetujui (LANJUT): setiap garis membawa makna dan konteks lembar (tahap 1); garis tersembunyi dibuang kecuali kategori putus-putus — bovenlicht/jendela tinggi, anak tangga di atas bidang potong, tepi mezzanine/balkon/bordes, ring balk/lintel di atas bukaan tinggi, balok di atas plafon atau di bawah plat tak terekspos, overstek di denah, rangka atap di denah atap, pondasi di denah pondasi; sloof di denah lantai 1 sebagai opsi per lembar; **garis as tidak pernah dipotong** (tahap 2); garis bertumpuk digabung menurut prioritas, toleransi 0,1 mm kertas (tahap 3); lalu detail menurut skala, tebal/jenis garis dari makna dengan layer DXF per makna, arsir per material (tahap 4–6). Ini menjawab pertanyaan terbuka "garis tersembunyi dibuang atau putus-putus". Rincian dan uji: `docs/rencana-v0.53.md`.""")
open(p,'w').write(s)
