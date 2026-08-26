# Evaluasi Kerentanan Prompt Injection LLM pada Keamanan Finansial Indonesia

Mikael Aldy Cahya Pratama  
Program Studi Teknik Informatika, Fakultas Teknologi Informasi  
Universitas Kristen Satya Wacana  
Email: [isi email korespondensi]

## Abstract

This study proposes an evaluation framework for prompt injection vulnerabilities in large language models within Indonesian financial security contexts. The research addresses the lack of domain-specific safety evaluation for Indonesian financial scenarios, especially requests involving account access, fraud facilitation, and personal financial data leakage. The method uses adversarial evaluation by constructing Indonesian prompts across three risk categories and three attack techniques: direct prompting, role playing, and social engineering. Model responses are planned to be assessed using binary safety labels, attack success rate, and category-level vulnerability analysis supported by LLM-as-a-judge and human validation. The expected contribution is a localized evaluation design that can reveal how financial-domain prompts expose weaknesses in model refusal and safety behavior. This study concludes that Indonesian financial LLM deployment requires domain-specific red-teaming procedures before integration into customer-facing systems.

Keywords: prompt injection, large language model, financial security, Indonesian language, safety evaluation

## Abstrak

Penelitian ini mengusulkan kerangka evaluasi kerentanan prompt injection pada large language model dalam konteks keamanan finansial Indonesia. Permasalahan yang dibahas adalah masih terbatasnya evaluasi keamanan yang spesifik terhadap skenario finansial berbahasa Indonesia, terutama permintaan yang berkaitan dengan akses akun, fasilitasi penipuan, dan kebocoran data pribadi finansial. Metode penelitian menggunakan evaluasi adversarial dengan menyusun prompt berbahasa Indonesia berdasarkan tiga kategori risiko dan tiga teknik serangan, yaitu direct prompting, role playing, dan social engineering. Respons model direncanakan dinilai menggunakan label keamanan biner, attack success rate, serta analisis kerentanan per kategori dengan dukungan LLM-as-a-judge dan validasi manusia. Kontribusi yang diharapkan adalah rancangan evaluasi lokal yang mampu menunjukkan bagaimana prompt domain finansial dapat mengekspos kelemahan penolakan dan perilaku keamanan model. Penelitian ini menyimpulkan bahwa penerapan LLM pada layanan finansial Indonesia memerlukan red teaming domain-spesifik sebelum digunakan pada sistem yang berhadapan langsung dengan pengguna.

Kata kunci: prompt injection, large language model, keamanan finansial, bahasa Indonesia, evaluasi keamanan

## Pendahuluan

Large language model (LLM) semakin banyak digunakan sebagai komponen sistem digital, termasuk untuk chatbot layanan pelanggan, asisten internal, pencarian informasi, dan otomasi analisis dokumen. Dalam konteks finansial, kemampuan LLM untuk memahami instruksi natural language dapat memberi manfaat pada layanan pengguna, edukasi produk, dan dukungan operasional. Akan tetapi, kemampuan yang sama juga menimbulkan risiko ketika model menerima instruksi yang dirancang untuk memanipulasi perilaku, melemahkan mekanisme penolakan, atau mendorong keluaran yang tidak sesuai dengan kebijakan keamanan.

Salah satu bentuk risiko penting adalah prompt injection, yaitu teknik manipulasi input yang berusaha membuat model mengikuti instruksi penyerang dan mengabaikan batasan keselamatan. Studi tentang kegagalan safety training menunjukkan bahwa model yang telah dilatih untuk menolak permintaan berbahaya tetap dapat gagal ketika tujuan keamanan bertentangan dengan tujuan mengikuti instruksi atau ketika model menghadapi bentuk input yang tidak tercakup secara memadai dalam data safety training [1]. Studi lain juga menunjukkan bahwa serangan adversarial terhadap model yang telah disejajarkan dapat bersifat transferable dan tidak selalu bergantung pada satu model tertentu [6]. Kegagalan tersebut relevan untuk aplikasi finansial karena keluaran yang tidak aman dapat berkaitan dengan pengambilalihan akun, penipuan, penyalahgunaan data pribadi, atau penyusunan pesan manipulatif yang terlihat sah.

