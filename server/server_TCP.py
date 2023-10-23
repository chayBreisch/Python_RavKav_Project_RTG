import socket as socket_library
from Message import Message, Request
import services as services

ADDRESS = ("192.168.56.1", 61761)
BUFFER_SIZE = 1024

server_socket = socket_library.socket(family=socket_library.AF_INET, type=socket_library.SOCK_STREAM)
server_socket.bind(ADDRESS)

server_socket.listen(5)
server_socket.settimeout(2.5)
clients = {}
while True:
    try:
        client, address = server_socket.accept()
        clients[client] = address
        client.settimeout(2.5)
    except socket_library.timeout:
        print("No accept. timed out")
    except ConnectionError:
        print("the server is unreachable and will be closed")
        break
    del_keys = []
    for key in clients:
        try:
            message = Message.decode_request(key.recv(BUFFER_SIZE).decode("UTF-8"))
            if int(message['request']) == Request.CREATE:
                ret = services.create_card(message['user_id'], message['contract_name'], message['wallet'])
            elif int(message['request']) == Request.CHECK_STATUS:
                ret = services.get_data_card(int(message['card_id']))
            elif int(message['request']) == Request.PAY:
                ret = services.pay_ride(message['card_id'], message['destination'])
            elif int(message['request']) == Request.FILL_WALLET:
                ret = services.fill_wallet(message['card_id'], message['wallet'])
            else:
                ret = services.change_contract(message['card_id'], message['contract_name'])

            if ret == -1:
                ans = Message.encode_answer(message['request'], 'Fails')
            elif int(message['request']) == Request.CREATE:
                ans = Message.encode_answer(message['request'], 'Done', ret)
            elif int(message['request']) == Request.CHECK_STATUS:
                ans = Message.encode_answer(message['request'], 'Done', ret[0], ret[1], ret[2])
            else:
                ans = Message.encode_answer(message['request'], 'Done')

            key.send(ans.encode("UTF-8"))
        except socket_library.timeout:
            print("No message received from", clients[key])
        except ConnectionError:
            print(f"{clients[key]} is disconnected")
            del_keys.append(key)
    for c in del_keys:
        del clients[c]








# import socket as socket_library
# from Message import Message, Request
# import services as services
# from enum import IntEnum
#
#
# class server_TCP:
#
#     def __init__(self):
#         ADDRESS = ("192.168.56.1", 61761)
#         BUFFER_SIZE = 1024
#
#         server_socket = socket_library.socket(family=socket_library.AF_INET, type=socket_library.SOCK_STREAM)
#         server_socket.bind(ADDRESS)
#
#         server_socket.listen(5)
#         server_socket.settimeout(2.5)
#         clients = {}
#
#     def run(self):
#         """
#
#         :return:
#         """
#         while True:
#             try:
#                 client, address = self.server_socket.accept()
#                 self.clients[client] = address
#                 client.settimeout(2.5)
#             except socket_library.timeout:
#                 print("No accept. timed out")
#             except ConnectionError:
#                 print("the server is unreachable and will be closed")
#                 break
#             del_keys = []
#             for key in self.clients:
#                 try:
#                     message = Message.decode_request(key.recv(self.BUFFER_SIZE).decode("UTF-8"))
#                     if int(message['request']) == Request.CREATE:
#                         ret = services.create_card(message['user_id'], message['contract_name'], message['wallet'])
#                     elif int(message['request']) == Request.CHECK_STATUS:
#                         ret = services.get_data_card(int(message['card_id']))
#                     elif int(message['request']) == Request.PAY:
#                         ret = services.pay_ride(message['card_id'], message['destination'])
#                     elif int(message['request']) == Request.FILL_WALLET:
#                         ret = services.fill_wallet(message['card_id'], message['wallet'])
#                     else:
#                         ret = services.change_contract(message['card_id'], message['contract_name'])
#
#                     if ret == -1:
#                         ans = Message.encode_answer(message['request'], 'Fails')
#                     elif int(message['request']) == Request.CREATE:
#                         ans = Message.encode_answer(message['request'], 'Done', ret)
#                     elif int(message['request']) == Request.CHECK_STATUS:
#                         ans = Message.encode_answer(message['request'], 'Done', ret[0], ret[1], ret[2])
#                     else:
#                         ans = Message.encode_answer(message['request'], 'Done')
#
#                     key.send(ans.encode("UTF-8"))
#                 except socket_library.timeout:
#                     print("No message received from", self.clients[key])
#                 except ConnectionError:
#                     print(f"{self.clients[key]} is disconnected")
#                     del_keys.append(key)
#             for c in del_keys:
#                 del self.clients[c]
