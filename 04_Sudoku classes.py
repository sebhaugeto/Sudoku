"""
A simple sudoku game for the terminal, written in Python. 
"""

def intro():
    print("WELCOME DEAR HUMAN! \n This is Sudoku by @sebhaugeto.")
    answer = ""
    while answer not in ("yes","no"):
        answer = input("Do you want to play? yes/no ").lower().strip()
    if answer == "yes":
        return True
    else:
        return False

class Board:
    def __init__(self):
        self.board = [[" "," "," "," "," "," "," "," "," "] for n in range(9)]

    def print_board(self):
        print(f"   {'0 1 2':^7} {'3 4 5':^7} {'6 7 8':^7}")
        print("  +-------+-------+-------+")
        i_list = [[0,1,2],[3,4,5],[6,7,8]]
        for i in range(3):
            for j in range(3):
                num = i_list[i][j]
                print(f"{num} | {' '.join(str(e) for e in self.board[num][:3])} | {' '.join(str(e) for e in self.board[num][3:6])} | {' '.join(str(e) for e in self.board[num][6:])} |")
            print("  +-------+-------+-------+")

    def check_input(self,input_,position):
        r,c = position

        #Creating the column:
        column = []
        for row in self.board:
            column.append(row[c])
        
        #Creating the square-list:
        square = []

        #Getting the right value for c
        if c <= 2: c = 0
        elif 2 < c <= 5: c = 3
        elif 5 < c <= 8: c = 6

        #Setting square = [] to the right values
        if r <= 2: square = self.board[0][c:c+3] + self.board[1][c:c+3] + self.board[2][c:c+3]
        elif 2 < r <= 5: square = self.board[3][c:c+3] + self.board[4][c:c+3] + self.board[5][c:c+3]
        elif 5 < r <= 8: square = self.board[6][c:c+3] + self.board[7][c:c+3] + self.board[8][c:c+3]
        
        #Checking if input_ is in the column or row or square
        if input_ < 0 or input_ in column or input_ in self.board[r] or input_ in square:
            return False
        else:
            return True

    def change_board(self,position,input_=None,add_or_del=True):
        r,c = position
        if add_or_del == True:
            self.board[r][c] = input_
        if add_or_del == False:
            self.board[r][c] = " "
    
    def check_win(self):
        #Creating the column-list
        columns = []
        for c in range(9):
            col = []
            for row in self.board:
                col.append(row[c])
            columns.append(col)
        
        #Creating the square-list:
        squares = []
        for big_row in range(3):
            for big_col in range(3):
                sq = []
                for row in range(3):
                    for col in range(3):
                        tot_row = 3*big_row + row
                        tot_col = 3*big_col + col
                        sq.append(self.board[tot_row][tot_col])
                squares.append(sq)
        
        #Checking if the rows, columns and squares contain 1 - 9:
        win = set([n for n in range(1,10)])
        for item in [self.board,columns,squares]:
            result = False
            for e in item:
                if win == set(e):
                    result = True
                else:
                    result = False
                    break
        return result
    
    #Save a board
    def save_board(self,filename):
        import pickle
        with open(filename,"wb") as f:
            pickle.dump(self.board,f)
    
    #Load a board
    def read_file(self,filename):
        import pickle
        with open(filename, "rb") as f:
            self.board = pickle.load(f)

def take_num():
    answer = float("inf")
    while answer not in [n for n in range(1,10)]:
        answer = int(input("Choose a number between 1 and 9: "))
    return answer

def take_position():
    col = float("inf")
    row = float("inf")
    while row not in [n for n in range(9)]:
        try:
            row = int(input("Choose a row number between 0 and 8: "))
        except:
            print("Invalid input")
    while col not in range(9):
        try:
            col = int(input("Choose a col number between 0 and 8: "))
        except:
            print("Invalid input")
    return(row,col)

def clear_output():
    for i in range(20):
        print()

def main():
    play = True    
    while play:
        if intro():
            #Init board
            play_board = Board()
            while True:
                #Display board, take input, take position
                clear_output()
                play_board.print_board()

                #Ask if user wants to add,delete,save or quit
                user_bool = None
                while user_bool not in ("add","del","s","q","o"):
                    user_bool = input("Do you want to: add element (add), delete element (del), save board (s), open board (o) or quit (q)? ").lower().strip()
                #Add element
                if user_bool == "add":
                    user_bool = True
                #Delete element
                elif user_bool == "del":
                    user_bool = False
                #Save file
                elif user_bool == "s":
                    play_board.save_board("sudokuboard")
                    print("File saved!")
                    user_bool = True
                #Open saved board
                elif user_bool == "o":
                    try: 
                        play_board.read_file("sudokuboard")
                        clear_output()
                        play_board.print_board()
                    except:
                        print("No saved board in memory.")
                #Quit game
                elif user_bool == "q":
                    print("Thank you for playing my game! By @sebhaugeto. Find me on Instagram!")
                    break

                #Check if position is valid
                position = (0,0)
                user_num = -1
                checked = play_board.check_input(user_num,position)
                #If user wants to add element
                while not checked and user_bool:
                    user_num = take_num()
                    position = take_position()
                    checked = play_board.check_input(user_num,position)
                #If user wants to delete element
                if not checked and not user_bool:
                    position = take_position()
                #Updatae board
                play_board.change_board(position,user_num,user_bool)
                #Check for win
                result = play_board.check_win()
                if result:
                    print("WOOOOOOOOOOW! You completed the game! NOT BAD AT ALL.")
                    answer = ""
                    while answer not in ("yes","no"):
                        answer = input("Do you want to play again? ").lower()
                    if answer == "yes":
                        break
                    else:
                        play = False
                        break
        
        try:
            if answer == "yes":
                continue
        except:          
            print("Bye.")
            play = False

main()




