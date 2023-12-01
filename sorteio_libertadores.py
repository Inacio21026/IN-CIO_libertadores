import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def toggle_fullscreen(event=None):
    state = not root.attributes('-fullscreen')
    root.attributes('-fullscreen', state)
    if state:
        # Criar uma nova janela simulando a tela cheia com a cor de fundo desejada
        fullscreen_window = tk.Toplevel(root)
        fullscreen_window.attributes('-fullscreen', True)
        fullscreen_window.configure(bg='blue')  # Cor de fundo desejada ao entrar em tela cheia
        fullscreen_window.bind('<Escape>', lambda e: fullscreen_window.destroy())  # Fechar ao pressionar ESC
    else:
        root.attributes('-fullscreen', False)

# Criar janela principal
root = tk.Tk()
root.title("Sorteio da Libertadores")
root.configure(bg='green')  # Definir cor de fundo padrão

# Configurar o tema da ttk explicitamente
style = ttk.Style(root)
style.configure('PaginaInicial.TFrame', background='green')  # Verde
style.configure('PaginaSorteio.TFrame', background='#800020')  # Grená

# Carregar a imagem do logo
image = Image.open("logo.png")
photo = ImageTk.PhotoImage(image)

# Função para iniciar o processo de seleção de times
def iniciar_selecao():
    mostrar_tela_selecao()

# Função para mostrar as instruções iniciais
def mostrar_instrucoes():
    frame_instrucoes.pack()
    frame_selecao.pack_forget()

# Função para mostrar a tela de seleção de times
def mostrar_tela_selecao():
    frame_instrucoes.pack_forget()
    frame_selecao.pack()
    frame_titulo.pack_forget()

# Definir o número de times por país e os times
times_por_pais = {
    "Brasil": ["Flamengo", "Palmeiras", "Santos", "São Paulo", "Fluminense", "Corinthians", "Vasco", "Botafogo", "Cruzeiro", "Atlético Mineiro", "Gremio", "Internacional", "Bahia", "Fortaleza", "Athletico Paranaense"],
    "Argentina": ["River Plate", "Boca Juniors", "Independiente", "Racing", "San Lorenzo", "Lanus", "Newells Old Boys", "Argentinos Juniors", "Defensa y Justicia", "Huracan", "Godoy Cruz", "Estudiantes"],
    "Chile": ["Colo-Colo", "Universidad de Chile", "Nublense", "Magallanes", "Universidad Catolica", "Palestino"],
    "Uruguai": ["Penarol", "Nacional", "Liverpool", "Fenix", "Defensor SC"],
    "Paraguai": ["Cerro Porteno", "Libertad", "Guarani", "Olimpia", "Tacuary"],
    "Bolívia": ["The Strongest", "Bolivar", "Nacional Potosí", "Oriente Petrolero", "Jorge Wilstermann"],
    "Colômbia": ["Atletico Nacional", "Santa Fe", "America de Cali", "Tolima", "Independiente Medellin", "Milonarios", "Deportivo Cali", "Junior Barranquila"],
    "Equador": ["Barcelona SC", "LDU", "Delfin", "Independiente del Valle", "Emelec", "Aucas", "Universidad Catolica"],
    "Peru": ["Sporting Cristal", "Melgar", "Alianza Lima", "Universitario", "Cesar Vallejo"],
    "Venezuela": ["Carabobo", "Caracas", "Metropolitanos", "Monagas"]
}

# Dicionário para armazenar os times selecionados por país
times_selecionados = {pais: [] for pais in times_por_pais.keys()}

# Dicionário para armazenar os grupos e os times sorteados
grupos_e_times = {}

