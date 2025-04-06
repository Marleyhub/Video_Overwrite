
import yt_dlp                       # lib que permite comunicação e transferencia de dados com youtube
import subprocess                   # lib que permite rodar comandos cmd/powershell via codigo
import validators                   # lib para validar se a url é valida (não é obrigatório mas é recomendado)
import glob                         # lib para achar arquivos a partir da sua extensão
import os                           # lib para interagir com arquivos
import whisper                      # lib para transcrever audio // Obs: ultilizar python 3.10.9
import google.generativeai as genai # lib para organizar e resumir audio transcrito
from dotenv import load_dotenv



while True:

    url = input("Enter a valid URL: ")                                                              # input de url pelo usuário                                                                               
    output_name = input("Enter a name for the audio: ")
    output_template = f"{output_name}.%(ext)s"
    comando_yt_audio = ["yt-dlp","-f", "bestaudio", "-o", output_template, url]                     # comando cmd para download  
  
    if validators.url(url):                                                                         # validaçãop de url
        processo = subprocess.run(comando_yt_audio, capture_output=True, text=True)                 # guardando output do comando cmd
        downloaded_files = glob.glob(f"{output_name}.*")                                            # colocando o arquivo baixado na viariável 
        
        if not downloaded_files: 
            print("Fail: Couldn't find this audio")
            continue
        print(processo)                                                                             # printando output do comando cmd

        audio_input = downloaded_files[0]
        audio_output = f"converted_{output_name}.mp3"
        comando_ffmpeg = ["ffmpeg", "-i", audio_input, "-vn", "-ab", "192k", "-y", audio_output]    # comando cmd para converter formatos
        subprocess.run(comando_ffmpeg)  
        print(f"Áudio convertido com sucesso: {audio_output}")

        os.remove(audio_input)

        #whisper config
        whisper_model = whisper.load_model("base")
        result = whisper_model.transcribe(f"./{audio_output}")
        print(f"The output text is: \n {result['text']}")

        #gemini config
        load_dotenv()
        api_key = os.getenv("API_KEY")
        genai.configure(api_key=api_key)
        genai_model = genai.GenerativeModel("gemini-pro")
        
        texto = f"{result}"
        prompt = f"Organize o seguinte texto em tópicos com numeração e títulos, como um índice de apresentação: \"\"\"{texto}\"\"\" "

        response = genai_model.generate_content(prompt)
        break
    

    else:
        print("Invalid URL. Please try again.")
        


        
       