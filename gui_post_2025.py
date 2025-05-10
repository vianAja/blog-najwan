import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QListWidget, QPushButton, QFileDialog, QMessageBox, QLabel, QScrollArea, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

MARKDOWN_DIR = "_posts"
if not os.path.exists(MARKDOWN_DIR):
    os.makedirs(MARKDOWN_DIR)

class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Editor with Viewer")
        self.setGeometry(100, 100, 1000, 600)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.save_button = QPushButton("Save Markdown")
        self.save_button.clicked.connect(self.save_markdown)

        left_layout.addWidget(self.editor)
        left_layout.addWidget(self.save_button)

        self.file_list = QListWidget()
        self.file_list.setFixedWidth(250)
        self.file_list.itemClicked.connect(self.open_markdown_dialog)

        self.update_file_list()

        layout.addLayout(left_layout)
        layout.addWidget(self.file_list)

        self.setLayout(layout)

    def save_markdown(self):
        text = self.editor.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Markdown File", MARKDOWN_DIR, "Markdown Files (*.md)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            self.update_file_list()
            QMessageBox.information(self, "Saved", f"File saved as {filename}")

    def update_file_list(self):
        self.file_list.clear()
        for fname in os.listdir(MARKDOWN_DIR):
            if fname.endswith(".md"):
                self.file_list.addItem(fname)

    def open_markdown_dialog(self, item):
        reply = QMessageBox.question(self, "Update?", "Apakah mau update?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            filepath = os.path.join(MARKDOWN_DIR, item.text())
            self.show_markdown_view(filepath)

    def show_markdown_view(self, filepath):
        viewer = MarkdownViewer(filepath)
        viewer.exec_()

class MarkdownViewer(QMessageBox):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("Markdown Viewer")
        self.setMinimumSize(800, 600)

        scroll = QScrollArea()
        content_widget = QWidget()
        layout = QVBoxLayout()

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = re.split(r'\n-{3,}\n', content)  # Pisahkan antar '---' garis

        for block in blocks:
            self.render_block(block.strip(), layout)

        content_widget.setLayout(layout)
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)

        layout_main = QVBoxLayout()
        layout_main.addWidget(scroll)
        self.setLayout(layout_main)

    def render_block(self, block, layout):
        if not block.strip():
            return

        # Tampilkan Judul jika ada
        title_match = re.match(r'### (.*)', block)
        if title_match:
            title = title_match.group(1)
            label = QLabel(title)
            label.setFont(QFont('Arial', 14, QFont.Bold))
            layout.addWidget(label)

        # Deteksi blok kode
        code_blocks = re.findall(r'```(.*?)```', block, re.DOTALL)
        text_only = re.sub(r'```.*?```', '', block, flags=re.DOTALL)

        if text_only.strip():
            text_label = QLabel(text_only.strip())
            text_label.setWordWrap(True)
            text_label.setStyleSheet("background-color: #f4f4f4; padding: 6px; border: 1px solid #ccc;")
            layout.addWidget(text_label)

        for code in code_blocks:
            code_label = QLabel(code.strip())
            code_label.setFont(QFont('Courier', 10))
            code_label.setStyleSheet("background-color: #222; color: #0f0; padding: 6px;")
            code_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            layout.addWidget(code_label)

        # Deteksi dan tampilkan gambar
        img_matches = re.findall(r'!\[.*?\]\((.*?)\)', block)
        for img_path in img_matches:
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
                layout.addWidget(image_label)
            else:
                err = QLabel(f"[Gambar tidak ditemukan: {img_path}]")
                layout.addWidget(err)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec_())
