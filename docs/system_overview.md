# EduSeedbank System Overview

## What is EduSeedbank?

EduSeedbank adalah sistem yang memungkinkan distribusi konten pendidikan ke daerah terpencil dengan konektivitas internet terbatas melalui jaringan LoRa mesh. Sistem ini mengemas konten edukatif dalam bentuk paket "bibit" yang dapat dikirim melalui jaringan dengan bandwidth rendah dan ditanam di server lokal sekolah.

## How It Works

### 1. Content Creation
Educators atau pembuat konten menggunakan EduSeedbank untuk mengemas materi pendidikan dalam bentuk paket yang disebut "seed". Setiap paket berisi:
- Video pendidikan yang dikompresi untuk transmisi LoRa
- Konten HTML interaktif dengan latihan dan kuis
- Metadata tentang kurikulum daerah dan mata pelajaran

### 2. Curriculum Customization
Konten dapat disesuaikan dengan kurikulum daerah tertentu, memastikan relevansi dengan kebutuhan pendidikan lokal.

### 3. Package Optimization
Konten dikompresi dan dioptimalkan untuk transmisi melalui jaringan LoRa yang memiliki bandwidth sangat terbatas (sekitar 300 bps hingga 50 kbps).

### 4. LoRa Mesh Distribution
Paket pendidikan (seed) didistribusikan melalui jaringan LoRa mesh:
- Node gateway menerima seed dari sumber konten
- Node petani dapat mengunduh seed dari gateway
- Sekolah dapat menerima seed dari gateway atau node petani lainnya

### 5. Planting Seeds
Sekolah "menanam" seed yang diunduh ke server lokal mereka:
- Server lokal menyimpan konten untuk akses offline
- Siswa dapat mengakses materi pendidikan tanpa koneksi internet
- Server menyediakan antarmuka web untuk mengakses konten

## Technical Components

### Packaging System
Menangani pembuatan paket konten edukatif dengan metadata yang sesuai.

### Video Compression
Mengompresi video pendidikan agar sesuai dengan bandwidth LoRa yang sangat terbatas.

### HTML Generator
Membuat konten HTML interaktif dengan latihan dan kuis untuk meningkatkan keterlibatan siswa.

### LoRa Networking
Mensimulasikan jaringan LoRa mesh untuk distribusi paket antar node.

### Local Server
Menyediakan server lokal di sekolah untuk menyajikan konten pendidikan kepada siswa.

## Usage Flow

1. Administrator EduSeedbank membuat paket konten menggunakan CLI
2. Paket dikirim ke node gateway melalui metode yang sesuai
3. Petani atau sekolah mengunduh paket melalui jaringan LoRa
4. Sekolah "menanam" paket di server lokal mereka
5. Siswa mengakses konten pendidikan melalui server lokal

## Benefits

- Membawa pendidikan berkualitas ke daerah terpencil tanpa infrastruktur internet
- Mengurangi ketergantungan pada koneksi internet yang tidak stabil
- Memungkinkan distribusi konten yang disesuaikan dengan kurikulum lokal
- Memberdayakan komunitas lokal untuk berpartisipasi dalam distribusi pendidikan