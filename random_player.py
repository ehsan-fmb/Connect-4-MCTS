import random
import time


class Random_Player:

    def __init__(self,root):
        self.__root=root

    def search(self):
        legal_moves=self.__root.legal_moves()
        random.shuffle(legal_moves)
        self.__root.change_board(legal_moves[0][0],legal_moves[0][1])
        time.sleep(4)
        return legal_moves[0][0],legal_moves[0][1]

    def change_root(self,row,cul):
        self.__root.set_player(-1*self.__root.get_player())
        self.__root.change_board(row,cul)
        self.__root.set_player(-1 * self.__root.get_player())