import paramiko
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTreeView, QFileDialog, QMessageBox, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.ssh.connect(self.host, self.port, self.username, self.password)
            return True
        except Exception as e:
            QMessageBox.warning(None, 'Error', str(e))
            return False

    def list_directory(self, path):
        sftp = self.ssh.open_sftp()
        files = sftp.listdir_attr(path)
        sftp.close()
        return files

    def is_directory(self, path):
        sftp = self.ssh.open_sftp()
        try:
            file_attr = sftp.stat(path)
            return file_attr.st_mode & 0o40000 == 0o40000
        except FileNotFoundError:
            return False
        finally:
            sftp.close()

    def close(self):
        self.ssh.close()



class FileTree(QTreeView):
    def __init__(self, ssh_client, root_path):
        super().__init__()
        self.ssh_client = ssh_client
        self.root_path = root_path
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.load_directory(root_path)

    def print_item_content(self, parent_item, indent=0):
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            path = item.data()
            print(' ' * indent + item.text() + ' (' + path + ')')
            if item.hasChildren():
                self.print_item_content(item, indent + 4)


    def load_directory(self, path, parent_item=None):
        if parent_item is None:
            parent_item = self.model.invisibleRootItem()

        files = self.ssh_client.list_directory(path)
        for file_attr in files:
            print(f'file_attr.filename: {file_attr.filename}')
            item = QStandardItem(file_attr.filename)
            item.setData(path + '/' + file_attr.filename)
            if self.ssh_client.is_directory(path + '/' + file_attr.filename):
                print(f'okkk')
                self.load_directory(path + '/' + file_attr.filename, item)  # 递归调用
            else:
                print(f'no')

            parent_item.appendRow(item)
            print('--------------')
        # self.print_item_content(parent_item)

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            path = index.data()
            if self.ssh_client.is_directory(path):
                self.load_directory(path)