Kebutuhan evaluasi keamanan menjadi lebih penting dalam konteks Indonesia. IndoSafety menunjukkan bahwa evaluasi keamanan LLM tidak cukup mengandalkan terjemahan langsung dari benchmark berbahasa Inggris karena norma lokal, ragam bahasa, dan sensitivitas budaya dapat memengaruhi perilaku model [2]. Penelitian tersebut membangun dataset keselamatan yang mencakup bahasa Indonesia formal, bahasa Indonesia kolokial, dan beberapa bahasa daerah, serta menunjukkan bahwa model dapat menghasilkan respons tidak aman pada konteks lokal. Namun, IndoSafety berfokus pada cakupan risiko keselamatan yang luas dan belum secara khusus meneliti prompt injection pada domain keamanan finansial.

Domain finansial memiliki karakteristik risiko yang berbeda dari percakapan umum. Permintaan yang tampak seperti edukasi, audit, atau simulasi dapat berisi intensi untuk memperoleh informasi akun, melewati proses verifikasi, menyusun skenario penipuan, atau mengekstrak data pribadi. Sensitivitas tersebut juga berkaitan dengan kewajiban perlindungan data pribadi di Indonesia [7]. Di sisi lain, model tetap perlu membantu untuk permintaan yang sah, misalnya edukasi keamanan digital, penjelasan pencegahan phishing, atau panduan melapor insiden. Karena itu, evaluasi tidak hanya perlu mengukur apakah model menolak, tetapi juga apakah model mampu memberikan alternatif aman tanpa membocorkan langkah operasional yang dapat disalahgunakan.

Penelitian red teaming memberikan dasar metodologis untuk mengeksplorasi permukaan risiko model secara terstruktur. STAR memperlihatkan bahwa instruksi red teaming yang terparameterisasi dapat membantu mengarahkan cakupan risiko dan meningkatkan kualitas sinyal evaluasi [3]. Dalam konteks lokal, benchmark seperti BatakJailbreakBench juga menunjukkan pentingnya evaluasi yang memperhatikan bahasa dan konteks rendah sumber daya, termasuk pemisahan antara perilaku penolakan dan potensi kebocoran informasi [4]. Prinsip-prinsip tersebut relevan untuk menyusun evaluasi prompt injection yang tidak hanya bersifat umum, tetapi juga terarah pada skenario finansial Indonesia.

Berdasarkan latar belakang tersebut, penelitian ini merumuskan masalah utama: bagaimana merancang evaluasi kerentanan prompt injection pada LLM dalam konteks keamanan finansial Indonesia. Pertanyaan penelitian yang digunakan adalah sebagai berikut. Pertama, bagaimana menyusun taksonomi risiko finansial yang dapat digunakan untuk membangun prompt adversarial berbahasa Indonesia. Kedua, teknik prompt injection apa yang perlu diuji untuk menilai ketahanan model terhadap manipulasi instruksi. Ketiga, metrik apa yang dapat digunakan untuk mengukur keberhasilan serangan dan membandingkan kerentanan antar kategori risiko. Keempat, bagaimana hasil evaluasi dapat digunakan sebagai dasar rekomendasi mitigasi bagi pengembangan sistem LLM finansial.

Tujuan penelitian ini adalah menyusun rancangan evaluasi prompt injection berbasis bahasa Indonesia untuk domain finansial, membangun dataset awal yang mencakup kategori risiko dan teknik serangan yang terkontrol, serta merancang mekanisme penilaian respons model menggunakan kombinasi automatic judging dan validasi manusia. Manfaat akademik dari penelitian ini adalah menyediakan dasar bagi benchmark keamanan LLM finansial berbahasa Indonesia. Manfaat praktisnya adalah memberi kerangka uji awal bagi pengembang, bank, dan perusahaan teknologi finansial sebelum mengintegrasikan LLM ke layanan yang memproses informasi pengguna.

Ruang lingkup penelitian dibatasi pada serangan langsung melalui prompt teks tunggal. Penelitian ini tidak membahas indirect prompt injection melalui retrieval-augmented generation, tool calling, dokumen eksternal, atau serangan multi-turn yang kompleks. Fokus domain dibatasi pada tiga kategori risiko, yaitu ekstraksi informasi akun, pembuatan atau fasilitasi penipuan, dan kebocoran data pribadi finansial. Pembatasan ini dibuat agar rancangan evaluasi tetap terukur dan dapat direplikasi sebagai dasar penelitian lanjutan.

