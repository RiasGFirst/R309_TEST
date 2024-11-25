#https://github.com/RiasGFirst/R309_TEST

import socket
import threading
import time

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import sys

clients = []
max_client = 0
server_start = False
server = None


def reception_message(client_sock, server):
    while True:
        try:
            message = client_sock.recv(1024).decode()
        except ConnectionResetError:
            print("Erreur client")
            client_sock.close()
            clients.remove(client_sock)
        except ConnectionAbortedError:
            client_sock.close()
            clients.remove(client_sock)
        else:
            print(message)
            client_sock.send("".encode())
            if message == "bye":
                print("Client deconnecter")
                client_sock.send("bye".encode())
                clients.remove(client_sock)
                client_sock.close()
                return
            else:
                try:
                    client_sock.send("".encode())
                except OSError:
                    return True

    pass


def server_main(address="0.0.0.0", port=4200, max_client=5):
    global clients, server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((address, port))
    except OSError:
        server.close()
        return

    server.listen(max_client)
    print(f"Listen on {address}:{port} for {max_client} clients")

    while True:
        try:
            client, addr = server.accept()
            print(f"Accept Connection: {addr}")
            tlisten = threading.Thread(target=reception_message, args=(client, server))
            tlisten.start()
            tlisten.join()
        except OSError:
            return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Le server de Tchat")

        self.setMinimumSize(400, 700)

        self.server_label = QLabel("Serveur")
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("0.0.0.0")

        self.port_label = QLabel("Port ")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("4200")

        self.client_label = QLabel("Nombre de clients maximum ")
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("5")

        self.start_button = QPushButton("Demarrage du serveur")
        self.start_button.clicked.connect(self.start_server)

        self.console = QTextEdit()


        layout = QGridLayout()
        layout.addWidget(self.server_label, 0, 0)
        layout.addWidget(self.server_input, 0, 1)
        layout.addWidget(self.port_label, 1, 0)
        layout.addWidget(self.port_input, 1, 1)
        layout.addWidget(self.client_label, 2, 0)
        layout.addWidget(self.client_input, 2, 1)
        layout.addWidget(self.start_button, 3, 0, 1, 2)
        layout.addWidget(self.console, 4, 0, 2, 2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_server(self):
        global server_start, server
        if server_start:
            server.close()
        else:
            try:
                server_ip = self.server_input.text()
                server_port = self.port_input.text()
                server_max_client = self.client_input.text()

                if server_ip == '' or server_port == '' or server_max_client == '':
                    server_ip = "0.0.0.0"
                    server_port = 4200
                    server_max_client = 5

                if not isinstance(server_port, int) or not isinstance(server_max_client, int):
                    print("Error")
                else:
                    self.start_button.setText("Arrêt du serveur")
                    server_start = True
                    server_main(server_ip, server_port, server_max_client)

            except Exception as e:
                print(e)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





