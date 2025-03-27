
import yt_dlp          # lib que permite comunicação e transferencia de dados com youtube
import subprocess      # lib que permite rodar comandos cmd/powershell via codigo
import validators      #lib para validar se a url é valida (não é obrigatório mas é recomendado)



while True:
    url = input("Enter a valid URL: ")                                                      #input de url pelo usuário
    comando_yt_audio = ["yt-dlp","-f", "bestaudio", url]                                    #comando cmd para download
    
    if validators.url(url):                                                                 #validaçãop de url
        processo = subprocess.run(comando_yt_audio, capture_output=True, text=True)         #guardando output do comando cmd
        print(processo)                                                                     #printando output do comando cmd
        break
    else:
        print("Invalid URL. Please try again.") 