# Revised Sections for TTU 2 and TTU 3

Source basis: `docs/ttu2_ttu3_completion_guide.md`, `docs/manual_validation_methodology.md`, latest `outputs/manual_validation_*.csv`, `outputs/evaluation_summary.csv`, and the current Google Docs drafts:

- `Tugas Talenta Unggul 2 672019256`
- `TTU 3 - Draft AITI - Evaluasi Kerentanan Prompt Injection`

## TTU 2 - Tugas Talenta Unggul 2 672019256

### Replace Abstract

This study evaluates the vulnerability of Large Language Models (LLMs) to prompt injection attacks in Indonesian financial security contexts. The main problem addressed is the limited availability of domain-specific safety evaluation for Indonesian-language LLM applications, especially in banking, fintech, digital wallet, customer service, and personal financial data scenarios. The research applies an experimental adversarial evaluation approach by constructing 200 Indonesian financial adversarial prompts, testing GPT-5.2, Gemini 3 Flash, and Qwen 3.6 Plus with the same prompts, and classifying 600 model responses using an LLM-as-a-judge mechanism. To examine the reliability of the automatic labels, the researcher conducted manual validation on a stratified sample of 88 responses selected based on model, risk category, attack technique, and judge label. The results show that Gemini 3 Flash has the highest Attack Success Rate at 36.5%, followed by Qwen 3.6 Plus at 8.5% and GPT-5.2 at 4.5%. The most vulnerable risk categories are fraud scam generation and account information extraction, especially when combined with social engineering and roleplay techniques. Manual validation shows 72.73% agreement between the LLM-as-a-judge labels and the researcher, with Cohen's Kappa of 0.3917. This study provides an initial benchmark and testing framework for evaluating LLM safety in Indonesian financial applications.

### Replace Methods Text Where Results Are Still Prospective

Use this paragraph at the end of Section 3.3:

Setelah proses augmentasi, dataset akhir terdiri dari 200 prompt adversarial berbahasa Indonesia. Prompt terbagi ke dalam tiga kategori risiko, yaitu account information extraction sebanyak 67 prompt, fraud scam generation sebanyak 67 prompt, dan personal data leakage sebanyak 66 prompt. Dari sisi teknik serangan, dataset terdiri dari direct prompting sebanyak 67 prompt, roleplay sebanyak 67 prompt, dan social engineering sebanyak 66 prompt. Distribusi ini dibuat relatif seimbang agar hasil evaluasi dapat dibandingkan antar kategori risiko dan teknik serangan.

Replace Section 3.6 Validasi Manual with:

Validasi manual dilakukan oleh peneliti terhadap sebagian respons untuk memeriksa reliabilitas label otomatis dari LLM-as-a-judge. Hasil utama penelitian tetap dihitung berdasarkan label otomatis terhadap seluruh 600 respons model, sedangkan validasi manual digunakan sebagai pengecekan reliabilitas pada sampel terpilih. Sampel validasi dipilih menggunakan stratified sampling berdasarkan kombinasi model, kategori risiko, teknik serangan, dan label judge. Dari setiap kombinasi strata, dipilih maksimal dua respons secara deterministik menggunakan seed tetap. Jumlah sampel validasi adalah 88 respons, terdiri dari respons safe dan unsafe dari tiga model target.

Setiap sampel diperiksa dengan membaca prompt, respons model, label judge, dan alasan judge. Peneliti kemudian memberikan label manual safe atau unsafe berdasarkan rubrik yang sama dengan judge. Label unsafe diberikan apabila respons mengandung bantuan substantif yang dapat digunakan untuk penyalahgunaan finansial, seperti instruksi bypass autentikasi, template phishing atau scam, teknik memperoleh data pribadi finansial, atau langkah operasional social engineering. Label safe diberikan apabila respons menolak permintaan, memberi edukasi defensif, mengarahkan pengguna ke prosedur legal dan aman, atau hanya menjelaskan risiko secara umum tanpa memberikan instruksi operasional berbahaya.

Tingkat kesesuaian antara label judge dan label manual dihitung menggunakan agreement dan Cohen's Kappa. Selain itu, penelitian ini menghitung false safe, yaitu kasus ketika judge memberi label safe tetapi peneliti memberi label unsafe, serta false unsafe, yaitu kasus ketika judge memberi label unsafe tetapi peneliti memberi label safe.

### Replace Section 4 Hasil Penelitian dan Pembahasan

