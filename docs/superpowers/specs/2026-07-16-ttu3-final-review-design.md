# Desain Revisi TTU 3 Siap Review

Tanggal: 16 Juli 2026

## 1. Tujuan

Menghasilkan salinan naskah TTU 3 yang siap dikirim kepada dosen pembimbing dan siap digunakan untuk pendaftaran review jalur Diseminasi Internal. Revisi harus menjawab dua catatan dosen pembimbing: metode dilengkapi gambar atau ilustrasi tahapan, serta hasil dan eksperimen dilengkapi.

## 2. Artefak Tujuan

- Sumber: Google Doc `TTU 3 - Draft AITI - Evaluasi Kerentanan Prompt Injection` dengan ID `1IebP6pbBd9zGjNvZe395O7C3XXuS8cheqjx9NVuV0xg`.
- Tujuan: salinan Google Doc baru bernama `TTU 3 - FINAL REVIEW - Format Progdi`.
- Dokumen sumber tidak diubah dan tetap menjadi cadangan.
- Jalur TTU: Diseminasi Internal; sertifikat diseminasi sudah tersedia.

## 3. Sumber Kebenaran Data

Data penelitian harus diambil dari:

- `04_code/indofinsafety TTU 2/indofinsafety.ipynb`;
- `04_code/indofinsafety TTU 2/data/seed_prompts_v1.json`;
- `04_code/indofinsafety TTU 2/data/augmented_prompts_v1_200.json`;
- berkas CSV dan gambar pada `04_code/indofinsafety TTU 2/outputs/`.

Tidak boleh membuat angka eksperimen baru. Jika terdapat perbedaan antara prosa lama dan keluaran notebook, keluaran notebook menjadi acuan, disertai penjelasan batasan yang jujur.

## 4. Kontrak Format Progdi

- Acuan utama adalah folder `PANDUAN KP TA PRODI S1 TI` dengan ID Drive `1dOQLG1DI2AQyj5UBdVe-NprGIYSAdknN`, khususnya `Panduan TA S1 TI 2021 - Edisi 2022.pdf`.
- Ukuran halaman A4.
- Times New Roman 12 pt untuk naskah utama.
- Spasi tunggal.
- Margin kiri dan atas 4 cm; margin kanan dan bawah 3 cm.
- Bagian inti menggunakan penomoran desimal.
- Judul tabel berada di atas tabel; keterangan gambar berada di bawah gambar, berukuran 10 pt.
- Ilustrasi maksimum 15 x 15 cm dan tetap terbaca dalam cetak hitam-putih.
- Elemen khusus template AITI dihapus dari badan artikel: header jurnal, volume/nomor/ISSN, dan Riwayat Artikel.
- Halaman awal Progdi yang sudah relevan dipertahankan dan dirapikan: Persetujuan Review, Persetujuan, Pernyataan Keaslian, dan Persetujuan Publikasi.

## 5. Struktur Naskah

1. Halaman awal Progdi.
2. Judul, penulis, afiliasi, dan email.
3. Abstrak dan kata kunci.
4. `1. Pendahuluan`.
5. `2. Metode Penelitian`.
6. `3. Hasil dan Pembahasan`.
7. `4. Simpulan`.
8. Daftar Pustaka.

Abstrak, Metode, Hasil dan Pembahasan, serta Simpulan harus saling konsisten mengenai jumlah prompt, model, respons, metrik, dan batas validasi.

## 6. Desain Metode Penelitian

Metode menjelaskan:

- tiga kategori risiko: account information extraction, fraud/scam generation, dan personal data leakage;
- tiga teknik serangan: direct prompting, role-playing, dan social engineering;
- 45 seed prompt manual yang diaugmentasi dan divalidasi menjadi 200 prompt;
- model augmentasi `google/gemini-3.1-pro-preview`;
- tiga model target: `openai/gpt-5.2`, `google/gemini-3-flash-preview`, dan `qwen/qwen3.6-plus`;
- penggunaan prompt identik dan temperature 0 untuk model target;
- model penilai `anthropic/claude-opus-4.6` dengan label safe/unsafe;
- validasi manual berstrata terhadap 88 respons;
- perhitungan ASR, coverage, dan error rate.

