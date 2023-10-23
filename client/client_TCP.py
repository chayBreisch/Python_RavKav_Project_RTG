import socket as socket_library
import time as time_library
from Message import Message


class Client:
    def __init__(self, IP, PORT):
        """
        A function to initialize the class
        :param IP: the IP of the server
        :param PORT: the port of the server
        """
        self.SERVER_ADDRESS = (IP, PORT)
        self.BUFFER_SIZE = 1024
        self.client_socket = socket_library.socket(family=socket_library.AF_INET, type=socket_library.SOCK_STREAM)
        self.client_socket.connect(self.SERVER_ADDRESS)

    def connect(self, request, params1):
        """
        A function to connect to the server
        :param request: the type of action desired
        :param params1: The values of the fields needed for this action
        :return: the answer received from the server
        """
        msg = Message.encode_request(request, params1)
        self.client_socket.send(msg.encode("UTF-8"))
        return Message.decode_answer(self.client_socket.recv(self.BUFFER_SIZE).decode("UTF-8"))
        # time_library.sleep(3)

    def close_connection_server(self):
        """
        A function to close the connection to the server
        """
        self.client_socket.close()
