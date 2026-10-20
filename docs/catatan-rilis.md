## Yang baru di 0.44.0

Detail perbesaran yang rapi dan informatif (21 Oktober 2026), acuan gambar konsultan dermaga KP Sorong.

- **Menu Atur detail**: pilih sebuah detail perbesaran di lembar, lalu atur nomor, judul, skala (1:5–1:50), bentuk bingkai (lingkaran atau persegi 1:1, 3:2, 2:1), tinggi bingkai di kertas (bagian yang diperbesar ikut menyesuaikan), dan garis penghubung ke lingkaran sumber.
- **Isi rinci di detail potongan** (bisa dinyalakan/dimatikan per detail): beton terpotong diarsir kerikil dan pasir (bukan blok hitam); tulangan dari data elemen — balok (sengkang dan tulangan atas/bawah, atau tulangan memanjang dan sengkang tiap jarak), pelat dan pile cap (dua lapis), tiang pipa baja (dinding pipa dan isian beton bertulang); ukuran lebar/tinggi elemen dalam cm; label penunjuk di luar bingkai (mis. "Balok memanjang tiang 40/70 · 8D19 · Ø10-150"); mutu beton di bawah judul.
- Pasang **RANCANG-Setup-0.44.0.exe** dan ganti ekstensi Claude desktop dengan **RANCANG.mcpb** 0.44.0 dari rilis yang sama.

## Yang baru di 0.43.1

Perbaikan dari gambar Layout Dermaga TUKS BBP (21 Oktober 2026).

- **As di bagian garis putus tidak lagi bertumpuk**: as yang jatuh di bagian yang dihilangkan garis putus tidak digambar (garis as, gelembung, dan ukurannya). Ukuran antar-as menyambung ke as terlihat berikutnya dengan nilai sebenarnya, mis. 3 → 18 = 90,00. Berlaku di denah/layout, rencana pile cap dan tiang, rencana balok dan pelat, tampak, dan potongan.
- **Simbol garis putus datar selebar benda**: zig-zag dan bidang putih penutup celah di denah/layout, rencana pile cap dan tiang, serta rencana balok dan pelat kini hanya selebar benda yang dipendekkan (mis. trestle 7 m), bukan setinggi seluruh gambar; garis as di luarnya tetap menyambung.
- Pasang **RANCANG-Setup-0.43.1.exe** dan ganti ekstensi Claude desktop dengan **RANCANG.mcpb** 0.43.1 dari rilis yang sama.

## Yang baru di 0.43.0

Rilis penyelaras (20 Oktober 2026): aplikasi desktop, ekstensi Claude (RANCANG.mcpb), dan artefak RANCANG di Claude kini memakai versi kode yang sama, sehingga model dan gambar yang dibuat Claude tampil persis sama di aplikasi Bapak.

- Isi fitur sama dengan 0.42.1 (alat dermaga v0.41, Fase 2 SketchUp/LayOut v0.42, perbaikan 0.42.1).
- Pasang **RANCANG-Setup-0.43.0.exe** dan ganti ekstensi Claude desktop dengan **RANCANG.mcpb** 0.43.0 dari rilis yang sama.

## Yang baru di 0.42.1

Perbaikan dari penyusunan gambar RAB dermaga BBP (20 Oktober 2026).

- **Tulangan pelat ulir**: pelat dengan `tul.ulir: true` kini masuk RAB sebagai besi ulir (D13), sebelumnya selalu polos (Ø13).
- **Kayu kelas I bawaan = kayu besi**: jeti kayu baru memakai *Kayu besi (kelas I)*; uraian RAB menjadi "tiang kayu Besi". Pilihan Merbau, Ulin, Bengkirai, dan Matoa tetap ada.
- **Garis putus di lembar bagian**: garis putus yang dipasang pada tampak/rencana zona juga berlaku di lembar bagiannya, dan gambar yang dipendekkan tetap di tengah lembar.
- **Dasar laut di tampak samping jeti**: tampak yang tidak sejajar profil dasar laut kini menggambar dasar laut dari profil di sepanjang gambar, bukan garis datum datar.
- **Nama tipe balok** di rencana balok tanpa keterangan letak dan nomor urut (Tie beam 12 → Tie beam, Balok induk kepala y=-18 → Balok induk kepala), sehingga keterangan tidak berulang.

