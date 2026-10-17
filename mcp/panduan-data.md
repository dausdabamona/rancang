# Panduan data model RANCANG

Satuan meter, sudut derajat. Sumbu X = timur, Y = utara, Z = atas. Elevasi ±0,00 = lantai rumah.
Setiap dokumen punya id: huruf awalan + nomor (D12, V3). Pakai `daftar_elemen` untuk melihat nomor yang sudah dipakai, lalu ambil nomor berikutnya.
Isian `nama` dan `catatan` (teks bebas) boleh ada di semua jenis. `grup` = id grup induk (opsional).
Isian `diubahOleh` / `diubahPada` diisi aplikasi; tidak perlu dikirim.

## Elemen (koleksi elemen)

| Awalan | jenis | Isian wajib | Contoh |
|---|---|---|---|
| D | dinding | awal{x,y}, akhir{x,y} (as dinding), tebal, tinggi, z0 | `{"jenis":"dinding","nama":"Dinding depan","awal":{"x":0,"y":0},"akhir":{"x":7,"y":0},"tebal":0.15,"tinggi":3.5,"z0":-0.11}` |
| B | bukaan | tipe 'pintu'/'jendela', dinding (id), jarak (dari ujung awal dinding ke tepi bukaan), lebar, tinggi, ambang (dari dasar dinding), kode | `{"jenis":"bukaan","tipe":"pintu","kode":"P1","dinding":"D5","jarak":1.2,"lebar":0.8,"tinggi":2.1,"ambang":0.11}` |
| V | volume | alas [{x,y}…] (≥3 titik), z0, tinggi. Bentuk lain: `bentuk:'lingkaran'` + pusat, jari; `bentuk:'busur'` + awal, akhir, tonjolan | `{"jenis":"volume","nama":"Lantai Kamar 1","alas":[{"x":0,"y":0},{"x":3,"y":0},{"x":3,"y":4},{"x":0,"y":4}],"z0":-0.11,"tinggi":0.11,"lantai":"ruang","penutupLantai":"k40"}` |
| C | kolom | tipe 'praktis'/'struktur', x, y (pusat), b (lebar X), h (lebar Y), tinggi, z0, tul{n,d,ulir}, sengkang{d,s}, fc, selimut | `{"jenis":"kolom","tipe":"praktis","x":0,"y":0,"b":0.15,"h":0.15,"tinggi":3.5,"z0":-0.11,"tul":{"n":4,"d":10,"ulir":false},"sengkang":{"d":8,"s":0.15},"fc":14.5,"selimut":0.02}` |
| S | slof | awal, akhir, b, h, z0 (dasar), tul, sengkang, fc, selimut | `{"jenis":"slof","awal":{"x":0,"y":0},"akhir":{"x":7,"y":0},"b":0.15,"h":0.2,"z0":-0.31,"tul":{"n":4,"d":10,"ulir":false},"sengkang":{"d":8,"s":0.15},"fc":18.7,"selimut":0.025}` |
| R | ringbalk | sama dengan slof | z0 = dasar ring balk |
| F | pondasi | tipe 'batukali' (awal, akhir, lebarAtas, lebarBawah, tinggi, aanstamping, pasir, z0); 'footplat' (x, y, p, l, tebal, tulPlat{d,s,ulir}, pedestal{b,h}, puncakPedestal, tul, sengkang, fc, selimut, z0); 'umpak' (x, y, bawah, atas, tinggi, fc, z0) | `{"jenis":"pondasi","tipe":"batukali","awal":{"x":0,"y":0},"akhir":{"x":7,"y":0},"lebarAtas":0.3,"lebarBawah":0.7,"tinggi":0.7,"aanstamping":0.15,"pasir":0.05,"z0":-0.31}` |
| A | atap | bentuk 'pelana'/'limas'/'sandar'/'datar', x0,y0,x1,y1 (batas dinding luar, tanpa overstek), z0 (dudukan), kemiringan, overstek, arah ('x'/'y' untuk pelana = arah bubungan; mata angin untuk sandar = arah turun), penutup ('spandek','gelombang','genteng','datar'), rangka ('bajaringan','kayu','tanpa'), jarakKuda, tebal. Opsional: lisplang ('papan'/'grc'), plafonMiring ('tanpa','penuh','tritisan'), kuda{…}, lisplangSisi{…} | `{"jenis":"atap","bentuk":"pelana","arah":"y","x0":0,"x1":7,"y0":0,"y1":9,"z0":3.72,"kemiringan":30,"overstek":0.9,"tebal":0.12,"penutup":"spandek","rangka":"kayu","jarakKuda":1.5}` |
| P | plafon | alas [{x,y}…], z0 (permukaan bawah plafon), bahan ('grc'/'gypsum'), rangka ('hollow'/'kayu') | `{"jenis":"plafon","alas":[…],"z0":3.36,"bahan":"gypsum","rangka":"hollow"}` |
| X | potong | nama (huruf A, B, …), awal, akhir, pandang (1 = melihat ke kiri dari awal ke akhir, −1 sebaliknya) | `{"jenis":"potong","nama":"A","awal":{"x":-2,"y":2.5},"akhir":{"x":9,"y":2.5},"pandang":1}` |
| N | anotasi | tipe 'teks' (titik{x,y,z}, teks), 'label' (titik, ujung, teks), 'ukuran' (titik, ujung), 'peil' (titik; teks kosong = elevasi otomatis), pada 'denah' | `{"jenis":"anotasi","tipe":"teks","teks":"Kamar 1","titik":{"x":1.5,"y":2,"z":0},"pada":"denah"}` |
| L | gambar2d | Benda gambar 2D di Ruang Lembar: bentuk ('garis','polyline','persegi','lingkaran','busur','teks','arsir'), lembar (mis. 'denah', 'potongan:X3', 'sampul'), tempel ('gambar' = titik dunia {x,y,z} meter; 'kertas' = titik {x,y} mm kertas), titik (garis 2 titik; persegi 2 sudut; lingkaran pusat + titik tepi; busur awal, akhir, titik pada busur), gaya {tebal mm, garis 'penuh'/'putus'/'as'/'titik', warna 'hitam'/'abu'/'merah'/'biru'}. Teks: teks, ukuran (mm). Arsir: pola ('beton','bata','tanah','pasir','kayu','keramik'). Polyline: tutup. Simbol perabot (`bentuk:'simbol'`, hanya denah/denah atap/denah pondasi, tempel 'gambar', titik = pusat): simbol ('kasur1','kasur2','lemari','mejaMakan','mejaKerja','sofa','klosetDuduk','klosetJongkok','wastafel','shower','bakMandi','kitchenSet','pohon'), rotasi (0/90/180/270). Legenda otomatis: `bentuk:'legenda'`, tempel 'kertas', titik = sudut kiri atas (mm). Di lembar detail, benda di dalam petak Detail bebas memakai `tempel:'petak'`, `petak` = id detail (E…), titik mm dari pojok kiri atas petak | `{"jenis":"gambar2d","bentuk":"teks","lembar":"denah","tempel":"kertas","titik":[{"x":30,"y":180}],"teks":"Catatan: semua ukuran dalam meter","ukuran":2.5,"gaya":{"warna":"hitam"}}` |
| E | detail | Detail di lembar detail ('det:1', 'det:2', …): template ('pondasiBatuKali','footplat','umpak','kudaKuda','sambunganKayu','bebas'), sumber (id elemen: pondasi untuk tiga template pertama, atap berangka kayu untuk kuda-kuda dan sambungan), lembar, skala (5, 10, 20, 25, 50, 75, 100), judul (opsional). sambunganKayu wajib `sambungan`: 'tumpuan','puncak','makelar','sokong','perpanjangan' | `{"jenis":"detail","template":"sambunganKayu","sumber":"A2","sambungan":"tumpuan","lembar":"det:2","skala":10}` |
| I | instance | definisi (id komponen K…), posisi{x,y}, rotasi (°), z0 | |

