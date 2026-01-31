# Evaluasi Kerentanan Prompt Injection LLM Bahasa Indonesia pada Sektor Keamanan Finansial


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Tugas Akhir S1 Teknik Informatika - Universitas Kristen Satya Wacana**  
> **Peneliti**: Mikael Aldy Cahya Pratama  
> **Pembimbing**: Prof. Hindriyanto Dwi Purnomo, S.T., M.IT., Ph.D.
> **Tahun**: 2026

---

## 📖 Tentang Penelitian

Penelitian ini membangun dataset prompt injection pertama untuk bahasa Indonesia dengan fokus pada keamanan data finansial, dan mengevaluasi kerentanan 3 Large Language Models:
- Gemini 3.0 Flash (Google)
- GPT-5.2 (OpenAI)
- SeaLLMs-v3-7B (Open-source)

**Dataset**: 100-300 prompts dalam bahasa Indonesia  
**Kategori**: Financial Privacy, Transaction Bypass, Data Leakage, Fraud Simulation, General Safety  
**Teknik**: Direct Jailbreak, Role-playing, Social Engineering

---

## 🎯 Tujuan Penelitian

1. Membangun dataset prompt injection comprehensive untuk bahasa Indonesia
2. Mengevaluasi kerentanan LLM terhadap serangan prompt injection
3. Mengidentifikasi pola kerentanan spesifik dalam konteks Indonesia
4. Memberikan rekomendasi untuk mitigasi risiko

---

## 📊 Struktur Repositori

```
├── 01_Proposal/          # Proposal TA1
├── 02_Literature/        # Paper & referensi
├── 03_Dataset/           # Prompt dataset (500 prompts)
├── 04_Code/              # Testing & evaluation scripts
├── 05_Results/           # Experimental results
├── 06_Documentation/     # Research logs & notes
├── 07_Writing/           # TA2 & TA3 papers
└── 08_Admin/             # Forms & certificates
```

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10+
pip install -r requirements.txt
```

### Setup
```bash
# Clone repository
git clone https://github.com/[username]/IndoPromptInject-TA.git
cd IndoPromptInject-TA

# Install dependencies
pip install -r requirements.txt

# Setup API keys (create .env file)
cp .env.example .env
# Edit .env dan isi API keys
```

### Run Pilot Test
```bash
cd 04_Code/data_collection
python pilot_test.py
```

---

## 📈 Preliminary Results

**Pilot Test (10 prompts - Gemini 3.0 Flash)**  
- Attack Success Rate: XX%
- Most Vulnerable Category: [Category]
- Most Effective Technique: [Technique]

*Full results akan dipublikasikan setelah penelitian selesai*

---

## 📝 Publications

- **TA2 (Working Paper)**: [Link akan ditambahkan]
- **TA3 (Journal/Conference)**: [Submitted to SINTA-X Journal]
- **Dataset Release**: [Kaggle/HuggingFace link segera ditambahkkan]

---

## 🤝 Contributing

Penelitian ini adalah bagian dari Tugas Akhir. Untuk pertanyaan atau kolaborasi:
- Email: mikaelaldy56@gmail.com
- LinkedIn: [LinkedIn profile]

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- Dosen Pembimbing: [Nama Dosen]
- Program Studi Teknik Informatika, FTI UKSW
- Inspired by: [IndoSafety](https://github.com/falensiazmi/IndoSafety)

---

## 📅 Timeline

- **Jan 2026**: Proposal & Literature Review
- **Feb 2026**: Data Collection, Testing, Analysis, Writing
- **Mar 2026**: Publication & Defense

---

## ⚠️ Ethical Considerations

All prompts are synthetic and for research purposes only. No real financial data or personal information is used. Results will be shared responsibly following coordinated disclosure principles.

---

**Last Updated**: 28 January 2026