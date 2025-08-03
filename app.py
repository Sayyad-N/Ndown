#Code Written By SayyadN
#Code For Dwonload Videos From Socials Platforms Using YT_DLP
#Date  : 3-8-2025


import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp
from datetime import datetime
import time

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get("url")
        quality = data.get("quality")     # high or low

        if not url:
            return jsonify({'success': False, 'error': '⚠️ الرابط غير موجود'})

        filename = f"{uuid.uuid4()}"
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{filename}.%(ext)s")

        ydl_opts = {
            'outtmpl': output_template,
            'quiet': True,
            'format': 'best' if quality == 'high' else 'worst',
            'postprocessors': [],
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir(DOWNLOAD_FOLDER):
            if filename in file:
                return jsonify({'success': True, 'path': f"/file/{file}"})

        return jsonify({'success': False, 'error': '⚠️ لم يتم العثور على الملف'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/file/<filename>')
def clean_old_files(folder, max_age_minutes=30):
    now = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_minutes * 60:
                try:
                    os.remove(file_path)
                    print(f"[CLEANER] Removed old file: {filename}")
                except Exception as e:
                    print(f"[CLEANER] Failed to delete {filename}: {e}")

def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    else:
        return "⚠️ الملف غير موجود أو تم حذفه", 404

# تنظيف الملفات القديمة كل تشغيل
clean_old_files(DOWNLOAD_FOLDER)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
