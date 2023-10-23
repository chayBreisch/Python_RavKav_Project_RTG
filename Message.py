from enum import IntEnum


class Request(IntEnum):
    CREATE = 1
    CHECK_STATUS = 2
    PAY = 3
    FILL_WALLET = 4
    CHANGE_CONTRACT = 5


class Message:
    @staticmethod
    def encode_request(request, params1):
        """
        A function to encode the request sent to the server
        :param request: the type of action desired
        :param params1: The values of the fields needed for this action
        :return: the encoded message to send to the server
        """
        msg = str(request) + '#'
        request = int(request)
        if request == Request.CREATE:
            msg += str(params1['user_id']) + '#' + str(params1['contract_name']) + '#' + str(params1['wallet'])
        elif request == Request.CHECK_STATUS:
            msg += str(params1['card_id'])
        elif request == Request.PAY:
            msg += str(params1['card_id']) + '#' + str(params1['contract_name'])
        elif request == Request.FILL_WALLET:
            msg += str(params1['card_id']) + '#' + str(params1['wallet'])
        elif request == Request.CHANGE_CONTRACT:
            msg += str(params1['card_id']) + '#' + str(params1['contract_name'])
        return msg

    @staticmethod
    def decode_request(request):
        """
        A function to decode the request received from the client
        :param request: the type of action desired
        :return: the decoded message
        """
        msg = request.split('#')
        if int(msg[0]) == Request.CREATE:
            return dict(request=msg[0], user_id=msg[1], contract_name=msg[2], wallet=msg[3])
        if int(msg[0]) == Request.CHECK_STATUS:
            return dict(request=msg[0], card_id=msg[1])
        if int(msg[0]) == Request.PAY:
            return dict(request=msg[0], card_id=msg[1], destination=msg[2])
        if int(msg[0]) == Request.FILL_WALLET:
            return dict(request=msg[0], card_id=msg[1], wallet=msg[2])
        if int(msg[0]) == Request.CHANGE_CONTRACT:
            return dict(request=msg[0], card_id=msg[1], contract_name=msg[2])

    @staticmethod
    def encode_answer(request, status, card_id=-1, contract_name=-1, wallet=-1):
        """
        A function to encode the answer sent to the client
        :param request: the type of action desired
        :param status: status of action if done or fails
        :param card_id: number of card id
        :param contract_name: name of the contract in card
        :param wallet: sum of wallet in card
        :return: the encoded answer to send to the client
        """
        msg = str(request) + '#' + status + '#'
        if card_id != -1:
            msg += str(card_id) + '#'
        if contract_name != -1:
            msg += str(contract_name) + '#'
        if wallet != -1:
            msg += str(wallet) + '#'
        return msg

    @staticmethod
    def decode_answer(answer):
        """
         function to decode the request received from the server
        :param answer: encoded answer received from the server
        :return: the decoded answer
        """
        msg = answer.split('#')
        if msg[1] == 'Fails':
            return dict(status=msg[1])
        if int(msg[0]) == Request.CREATE:
            return dict(status=msg[1], card_id=msg[2])
        if int(msg[0]) == Request.CHECK_STATUS:
            return dict(status=msg[1], card_id=msg[2], contract_name=msg[3], wallet=msg[4])
        else:
            return dict(status=msg[1])
