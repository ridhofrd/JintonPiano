Tutorial Penggunaan
# Tugas Besar PCD - Piano Virtual Berbasis MediaPipe
Proyek ini menggunakan MediaPipe Hand Landmarker untuk mendeteksi gerakan tangan dan memainkan piano virtual dengan 2 oktaf.

## Cara Menjalankan
1. Clone repo: `git clone https://github.com/ridhofrd/Tugas_Besar_PCD_PianoTangan`
2. Install dependensi: `pip install -r 02_FastAPI_Interface/requirements.txt`
3. Download `hand_landmarker.task` dari https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker dan taruh di `01_Notebook_Eksplorasi/model/` dan `02_FastAPI_Interface/model/`.
4. Taruh file suara (.wav) di `01_Notebook_Eksplorasi/sounds/` dan `02_FastAPI_Interface/sounds/`.
5. Jalankan notebook: `jupyter notebook 01_Notebook_Eksplorasi/PianoTangan_MediaPipe.ipynb`
6. Jalankan API: `cd 02_FastAPI_Interface && uvicorn main:app --reload`
7. Jalankan demo: `python 01_Notebook_Eksplorasi/main.py --model_path "model/hand_landmarker.task" --num_octaves 2 --list_of_octaves "[1,3]" --height_and_width_black "[[5,8],[5,8]]" --shape "(800,600,3)" --tap_threshold 20 --piano_config_threshold 30 --piano_config 1`
8. Lihat video demo: [YouTube](https://www.youtube.com/watch?v=abcdef12345)

## Struktur Folder
- `01_Notebook_Eksplorasi/`: Kode lengkap dan evaluasi.
- `02_FastAPI_Interface/`: API untuk inferensi.
- `03_Dokumen_Proses_Analisis.pdf`: Narasi proyek.
- `04_File_Presentasi.pptx`: Presentasi ringkas.
- `Link_YouTube.txt`: Link video demo.