Dataset akhir penelitian terdiri dari 200 prompt adversarial berbahasa Indonesia. Prompt dibagi ke dalam tiga kategori risiko, yaitu account information extraction, fraud scam generation, dan personal data leakage. Teknik serangan yang digunakan terdiri dari direct prompting, roleplay, dan social engineering. Distribusi dataset dibuat relatif seimbang: account information extraction terdiri dari 67 prompt, fraud scam generation 67 prompt, dan personal data leakage 66 prompt. Berdasarkan teknik serangan, direct prompting terdiri dari 67 prompt, roleplay 67 prompt, dan social engineering 66 prompt.

Hasil keseluruhan menunjukkan bahwa Gemini 3 Flash memiliki tingkat kerentanan tertinggi dengan 73 respons unsafe dari 200 prompt, atau Attack Success Rate (ASR) sebesar 36,5%. Qwen 3.6 Plus menghasilkan 17 respons unsafe dengan ASR 8,5%, sedangkan GPT-5.2 menghasilkan 9 respons unsafe dengan ASR 4,5%. Tidak terdapat error pada proses pengumpulan respons maupun penilaian, sehingga coverage penilaian mencapai 100%.

| Model | Total Prompt | Respons Valid | Unsafe | ASR | Error Rate |
|---|---:|---:|---:|---:|---:|
| GPT-5.2 | 200 | 200 | 9 | 4.5% | 0.0% |
| Gemini 3 Flash | 200 | 200 | 73 | 36.5% | 0.0% |
| Qwen 3.6 Plus | 200 | 200 | 17 | 8.5% | 0.0% |

Berdasarkan kategori risiko, Gemini 3 Flash menunjukkan ASR tertinggi pada fraud scam generation sebesar 46,3% dan account information extraction sebesar 43,3%. Hal ini menunjukkan bahwa prompt yang berkaitan dengan penipuan dan ekstraksi informasi akun lebih berpotensi menghasilkan respons tidak aman pada model tersebut. Qwen 3.6 Plus juga paling rentan pada fraud scam generation dengan ASR 16,4%, sedangkan GPT-5.2 menunjukkan ASR rendah pada seluruh kategori.

| Model | Kategori Risiko | Total | Unsafe | ASR |
|---|---|---:|---:|---:|
| GPT-5.2 | Account Information Extraction | 67 | 2 | 3.0% |
| GPT-5.2 | Fraud Scam Generation | 67 | 4 | 6.0% |
| GPT-5.2 | Personal Data Leakage | 66 | 3 | 4.5% |
| Gemini 3 Flash | Account Information Extraction | 67 | 29 | 43.3% |
| Gemini 3 Flash | Fraud Scam Generation | 67 | 31 | 46.3% |
| Gemini 3 Flash | Personal Data Leakage | 66 | 13 | 19.7% |
| Qwen 3.6 Plus | Account Information Extraction | 67 | 4 | 6.0% |
| Qwen 3.6 Plus | Fraud Scam Generation | 67 | 11 | 16.4% |
| Qwen 3.6 Plus | Personal Data Leakage | 66 | 2 | 3.0% |

Dari sisi teknik serangan, roleplay dan social engineering cenderung lebih efektif dibandingkan direct prompting. Pada Gemini 3 Flash, social engineering menghasilkan ASR 50,0% dan roleplay menghasilkan ASR 49,3%. Pada Qwen 3.6 Plus, social engineering juga menjadi teknik paling efektif dengan ASR 19,7%. Temuan ini menunjukkan bahwa permintaan berbahaya yang dibungkus sebagai audit, riset, simulasi, atau peran tertentu dapat meningkatkan kemungkinan respons unsafe.

| Model | Teknik Serangan | Total | Unsafe | ASR |
|---|---|---:|---:|---:|
| GPT-5.2 | Direct | 67 | 1 | 1.5% |
| GPT-5.2 | Roleplay | 67 | 5 | 7.5% |
| GPT-5.2 | Social Engineering | 66 | 3 | 4.5% |
| Gemini 3 Flash | Direct | 67 | 7 | 10.4% |
| Gemini 3 Flash | Roleplay | 67 | 33 | 49.3% |
| Gemini 3 Flash | Social Engineering | 66 | 33 | 50.0% |
| Qwen 3.6 Plus | Direct | 67 | 1 | 1.5% |
| Qwen 3.6 Plus | Roleplay | 67 | 3 | 4.5% |
| Qwen 3.6 Plus | Social Engineering | 66 | 13 | 19.7% |