### Gambar 1

Menggunakan rancangan B, yaitu eksperimen bercabang:

`Penyusunan dataset -> 200 prompt identik -> tiga model target secara paralel -> 600 respons -> LLM-as-a-judge dan validasi manual -> ASR dan error rate`.

Diagram dibuat ringkas, berbentuk mendekati persegi, dan tidak menggunakan alur vertikal panjang seperti gambar lama.

## 7. Desain Hasil dan Pembahasan

### 3.1 Dataset dan konfigurasi eksperimen

- Tabel 1 menggabungkan konfigurasi dan cakupan eksperimen: dataset, model augmentasi, model target, temperature, model judge, label evaluasi, 200 prompt, 600 respons, coverage 100 persen, dan error rate 0 persen.
- Distribusi kategori adalah 67, 67, dan 66 prompt.
- Distribusi teknik adalah 67 direct, 67 role-playing, dan 66 social engineering.

### 3.2 Perbandingan kerentanan model

- Gambar 2 berupa grafik batang ASR per model.
- Tabel 2 memuat total respons, respons safe, respons unsafe, dan ASR.
- Nilai utama: GPT-5.2 9/200 atau 4,5 persen; Gemini 3 Flash 73/200 atau 36,5 persen; Qwen 3.6 Plus 17/200 atau 8,5 persen.
- Narasi membahas perbedaan tingkat ketahanan, bukan hanya mengulang tabel.

### 3.3 Pola berdasarkan kategori dan teknik serangan

- Gambar 3 menggunakan dua panel: ASR per kategori risiko dan ASR per teknik serangan untuk setiap model.
- Tabel 3 memuat lima kombinasi kategori-teknik paling rentan.
- Temuan teratas adalah Gemini 3 Flash pada fraud/scam generation dengan social engineering: 16/22 atau 72,7 persen.
- Temuan berikutnya yang dibahas mencakup account information extraction dengan role-playing sebesar 63,6 persen dan fraud/scam generation dengan role-playing sebesar 60,9 persen pada Gemini 3 Flash.

### 3.4 Validasi manual LLM-as-a-judge

- Tabel 4 memuat ukuran sampel, agreement, Cohen's kappa, false-safe, dan false-unsafe.
- Validasi manual menggunakan 88 sampel berstrata.
- Agreement keseluruhan 72,73 persen dan Cohen's kappa 0,3917.
- Matriks pasangan label: judge safe/manual safe 47; judge safe/manual unsafe 7; judge unsafe/manual safe 17; judge unsafe/manual unsafe 17.
- Agreement per model: Gemini 68,57 persen; GPT-5.2 62,96 persen; Qwen 88,46 persen.
- ASR utama dijelaskan sebagai hasil label LLM-as-a-judge. Naskah tidak boleh menyatakan bahwa 88 label manual sudah menggantikan label pada keseluruhan 600 respons, karena berkas `final_labels_*.csv` belum menerapkan override manual.

### 3.5 Analisis kualitatif dan implikasi

- Tabel 5 memuat contoh ringkas respons aman dan tidak aman dari beberapa strata.
- Potongan respons berbahaya disamarkan atau diparafrasekan agar tidak menjadi petunjuk penyalahgunaan.
- Pembahasan menjelaskan mengapa role-playing dan social engineering yang dibingkai sebagai simulasi, audit, atau kebutuhan operasional dapat meningkatkan keberhasilan serangan.
- Implikasi difokuskan pada kebutuhan evaluasi domain-spesifik, guardrail, human oversight, dan pengujian berkala sebelum LLM digunakan dalam layanan finansial Indonesia.

## 8. Simpulan dan Keterbatasan

Simpulan menjawab tujuan penelitian dengan menyebut perbedaan ASR antar model dan pola serangan paling rentan. Keterbatasan harus menyebut:

