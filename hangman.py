from random import randrange
import json

class Model:

    word = ''
    board = []
    guessed_letters = []
    wrong_guesses = 0
    correct_spots = 0

    def word_list():
        contents = []
        with open('5desk.txt') as list:
            for line in list:
                contents.append([])
                for item in line.split():
                    if len(item) > 4 and len(item) < 13:
                        contents[-1].append(item)
        return contents


    def choose_word():
        x = randrange(len(Model.word_list()))
        word = Model.word_list()[x]
        if len(word) == 0:
            return Model.choose_word()
        else:
            Model.word = word[0].lower()


    def make_game_board():
        for letter in Model.word:
            Model.board.append('')


    def save_game():
        saved_game = {
            "word": Model.word,
            "board": Model.board,
            "guessed_letters": Model.guessed_letters,
            "wrong_guesses": Model.wrong_guesses,
            "correct_spots": Model.correct_spots
        }
        s = json.dumps(saved_game)
        print(s)
        with open('hangman.txt', 'w') as log:
            log.write(s)


class Controller:

    def play_game():
        print(' ')
        print('Hangman!')
        print('Six Wrong Guesses and you Hang')
        print(' ')
        x = input('1 to start a new game. 2 to load a saved game. ')
        if x == '1':
            Model.choose_word()
            print(' ')
            Model.make_game_board()
        elif x == '2':
            print(' ')
            f = open('hangman.txt')
            s = f.read()
            contents = json.loads(s)
            Model.word = contents['word']
            Model.board = contents['board']
            Model.guessed_letters = contents['guessed_letters']
            Model.wrong_guesses = contents['wrong_guesses']
            Model.correct_spots = contents['correct_spots']
        else:
            return Controller.play_game()
        print(Model.board)
        while True:
            Controller.display_data()
            if Controller.make_guess():
                break
            print(' ')
            print(Model.board)
            if Controller.check_for_win():
                break
            if Controller.check_for_loss():
                break


    def display_data():
        print('Guessed letters: ' + str(Model.guessed_letters))
        print('Wrong Guesses: ' + str(Model.wrong_guesses))
        print(' ')


    def make_guess():
        get_letter = input("Guess a letter. Enter '1' to save: ")
        x = get_letter.lower()
        if x == '1':
            print('saving...')
            Model.save_game()
            return True
        if len(x) != 1:
            print('Pick one letter')
            return Controller.make_guess()
        for letter in Model.guessed_letters:
            if letter == x:
                print('You already picked that letter!')
                return Controller.make_guess()
        Model.guessed_letters.append(x)
        Controller.search_letter(x)


    def search_letter(char):
        correct_letters = 0
        for i in range(len(Model.word)):
            if Model.word[i] == char:
                Model.board[i] = char
                correct_letters += 1
        Model.correct_spots += correct_letters
        if correct_letters == 0:
            Model.wrong_guesses +=1


    def check_for_win():
        if Model.correct_spots == len(Model.board):
            print('You Win!')
            return True


    def check_for_loss():
        if Model.wrong_guesses >= 6:
            print(Model.word)
            print('6 wrong guesses. You Lose.')
            return True


Controller.play_game()