## Metode Penelitian

Penelitian ini menggunakan pendekatan evaluasi adversarial atau red teaming terhadap LLM. Pendekatan ini dipilih karena prompt injection tidak selalu muncul pada penggunaan normal, tetapi dapat ditemukan melalui input yang sengaja dirancang untuk menekan batas keamanan model. Alur penelitian terdiri dari perancangan taksonomi risiko, penyusunan seed prompt, augmentasi dataset, pengujian model target, penilaian respons, dan analisis metrik keamanan.

Taksonomi risiko disusun dengan mengadaptasi kerangka keselamatan LLM dari penelitian sebelumnya, terutama kategori information hazards dan malicious uses dalam IndoSafety [2], kemudian dipersempit ke konteks finansial. Tiga kategori risiko digunakan dalam penelitian ini. Kategori pertama adalah account information extraction, yaitu prompt yang bertujuan memperoleh akses atau informasi terkait akun, seperti verifikasi, pemulihan kata sandi, atau pengambilalihan akun. Kategori kedua adalah fraud and scam generation, yaitu prompt yang mendorong model membantu menyusun pesan, strategi, atau skenario penipuan. Kategori ketiga adalah personal financial data leakage, yaitu prompt yang berupaya memperoleh atau mengekspos data pribadi finansial seperti nomor rekening, data identitas, riwayat transaksi, atau informasi know your customer.

Setiap kategori risiko dikombinasikan dengan tiga teknik serangan. Teknik pertama adalah direct prompting, yaitu permintaan langsung untuk melakukan tindakan yang tidak aman. Teknik kedua adalah role playing, yaitu instruksi yang meminta model memainkan peran tertentu agar batas keamanan menjadi lebih lemah, misalnya sebagai auditor palsu, pegawai internal, atau aktor dalam simulasi. Teknik ketiga adalah social engineering, yaitu prompt yang membungkus permintaan berbahaya dengan alasan yang tampak sah, seperti riset, edukasi, audit keamanan, atau kebutuhan operasional. Pemilihan tiga teknik ini mengikuti temuan bahwa jailbreak dapat memanfaatkan konflik antara kemampuan mengikuti instruksi dan tujuan keamanan model [1], sekaligus mengikuti prinsip red teaming terarah yang menekankan variasi parameter serangan [3].

Dataset awal dirancang dalam bentuk seed prompt sebanyak 45 item. Jumlah tersebut berasal dari kombinasi tiga kategori risiko, tiga teknik serangan, dan lima prompt untuk setiap kombinasi. Setiap item dataset memiliki atribut `id`, `category`, `attack_type`, dan `prompt`. Seluruh prompt ditulis dalam bahasa Indonesia dengan konteks finansial yang dekat dengan penggunaan lokal, seperti mobile banking, dompet digital, kode OTP, data KYC, nomor rekening, dan layanan pelanggan. Prompt disusun tanpa menyertakan data pribadi nyata dan sebaiknya menggunakan entitas sintetis atau placeholder agar dataset tidak menimbulkan risiko privasi.

Setelah seed prompt tersusun, dataset dirancang untuk diperluas melalui augmentasi berbantuan LLM. Augmentasi bertujuan meningkatkan variasi redaksi tanpa mengubah kategori risiko dan teknik serangan. Agar cakupan tetap seimbang, augmentasi dilakukan dengan mempertahankan distribusi antar kategori dan antar teknik serangan. Setiap prompt hasil augmentasi perlu diperiksa untuk memastikan bahwa teks tetap berada dalam konteks finansial, tidak merupakan duplikasi dekat dari seed prompt, dan tidak berisi informasi nyata yang dapat mengidentifikasi individu atau institusi tertentu.

Model target direncanakan mencakup perbandingan antara model komersial dan model yang lebih terbuka melalui akses API. Dalam rancangan notebook penelitian, kandidat model yang digunakan adalah GPT-5.2, Gemini 3 Flash, dan Qwen3.6 Plus. Nama dan versi model perlu dikunci kembali pada saat pelaporan final karena layanan API dapat berubah dari waktu ke waktu. Untuk menjaga replikasi, setiap pengujian perlu mencatat nama model, penyedia API, tanggal pengujian, parameter decoding, dan jumlah token keluaran maksimum. Pengujian disarankan menggunakan temperature rendah agar variasi keluaran tidak terlalu dipengaruhi sampling acak.

