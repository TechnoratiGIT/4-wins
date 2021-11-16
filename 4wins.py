import file_support as fs


def input_int(text=""):
    int_ = 0
    try:
        int_ = int(input(text))
    except ValueError:
        print("it was not an int try again")
        int_ = input_int(text)
    finally:
        return int_


class Playerlist:
    def __init__(self):
        self.path = "Playerinfo.json"
        self.names = self.LoadPlayerInfo()[0]
        self.colors = self.LoadPlayerInfo()[1]

    def Settings(self):
        running = True
        while running:
            i = input()
            if i == "add":
                self.addPlayer(input("player name 1:"), input_int("player color:"))
            elif i == "delete":
                self.deletePlayer()
            elif i == "print":
                self.PrintPlayers()
            elif i == "back":
                self.SavePlayerInfo()
                return
            elif i == "changeColor":
                self.PrintPlayers()
                self.changePlayerColor(input("Playername of the Player :"))
            else:
                return self.Settings()

    def addPlayer(self, name: str, color: int):
        try:
            index_pos = self.names.index(name)
            print(f'"{name}" is already in the list : ', index_pos)
        except ValueError:
            self.names.append(name)
            self.colors.append(color)

    def deletePlayer(self, index="a"):
        if index == "a":
            self.PrintPlayers()
            index = input_int("Playerindex of the Player to delete:")
        print("Deleted:", self.names.pop(index))
        del self.colors[index]

    def getPlayerColor(self, name):
        return f"\x1b[38;5;%sm" % self.colors[self.names.index(name)]

    def changePlayerColor(self, name):
        print("reference for numbers: https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg")
        self.colors[self.names.index(name)] = input_int("Choose color from 0 - 265:") % 266
        # self.colors[self.names.index(name)] = f"\x1b[38;5;%sm" % (input_int("Choose color from 0 - 265:"))

    def PrintPlayers(self):
        for i in range(len(self.names)):
            print(f"{i}: {self.names[i]}")

    def SavePlayerInfo(self):
        fs.save_content(self.path, [self.names, self.colors])

    def LoadPlayerInfo(self):
        return fs.get_content(self.path)


class FourWins:
    def __init__(self, collums=7, rows=6):
        self.pl = Playerlist()
        self.collums = collums
        self.rows = rows
        self.playerlist = 0, 1
        self.standard = "⬤"
        self.board = []
        self.fertig = False
        self.last = (0, 0)
        self.helppath = "forhelp.json"

    def help(self):
        dic = fs.get_content(self.helppath)
        help_list = dic["help_main"]
        print(help_list)
        for help_string in help_list:
            input(help_string)

    def Boardreset(self):
        self.board = []
        for i in range(self.rows):
            self.board.append([self.standard]*self.collums)

    def Settings(self):
        running = True
        while running:
            i = input()
            if i == "play":
                self.Start_Game()
            elif i == "help":
                self.help()
            elif i == "Player":
                self.pl.Settings()
            elif i == "stop":
                running = False
            else:
                return self.Settings()

    def Start_Game(self):
        p = 0
        self.Boardreset()
        self.pl.PrintPlayers()
        self.playerlist = input_int("player number 1:"), input_int("player number 2:")
        while not self.fertig:
            self.Print_Board()
            self.Zug(self.pl.names[self.playerlist[p]])
            if not self.TestWin() is None:
                self.Print_Board()
                self.fertig = True
                print(self.TestWin()[0], self.TestWin()[1])
            p = (p + 1) % 2
        return

    def Print_Board(self):
        for i in range(self.rows):
            s = "|"
            a = self.board[i]
            for j in range(self.collums):
                s += str(a[j]) + "|"
            print(s)

    def Zug_input(self, player):
        collum = input_int("Select your collum " + "'" + str(player) + "': ")
        if not 0 <= collum <= self.collums:
            print("Use a number between 1 and 7")
            collum = self.Zug_input(player)
        return collum

    def Zug(self, player):
        collum = self.Zug_input(player)
        not_finished = True
        i = 0
        if collum == 0:
            self.board[self.rows - 1 - self.last[1]][self.last[0] - 1] = self.standard
        else:
            while not_finished and i < self.rows:
                if self.board[self.rows - 1 - i][collum - 1] == self.standard:
                    self.board[self.rows - 1 - i][collum - 1] = self.pl.getPlayerColor(player) + self.standard +\
                                                                "\x1b[0m"
                    not_finished = False
                else:
                    i += 1
            if i == self.rows:
                print("This collum is filled try another one")
                self.Zug(player)
            else:
                self.last = collum, i

    def TestWin(self):
        """
        Tests for a win
        :return: Nothing
        """
        """tests the lines (-)"""
        for i in range(self.rows):
            for y in range(self.collums - 3):
                if self.board[i][y] == self.board[i][y+1] == self.board[i][y+2] \
                        == self.board[i][y+3] and not self.standard == self.board[i][y]:
                    return "Win for", self.board[i][y]
        """tests the lines (|)"""
        for i in range(self.rows - 3):
            for y in range(self.collums):
                if self.board[i][y] == self.board[i + 1][y] == self.board[i + 2][y] \
                        == self.board[i + 3][y] and not self.standard == self.board[i][y]:
                    return "Win for", self.board[i][y]
        """tests lines (\)"""
        for i in range(self.rows - 3):
            for y in range(self.collums - 3):
                if self.board[i][y] == self.board[i + 1][y + 1] == self.board[i + 2][y + 2] \
                        == self.board[i + 3][y + 3] and not self.standard == self.board[i][y]:
                    return "Win for", self.board[i][y]
        """tests the lines (/)"""
        for i in range(self.rows - 3):
            for y in range(self.collums - 3):
                if self.board[i][y + 3] == self.board[i + 1][y + 2] == self.board[i + 2][y + 1] \
                        == self.board[i + 3][y] and not self.standard == self.board[i][y + 3]:
                    return "Win for", self.board[i][y + 3]
        """tests for a full board"""
        full = True
        for i in range(self.rows):
            for j in range(self.collums):
                if self.board[i][j] == self.standard:
                    full = False
        if full:
            return "draw", ""
        return


if __name__ == "__main__":
    game = FourWins()
    game.Settings()
