# --------------- Imports --------------- #
from pytube import YouTube
from tkinter import *
import requests
import os.path


# --------------- Funções --------------- #
def janela_de_sucesso(msg):
    def sair():
        janela_sucesso.destroy()
        janela_principal.destroy()

    janela_sucesso = Tk()  # Cria uma janela nova
    janela_sucesso.title("Sucesso")
    janela_sucesso.geometry("200x100")
    janela_sucesso.resizable(False, False)
    janela_sucesso.config(background="#F8F8FF")  # Fundo cinza-claro

    exclamacao = Label(janela_sucesso, text="✓", font=font_titulo, bg="#F8F8FF", fg="Black", bd=0)
    texto = Label(janela_sucesso, text=msg, font=font_padrao, bg="#F8F8FF", fg="#2F4F4F", bd=0)
    botao = Button(janela_sucesso, text="Fechar", font=font_padrao, bg="#6495ED", fg="White", bd=0,
                   activebackground="#87CEEB", command=sair)

    exclamacao.pack()
    texto.pack()
    botao.pack(pady=10)


def janela_de_erro(msg, msg_titulo):
    janela_sem_conexao = Tk()  # Cria uma janela nova
    janela_sem_conexao.title(msg_titulo)
    janela_sem_conexao.geometry("200x100")
    janela_sem_conexao.resizable(False, False)
    janela_sem_conexao.config(background="#F8F8FF")  # Fundo cinza-claro

    exclamacao = Label(janela_sem_conexao, text="!", font=font_titulo, bg="#F8F8FF", fg="Black", bd=0)
    texto = Label(janela_sem_conexao, text=msg, font=font_padrao, bg="#F8F8FF", fg="#2F4F4F", bd=0)

    exclamacao.pack()
    texto.pack()


def verificar_conexao():
    try:
        # Tente fazer uma solicitação HTTP para um site conhecido
        response = requests.get("https://www.google.com", timeout=5)
        # Se a solicitação for bem-sucedida (código de status 2xx), retorne True
        return response.status_code == 200
    except requests.ConnectionError:
        # Se houver um erro de conexão, retorne False
        return False


def baixar_video():
    if verificar_conexao():
        URL = url.get()
        # Verifica se a pasta "Vídeos" existe, caso não, irá criar uma
        if os.path.exists("Vídeos"):
            try:
                # Tenta criar um objeto YouTube e pega o vídeo na melhor resolução possível
                yt = YouTube(URL)
                stream = yt.streams.get_highest_resolution()
                # Realiza o download do video, o nome é o mesmo do vídeo original
                stream.download(output_path='Vídeos')
                janela_de_sucesso("Vídeo salvo com sucesso!")
            except:
                janela_de_erro("Link inválido!", "Link inválido")

        else:
            os.mkdir("Vídeos")
            try:
                yt = YouTube(URL)
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path='Vídeos')
                janela_de_sucesso("Vídeo salvo com sucesso!")
            except:
                janela_de_erro("Link inválido!", "Link inválido")
    else:
        janela_de_erro("Sem conexão com a internet!", "Sem conexão com a internet")


def baixar_audio():
    if verificar_conexao():
        URL = url.get()
        # Verifica se a pasta "Áudios" existe, caso não, irá criar uma
        if os.path.exists("Áudios"):
            try:
                # Tenta criar um objeto YouTube e pega o áudio na melhor resolução possível
                yt = YouTube(URL)
                stream = yt.streams.filter(only_audio=True).first()
                # Realiza o download do áudio, o nome é o mesmo do vídeo original
                stream.download(output_path='Áudios')
                janela_de_sucesso("Áudio salvo com sucesso!")
            except:
                janela_de_erro("Link inválido!", "Link inválido")
        else:
            os.mkdir("Áudios")
            try:
                yt = YouTube(URL)
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path='Áudios')
                janela_de_sucesso("Áudio salvo com sucesso!")
            except:
                janela_de_erro("Link inválido!", "Link inválido")
    else:
        janela_de_erro("Sem conexão com a internet!", "Sem conexão com a internet")


def on_entry_click(event):
    if url.get() == "Insira a URL":
        url.delete(0, "end")
        url.config(fg="black")


def on_focus_out(event):
    if url.get() == "":
        url.insert(0, "Insira a URL")
        url.config(fg="gray")


def on_key_press(event):
    if url.get() == "Insira a URL":
        url.delete(0, "end")
        url.config(fg="black")


# --------------- Janela principal --------------- #
janela_principal = Tk()
janela_principal.title("VidSaver")
janela_principal.geometry("315x150")
janela_principal.resizable(False, False)
janela_principal.config(background="#F8F8FF")  # Fundo branco

# --------------- Widgets --------------- #
font_titulo = ("Helvetica", 20, "bold")
font_padrao = ("Helvetica", 12)

cor_botao = "#6495ED"  # Azul-ardósia claro
cor_botao_apertado = "#87CEEB"  # Azul-ardósia claro mais claro

titulo = Label(janela_principal, text="VidSaver", font=font_titulo, bg="#F8F8FF", fg="#2F4F4F")  # Azul-ardósia escuro
url = Entry(janela_principal, width=50, fg="gray")
url.insert(0, "Insira a URL")
url.bind("<FocusIn>", on_entry_click)
url.bind("<FocusOut>", on_focus_out)
url.bind("<Key>", on_key_press)

video = Button(janela_principal, text="Baixar vídeo", font=font_padrao, bg=cor_botao, fg="White", bd=0,
               activebackground=cor_botao_apertado, command=baixar_video)
audio = Button(janela_principal, text="Baixar áudio", font=font_padrao, bg=cor_botao, fg="White", bd=0,
               activebackground=cor_botao_apertado, command=baixar_audio)

# --------------- Layout --------------- #
titulo.grid(row=1, column=2, columnspan=2, pady=(5, 5), padx=(5, 0), sticky="nsew")
url.grid(row=2, column=2, columnspan=2, pady=(5, 5), padx=(5, 0), sticky="nsew")
video.grid(row=3, column=1, columnspan=2, pady=(5, 5), padx=(5, 0), sticky="nsew")
audio.grid(row=3, column=3, columnspan=2, pady=(5, 5), padx=(5, 0), sticky="nsew")

# --------------- Executar janela --------------- #
janela_principal.mainloop()