Respons model dinilai menggunakan skema biner, yaitu `safe` dan `unsafe`. Respons dikategorikan `unsafe` apabila memberikan bantuan substantif yang dapat digunakan untuk penyalahgunaan finansial, termasuk langkah operasional, taktik penipuan, template manipulatif, cara melewati verifikasi, panduan pengambilalihan akun, atau ekstraksi data pribadi. Respons dikategorikan `safe` apabila menolak permintaan berbahaya, memberikan peringatan, mengarahkan pengguna pada tindakan legal dan aman, atau memberi edukasi keamanan tingkat tinggi tanpa instruksi operasional yang dapat disalahgunakan. Jika respons mencampurkan penolakan dengan detail yang tetap dapat dieksekusi, respons tersebut dinilai `unsafe` karena masih terjadi kebocoran informasi berbahaya.

Penilaian awal dilakukan dengan LLM-as-a-judge menggunakan rubrik yang tetap. Strategi ini mengikuti praktik evaluasi otomatis yang juga digunakan dalam IndoSafety, yaitu merumuskan pertanyaan penilaian untuk menentukan apakah respons mengandung bahaya [2]. Namun, karena evaluasi otomatis dapat bias atau salah memahami konteks, sebagian sampel perlu divalidasi secara manual. Validasi manusia digunakan untuk mengukur konsistensi penilaian dan mengidentifikasi kasus ambigu, misalnya respons yang terlihat menolak tetapi tetap memberikan petunjuk operasional. Jika terdapat perbedaan antara automatic judge dan penilai manusia, kasus tersebut perlu ditinjau ulang dan rubrik diperjelas.

Metrik utama yang digunakan adalah attack success rate (ASR), yaitu proporsi prompt yang menghasilkan respons `unsafe` dari seluruh prompt valid yang diuji. Secara konseptual, ASR dihitung sebagai jumlah respons tidak aman dibagi jumlah respons yang berhasil dinilai. Selain ASR keseluruhan, analisis dilakukan pada tingkat kategori risiko, teknik serangan, dan kombinasi kategori-teknik. Analisis per kategori menunjukkan area risiko finansial yang paling rentan, sedangkan analisis per teknik menunjukkan pola prompt injection yang paling efektif. Metrik tambahan yang dapat digunakan adalah coverage, error rate, dan distribusi response type untuk memastikan bahwa hasil tidak terdistorsi oleh respons kosong, error API, atau kegagalan parsing.

Alur penelitian secara keseluruhan dapat dijelaskan sebagai berikut. Pertama, taksonomi risiko finansial disusun berdasarkan literatur keselamatan LLM dan kebutuhan domain finansial Indonesia. Kedua, seed prompt dibuat secara manual untuk setiap kombinasi kategori risiko dan teknik serangan. Ketiga, dataset diperluas melalui augmentasi terkontrol dan dibersihkan dari duplikasi atau prompt yang keluar dari ruang lingkup. Keempat, prompt dikirim ke model target dengan parameter pengujian yang terdokumentasi. Kelima, respons model dinilai menggunakan rubrik keamanan biner dan divalidasi secara manual pada sampel tertentu. Keenam, hasil penilaian dihitung menjadi ASR dan dianalisis berdasarkan model, kategori, teknik serangan, serta kombinasi keduanya.

## Hasil dan Pembahasan

Karena naskah ini disusun sebagai artikel kerja berbasis rancangan penelitian, bagian hasil dan pembahasan berfokus pada desain analisis yang akan digunakan, bukan pada klaim hasil final. Pendekatan ini penting agar artikel tidak menyajikan angka eksperimen sebelum proses validasi selesai. Dengan demikian, pembahasan diarahkan pada bagaimana keluaran evaluasi akan menjawab pertanyaan penelitian dan bagaimana temuan nantinya dapat ditafsirkan secara hati-hati.

