
import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QMainWindow, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar,
    QFileDialog, QProgressBar
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from deepfaceresult import DeepFaceResults



class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Kullanıcı Girişi')
        self.setGeometry(200, 200, 300, 150)

        self.label_username = QLabel('Username:', self)
        self.label_username.move(20, 20)
        
        self.label_password = QLabel('Password:', self)
        self.label_password.move(20, 60)

        self.input_username = QLineEdit(self)
        self.input_username.move(120, 20)

        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.move(120, 60)

        # Login button
        self.label_pushbutton = QPushButton('Login', self)
        self.label_pushbutton.move(20, 100)
        self.label_pushbutton.clicked.connect(self.check_login)

    def check_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == 'root' and password == 'kali':
            self.home_page = HomePage()
            self.home_page.show()
            self.close()
        else:
            self.show_error_message('Incorrect username or password!')

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Error')
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.exec_()


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Vidgen - Ana Sayfa')
        self.setGeometry(200, 200, 440, 500)
        
        self.widget = QWidget()
        layout = QVBoxLayout()


        self.file_path = '...'
        self.stat = '...'
        self.stat_loading = 'in progress'
        self.result_deepface = 'scanning'
        self.range_of_row = -1


        bar = QMenuBar(self.widget)
        file_menu = bar.addMenu('File')
        file_menu.addAction(QAction('File', self))
        file_menu.addAction(QAction('Result', self))
        file_menu.addAction(QAction('Info', self))

        layout.addWidget(bar)


        self.model = QStandardItemModel()
        self.model.setRowCount(9)
        self.model.setColumnCount(3)
        

        table_view = QTableView()
        table_view.setModel(self.model)
        layout.addWidget(table_view)


        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)
        
        self.stop_button = QPushButton("Stop", self)
        
        layout.addWidget(self.stop_button)


        self.file_label = QLabel(f"Seçilen Dosya: {self.file_path}", self)
        layout.addWidget(self.file_label)


        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        self.reload_table("...")

        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        
        if hasattr(self, 'data_loader') and self.data_loader.isRunning():
            self.data_loader.stop() 
        event.accept()
        
    def open_file_dialog(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Video Dosyaları (*.mp4 *.avi *.mkv)")
        
        if self.file_path:
            self.range_of_row += 1
            self.file_label.setText(f"Seçilen Dosya: {self.file_path}")
            self.reload_table(self.result_deepface)
            
            print(self.range_of_row)
            self.start_data_loader()

    def start_data_loader(self):
        self.file_path = self.file_path.replace("/", "//")
        self.data_loader = GetResultDeepface(self.file_path)
        self.data_loader.signal.connect(self.reload_table)
        self.data_loader.progress_signal.connect(self.update_progress)
        self.data_loader.start()
        self.stop_button.clicked.connect(self.stop_button_using)
    
    def stop_button_using(self):
        self.data_loader.stop()
        self.reload_table('stopped')
    
    def reload_table(self, result_deepface):
        if self.range_of_row == 9:
            for row in range(9):
                for column in range(3):
                    item = QStandardItem("")
                    self.model.setItem(row, column, item)
            self.range_of_row = 0
        

        item = QStandardItem(f'{os.path.basename(self.file_path)}')
        status_item = QStandardItem(self.stat)
        status_loading = QStandardItem(self.stat_loading)

        if "fake" in result_deepface.lower():
            self.stat = result_deepface
        elif "real" in result_deepface.lower():
            self.stat = result_deepface
        elif "stopped" in result_deepface.lower():
            self.stat = 'Stopped'
            
            
        print(self.range_of_row)
        status_item = QStandardItem(self.stat)
        status_loading = QStandardItem(self.stat_loading)
        self.model.setItem(self.range_of_row, 0, item)
        self.model.setItem(self.range_of_row, 1, status_loading)
        self.model.setItem(self.range_of_row, 2, status_item)
        self.progress_bar.setValue(100)
        self.stat = 'scanning...'
        self.stat_loading = 'in progress'

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)


class GetResultDeepface(QThread):
    signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.running = True

    def run(self):
        try:
            if self.running:
                result = DeepFaceResults().start(self.path, self.progress_signal)
                self.signal.emit(str(result))
        except Exception as e:
            self.signal.emit(f"Hata: {str(e)}")

    def stop(self):
        self.running = False
        self.terminate()
        self.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginApp()
    login_window.show()
    sys.exit(app.exec_())
