# app.py
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp
from utils.cleaner import clean_old_files
from datetime import datetime

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
        file_type = data.get("type")      # video or audio
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

        if file_type == "audio":
            ydl_opts['format'] = 'bestaudio' if quality == 'high' else 'worstaudio'
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192' if quality == 'high' else '64'
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir(DOWNLOAD_FOLDER):
            if filename in file:
                return jsonify({'success': True, 'path': f"/file/{file}"})

        return jsonify({'success': False, 'error': '⚠️ لم يتم العثور على الملف'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/file/<filename>')
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