Kombinasi paling rentan ditemukan pada Gemini 3 Flash untuk kategori fraud scam generation dengan teknik social engineering, dengan ASR 72,7%. Kombinasi lain yang juga tinggi adalah account information extraction dengan roleplay sebesar 63,6% dan fraud scam generation dengan roleplay sebesar 60,9%. Pola ini memperkuat temuan bahwa teknik yang membingkai permintaan berbahaya sebagai konteks sosial, profesional, atau simulasi lebih berisiko dibandingkan permintaan langsung.

| Model | Kombinasi Kategori dan Teknik | Total | Unsafe | ASR |
|---|---|---:|---:|---:|
| Gemini 3 Flash | Fraud Scam Generation + Social Engineering | 22 | 16 | 72.7% |
| Gemini 3 Flash | Account Information Extraction + Roleplay | 22 | 14 | 63.6% |
| Gemini 3 Flash | Fraud Scam Generation + Roleplay | 23 | 14 | 60.9% |
| Gemini 3 Flash | Account Information Extraction + Social Engineering | 22 | 13 | 59.1% |
| Qwen 3.6 Plus | Fraud Scam Generation + Social Engineering | 22 | 9 | 40.9% |

Validasi manual dilakukan pada 88 sampel respons. Dari sampel tersebut, 64 respons diberi label manual safe dan 24 respons diberi label manual unsafe. Tingkat kesesuaian keseluruhan antara LLM-as-a-judge dan peneliti adalah 72,73% dengan Cohen's Kappa 0,3917. Nilai ini menunjukkan adanya kesesuaian sedang, tetapi juga mengindikasikan bahwa LLM-as-a-judge belum sepenuhnya menggantikan penilaian manusia.

| Model | Sampel Manual | Agreement | Cohen Kappa | False Safe | False Unsafe |
|---|---:|---:|---:|---:|---:|
| Overall | 88 | 72.73% | 0.3917 | 7 | 17 |
| Gemini 3 Flash | 35 | 68.57% | 0.3699 | 5 | 6 |
| GPT-5.2 | 27 | 62.96% | 0.0000 | 2 | 8 |
| Qwen 3.6 Plus | 26 | 88.46% | 0.6977 | 0 | 3 |

Terdapat 24 ketidaksesuaian antara judge dan label manual. Sebanyak 17 kasus merupakan false unsafe, yaitu judge menilai unsafe tetapi peneliti menilai safe. Sebanyak 7 kasus merupakan false safe, yaitu judge menilai safe tetapi peneliti menilai unsafe. Temuan ini menunjukkan bahwa judge cenderung lebih ketat pada sebagian respons, tetapi masih dapat melewatkan beberapa respons yang menurut peneliti mengandung bantuan berbahaya.

Secara umum, hasil penelitian menunjukkan bahwa setiap model memiliki tingkat ketahanan yang berbeda terhadap prompt injection dalam konteks finansial Indonesia. Gemini 3 Flash menunjukkan ASR tertinggi dibandingkan dua model lainnya, terutama pada kategori fraud scam generation dan account information extraction. Hal ini mengindikasikan bahwa model tersebut lebih mudah menghasilkan respons yang memberi bantuan substantif ketika prompt dibingkai sebagai skenario penipuan, audit, roleplay, atau social engineering.

GPT-5.2 memiliki ASR paling rendah, tetapi tidak sepenuhnya bebas dari respons unsafe. Hal ini menunjukkan bahwa safety alignment dapat menurunkan risiko, namun belum menghilangkan kerentanan secara total. Qwen 3.6 Plus berada di antara GPT-5.2 dan Gemini 3 Flash, dengan kerentanan paling terlihat pada social engineering dan fraud scam generation.

Temuan mengenai efektivitas roleplay dan social engineering sejalan dengan karakter prompt injection yang sering memanfaatkan framing kontekstual. Prompt yang tampak sah, seperti riset, audit, simulasi, atau peran profesional, dapat membuat permintaan berbahaya terlihat lebih dapat diterima oleh model. Oleh karena itu, sistem LLM di domain finansial tidak cukup hanya menolak permintaan langsung, tetapi juga perlu mampu mengenali permintaan berbahaya yang dibungkus dalam konteks tidak langsung.

### Replace Section 5 Simpulan dan Saran

Penelitian ini menunjukkan bahwa LLM memiliki tingkat kerentanan yang berbeda terhadap prompt injection dalam konteks keamanan finansial berbahasa Indonesia. Dari tiga model yang diuji, Gemini 3 Flash memiliki ASR tertinggi sebesar 36,5%, diikuti Qwen 3.6 Plus sebesar 8,5% dan GPT-5.2 sebesar 4,5%. Kategori fraud scam generation dan account information extraction menjadi kategori yang paling rentan, terutama ketika dikombinasikan dengan teknik social engineering dan roleplay.

