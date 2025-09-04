# EduSeedbank

EduSeedbank adalah repositori Python yang men-generate paket konten edukatif offline (video terkompresi + HTML interaktif) yang disesuaikan dengan kurikulum daerah; petani dapat mengunduh "bibit pengetahuan" lewat LoRa mesh dan menanamnya di server lokal sekolah desa.

## Overview

EduSeedbank memungkinkan distribusi konten pendidikan ke daerah terpencil dengan konektivitas internet terbatas melalui jaringan LoRa mesh. Sistem ini mengemas konten edukatif dalam bentuk paket "bibit" yang dapat dikirim melalui jaringan dengan bandwidth rendah dan ditanam di server lokal sekolah.

## Fitur Utama

- Generasi paket konten edukatif offline
- Kompresi video untuk transmisi LoRa
- Konten HTML interaktif
- Kustomisasi kurikulum daerah
- Distribusi melalui jaringan LoRa mesh
- Server lokal untuk akses konten

## Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/your-username/eduseedbank.git
   cd eduseedbank
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

## Penggunaan

### CLI Interface

EduSeedbank menyediakan antarmuka command-line untuk berinteraksi dengan sistem:

```bash
# Membuat paket konten edukatif baru
python -m eduseedbank.cli.main create-package

# Mengompresi video untuk transmisi LoRa
python -m eduseedbank.cli.main compress-video

# Membuat halaman HTML interaktif
python -m eduseedbank.cli.main create-html

# Mensimulasikan jaringan LoRa
python -m eduseedbank.cli.main simulate-network

# Menjalankan server lokal
python -m eduseedbank.cli.main run-server
```

### Contoh Penggunaan

Lihat file `examples/demo.py` untuk contoh penggunaan lengkap sistem EduSeedbank:

```bash
python examples/demo.py
```

Untuk melihat alur kerja lengkap dari pembuatan konten hingga distribusi dan penanaman di server lokal:

```bash
python examples/complete_workflow.py
```

### API

Untuk menggunakan EduSeedbank sebagai library dalam aplikasi Python Anda:

```python
from eduseedbank.packaging.core import PackagingSystem

# Membuat sistem packaging
packaging_system = PackagingSystem()

# Membuat paket baru
package = packaging_system.create_package(
    title="Matematika Dasar untuk Petani",
    description="Materi matematika dasar yang relevan dengan kegiatan pertanian",
    curriculum="Jawa Tengah",
    subject="Matematika"
)

# Menyimpan paket
package_path = package.save("output/matematika_dasar")
```

## Struktur Proyek

```
eduseedbank/
├── src/
│   └── eduseedbank/
│       ├── packaging/      # Sistem packaging konten
│       ├── compression/    # Kompresi video
│       ├── network/        # Jaringan LoRa
│       ├── server/         # Server lokal
│       └── cli/            # Interface command-line
├── tests/                  # Unit tests
├── examples/               # Contoh penggunaan
├── docs/                   # Dokumentasi
├── requirements.txt        # Dependensi
└── setup.py               # Konfigurasi paket
```

## Cara Kerja EduSeedbank

1. **Pembuatan Konten**: Educator membuat paket konten edukatif menggunakan sistem packaging
2. **Kustomisasi Kurikulum**: Konten disesuaikan dengan kurikulum daerah tertentu
3. **Optimasi**: Video dikompresi untuk transmisi LoRa yang memiliki bandwidth terbatas
4. **Distribusi**: Paket dikirim melalui jaringan LoRa mesh dari gateway ke node petani/sekolah
5. **Penanaman**: Sekolah "menanam" paket di server lokal mereka
6. **Akses**: Siswa mengakses konten pendidikan secara offline melalui server lokal

## Kontribusi

Kontribusi sangat dialu-alukan! Silakan buat issue atau pull request untuk perbaikan atau penambahan fitur.

## Lisensi

MIT License - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.