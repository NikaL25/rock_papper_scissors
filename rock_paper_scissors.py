import hashlib
import hmac
import random
import secrets
import sys



class RockPaperScissorsGame:
    def __init__(self, moves):
        self.moves = moves

    def print_table(table):
        col_width = max(len(max(row, key=len)) for row in table)
        for row in table:
            print(" | ".join(row).center(col_width * len(row) + len(row) - 1))
    def generate_key(self):
        return secrets.token_bytes(32)  

    def generate_computer_move(self):
        return random.choice(self.moves)

    def calculate_hmac(self, key, move):
        return hmac.new(key, move.encode(), hashlib.sha256).hexdigest()

    def determine_winner(self, user_move, computer_move):
        if user_move == computer_move:
            return "Draw"

        move_count = len(self.moves)
        half_count = move_count // 2
        user_move_index = self.moves.index(user_move)
        computer_move_index = self.moves.index(computer_move)

        if (user_move_index + half_count) % move_count == computer_move_index:
            return "You win!"
        else:
            return "Computer wins!"

    def print_help_table(self):
        move_count = len(self.moves)
        header = ["+-------------+"] + [f"{move:^11}" for move in self.moves]
        divider = ["+-------------+"] + ["+" * 11 for _ in range(move_count)]
        
        print("".join(header))
        for i in range(move_count):
            move = self.moves[i]
            row = [f"| {move:^11} |"]
            for j in range(move_count):
                result = "Draw" if i == j else ("Win" if (i + 1) % move_count == j else "Lose")
                row.append(f"{result:^11}")
            print("".join(row))
            if i < move_count - 1:
                print("".join(divider))



       

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 3 or len(args) % 2 == 0 or len(args) != len(set(args)):
        print("Incorrect input. Please provide an odd number of non-repeating strings.")
        print("Example: python rock_paper_scissors.py rock paper scissors lizard Spock")
        sys.exit(1)

    game = RockPaperScissorsGame(args)

    print("Available moves:")
    for i, move in enumerate(args, start=1):
            print(f"{i} - {move}")
    print("0 - exit")
    print("? - help")


    while True:
        game.key = game.generate_key()  
        game.computer_move = game.generate_computer_move()  
        game.computer_hmac = game.calculate_hmac(game.key, game.computer_move)  

        
         
        user_choice = input("Enter your move: ")

        if user_choice == '0':
            sys.exit(0)
        elif user_choice == '?':
            game.print_help_table()
        elif user_choice.isdigit() and 1 <= int(user_choice) <= len(args):
            user_move = args[int(user_choice) - 1]
            print(f"\nYour move: {user_move}")
            hmac_result = game.calculate_hmac(game.key, user_move)
            print(f"Your HMAC: {hmac_result}")
            print(f"Computer move: {game.computer_move}")
            print(f"Computer HMAC: {game.computer_hmac}")
            result = game.determine_winner(user_move, game.computer_move)
            print(result)
        else:
            print("Invalid input. Please select a valid move or option.")
