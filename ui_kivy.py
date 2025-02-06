import os
import shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage
from PIL import Image as PILImage

# Definir a pasta base
folder_path = os.path.join(os.path.dirname(__file__), "imgs")

# Função para redimensionar a imagem
def image_resize(img, tgt_w=800, tgt_h=500):
    org_w, org_h = img.size
    ratio_w = tgt_w / org_w
    ratio_h = tgt_h / org_h

    if ratio_w < ratio_h:
        new_w = tgt_w
        new_h = int(org_h * ratio_w)
    else:
        new_h = tgt_h
        new_w = int(org_w * ratio_h)

    return img.resize((new_w, new_h), PILImage.LANCZOS)

class MeuApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Lista de imagens
        self.images = [os.path.join('imgs', image) for image in os.listdir("imgs")
                       if not image.endswith('mp4') and not os.path.isdir(f'imgs/{image}') and 'part' not in image]

        self.image_index = 0

        # Exibir a primeira imagem
        self.img = PILImage.open(self.images[self.image_index])
        self.img = image_resize(self.img)
        self.img_tk = CoreImage(self.images[self.image_index]).texture
        self.image_widget = Image(texture=self.img_tk)

        self.layout.add_widget(self.image_widget)

        # Layout para botões
        self.buttons_layout = BoxLayout(size_hint=(1, 0.2))
        self.botao_prev = Button(text="<", on_press=self.change_image_prev)
        self.botao_next = Button(text=">", on_press=self.change_image_next)
        self.botao_criar_pasta = Button(text="Criar Pasta", on_press=self.criar_pasta)
        self.botao_salvar_imagem = Button(text="Salvar Imagem", on_press=self.salvar_imagem)

        self.buttons_layout.add_widget(self.botao_prev)
        self.buttons_layout.add_widget(self.botao_criar_pasta)
        self.buttons_layout.add_widget(self.botao_salvar_imagem)
        self.layout.add_widget(self.buttons_layout)

        # Dropdown para escolher a pasta
        self.dropdown = DropDown()
        self.combobox_pastas = Button(text='Escolha a pasta', size_hint=(None, None))
        self.combobox_pastas.bind(on_release=self.dropdown.open)

        # Adicionando as pastas ao dropdown
        self.atualizar_combos()

        # Layout de navegação e pasta
        self.dropdown.add_widget(self.combobox_pastas)
        self.layout.add_widget(self.dropdown)

        return self.layout

    def change_image_next(self, instance):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.update_image()

    def change_image_prev(self, instance):
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.images) - 1
        self.update_image()

    def update_image(self):
        img = PILImage.open(self.images[self.image_index])
        img = image_resize(img)
        img_tk = CoreImage(self.images[self.image_index]).texture
        self.image_widget.texture = img_tk

    def criar_pasta(self, instance):
        # Função para criar pasta
        popup = Popup(title="Criar Pasta", content=FileChooserIconView(), size_hint=(0.8, 0.8))
        filechooser = FileChooserIconView()
        filechooser.path = folder_path
        filechooser.bind(on_selection=lambda *args: self.criar_pasta_selecionada(filechooser.selection))
        popup.content = filechooser
        popup.open()

    def criar_pasta_selecionada(self, selection):
        if selection:
            pasta_nome = os.path.basename(selection[0])
            pasta_destino = os.path.join(folder_path, pasta_nome)
            try:
                os.makedirs(pasta_destino, exist_ok=True)
                print(f"Pasta '{pasta_destino}' criada com sucesso!")
            except Exception as e:
                print(f"Erro ao criar pasta: {e}")

    def salvar_imagem(self, instance):
        pasta_selecionada = self.combobox_pastas.text
        if pasta_selecionada:
            old_file_path = self.images[self.image_index]
            new_file_path = os.path.join(pasta_selecionada, os.path.basename(old_file_path))
            #shutil.move(old_file_path, new_file_path)
            print(f"Imagem movida para: {new_file_path}")
            #self.images.remove(old_file_path)
            #self.update_image()

    def atualizar_combos(self):
        pastas = [os.path.join('imgs', pasta) for pasta in os.listdir("imgs")
                  if os.path.isdir(os.path.join('imgs', pasta))]
        for pasta in pastas:
            pasta_button = Button(text=os.path.basename(pasta), size_hint_y=None, height=44)
            pasta_button.bind(on_release=lambda btn, pasta=pasta: self.combobox_pastas.set_text(pasta))
            self.dropdown.add_widget(pasta_button)

if __name__ == '__main__':
    MeuApp().run()