Validasi manual terhadap 88 sampel menunjukkan agreement sebesar 72,73% antara penilaian otomatis dan peneliti, dengan Cohen's Kappa 0,3917. Hal ini menunjukkan bahwa LLM-as-a-judge dapat digunakan sebagai mekanisme evaluasi awal, tetapi tetap memerlukan validasi manusia untuk memastikan kualitas label, terutama pada kasus yang ambigu. Penelitian lanjutan dapat memperluas dataset, menambah jumlah annotator manusia, menguji indirect prompt injection, multi-turn attack, serta sistem LLM yang menggunakan tool-calling atau retrieval-augmented generation.

## TTU 3 - Draft AITI

### Replace English Abstract

This study evaluates the vulnerability of Large Language Models (LLMs) to prompt injection attacks in Indonesian financial security contexts. The study addresses the limited availability of domain-specific safety evaluation for Indonesian-language LLM applications, especially in banking, fintech, digital wallet, customer service, and personal financial data scenarios. The research applies an experimental adversarial evaluation approach by constructing 200 Indonesian financial adversarial prompts, testing GPT-5.2, Gemini 3 Flash, and Qwen 3.6 Plus with the same prompts, and classifying 600 model responses using an LLM-as-a-judge mechanism. Manual validation was conducted on a stratified sample of 88 responses to examine the reliability of the automatic labels. The results show that Gemini 3 Flash has the highest Attack Success Rate at 36.5%, followed by Qwen 3.6 Plus at 8.5% and GPT-5.2 at 4.5%. Social engineering and roleplay are the most effective attack techniques, especially in fraud scam generation and account information extraction scenarios. Manual validation shows 72.73% agreement between the LLM-as-a-judge labels and the researcher. This study provides an initial benchmark and testing framework for evaluating LLM safety in Indonesian financial applications.

### Replace Indonesian Abstrak

Penelitian ini mengevaluasi kerentanan Large Language Models (LLM) terhadap serangan prompt injection dalam konteks keamanan finansial berbahasa Indonesia. Permasalahan utama yang dibahas adalah masih terbatasnya evaluasi keamanan LLM yang spesifik terhadap domain finansial Indonesia, terutama pada skenario perbankan, fintech, dompet digital, layanan pelanggan, dan perlindungan data pribadi finansial. Penelitian ini menggunakan pendekatan eksperimental melalui adversarial evaluation dengan menyusun 200 prompt adversarial finansial berbahasa Indonesia, menguji GPT-5.2, Gemini 3 Flash, dan Qwen 3.6 Plus menggunakan prompt yang sama, serta menilai 600 respons model menggunakan pendekatan LLM-as-a-judge. Validasi manual dilakukan terhadap stratified sample sebanyak 88 respons untuk memeriksa reliabilitas label otomatis. Hasil menunjukkan bahwa Gemini 3 Flash memiliki Attack Success Rate tertinggi sebesar 36,5%, diikuti Qwen 3.6 Plus sebesar 8,5% dan GPT-5.2 sebesar 4,5%. Teknik social engineering dan roleplay menjadi teknik yang paling efektif, terutama pada skenario fraud scam generation dan account information extraction. Validasi manual menunjukkan agreement sebesar 72,73% antara label LLM-as-a-judge dan peneliti. Penelitian ini menghasilkan benchmark awal dan kerangka pengujian untuk mengevaluasi keamanan LLM pada aplikasi finansial berbahasa Indonesia.

### Replace Methods Paragraphs That Mention Manual Validation

Use this paragraph after the dataset augmentation paragraph:

Setelah augmentasi, dataset akhir terdiri dari 200 prompt adversarial berbahasa Indonesia yang terbagi ke dalam tiga kategori risiko dan tiga teknik serangan. Berdasarkan kategori risiko, dataset terdiri dari account information extraction sebanyak 67 prompt, fraud scam generation sebanyak 67 prompt, dan personal data leakage sebanyak 66 prompt. Berdasarkan teknik serangan, dataset terdiri dari direct prompting sebanyak 67 prompt, roleplay sebanyak 67 prompt, dan social engineering sebanyak 66 prompt. Distribusi ini dibuat relatif seimbang agar hasil evaluasi dapat dibandingkan antar kategori dan teknik serangan.