# Função para atualizar a lista de times disponíveis quando um país é selecionado
def atualizar_lista_times(event):
    pais = combo_paises.get()
    combo_times.set("")  # Limpar seleção de time
    combo_times["values"] = times_por_pais[pais]

    # Atualizar a imagem da bandeira do país selecionado
    if pais in imagens_bandeiras:
        bandeira_label.config(image=imagens_bandeiras[pais])
        bandeira_label.image = imagens_bandeiras[pais]
    else:
        # Se não houver uma imagem de bandeira para o país, exiba uma imagem em branco
        bandeira_em_branco = Image.open("bandeiras/em_branco.png")  
        bandeira_em_branco = bandeira_em_branco.resize((30, 20), Image.BILINEAR)
        imagem_em_branco = ImageTk.PhotoImage(bandeira_em_branco)
        bandeira_label.config(image=imagem_em_branco)
        bandeira_label.image = imagem_em_branco

# Função para adicionar time selecionado
def adicionar_time():
    pais = combo_paises.get()
    selected_times = combo_times.get()
    selected_times = selected_times.split(',')  # Dividir os tempos selecionados por vírgula
    
     # Verificar se o usuário já escolheu 8 times deste país
    if len(times_selecionados[pais]) + len(selected_times) > 8:
        tk.messagebox.showerror("Limite de Times", "Você já escolheu o limite máximo de 8 times deste país.")
    else:
        for time in selected_times:
            if time.strip() not in times_selecionados[pais]:
                times_selecionados[pais].append(time.strip())

        atualizar_listbox()
        update_contagem()  

# Função para remover time selecionado
def remover_time():
    pais = combo_paises.get()
    selecionados = listbox_times.curselection()
    
    for index in selecionados:
        time = listbox_times.get(index)
        times_selecionados[pais].remove(time)
    
    atualizar_listbox()
    update_contagem()  

# Função para atualizar o Listbox
def atualizar_listbox():
    listbox_times.delete(0, tk.END)
    pais = combo_paises.get()
    for time in times_selecionados[pais]:
        listbox_times.insert(tk.END, time)

# Função para atualizar a contagem de times escolhidos
def update_contagem():
    contagem_text.config(state="normal")
    contagem_text.delete(1.0, tk.END)
    
    for pais, times in times_selecionados.items():
        contagem_text.insert(tk.END, f'{pais}: {len(times)} times selecionados\n')
    
    total_selecionados = sum(len(times) for times in times_selecionados.values())
    contagem_text.insert(tk.END, f'Total: {total_selecionados} de 32 times selecionados\n')
    
    contagem_text.config(state="disabled")

# Função para realizar o sorteio
def realizar_sorteio():
    # Verificar se foram selecionados 32 times
    total_selecionados = sum(len(times) for times in times_selecionados.values())
    
    if total_selecionados != 32:
        resultado_text.config(state="normal")
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Selecione exatamente 32 times para realizar o sorteio.")
        resultado_text.config(state="disabled")
    else:
        # Limpar grupos e times sorteados
        grupos_e_times = {f"Grupo {chr(65 + i)}": [] for i in range(8)}

        # Realizar o sorteio
        times_ordenados = []
        for pais, times in times_selecionados.items():
            random.shuffle(times)
            times_ordenados.extend([(pais, time) for time in times])
        
        for i, (pais, time) in enumerate(times_ordenados):
            grupo = f"Grupo {chr(65 + i % 8)}"
            grupos_e_times[grupo].append(f"{pais}: {time}")

        # Exibir o resultado na interface
        resultado_text.config(state="normal")
        resultado_text.delete(1.0, tk.END)
        for grupo, times in grupos_e_times.items():
            resultado_text.insert(tk.END, f'{grupo}:\n')
            for time in times:
                resultado_text.insert(tk.END, f'  - {time}\n')
        resultado_text.config(state="disabled")

# Carregar imagens das bandeiras
imagens_bandeiras = {}  # Dicionário para armazenar as imagens das bandeiras

# Iterar sobre os países e verificar se há uma imagem de bandeira correspondente
for pais in times_por_pais.keys():
    bandeira_path = os.path.join("bandeiras", f"{pais}.png")
    if os.path.isfile(bandeira_path):
        imagem_bandeira = Image.open(bandeira_path)
        imagem_bandeira = imagem_bandeira.resize((30, 20), Image.BILINEAR)
        imagens_bandeiras[pais] = ImageTk.PhotoImage(imagem_bandeira)


