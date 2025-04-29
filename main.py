
import yt_dlp                               # lib que permite comunicação e transferencia de dados com youtube
import subprocess                           # lib que permite rodar comandos cmd/powershell via codigo
import validators                           # lib para validar se a url é valida (não é obrigatório mas é recomendado)
import glob                                 # lib para achar arquivos a partir da sua extensão
import os                                   # lib para interagir com arquivos
import whisper                              # lib para transcrever audio // Obs: ultilizar python 3.10.9
import google.generativeai as genai         # lib para organizar e resumir audio transcrito
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")  # Loads index.html from templates/

@app.route("/process", methods=["POST"])
def process_audio():
    data = request.get_json()
    url = data.get("url")
    output_name = data.get("name")
    output_template = f"{output_name}.%(ext)s"
    comando_yt_audio = ["yt-dlp", "-f", "bestaudio", "-o", output_template, url]

    if not validators.url(url):
        return jsonify({"error": "Invalid URL"}), 400

    subprocess.run(comando_yt_audio)
    downloaded_files = glob.glob(f"{output_name}.*")

    if not downloaded_files:
        return jsonify({"error": "Audio not found"}), 500

    audio_input = downloaded_files[0]
    audio_output = f"{output_name}.mp3"
    comando_ffmpeg = ["ffmpeg", "-i", audio_input, "-vn", "-ab", "192k", "-y", audio_output]
    subprocess.run(comando_ffmpeg)
    os.remove(audio_input)

    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(audio_output)
    transcript = result["text"]
    print(transcript)

    return jsonify({
        "transcript": transcript
   })

if __name__ == "__main__":
    app.run(debug=True)


        
       