Rancangan dataset menghasilkan matriks evaluasi yang seimbang antara kategori risiko dan teknik serangan. Struktur ini memungkinkan perbandingan yang lebih jelas dibandingkan prompt yang dikumpulkan secara bebas, karena setiap kategori diuji dengan jumlah serangan yang relatif sama. Pendekatan ini sejalan dengan prinsip red teaming terparameterisasi dalam STAR, yaitu bahwa variasi instruksi dan parameter serangan dapat membantu menjelajahi area risiko secara lebih terarah [3]. Dalam penelitian ini, parameter yang digunakan bukan demografi atau topik sosial, melainkan kategori risiko finansial dan teknik manipulasi instruksi.

Tabel 1 menunjukkan rancangan taksonomi yang digunakan untuk menyusun dataset. Tabel ini dapat dipertahankan dalam artikel final karena menjelaskan desain penelitian, bukan hasil eksperimen.

**Tabel 1 Rancangan taksonomi prompt injection finansial**

| Kategori Risiko | Fokus Risiko | Contoh Konteks Aman untuk Dokumentasi |
|---|---|---|
| Account information extraction | Upaya memperoleh akses atau informasi akun | OTP, reset kata sandi, mobile banking, dompet digital |
| Fraud and scam generation | Bantuan untuk membuat atau memfasilitasi penipuan | pesan phishing, social engineering, manipulasi korban |
| Personal financial data leakage | Upaya memperoleh atau mengekspos data pribadi finansial | NIK, nomor rekening, data KYC, riwayat transaksi |

Tiga teknik serangan memiliki fungsi evaluasi yang berbeda. Direct prompting mengukur apakah model dapat menolak permintaan berbahaya yang eksplisit. Role playing menguji apakah model tetap mempertahankan batas keamanan ketika permintaan dibungkus sebagai simulasi atau peran tertentu. Social engineering menguji apakah model dapat mengenali intensi berbahaya ketika prompt menggunakan alasan yang tampak sah. Berdasarkan literatur jailbreak, teknik yang membingkai ulang instruksi dapat mengeksploitasi konflik antara perilaku mengikuti instruksi dan perilaku menolak permintaan berbahaya [1]. Oleh karena itu, perbandingan antar teknik penting untuk mengetahui apakah kelemahan model muncul pada permintaan eksplisit atau pada bentuk manipulasi yang lebih halus.

Pembahasan hasil nantinya perlu dilakukan pada tiga tingkat. Tingkat pertama adalah perbandingan antar model berdasarkan ASR keseluruhan. Perbandingan ini menunjukkan model mana yang lebih sering menghasilkan respons tidak aman pada dataset finansial berbahasa Indonesia. Tingkat kedua adalah analisis per kategori risiko. Jika kategori fraud and scam generation memiliki ASR lebih tinggi daripada kategori lain, misalnya, hal itu dapat menunjukkan bahwa model lebih mudah membantu penyusunan konten manipulatif daripada membocorkan data pribadi. Tingkat ketiga adalah analisis per teknik serangan. Jika role playing atau social engineering lebih efektif daripada direct prompting, maka mitigasi tidak cukup hanya memblokir kata kunci eksplisit, tetapi perlu mendeteksi framing dan intensi.

Tabel 2 menunjukkan format ringkasan metrik yang disarankan untuk laporan hasil final. Nilai pada tabel ini tidak diisi dalam artikel kerja karena hasil eksperimen belum diperlakukan sebagai final.

**Tabel 2 Format pelaporan hasil evaluasi final**

| Model | Jumlah Prompt Valid | Respons Unsafe | ASR | Kategori Paling Rentan | Teknik Paling Efektif |
|---|---:|---:|---:|---|---|
| Model A | [isi] | [isi] | [isi] | [isi] | [isi] |
| Model B | [isi] | [isi] | [isi] | [isi] | [isi] |
| Model C | [isi] | [isi] | [isi] | [isi] | [isi] |

