import sys
import os
import shutil
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog, QHBoxLayout, QDialog, QDialogButtonBox, QLineEdit, QMessageBox

folder_path = os.path.join(os.path.dirname(__file__), "imgs")

# Função para redimensionar a imagem
def image_resize(img, tgt_w=800, tgt_h=500):
    org_w, org_h = img.width(), img.height()
    ratio_w = tgt_w / org_w
    ratio_h = tgt_h / org_h

    if ratio_w < ratio_h:
        new_w = tgt_w
        new_h = int(org_h * ratio_w)
    else:
        new_h = tgt_h
        new_w = int(org_w * ratio_h)

    return img.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface com Imagem")
        self.setGeometry(100, 100, 800, 600)

        self.images = [os.path.join('imgs', image) for image in os.listdir("imgs")
                       if not image.endswith('mp4') and not os.path.isdir(f'imgs/{image}') and 'part' not in image and 'Tumblr' in image]

        self.last_index_file = "last_index"
        if os.path.exists(self.last_index_file):
            with open(self.last_index_file) as file:
                self.image_index = int(file.readlines()[0].strip())
        else:
            self.image_index = 0
        self.img_label = QLabel(self)

        # Layout da janela principal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)


        # region Buttons 
        self.buttons = QVBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.setAlignment(Qt.AlignTop)

        self.folder_name = QLineEdit(self)
        self.folder_name.setPlaceholderText("Enter folder name")
        self.buttons.addWidget(self.folder_name)

        self.botao_criar_pasta = QPushButton("Criar Pasta", self)
        self.botao_criar_pasta.clicked.connect(self.criar_pasta)
        self.buttons.addWidget(self.botao_criar_pasta)

        self.reset_index = QPushButton("Reset Index", self)
        self.reset_index.clicked.connect(self.reset_index_func)
        self.buttons.addWidget(self.reset_index)

        self.combobox_pastas = QComboBox(self)
        self.combobox_pastas.currentIndexChanged.connect(self.on_pasta_change)
        self.buttons.addWidget(self.combobox_pastas)

        self.botao_salvar_imagem = QPushButton("Salvar Imagem", self)
        self.botao_salvar_imagem.clicked.connect(self.salvar_imagem)
        self.buttons.addWidget(self.botao_salvar_imagem)

        self.buttons.addStretch(1)

        self.layout.addLayout(self.buttons)
        # endregion

        self.layout.addStretch()

        # region Imagem
        self.image_layout = QVBoxLayout()
        self.layout.addLayout(self.image_layout)
        self.image_layout.addStretch(1)

        # Configura a exibição da imagem
        self.img = QImage(self.images[int(self.image_index)])
        self.img = image_resize(self.img)
        self.img_pixmap = QPixmap(self.img)
        self.img_label.setPixmap(self.img_pixmap)

        self.image_layout.addWidget(self.img_label, alignment=Qt.AlignCenter)
        self.image_layout.addStretch(1)

        # endregion

        # Layout de botões
        self.navButtons = QHBoxLayout()
        self.image_layout.addLayout(self.navButtons)

        self.botao_prev = QPushButton("<", self)
        self.botao_prev.clicked.connect(self.change_image_prev)
        self.navButtons.addWidget(self.botao_prev)

        self.botao_next = QPushButton(">", self)
        self.botao_next.clicked.connect(self.change_image_next)
        self.navButtons.addWidget(self.botao_next)

        self.layout.setStretch(0,1)
        self.layout.setStretch(1,1)

        self.atualizar_combos()

    def reset_index_func(self):
        with open('last_index', 'w') as file:
            file.write('0')
        self.image_index = 0
        self.update_image()
        QMessageBox.information(self,"Info","Index reseted!")

    def change_image_next(self):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.update_image()

    def change_image_prev(self):
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.images) - 1
        self.update_image()

    def update_image(self):
        self.img = QImage(self.images[self.image_index])
        self.img = image_resize(self.img)
        self.img_pixmap = QPixmap(self.img)
        self.img_label.setPixmap(self.img_pixmap)


    def criar_pasta(self):
        try:
            caminho = self.folder_name.text().strip()
            destino = os.path.join("imgs", caminho)
            os.makedirs(destino, exist_ok=True)
            QMessageBox.information(self,"Info","Folder Created")
            self.atualizar_combos()

            curr_index = self.pastas.index(destino)

            self.combobox_pastas.setCurrentIndex(curr_index)
        except Exception as e:
            QMessageBox.critical(self, "Error",f"Folder not created {e}")
            print(e)

    def salvar_imagem(self):
        pasta_selecionada = self.combobox_pastas.currentText()
        if pasta_selecionada:
            old_file_path = self.images[self.image_index]
            new_file_path = os.path.join(pasta_selecionada, os.path.basename(old_file_path))
            shutil.move(old_file_path, new_file_path)
            print(f"Imagem movida para: {new_file_path}")
            self.images.remove(old_file_path)
            self.update_image()

    def atualizar_combos(self):
        self.pastas = [os.path.join('imgs', pasta) for pasta in os.listdir("imgs")
                  if os.path.isdir(os.path.join('imgs', pasta))]
        self.combobox_pastas.clear()
        self.combobox_pastas.addItems(self.pastas)

    def on_pasta_change(self, index):
        pasta_selecionada = self.combobox_pastas.currentText()
        print(f"Pasta selecionada: {pasta_selecionada}")

    def set_system_style(self):
        QApplication.setStyle("Fusion")
        palette = QApplication.palette()
        palette.setColor(palette.window, Qt.black)
        palette.setColor(palette.windowText, Qt.white)
        QApplication.setPalette(palette)

    def closeEvent(self,event):
        with open(self.last_index_file, 'w') as file:
            file.write(f'{self.image_index}')
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
