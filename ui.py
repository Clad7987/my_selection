import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

folder_path = os.path.join(os.path.dirname(__name__), "imgs")

# Função para criar a pasta
def criar_pasta():
    pasta_nome = tk.simpledialog.askstring("Nome da Pasta", "Digite o nome da nova pasta:")
    if pasta_nome:
        pasta_nome = os.path.join(folder_path, pasta_nome)
        try:
            os.makedirs(pasta_nome)
            messagebox.showinfo("Sucesso", f"Pasta '{pasta_nome}' criada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a pasta: {e}")
    atualizar_combos()

# Função para salvar a imagem
def salvar_imagem():
    global images, legend
    pasta_selecionada = combobox_pastas.get()
    if pasta_selecionada:
        # Escolher o caminho para salvar a imagem
        old_file_path = images[image_index]
        new_file_path = os.path.join(pasta_selecionada, os.path.basename(old_file_path))
        shutil.move(old_file_path, new_file_path)
        images.remove(old_file_path)
        legend.config(text=f"{image_index}/{len(images)}")

        update_image(image_index)


# Função para atualizar o combobox com as pastas disponíveis
def atualizar_combos():
    pastas = [os.path.join('imgs',pasta) for pasta in os.listdir("imgs") if os.path.isdir(f"imgs/{pasta}")]
    combobox_pastas['values'] = pastas
    if pastas:
        combobox_pastas.set(pastas[0])

# Criando a janela principal
root = tk.Tk()
root.title("Interface com Imagem")
root.geometry('800x600')

images = [os.path.join('imgs', image) for image in os.listdir("imgs") if not image.endswith('mp4') and not os.path.isdir(f'imgs/{image}') and 'part' not in image]

# Carregar a imagem que será exibida no label
def image_resize(img, tgt_w=800, tgt_h=500):
    org_w,org_h = img.size

    ratio_w = tgt_w / org_w
    ratio_h = tgt_h / org_h

    if ratio_w < ratio_h:
        new_w = tgt_w
        new_h = int(org_h * ratio_w)
    else:
        new_h = tgt_h
        new_w = int(org_w * ratio_h)

    return img.resize((new_w,new_h), Image.LANCZOS)

def mine_image_resize(img):
    org_w, org_h = img.size
    width, height = org_w, org_h
    tgt_w,tgt_h = 800,500

    if width < height:
        while (tgt_h < height):
            height -= (height*.2)

        ratio = height/org_h
        width = (width*ratio)
    else:
        while (tgt_w < width):
            width -= (width *.2)

        ratio = width/org_w
        height = (height*ratio)

    return img.resize((int(width), int(height)))

image_index = 114
imagem = Image.open(images[image_index])  # Substitua pelo caminho da sua imagem
imagem = image_resize(imagem)
imagem_tk = ImageTk.PhotoImage(imagem)

def update_image(index):
    global label_imagem
    img = Image.open(images[index])
    img = image_resize(img)
    img_tk = ImageTk.PhotoImage(img)
    label_imagem.config(image=img_tk)
    label_imagem.photo = img_tk

def change_image(index):
    global image_index, legend
    image_index += index
    legend.config(text=f'{image_index+1}/{len(images)}')
    update_image(image_index)

# Label para exibir a imagem
label_imagem = tk.Label(root, image=imagem_tk)
label_imagem.pack(padx=10, pady=10)


buttons_frame = tk.Frame(root)
buttons_frame.pack(side='bottom')

# Buttons
botao_next = tk.Button(buttons_frame, text=">", command=lambda: change_image(1))
botao_prev = tk.Button(buttons_frame, text="<", command=lambda: change_image(-1))
botao_criar_pasta = tk.Button(buttons_frame, text="Criar Pasta", command=criar_pasta)
botao_salvar_imagem = tk.Button(buttons_frame, text="Salvar Imagem", command=salvar_imagem)
combobox_pastas = ttk.Combobox(buttons_frame)
legend = tk.Label(buttons_frame, text=f"{image_index+1}/{len(images)}")

# Pack Buttons
botao_prev.pack(pady=5,padx=5,side='left')
botao_criar_pasta.pack(pady=5, padx=5, side='left')
botao_salvar_imagem.pack(pady=5, padx=5, side='left')
combobox_pastas.pack(pady=5, padx=5, side='left')
legend.pack(pady=5,padx=5,side='left')
botao_next.pack(pady=5,padx=5,side='left')

# Inicializar pastas disponíveis
atualizar_combos()

# Iniciar a interface
root.mainloop()