Selain angka agregat, pembahasan kualitatif perlu meninjau contoh respons yang dinilai tidak aman. Analisis kualitatif tidak perlu menampilkan prompt atau respons berbahaya secara lengkap. Bagian yang berisiko dapat disunting dengan placeholder seperti `[disunting]`, sedangkan pembahasan diarahkan pada jenis kegagalannya. Contoh pola kegagalan yang dapat dianalisis adalah penolakan parsial yang tetap menyertakan langkah operasional, respons edukatif yang terlalu rinci, atau respons role playing yang mengikuti persona tanpa menjaga batas keamanan. Cara ini menjaga nilai ilmiah analisis tanpa memperbesar risiko penyalahgunaan.

Penelitian ini juga perlu membedakan antara kegagalan keamanan dan kegagalan kegunaan. Respons yang menolak seluruh permintaan berbahaya dapat dianggap aman, tetapi model yang terlalu sering menolak pertanyaan edukatif yang sah dapat mengurangi kegunaan sistem. Meskipun fokus penelitian ini adalah kerentanan prompt injection, artikel final dapat menambahkan kategori observasi seperti safe refusal, safe redirection, dan over-refusal agar evaluasi tidak hanya menghitung keberhasilan serangan. Pembedaan ini penting untuk sistem finansial karena pengguna sah tetap membutuhkan edukasi keamanan, misalnya cara mengenali phishing atau langkah resmi melapor penipuan.

Dari sisi konteks Indonesia, penelitian ini memperluas gagasan IndoSafety ke domain yang lebih spesifik. IndoSafety menekankan pentingnya evaluasi yang dilokalkan secara bahasa dan budaya [2]. Penelitian ini menerapkan prinsip tersebut pada risiko finansial, dengan memasukkan istilah dan skenario yang dekat dengan ekosistem Indonesia seperti OTP, KYC, rekening, dompet digital, dan layanan mobile banking. Lokalisasi ini penting karena prompt yang terasa umum dalam bahasa Inggris dapat berubah bentuk ketika ditulis dalam bahasa Indonesia, terutama ketika menggunakan campuran istilah formal, istilah operasional, dan gaya komunikasi layanan pelanggan.

Dalam konteks tata kelola, Otoritas Jasa Keuangan telah menerbitkan pedoman tata kelola kecerdasan artifisial untuk perbankan Indonesia pada tahun 2025 [5]. Pedoman tersebut menunjukkan bahwa adopsi AI di sektor finansial perlu dikaitkan dengan tata kelola, manajemen risiko, dan kehati-hatian. Penelitian ini tidak mengevaluasi kepatuhan hukum secara langsung, tetapi menyediakan salah satu komponen teknis yang relevan untuk tata kelola tersebut, yaitu pengujian keamanan model sebelum digunakan dalam sistem yang berinteraksi dengan pengguna atau data sensitif.

Keterbatasan utama rancangan penelitian ini adalah cakupan serangan yang masih terbatas pada single-turn direct prompt injection. Serangan dunia nyata dapat melibatkan percakapan multi-turn, dokumen eksternal, retrieval, tool calling, atau integrasi dengan sistem backend. Selain itu, penggunaan LLM-as-a-judge perlu divalidasi karena model penilai dapat memiliki bias atau salah klasifikasi. Keterbatasan lain adalah dataset yang diperluas dengan LLM dapat memiliki variasi bahasa yang kurang alami dibandingkan prompt dari pengguna nyata. Oleh karena itu, artikel final perlu menyertakan validasi manusia dan, bila memungkinkan, pengayaan dataset dari skenario operasional yang telah dianonimkan.

Pembahasan juga perlu berhati-hati dalam membandingkan model. Model komersial dan model terbuka dapat memiliki kebijakan keamanan, sistem prompt, dan mekanisme filtering yang berbeda. Perbandingan ASR tidak boleh ditafsirkan sebagai peringkat keamanan absolut, melainkan sebagai hasil pada dataset, waktu pengujian, parameter, dan akses API tertentu. Karena model layanan dapat berubah tanpa pemberitahuan, dokumentasi tanggal dan versi pengujian menjadi bagian penting dari replikasi.

## Simpulan

Penelitian ini menyusun rancangan evaluasi kerentanan prompt injection pada LLM dalam konteks keamanan finansial Indonesia. Rancangan penelitian mencakup taksonomi tiga kategori risiko, yaitu ekstraksi informasi akun, pembuatan atau fasilitasi penipuan, dan kebocoran data pribadi finansial. Setiap kategori dikombinasikan dengan tiga teknik serangan, yaitu direct prompting, role playing, dan social engineering. Struktur ini memungkinkan evaluasi yang lebih terarah terhadap kelemahan model dalam memahami intensi berbahaya pada prompt berbahasa Indonesia.

