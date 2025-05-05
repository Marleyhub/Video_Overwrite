import subprocess                                                       # lib que permite rodar comandos cmd/powershell via codigo
import validators                                                       # lib para validar se a url é valida (não é obrigatório mas é recomendado)
import glob                                                             # lib para achar arquivos a partir da sua extensão
import os                                                               # lib para interagir com arquivos
import whisper                                                          # lib para transcrever audio // Obs: ultilizar python 3.10.9
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai


app = Flask(__name__)
CORS(app)

## Home route
@app.route("/")
def index():
    return render_template("index.html") 

## Processing audio route
@app.route("/process", methods=["POST"])
def process_audio():
    data = request.get_json()
    url = data.get("url")
    output_name = data.get("name")
    output_template = f"{output_name}.%(ext)s"
    comando_yt_audio = ["yt-dlp", "-f", "bestaudio", "-o", output_template, url]

    if not validators.url(url):
        return jsonify({"error": "Invalid URL"}), 400

    ##Running yt-dlp command to download audio
    try:
        subprocess.run(comando_yt_audio, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to download audio"}), 500
    ##finding the downloaded file
    downloaded_files = glob.glob(f"{output_name}.*")

    ##Check if the file was downloaded
    if not downloaded_files:
        return jsonify({"error": "Audio not found"}), 500

    ##Converting to .mp3
    audio_input = downloaded_files[0]
    audio_output = f"{output_name}.mp3"
    comando_ffmpeg = ["ffmpeg", "-i", audio_input, "-vn", "-ab", "192k", "-y", audio_output]
    subprocess.run(comando_ffmpeg)
    os.remove(audio_input)

    ##Transcripting
    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(audio_output)
    transcript = result["text"]

    ##generative AI
    summary = genAi(transcript)

    return jsonify({
        "summary": summary,
        "transcript": transcript
   })

## Generative AI to summarize text
def genAi(transcript):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("API_KEY"))
    response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Summarize the following text, add topics if it has more than 100 words and a index it with the titles of each topic, index should apear first:" + transcript
    )
    summary = response.text
    return summary


if __name__ == "__main__":
    app.run(debug=True)


        
       