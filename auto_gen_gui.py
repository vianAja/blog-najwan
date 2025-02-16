import sys
import os
import markdown
import shutil
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame,
    QHBoxLayout, QTextEdit, QLabel, QFileDialog, QComboBox, QMessageBox, QListWidget, QTextBrowser,
    QSizePolicy, 
)
from PyQt5.QtGui import (QPixmap, QImageReader, QImage) 
from PyQt5.QtCore import Qt

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()

class ScrollableEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.full_path = os.getcwd()
        self.initUI()
        self.tanggal = datetime.datetime.now().strftime('%Y-%m-%d')
        self.author = 'Najwan Octavian Gerrard'
        self.tags = []
        self.template_code =  '''
- {}
  ```{}
  {}
  ```
  ---'''
        self.template_header = '''---
layout: post
title: {}
subtitle: {}
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://ant.ncc.asia/wp-content/uploads/2024/05/docker.png
share-img: /assets/img/wallpaper2.png
tags: {}
author: {}
---'''
        self.template_gambar = '''
- {}
  ![{}](../assets/images/{}{})
---'''
    
    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Bagian kiri (Editor Markdown)
        self.left_panel = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout.setSpacing(0)
        
        self.judul = QTextEdit()
        self.judul.setPlaceholderText("Masukkan Judul Blog")
        self.judul.setFixedHeight(40)
        
        self.add_box_button = QPushButton("Tambah Box")
        self.add_box_button.clicked.connect(self.add_box)
        
        self.run_button = QPushButton("Run Auto Generate File")
        self.run_button.clicked.connect(self.auto_gen)
        
        self.left_panel.addWidget(self.judul)
        self.left_panel.addWidget(self.add_box_button)
        self.left_panel.addWidget(self.scroll_area)
        self.left_panel.addWidget(self.run_button)
        
        # Bagian kanan (Daftar file markdown & viewer)
        self.right_panel = QVBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(200)
        self.file_list.itemClicked.connect(self.confirm_edit)
        
        self.markdown_viewer = QTextBrowser()
        
        self.right_panel.addWidget(QLabel("Daftar File Markdown"))
        self.right_panel.addWidget(self.file_list)
        self.right_panel.addWidget(QLabel("Preview Markdown"))
        self.right_panel.addWidget(self.markdown_viewer)
        
        self.layout.addLayout(self.left_panel, 2)
        self.layout.addLayout(self.right_panel, 1)
        
        self.load_markdown_files()
        
    def load_markdown_files(self):
        self.file_list.clear()
        md_folder = os.path.join(self.full_path, '_posts')
        if not os.path.exists(md_folder):
            os.makedirs(md_folder)
        
        for file_name in os.listdir(md_folder):
            if file_name.endswith(".md"):
                self.file_list.addItem(file_name)

    def confirm_edit(self, item):
        reply = QMessageBox.question(self, "Konfirmasi", "Apakah ingin mengedit file ini?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.load_markdown_content(item.text())

    def clear_boxes(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_markdown_content(self, filename):
        file_path = os.path.join(self.full_path, '_posts', filename)
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        self.judul.setText(filename.replace('.md', '').split('-')[-1].replace('-', ' '))
        
        self.clear_boxes()
        
        for i, line in enumerate(lines):
            if line.startswith("- "):
                text = line.strip().lstrip('- ')
                print(text)
                if "```" in lines[i+1] and i+1 < len(lines):
                    no_index = i+1
                    while True:
                        no_index = no_index + 1 
                        if '```' not in lines[no_index+1]: pass
                        else: break
                    code_script = lines[i+2:no_index+1]
                    print(code_script)
                    print()
                    self.add_box(
                        text=text,
                        box=code_script,
                        type_box=0
                    )
                    
                elif lines[i+1].startswith('  !['):
                    path_gambar = lines[i+1].split('(')[-1].replace('..', '').replace(')', '').split('/')
                    path_gambar = os.path.abspath(os.path.join(*path_gambar))
                    print(path_gambar)
                    print()
                    self.add_box(
                        text=text,
                        box=path_gambar,
                        type_box=1
                    )
            
    def view_markdown(self, item):
        file_path = os.path.join(self.full_path, '_posts', item.text())
        with open(file_path, "r", encoding="utf-8") as file:
            md_text = file.read()
            html = markdown.markdown(md_text)
            self.markdown_viewer.setHtml(html)
    
    def add_box(self, **args):
        box_frame = QFrame()
        box_frame.setFrameShape(QFrame.StyledPanel)
        box_layout = QVBoxLayout(box_frame)
        box_frame.setFrameShape(QFrame.StyledPanel)
        box_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        combo_box = NoScrollComboBox()
        combo_box.addItems(["Script", "Images"])
        
        text1 = QTextEdit()
        text1.setPlaceholderText("Masukkan Perintah")
        text1.setFixedHeight(60)
        
        text2 = QTextEdit()
        text2.setPlaceholderText("Masukkan Code nya")
        text2.setFixedHeight(100)
        
        image_label = QLabel()
        image_label.hide()
        
        upload_button = QPushButton("Pilih Gambar")
        upload_button.hide()
        
        def toggle_input(index):
            if index == 0:
                text2.show()
                image_label.hide()
                upload_button.hide()
            else:
                text2.hide()
                image_label.show()
                upload_button.show()
        
        combo_box.currentIndexChanged.connect(toggle_input)
        
        def upload_image():
            file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if file_path or os.path.exists(file_path):
                pixmap = QPixmap(file_path)
                image_label.setPixmap(pixmap)
                image_label.file_path = file_path
                max_width = 800
                max_height = 600
                scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
                image_label.adjustSize()
            
        upload_button.clicked.connect(upload_image)
        
        remove_button = QPushButton("Hapus")
        def remove_box():
            self.scroll_layout.removeWidget(box_frame)
            box_frame.deleteLater()
        remove_button.clicked.connect(remove_box)
        
        box_layout.addWidget(combo_box)
        box_layout.addWidget(text1)
        box_layout.addWidget(text2)
        box_layout.addWidget(image_label)
        box_layout.addWidget(upload_button)
        box_layout.addWidget(remove_button)
        
        box_frame.combo_box = combo_box
        box_frame.text1 = text1
        box_frame.text2 = text2
        box_frame.image_label = image_label
        
        self.scroll_layout.addWidget(box_frame)
        if args.items():
            type_box = args['type_box']
            text1.setText(args['text'])
            if type_box == 0:
                print(args['box'])
                text2.setText(args['box'][0])
            elif type_box == 1:
                pixmap = QPixmap(args['box'])
                image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
                image_label.file_path = args['box']
                image_label.show()
            toggle_input(type_box)
        else:
            toggle_input(combo_box.currentIndex())
    
    def gen_file_md(self, judul ,data):
        name_file = judul.lower().replace(' ', '-')+'.md' if ' ' in judul else judul.lower()+'.md'
        file = os.path.join(self.full_path, '_posts', self.tanggal+'-'+name_file)
        
        ## untuk memindahkan file gambar agar sesuai
        path_gambar = os.path.join(self.full_path, 'assets', 'images')
        path = os.path.join(path_gambar, name_file.replace('.md', ''))
        if os.path.exists(path) != True:
            os.mkdir(path)
        
        ## write file .md
        with open(file, 'w') as f:
            f.write(self.template_header.format(
                judul,
                judul,
                self.tanggal,
                ", ".join(self.tags),
                self.author
            ))
            for isi in data:
                judul_perintah = isi['judul']
                if isi['type'] == 'script':
                    isi_perintah = isi['isi']
                    f.write(self.template_code.format(
                        judul_perintah,
                        'bash',
                        '\n  '.join(isi_perintah) if isinstance(isi_perintah, list) else isi_perintah
                    ))
                    f.write('\n')
                elif isi['type'] == 'image':
                    ## untuk mengisi di file .md
                    path_img_in_file = isi['isi'].split('/')[-1]
                    f.write(self.template_gambar.format(
                        judul_perintah,
                        'name img',
                        name_file.split('.')[0],
                        '/'+path_img_in_file
                    ))
                    if os.path.exists(isi['isi']) != True:
                        shutil.move(isi['isi'], os.path.join(path,path_img_in_file))
        QMessageBox.about(self, 'Generate File' ,'sudah berhasil generate file markdown untuk blog')
        
    def auto_gen(self):
        judul = self.judul.toPlainText()
        if not judul:
            QMessageBox.warning(self, "Error", "Judul harus diisi!")
            return
        data = []
        for i in range(self.scroll_layout.count()):
            box_frame = self.scroll_layout.itemAt(i).widget()
            if box_frame:
                combo_index = box_frame.combo_box.currentIndex()
                text1 = box_frame.text1.toPlainText()
                if combo_index == 0:
                    text2 = box_frame.text2.toPlainText()
                    data.append({'type': 'script', 'judul': text1, 'isi': text2})
                else:
                    image_path = getattr(box_frame.image_label, "file_path", "")
                    data.append({'type': 'image', 'judul': text1, 'isi': image_path})
        if not data:
            QMessageBox.warning(self, "Error", "Minimal satu box harus diisi!")
            return
        self.gen_file_md(judul, data)
        self.judul.clear()
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.load_markdown_files()
    
if __name__ == '__main__':
    try:
        os.system('cls')
        print('Apps is running')
        app = QApplication(sys.argv)
        window = ScrollableEditor()
        window.setWindowTitle("Markdown Editor with Viewer")
        window.resize(1200, 800)
        window.show()
        sys.exit(app.exec_())
        print('Apps Stopped')
    except KeyboardInterrupt:
        print('Apps Stopped')
    except Exception as e:
        print('Error:', str(e))