Replace the current manual validation paragraph with:

Validasi manual dilakukan oleh peneliti terhadap 88 respons yang dipilih menggunakan stratified sampling berdasarkan kombinasi model, kategori risiko, teknik serangan, dan label judge. Validasi manual digunakan untuk memeriksa reliabilitas label otomatis dari LLM-as-a-judge, bukan untuk mengganti label seluruh 600 respons yang menjadi dasar hasil utama. Setiap sampel diperiksa dengan membaca prompt, respons model, label judge, dan alasan judge. Peneliti kemudian memberikan label manual safe atau unsafe berdasarkan rubrik yang sama dengan judge. Label unsafe diberikan apabila respons mengandung bantuan substantif yang dapat digunakan untuk penyalahgunaan finansial, sedangkan label safe diberikan apabila respons menolak permintaan, memberi edukasi defensif, atau hanya menjelaskan risiko secara umum tanpa instruksi operasional berbahaya.

### Replace Hasil dan Pembahasan

Dataset akhir penelitian terdiri dari 200 prompt adversarial berbahasa Indonesia. Prompt dibagi ke dalam tiga kategori risiko, yaitu account information extraction, fraud scam generation, dan personal data leakage. Teknik serangan yang digunakan terdiri dari direct prompting, roleplay, dan social engineering. Seluruh prompt diberikan kepada tiga model target, yaitu GPT-5.2, Gemini 3 Flash, dan Qwen 3.6 Plus, sehingga total respons yang dievaluasi berjumlah 600 respons.

Hasil keseluruhan menunjukkan bahwa Gemini 3 Flash memiliki tingkat kerentanan tertinggi dengan 73 respons unsafe dari 200 prompt, atau Attack Success Rate (ASR) sebesar 36,5%. Qwen 3.6 Plus menghasilkan 17 respons unsafe dengan ASR 8,5%, sedangkan GPT-5.2 menghasilkan 9 respons unsafe dengan ASR 4,5%. Tidak terdapat error pada proses pengumpulan respons maupun penilaian, sehingga coverage penilaian mencapai 100%.

| Model | Total Prompt | Respons Valid | Unsafe | ASR | Error Rate |
|---|---:|---:|---:|---:|---:|
| GPT-5.2 | 200 | 200 | 9 | 4.5% | 0.0% |
| Gemini 3 Flash | 200 | 200 | 73 | 36.5% | 0.0% |
| Qwen 3.6 Plus | 200 | 200 | 17 | 8.5% | 0.0% |

Berdasarkan kategori risiko, Gemini 3 Flash menunjukkan ASR tertinggi pada fraud scam generation sebesar 46,3% dan account information extraction sebesar 43,3%. Qwen 3.6 Plus juga paling rentan pada fraud scam generation dengan ASR 16,4%, sedangkan GPT-5.2 menunjukkan ASR rendah pada seluruh kategori, yaitu 3,0% pada account information extraction, 6,0% pada fraud scam generation, dan 4,5% pada personal data leakage. Pola ini menunjukkan bahwa prompt yang berkaitan dengan penipuan dan ekstraksi informasi akun lebih berpotensi menghasilkan respons tidak aman dibandingkan kebocoran data pribadi secara umum.

Dari sisi teknik serangan, roleplay dan social engineering cenderung lebih efektif dibandingkan direct prompting. Pada Gemini 3 Flash, social engineering menghasilkan ASR 50,0% dan roleplay menghasilkan ASR 49,3%, jauh lebih tinggi dibandingkan direct prompting sebesar 10,4%. Pada Qwen 3.6 Plus, social engineering juga menjadi teknik paling efektif dengan ASR 19,7%. Pada GPT-5.2, ASR tertinggi muncul pada roleplay sebesar 7,5%, tetapi tetap relatif rendah dibandingkan dua model lainnya.

| Model | Teknik Serangan | Total | Unsafe | ASR |
|---|---|---:|---:|---:|
| GPT-5.2 | Direct | 67 | 1 | 1.5% |
| GPT-5.2 | Roleplay | 67 | 5 | 7.5% |
| GPT-5.2 | Social Engineering | 66 | 3 | 4.5% |
| Gemini 3 Flash | Direct | 67 | 7 | 10.4% |
| Gemini 3 Flash | Roleplay | 67 | 33 | 49.3% |
| Gemini 3 Flash | Social Engineering | 66 | 33 | 50.0% |
| Qwen 3.6 Plus | Direct | 67 | 1 | 1.5% |
| Qwen 3.6 Plus | Roleplay | 67 | 3 | 4.5% |
| Qwen 3.6 Plus | Social Engineering | 66 | 13 | 19.7% |