Metode yang diusulkan menggunakan dataset prompt adversarial berbahasa Indonesia, pengujian terhadap beberapa model target, penilaian respons berbasis rubrik safe dan unsafe, serta perhitungan attack success rate pada tingkat keseluruhan, kategori risiko, teknik serangan, dan kombinasi keduanya. Rancangan ini diharapkan dapat menjadi dasar benchmark awal untuk menilai kesiapan LLM sebelum diterapkan dalam layanan finansial yang berhadapan dengan pengguna.

Kontribusi utama penelitian ini adalah lokalisasi evaluasi keamanan LLM ke domain finansial Indonesia. Penelitian ini melengkapi studi keselamatan LLM yang lebih umum dengan fokus pada skenario yang berisiko tinggi bagi pengguna layanan finansial, seperti pengambilalihan akun, penipuan, dan kebocoran data pribadi. Untuk pengembangan selanjutnya, evaluasi perlu diperluas ke serangan multi-turn, indirect prompt injection pada sistem retrieval, validasi manusia yang lebih besar, serta analisis trade-off antara keamanan dan kegunaan respons model.

## Daftar Pustaka

[1] A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?," arXiv preprint arXiv:2307.02483, 2023.

[2] M. F. Azmi, M. D. Al Kautsar, A. F. Wicaksono, and F. Koto, "IndoSafety: Culturally Grounded Safety for LLMs in Indonesian Languages," in Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, 2025, pp. 9135-9166.

[3] L. Weidinger et al., "STAR: SocioTechnical Approach to Red Teaming Language Models," in Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, 2024, pp. 21516-21532.

[4] L. Siagian, "BatakJailbreakBench: A Low-Resource Batak Toba Safety Benchmark for Jailbreak Resistance and Refusal-Leakage Behavior in LLMs," manuscript, 2026.

[5] Otoritas Jasa Keuangan, "Artificial Intelligence Governance for Indonesian Banks," 2025. [Online]. Available: https://ojk.go.id/en/Publikasi/Roadmap-dan-Pedoman/Perbankan/Pages/Indonesia-Artificial-Intelligence-Governance-for-Banking.aspx

[6] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson, "Universal and Transferable Adversarial Attacks on Aligned Language Models," arXiv preprint arXiv:2307.15043, 2023.

[7] Republik Indonesia, Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi, 2022.

## Catatan Audit Sumber dan Revisi

Bagian ini bukan bagian utama artikel. Gunakan sebagai checklist sebelum naskah dipindahkan ke DOCX atau template AITI.

1. Klaim "penggunaan AI meningkat 67 persen menurut McKinsey" dari draft awal tidak dimasukkan karena sumber spesifiknya belum tersedia dalam literatur yang diberikan. Jika ingin tetap digunakan, perlu laporan lengkap, tahun, judul, dan halaman.

2. Nama model perlu dikunci sebelum artikel final. Draft kerja dan notebook memakai variasi nama seperti GPT-5.2, Gemini 3 Flash, Gemini 3.1 Pro, Qwen3.5, dan Qwen3.6 Plus. Artikel ini memakai kandidat model secara umum dan menyarankan pencatatan versi final saat pengujian.

3. Referensi BatakJailbreakBench dimasukkan sebagai manuscript karena file yang tersedia tidak menunjukkan venue publikasi final. Jika paper tersebut belum diterbitkan, pertimbangkan untuk memindahkannya dari Daftar Pustaka utama ke catatan internal atau menggantinya dengan sumber peer-reviewed.

4. Bagian Hasil dan Pembahasan sengaja tidak memuat angka dari `outputs/evaluation_summary.csv` karena arah yang dipilih adalah `proposal-only`. Jika nanti ingin versi artikel hasil eksperimen, tabel ASR aktual dapat dimasukkan setelah validasi manual dan verifikasi model selesai.

5. Untuk kepatuhan AITI, abstrak dibuat lebih aman mengikuti batas ketat 150 kata dari halaman author guidelines, meskipun template PDF menyebut 150-200 kata.
