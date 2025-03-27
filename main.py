import yt_dlp # lib que permite comunicação e transferencia de dados com youtube 
import subprocess # lib que permite rodar comandos cmd/powershell via codigo
import validators #lib para validar se a url é valida (não é obrigatório mas é recomendado)



while True:
    url = input("Enter a valid URL: ")
    comando_yt_audio = ["yt-dlp","-f", "bestaudio", url] # comando que vai rodar no cmd para baixar o audio
    
    if validators.url(url):
        processo = subprocess.run(comando_yt_audio, capture_output=True, text=True)
        print(processo)
        break
    else:
        print("Invalid URL. Please try again.")