# Criar estruturas para organizar as telas
frame_selecao = ttk.Frame(root)
frame_instrucoes = ttk.Frame(root)

# Criar estruturas para organizar as telas
frame_selecao = ttk.Frame(root, style='PaginaSorteio.TFrame')  # Grená
frame_instrucoes = ttk.Frame(root, style='PaginaInicial.TFrame')  # Verde

# Tela de instruções iniciais
frame_instrucoes.pack()

# Título com imagem
frame_titulo = ttk.Frame(frame_instrucoes)
frame_titulo.pack(pady=10)
titulo_label = ttk.Label(frame_titulo, text="Bem-vindo ao Sorteio da Libertadores", image=photo, compound="left", font=("Helvetica", 16, "bold"))
titulo_label.pack()

# Adicionar mensagem e escudo
mensagem_label = ttk.Label(frame_titulo, text="Atual Campeão: FLUMINENSE", font=("Helvetica", 12))
mensagem_label.pack(side=tk.LEFT, padx=10)  

# Adicionar escudo 
escudo_fluminense = Image.open("fluminense.png")  
escudo_fluminense = escudo_fluminense.resize((30, 30), Image.BILINEAR)
imagem_escudo = ImageTk.PhotoImage(escudo_fluminense)
escudo_label = ttk.Label(frame_titulo, image=imagem_escudo)
escudo_label.image = imagem_escudo
escudo_label.pack(side=tk.LEFT)
instrucoes_label = ttk.Label(frame_instrucoes, text="Instruções:\n\n1. Escolha até no máximo 8 times por país, não é possível selecionar mais de 8 times por país.\n2. Selecione exatamente 32 times para realizar o sorteio.\n3. Para selecionar mais de um time por vez, escreva na aba dos times, logo após selecionar o país, os nomes dos times desejados, separando-os por vírgulas.\n4. É possível escrever o nome de times que não estão na aba principal dos times, nesta aba estão os times mais conhecidos de cada país para o usuário se situar.\n5. Clique em 'Iniciar Seleção' para começar.")
instrucoes_label.pack()

# Botão para iniciar seleção
iniciar_selecao_button = ttk.Button(frame_instrucoes, text="Iniciar Seleção", command=iniciar_selecao)
iniciar_selecao_button.pack(pady=10)

# Combobox para seleção de países e times
combo_paises = ttk.Combobox(frame_selecao, values=list(times_por_pais.keys()))
combo_paises.pack(pady=10)
combo_paises.bind("<<ComboboxSelected>>", atualizar_lista_times)

combo_times = ttk.Combobox(frame_selecao, values=[])
combo_times.pack(pady=10)

# Frame para a imagem da bandeira
frame_bandeira = ttk.Frame(frame_selecao)
frame_bandeira.pack()
bandeira_label = ttk.Label(frame_bandeira)
bandeira_label.pack()

# Listbox para exibir times selecionados
listbox_times = tk.Listbox(frame_selecao, selectmode=tk.MULTIPLE, height=10)
listbox_times.pack()

# Botões para adicionar e remover times
adicionar_time_button = ttk.Button(frame_selecao, text="Adicionar Time", command=adicionar_time)
remover_time_button = ttk.Button(frame_selecao, text="Remover Time", command=remover_time)
adicionar_time_button.pack()
remover_time_button.pack()

# Botão para realizar o sorteio
btn_sorteio = ttk.Button(frame_selecao, text="Realizar Sorteio", command=realizar_sorteio)
btn_sorteio.pack(pady=10)

# Caixa de texto para exibir o resultado
resultado_text = tk.Text(frame_selecao, wrap=tk.WORD, width=40, height=20, state="disabled")
resultado_text.pack()

# Caixa de texto para exibir a contagem de times escolhidos
contagem_text = tk.Text(frame_selecao, wrap=tk.WORD, width=40, height=5, state="disabled")
contagem_text.pack()

root.bind('<F11>', toggle_fullscreen)

# Exibir a interface gráfica
root.mainloop()