## Yang baru di 0.42.0

Kebiasaan SketchUp dan LayOut untuk pendetilan, Fase 2 (20 Oktober 2026). Dibangun di atas cabang dermaga (v0.41).

- **As grid manual** (alat *As grid* di kelompok Gambar): klik titik as pertama, arahkan, lalu ketik **6x5** (6 as berjarak 5 m) atau **5;5;4,5** (jarak berturut-turut). As tegak diberi angka 1, 2, 3 dari barat; as mendatar diberi huruf A, B, C dari utara, melanjutkan label yang sudah ada. Garis as adalah garis bantu ber-label: tetap menjadi titik tangkap semua alat, bisa miring, dan labelnya bisa diganti di panel (mis. B'); garis bantu biasa bisa dijadikan as dengan mengisi labelnya. Gambar 2D (denah, denah pondasi, rencana balok/pelat, tampak, potongan) memakai as manual dengan gelembung dan ukuran antar as, menggantikan as otomatis dari kolom/tiang. MCP: `as: {label}` pada garis bantu.
- **Jadikan komponen yang lebih mudah**: G kini membuka kotak isian berisi nama komponen, titik sisip (pojok kiri bawah, tengah alas, atau klik titik di model), dan centang **Ganti juga salinan yang sama** (menyala bawaan). Kelompok elemen lain yang isinya sama, hanya bergeser atau berputar 90°/180°/270°, ikut menjadi salinan komponen; RAB tidak berubah. Contoh: di Asrama Putri, satu kolom lantai 2 + foot plat dijadikan komponen, 37 pasangan kembar lain ikut menjadi salinan.
- **Komponen proyek** di panel ringkasan (juga dari palet Ctrl+K): ganti nama definisi, *Pilih semua* salinan, hapus definisi yang tidak terpakai. Panel salinan komponen bertambah *Ganti dengan komponen* untuk menukar definisi salinan terpilih.
- **Viewport bebas di Ruang Lembar** (alat *Viewport* di bilah Gambar 2D): klik dua sudut kotak di kertas; isinya gambar lain (denah per lantai, denah atap, rencana plafon, denah pondasi, rencana balok/pelat, tampak, potongan) dengan skala dan pusat sendiri, judul bergaris bawah dan skala otomatis di bawahnya. Isi dan skala diganti di bilah atas, seret memindah kotak, **Alt + seret** menggeser isinya. Isinya dirender ulang dari model, jadi ikut berubah bila model berubah, dan ikut ke PDF. Detail perbesaran memakai jalur render yang sama. MCP: benda gambar 2D `bentuk:'viewport'`.
- Perbaikan: benda gambar 2D yang dibuat di lembar denah per lantai kini ikut tampil di lembarnya; skala grafis bertambah calon panjang untuk skala seperti 1:300.
## Yang baru di 0.41.0

Alat gambar dermaga beton, dari model sampai gambar kerja dan detail (20 Oktober 2026, diuji dengan model ulang Dermaga Poltek KP Sorong TA 2020).

- **Dermaga kayu (jeti)**: elemen *Jeti kayu* satu ruas lurus dengan portal tiang, balok kepala ganda, gelagar, papan lantai berjarak, dan skor silang; RAB kayu DM-201 s.d. DM-208.
- **Tiang miring dan selimut**: tiang pancang bisa miring 1 : n ke arah tertentu (RAB DM-091), dan diberi selimut beton anti karat di zona pasang surut (beton, bekisting, besi + spiral masuk RAB).
- **Causeway / timbunan**: penampang trapesium sepanjang as dengan talud 1 : n yang dasarnya mengikuti dasar laut (RAB DM-301 timbunan, DM-302 armour talud).
- **Profil dasar laut**: datum dasar laut boleh berupa profil (jarak, elevasi) sepanjang garis; tampak dan potongan menggambar dasar laut miring, dan tabel elevasi dasar laut muncul di bawah tampak/potongan memanjang.
- **Zona gambar 2D**: grup ber-zona (gedung, dermaga, jeti) memiliki set lembarnya sendiri, dengan kode lembar proyek (mis. PKP-01).
- **Lembar gabungan**: beberapa gambar dalam satu lembar dengan simbol judul dan skala seragam (mis. layout + rencana pile cap, tampak samping + depan, rencana balok + penulangan pelat). Lembar bagian memecah gambar panjang (rencana pondasi dan tampak samping) pada 1 : 200 dengan garis sambung di as.
- **Grid as dermaga otomatis** dari tiang (nomor dari ujung laut, huruf melintang) di layout, rencana, tampak, dan potongan; **kedalaman pandang potongan** agar potongan melintang tidak memperlihatkan tiang jauh di belakangnya.
- **Rencana balok** dan **rencana penulangan pelat** dermaga.
- **Detail penulangan dermaga** di Pustaka Detail: penampang balok T, tulangan pile cap PC-1/PC-2 dengan beton isian dan stek, selimut dan isian tiang, penulangan bollard.
- **Garis putus** (pemendekan tiang dan bagian berulang) dan **detail perbesaran** di Ruang Lembar; garis putus tiang bisa dibuat otomatis dari panel garis potong.
- **Dimensi, sudut, kemiringan, dan label** baru di Ruang Lembar: dimensi tunggal atau berantai yang angkanya dihitung dari model (cm di potongan, m di denah/tampak), sudut berbusur, kemiringan 1 : n (°), label penunjuk yang teksnya diambil dari data benda. Semua alat 2D kini juga berfungsi di lembar gabungan.
- **Keterangan otomatis dermaga**: potongan melintang langsung diberi ukuran lebar dan jarak tiang, rantai tinggi, label komponen, dan kemiringan tiang; potongan causeway diberi lebar puncak, tinggi, dan talud. Sakelar *Keterangan otomatis* per lembar.
- Skala otomatis bertambah 1 : 250 dan 1 : 300.

## Yang baru di 0.40.0

Kebiasaan SketchUp dan LayOut untuk pendetilan, Fase 1 (20 Oktober 2026, hasil mempelajari berkas .skp dan .layout di Google Drive).

- **Larik salinan dengan Pindah + Ctrl**: sesudah menyalin, ketik **24x** lalu Enter untuk 24 salinan berjarak sama, atau **/4** untuk membagi jarak salinan pertama menjadi 4. Angka boleh diganti berkali-kali (6x, lalu /3, …) dan **satu Ctrl+Z menghapus seluruh deret** beserta salinan pertamanya. Cocok untuk deret tiang + pile cap dermaga, kolom, atau kusen.
- **Label terhubung data elemen**: label berpanah yang ujung panahnya diklik pada benda otomatis terhubung ke benda itu dan teksnya dibaca dari data: pintu/jendela `{kode}`, lantai `{nama} · {luas} m²`, kolom `K {b}/{h} · {tulangan}`, slof/balok `{b}/{h} · {tulangan}`, dinding `Dinding t={tebal} cm`, atap `{penutup} {kemiringan}°`, tiang `Ø{diameter} · L {panjang} m`, plat `Plat t={tebal} cm · {tulangan}`. Pola bisa diubah di Properti (3D) atau kotak teks anotasi (Gambar 2D, khusus denah). Kode pintu, nama ruang, dan ukuran yang diubah langsung ikut di label. Bila bendanya dihapus, label memakai teks terakhir dan ditandai *sumber hilang*; tombol *Lepas tautan* menjadikannya teks bebas. MCP: tambahkan `sumber` dan `isi` pada anotasi label.
- **Revisi di kop**: panel Kop bertambah bagian *Revisi gambar* (tanggal, uraian, Tambah revisi). Berlaku untuk semua lembar: kop kanan menampilkan tiga revisi terakhir (paraf dibiarkan kosong untuk ditandatangani), dan kolom tanggal di ketiga model kop menjadi tanggal revisi terakhir + *Rev. n*.
- **Skala grafis** di pojok kanan bawah setiap lembar berskala (denah, denah atap, pondasi, plafon, tampak, potongan, detail penulangan): batang ±50 mm, mis. 0·1·2·5 m pada 1:100 dan 0·0,5·1 m pada 1:20, tetap benar walau lembar dicetak diperkecil. Bisa dimatikan lewat centang *Skala grafis* (tersimpan di pengaturan lembar).
- **Panah utara** kini juga di denah atap, denah pondasi, dan rencana plafon.

## Yang baru di 0.39.1

Perbaikan plafon miring dari PR #24 (v0.34.1) yang tertinggal, dipasang ulang di atas 0.39.0 (20 Oktober 2026). Rinciannya ada di bagian *Yang baru di 0.34.1* di bawah: plafon miring berhenti di sisi dalam lisplang, bawaan *Mundur dari ujung seng* 20 cm untuk semua rangka (atap baja ringan lama ikut bergeser 20 cm ke dalam), isian *Jarak tepi plafon dari ujung seng* di Properti plafon miring, dan papan lisplang sebagai batas Perpanjang/Pangkas.

## Yang baru di 0.39.0

Elemen dermaga, Fase 1 (20 Oktober 2026, disiapkan untuk RAB dermaga TUKS trestle 150 × 10 m di Sorong).

- **Tiang pancang** (alat *Tiang* di bilah Struktur, Tab mengganti bahan): pipa baja (diameter luar dan tebal dinding dalam mm, bawaan Ø508 × 12 mm = 20"), spun pile, tiang beton persegi, dan tiang kayu. Isian: elevasi kepala, panjang, panjang per segmen (sambungan las = segmen − 1), coating epoxy, dan isian beton bertulang di kepala tiang. Panel menampilkan berat pipa (0,02466 × t × (D − t) kg/m), elevasi ujung bawah, luas selimut, beton dan besi isian.
- **Pile cap**: jenis pondasi baru (alat Pondasi, Tab sampai *Pile cap*). Bawaan 90 × 90 × 90 cm, D16-150 dua lapis dua arah, fc' 29 MPa; dipasang di atas tiang, dasarnya otomatis 10 cm di bawah kepala tiang. Bekisting dihitung sisi + dasar (cor di atas air).
- **Perlengkapan dermaga** (alat *Bolder*, Tab: bolder → fender → lampu PJU → tangga monyet): kapasitas bolder (ton), panjang dan model fender, tinggi tiang PJU dan tangga monyet, rotasi (+Y lokal = arah ke laut).
- **Datum pasang surut** di panel ringkasan (bagian *Datum pasang surut*): HWL, MSL, LWL, dan dasar laut. Potongan dan tampak menggambar garis air putus-putus biru dan garis dasar laut berarsir, menggantikan garis tanah ±0,00. Disimpan sebagai level ber-`datum`, jadi bisa diatur Claude lewat MCP dan tidak ikut daftar level lantai.
- **RAB divisi Pekerjaan Dermaga**: pengadaan tiang per spesifikasi (kg untuk pipa baja, m' untuk spun/beton, m³ untuk kayu), pemancangan di laut (m'), sambungan las (titik), perataan kepala tiang (titik), coating (m²), jumlah pile cap, dan perlengkapan per buah. Beton, besi, dan bekisting pile cap, isian tiang, plat, dan balok tetap di divisi beton.
- Gambar 2D: tiang tampil di denah dan denah pondasi (lingkaran bersilang, keterangan otomatis), tiang bulat di potongan digambar sebagai satu siluet, dan tampak kini memuat tiang, plat, pile cap, balok lantai, serta perlengkapan.
- Diameter tulangan bertambah D22, D25, D29, D32. Panduan data (MCP `panduan_data`) bertambah jenis `tiang` (Z), `perlengkapan` (O), pondasi `pilecap`, dan `datum` pada level.

## Yang baru di 0.38.0

Alat untuk bangunan dua lantai dan rangka baja profil (20 Oktober 2026, disiapkan untuk Gedung Penunjang dua lantai dan atap Aula limas patah Masjid Agung Al-Mulk).

- **Balok lantai**: tombol Slof kini berganti dengan Tab Slof → Ring balk → **Balok lantai**. Bawaan 25/40, 6D13, sengkang Ø10-150, fc' 20,75 MPa; puncak balok otomatis rata dengan level lantai berikutnya (atau puncak dinding bila belum ada level). Ring balk yang sudah ada bisa diubah perannya di panel Properti (*Peran*: Ring balk / Balok lantai). Detail penulangan memberi kode **B** untuk balok lantai.
- **Kolom menerus**: kolom tidak lagi dipotong oleh balok lantai, sehingga satu kolom bisa naik dari pondasi sampai lantai atas (ring balk tetap memotong kolom seperti sebelumnya).
- **Baja profil** untuk batang (kuda-kuda, gording, tiang, balok): bahan baru *Baja profil* dengan pilihan profil WF 150/200/250/300, H 150, kanal C 125/150, siku L 50/60, siku ganda 2L 60, pipa Ø76,3 dan Ø114,3, hollow 100×100 dan 50×100. Lebar dan tinggi penampang mengikuti profil; mengetik b/h sendiri melepas profil. Panel menampilkan berat (kg).
- **RAB divisi Pekerjaan Struktur Baja**: berat per profil = panjang × kg/m + 10% (pelat sambung, baut, sisa potong), jumlah batang 12 m, dan baris pengecatan baja (perkiraan 25 m² per ton).
- **Sekat modern**: bahan dinding baru *Panel PVC/WPC* (tanpa cat) dan *Kaca tempered 10 mm* (tembus pandang di 3D; RAB satu sisi + rangka aluminium, tidak masuk pengecatan).
- **Naikkan dinding sampai atap** (klik kanan atau palet Ctrl+K): dinding terpilih, termasuk yang di dalam grup, dinaikkan sampai bidang dudukan atap di atasnya; tepi atas otomatis mengikuti kemiringan atap (gunungan/dinding di bawah bubungan) lewat `profilAtas`, disederhanakan ≤ 16 titik.
- Panduan data (MCP `panduan_data`) bertambah: `peran:'balok'` pada ring balk dan `bahan:'baja'` + `profil` pada batang.

## Yang baru di 0.37.0

Atap denah bebas ala Roof by Footprint (Revit), penyatuan atap, dan rangka kayu otomatis untuk atap L (19 Oktober 2026, dikerjakan bersama untuk gambar Masjid 20 × 20 m).

- **Atap denah bebas (L/T/U)**: bentuk atap baru *Denah bebas*. Gambar dengan alat Atap (Tab sampai *Denah bebas*): klik titik keliling denah, tutup dengan klik titik pertama, klik 2×, atau Enter. Tiap tepi diberi tanda **tritisan** (miring) atau **dinding/gunungan**, dengan overstek dan kemiringan sendiri; permukaan diambil dari bidang terendah sehingga jurai terbentuk sendiri. Boleh diputar dengan sudut bebas.
- **Tinggi tepi atas rata**: isi satu elevasi; kemiringan tiap tritisan dihitung dari bentangnya sehingga jurai jatuh dari sudut ke sudut dan tepi atas semua sayap setinggi (mis. serambi 17,9° + sayap 10°).
- **Gabung atap (satu denah)** dan **Jadikan atap denah** di menu klik kanan: union denah beberapa atap; tepi hasil mewarisi tritisan/gunungan atap asal.
- **Rangka kayu otomatis atap denah**: murplat 8/12 di tritisan, balok dudukan atas 8/12 di dinding tepi atas, balok jurai 8/15, kuda-kuda sandar ±3 m (menempel ke dinding di bawahnya bila dekat), tiang penggantung di atas dinding yang dilintasi, tiang tengah bila bentang tak bertumpu > 3,5 m, sokong dari kaki tiang yang bertumpu ke puncak tiang berikutnya, gording pada ketinggian sama di semua bidang (berpasangan di jurai), klos di tiap kaki dan di jurai.
- **Prioritas denah di pertemuan atap**: bagian atap di atas denah dindingnya sendiri tidak dipangkas overstek atap lain; overstek yang menyembul di atas denah atap lain dipangkas. Sakelar baru per atap: *Satukan dengan atap lain*.
- **Perbaikan plafon miring**: ujung plafon tidak lagi menembus papan lisplang di tritisan (koreksi turun plafon × sin kemiringan).
- Fase berikutnya: jurai dalam di sudut cekung antara dua tritisan (Fase 2), rangka baja ringan atap denah.

## Yang baru di 0.36.0

Ukur dan dimensi ala SketchUp, denah per lantai, dan kusen gabung (19 Oktober 2026).

- **Meteran** (Shift+T, kelompok Anotasi, palet: *meteran*, *ukur*, *tape*): klik dua titik; jarak miring serta ΔX, ΔY, ΔZ tampil langsung di bilah bawah tanpa membuat elemen. Klik kedua mengunci hasil dan menyalin jaraknya; Ctrl+klik kedua menjadikannya garis bantu.
- **Dimensi** (D, palet: *dimensi*, *DIM*): klik dua titik, tarik ke samping untuk menentukan jarak garis ukur dari benda, lalu klik (atau ketik jaraknya lalu Enter). Dimensi bergaris bantu tegak dan bertanda miring, tampil di 3D dan ikut ke denah, tampak, serta potongan. Data: anotasi `ukuran` dengan isian baru `geser` {x, y, z}; dimensi lama tetap terbaca.
- **DXF semua lembar dalam 1 berkas**: tombol baru di Gambar 2D menyusun semua lembar yang dicentang dalam satu DXF seperti matriks (kolom ⌈√n⌉, kiri→kanan lalu turun, jarak 20 mm), kode dan nama lembar di layer `LEMBAR-JUDUL`. Tombol ZIP tetap ada. API: `rancangAPI.dxf({semua: true})`.
- **Proyek contoh Kantor Utama 2 lantai** (478 elemen: gedung 30 × 12 m, hall tengah, tangga dogleg, teras mobil, kanopi dak, atap perisai + gable, kusen bertipe; sumber PDF CV. Wahana Multikarya Consultan 2015) — `app/contoh/kantor-utama.json`, dibangkitkan `scripts/contoh-kantor-utama.py`.
- Denah per level kini juga menyaring anotasi menurut ketinggian (teks lantai 2 tidak muncul di denah lantai 1).
- **Kusen gabung satu rangka**: pintu, jendela, dan angin-angin yang bersentuhan di dinding yang sama otomatis berbagi satu tiang/ambang kusen (3D, tampak, potongan), tidak lagi bertiang ganda.
- **Isi bovenlicht jalusi**: tipe kusen kini bisa memakai boven jalusi (angin-angin) selain kaca — panel Tipe kusen → *Isi bovenlicht*.
- **Lembar denah per lantai**: bila ada dua level atau lebih yang berdinding, set lembar (daftar gambar, PDF set, DXF) memuat *Denah Lantai 1*, *Denah Lantai 2*, … masing-masing dengan kode dan kopnya sendiri; denah gabungan tetap bisa dipilih di pratinjau. Lantai 3 cukup ditambah lewat panel Proyek → *Tambah level*. MCP `gambar_2d` menerima `jenis: "denah:4"`.

## Yang baru di 0.35.0

Alat untuk bangunan bertingkat (disiapkan untuk menggambar Asrama Putri dua lantai, 18 Oktober 2026).

- **Alat Tangga** (kelompok Struktur, palet: *tangga*, *ST*, *TG*): klik pangkal bawah, klik ke arah naik; jumlah anak tangga dihitung dari tinggi ke level berikutnya (optrede ≤ 18 cm), antrede dari panjang klik kedua atau bawaan 28 cm. Panel Properti: lebar, tinggi naik, jumlah anak, antrede, tebal plat miring, arah, elevasi pangkal, railing (tanpa/kiri/kanan/dua). Di denah: garis anak tangga (putus-putus di atas bidang potong), panah NAIK/TURUN dengan keterangan `23 × 17/28`. RAB: beton plat miring + anak tangga, besi plat dua lapis Ø10-150 dan Ø8 anak, bekisting, panjang railing.
- **Plat lantai beton** (jenis `plat`, awalan W): dari lantai biasa dengan tombol *Jadikan plat lantai beton* di panel Properti (tebal = tinggi volume, bawaan 12 cm), bisa berlubang (void tangga). Panel: elevasi permukaan atas, tebal, tulangan Ø dan jarak, Ukuran alas. RAB: beton, besi dua lapis dua arah, bekisting bawah + tepi; butir ST-030/ST-031 menampilkan luas plat dan jumlah tangga.
- **Denah per level**: pemilih *Level* di bar Gambar 2D (tampil bila ada level di atas ±0,00): denah lantai 2 hanya menggambar benda yang terpotong bidang denah level itu, lantai/plat miliknya, dan tangga yang tiba di sana. MCP `gambar_2d` menerima `level` (elevasi dalam meter).
- Panduan data bertambah baris Y (tangga) dan W (plat); id elemen `Y…`, `W…`.
- **Proyek contoh Asrama Putri 2 lantai** (375 elemen: struktur lengkap, 16 kamar + KM, plat lantai berlubang, tangga, atap limas kayu, kusen bertipe) — buka lewat palet Ctrl+K *Buka contoh* atau panel Proyek → *Contoh*. Berkas `contoh/asrama-putri.json` ikut dipaketkan di desktop dan artifact; perintah *Buka proyek (.json)* juga tersedia di palet.

## Yang baru di 0.34.1

- **Plafon miring berhenti di lisplang.** Alat Plafon mode *Miring* kini memotong plafon di sisi dalam papan lisplang, bukan di ujung seng. Seng tetap menjorok sejauh *Mundur dari ujung seng* (bawaan 20 cm pada rangka kayu; 0 pada baja ringan), yang bisa diatur per sisi di panel atap → Lisplang. Atap tanpa lisplang tetap memakai tepi penutup.
- **Bawaan *Mundur dari ujung seng* kini 20 cm untuk semua rangka** (sebelumnya hanya kayu; baja ringan 0 sehingga lisplang menempel di ujung seng dan plafon tampak tidak berubah). Atap baja ringan yang sudah ada ikut bergeser 20 cm ke dalam; atur per sisi bila perlu.
- **Atap yang sudah dipecah** (bidang H) juga berhenti di lisplang: tepi bidang penutup yang berpapan lisplang (bidang H peran lisplang yang sejajar dan menempel) dimundurkan sampai sisi dalam papan saat dijadikan plafon miring.
- **Isian baru di Properti plafon miring: *Jarak tepi plafon dari ujung seng (m)*.** Terisi otomatis saat dibuat (jorokan seng + tebal papan, mis. 0,225) dan bisa diketik ulang; tepi luar plafon yang berhadapan dengan lisplang bergeser mengikuti angka itu, tepi lain tetap.
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