Lantai (volume): `lantai` = 'ruang' / 'km' / 'teras' / 'lain'; `penutupLantai` = 'k40', 'k30', 'k20' (kasar anti licin), 'g60', 'plester'.

Pintu: `bukaKe` = 1 / −1 (sisi kiri / kanan dinding dilihat dari awal ke akhir; kosong = otomatis ke dalam bangunan); `balikEngsel` = true untuk membalik engsel.

## Koleksi lain

- G (grup): `{"nama":"Rumah","induk":null}`. Elemen masuk grup lewat isian `grup`.
- K (komponen): `{"nama":"Kloset","elemen":[…data elemen lokal…]}`; dipasang lewat instance.
- T (tipe kusen): `{"kode":"P1","untuk":"pintu","nama":"Pintu panil","daun":1,"isi":"panil6","buka":"kiri","profil":0.06,"boven":{"tinggi":0.4,"kolom":2,"baris":1}}`. isi: panil6, kaca, polos, jalusi; buka: kiri, kanan, kupu, tetap. Berlaku untuk semua bukaan berkode sama.

## Kebiasaan yang baik

- Dinding digambar pada as; tebal dibagi rata kiri-kanan as. Sambungan dinding di titik as yang sama.
- Kirim perubahan yang saling terkait dalam satu panggilan `terapkan_perubahan` (misalnya dinding beserta pintunya) agar tercatat sebagai satu langkah Undo.
- Untuk mengubah satu isian, ambil dulu datanya dengan `ambil_elemen`, ubah isiannya, lalu kirim data lengkapnya (perubahan menimpa seluruh dokumen).
- Hapus = kirim `"data": null`. Menghapus dinding tidak otomatis menghapus pintunya; hapus bukaannya juga.
- Periksa hasil dengan `gambar_2d` (denah) atau `tangkap_layar_3d` sebelum melapor ke pengguna.
