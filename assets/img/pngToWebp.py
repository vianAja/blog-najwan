from PIL import Image
import os

def optimize_image(input_path, output_path, max_width=1200, quality=80):
    try:
        # Buka gambar
        with Image.open(input_path) as img:
            # 1. Hitung proporsi agar gambar tidak gepeng
            w_percent = (max_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            
            # 2. Resize menggunakan filter high-quality (LANCZOS)
            img_resized = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
            
            # 3. Simpan sebagai WebP dengan kompresi
            # Jika file asli PNG (transparan), WebP akan otomatis menjaganya
            img_resized.save(output_path, "WEBP", quality=quality, optimize=True)
            
            print(f"Berhasil: {output_path} tersimpan.")
            
    except Exception as e:
        print(f"Gagal memproses {input_path}: {e}")

# Contoh Penggunaan
input_file = "foto_produk.jpg" # Ganti dengan nama file kamu
output_file = "foto_produk_optimized.webp"

db = [
    'wallpaper1.png',
    'wallpaper2.png',
    'wallpaper3.png',
    'wallpaper4.png',
    'wallpaper5.png',
    'wallpaper6.png',
    'wallpaper7.png',
]
for data in db:
    optimize_image(data, data.split('.')[0]+'.webp', max_width=1200, quality=75)