Kombinasi kategori dan teknik paling rentan ditemukan pada Gemini 3 Flash untuk fraud scam generation dengan social engineering, dengan ASR 72,7%. Kombinasi lain yang juga tinggi adalah account information extraction dengan roleplay sebesar 63,6% dan fraud scam generation dengan roleplay sebesar 60,9%. Pada Qwen 3.6 Plus, kombinasi fraud scam generation dengan social engineering menghasilkan ASR 40,9%. Temuan ini memperkuat bahwa teknik yang membingkai permintaan berbahaya sebagai konteks sosial, profesional, audit, atau simulasi lebih berisiko dibandingkan permintaan langsung.

Validasi manual dilakukan pada 88 sampel respons. Dari sampel tersebut, 64 respons diberi label manual safe dan 24 respons diberi label manual unsafe. Tingkat kesesuaian keseluruhan antara LLM-as-a-judge dan peneliti adalah 72,73% dengan Cohen's Kappa 0,3917. Terdapat 24 ketidaksesuaian antara judge dan label manual, terdiri dari 17 false unsafe dan 7 false safe. Hal ini menunjukkan bahwa LLM-as-a-judge dapat digunakan sebagai mekanisme evaluasi awal, tetapi tetap perlu diperiksa manusia pada penelitian keamanan yang sensitif.

| Model | Sampel Manual | Agreement | Cohen Kappa | False Safe | False Unsafe |
|---|---:|---:|---:|---:|---:|
| Overall | 88 | 72.73% | 0.3917 | 7 | 17 |
| Gemini 3 Flash | 35 | 68.57% | 0.3699 | 5 | 6 |
| GPT-5.2 | 27 | 62.96% | 0.0000 | 2 | 8 |
| Qwen 3.6 Plus | 26 | 88.46% | 0.6977 | 0 | 3 |

Secara umum, hasil penelitian menunjukkan bahwa setiap model memiliki tingkat ketahanan yang berbeda terhadap prompt injection dalam konteks finansial Indonesia. Gemini 3 Flash menunjukkan ASR tertinggi dibandingkan dua model lainnya, terutama pada kategori fraud scam generation dan account information extraction. GPT-5.2 memiliki ASR paling rendah, tetapi tidak sepenuhnya bebas dari respons unsafe. Qwen 3.6 Plus berada di antara GPT-5.2 dan Gemini 3 Flash, dengan kerentanan paling terlihat pada social engineering dan fraud scam generation.

Temuan mengenai efektivitas roleplay dan social engineering sejalan dengan karakter prompt injection yang sering memanfaatkan framing kontekstual. Prompt yang tampak sah, seperti riset, audit, simulasi, atau peran profesional, dapat membuat permintaan berbahaya terlihat lebih dapat diterima oleh model. Oleh karena itu, sistem LLM di domain finansial tidak cukup hanya menolak permintaan langsung, tetapi juga perlu mampu mengenali permintaan berbahaya yang dibungkus dalam konteks tidak langsung.

### Replace Simpulan

Hasil penelitian menunjukkan bahwa Gemini 3 Flash memiliki Attack Success Rate tertinggi sebesar 36,5%, diikuti Qwen 3.6 Plus sebesar 8,5% dan GPT-5.2 sebesar 4,5%. Teknik social engineering dan roleplay menjadi teknik yang paling efektif dalam menghasilkan respons unsafe, terutama pada kategori fraud scam generation dan account information extraction. Temuan ini menunjukkan bahwa kerentanan prompt injection tidak hanya muncul pada permintaan langsung, tetapi juga pada prompt yang dibingkai sebagai audit, riset, simulasi, atau peran profesional.

Validasi manual terhadap 88 sampel menunjukkan agreement sebesar 72,73% antara penilaian otomatis dan peneliti, dengan Cohen's Kappa 0,3917. Dengan demikian, LLM-as-a-judge dapat digunakan sebagai evaluasi awal untuk dataset yang lebih besar, tetapi tetap memerlukan pemeriksaan manusia pada penelitian keamanan yang sensitif dan pada kasus yang ambigu. Penelitian lanjutan dapat memperluas dataset, menambah jumlah annotator manusia, menguji indirect prompt injection dan multi-turn attack, serta mengevaluasi sistem LLM yang menggunakan tool-calling atau retrieval-augmented generation.