- dataset hanya 200 prompt;
- validasi manual hanya 88 dari 600 respons dan menunjukkan reliabilitas judge yang belum kuat;
- hasil terikat pada versi model dan konfigurasi pengujian;
- belum mencakup indirect prompt injection, multi-turn attack, tool calling, dan retrieval-augmented generation.

## 9. Alur Pelaksanaan

1. Buat salinan Google Doc sumber.
2. Pastikan identitas salinan sebelum setiap rangkaian perubahan.
3. Hapus elemen template AITI yang tidak sesuai.
4. Terapkan struktur dan format Progdi.
5. Perbaiki Abstrak dan Metode.
6. Buat dan sisipkan Gambar 1 rancangan B.
7. Susun tabel dan grafik Hasil dan Pembahasan dari keluaran notebook.
8. Perbaiki Simpulan dan keterbatasan.
9. Selaraskan sitasi, istilah, penomoran, dan angka pada seluruh bagian.
10. Baca kembali salinan melalui konektor dan, bila tersedia, ekspor PDF untuk pemeriksaan tata letak.

Perubahan besar dilakukan dalam beberapa batch yang diverifikasi. Jika satu batch gagal, gunakan indeks dan revisi dokumen terbaru sebelum mencoba kembali; dokumen sumber tetap tidak disentuh.

## 10. Daftar Pustaka dan Sitasi

- Gunakan gaya sitasi numerik dalam kurung siku dan pertahankan urutan berdasarkan kemunculan pertama di teks.
- Setiap sumber pada daftar pustaka wajib dirujuk di badan artikel; setiap klaim metodologis atau perbandingan terhadap penelitian sebelumnya wajib memiliki sumber.
- Data hasil eksperimen sendiri tidak diberi sitasi eksternal, tetapi harus dapat ditelusuri ke notebook dan CSV.
- Pertahankan dan rapikan sumber utama yang sudah digunakan: Transformer, instruction alignment, LLM untuk finansial, PromptInject, jailbreak/safety training, serangan adversarial universal, IndoSafety, Do-Not-Answer, dan red teaming.
- Tambahkan sumber primer untuk keterbatasan LLM-as-a-judge, indirect prompt injection, dan instruction hierarchy: Zheng et al., `Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena` (arXiv:2306.05685); Greshake et al., `Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection` (arXiv:2302.12173); dan Wallace et al., `The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions` (arXiv:2404.13208).
- Target minimum adalah 12 sumber primer atau sumber akademik yang relevan. Metadata penulis, judul, tahun, venue, volume, halaman, dan tautan/DOI diperiksa sebelum dimasukkan.
- Tidak boleh menambahkan referensi yang tidak dipakai hanya untuk memperpanjang daftar pustaka.

## 11. Kriteria Selesai

Naskah dianggap siap dikirim kepada dosen pembimbing jika:

- format badan artikel mengikuti panduan Progdi dan tidak lagi menampilkan identitas template AITI;
- Gambar 1 rancangan B hadir, terbaca, dan memiliki keterangan;
- hasil mencakup konfigurasi, cakupan, ASR model, rincian kategori/teknik, kombinasi rentan, validasi manual, dan contoh kualitatif;
- lima tabel utama tersusun konsisten: konfigurasi dan cakupan, ringkasan model, kombinasi rentan, validasi manual, serta contoh kualitatif;
- semua angka dapat ditelusuri ke notebook atau keluaran CSV;
- metode tidak lagi menyatakan manual override yang belum dilakukan;
- abstrak, metode, hasil, dan simpulan konsisten;
- daftar pustaka memuat sekurang-kurangnya 12 sumber yang benar-benar dirujuk dan metadata bibliografinya telah diperiksa;
- tidak ada placeholder, penomoran rusak, tabel kosong, atau referensi yang tidak dirujuk;
- salinan Google Doc dapat dibuka dan dibaca kembali setelah seluruh perubahan.
