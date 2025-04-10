from os import name, system
from colorama import Fore
from shutil import get_terminal_size
from copy import deepcopy
import pickle
from pynput import keyboard

class Screen:
    min_width = 72
    min_height = 16
    title = Fore.YELLOW + '''  _______                              __   _    _                   _ 
 |__   __|                            / _| | |  | |                 (_)
    | | _____      _____ _ __    ___ | |_  | |__| | __ _ _ __   ___  _ 
    | |/ _ \ \ /\ / / _ \ '__|  / _ \|  _| |  __  |/ _` | '_ \ / _ \| |
    | | (_) \ V  V /  __/ |    | (_) | |   | |  | | (_| | | | | (_) | |
    |_|\___/ \_/\_/ \___|_|     \___/|_|   |_|  |_|\__,_|_| |_|\___/|_|                                                                   
                                                                       '''
    gap = '           '
    disks = [
        '         ',
        Fore.BLUE + '   ===   ',
        Fore.YELLOW +  '  =====  ',
        Fore.GREEN +  ' ======= ',
        Fore.RED +  '========='
    ]
    def __init__(self):
        self.columns, self.rows = get_terminal_size(fallback=(72, 16))
        if self.columns < Screen.min_width or self.rows < Screen.min_height:
            print(f"⚠️  Terminal too small! Detected: {self.columns}x{self.rows}. Need at least {Screen.min_width}x{Screen.min_height} Please resize your window and try again.")
            quit()
    def clear(self):
        system('cls' if name == 'nt' else 'clear')
    def draw(self, pegs, moves):
        self.clear()
        print(Screen.title)
        print(Fore.WHITE + f'Moves: {len(moves)}\n')
        pegs_with_blanks = deepcopy(pegs)
        for peg in pegs_with_blanks:
            while len(peg) < 4:
                peg.insert(0,0)
        for disk in range(4):
            for stack in range(1,4):
                print(Screen.gap + Screen.disks[pegs_with_blanks[stack][disk]], end="")
            print('\n', end="")
        print('\n' + Fore.CYAN + '(1-3)Move (U)ndo             ' + Fore.MAGENTA + '(L)oad (S)ave             ' + Fore.LIGHTRED_EX + '(R)estart (Q)uit\n')
    def draw_splash_screen(self):
        print(Screen.title)
        print(Fore.LIGHTBLUE_EX + '                        Press any key to start\n\n')
        
class Game:
    def __init__(self):
        self.moves = []
        self.pegs = [[],[1,2,3,4],[],[]]
        self.screen = Screen()
        self.screen.clear()
        self.screen.draw_splash_screen()
        self.get_input()
        self.play()
    def play(self):
        while True:
            self.screen.draw(self.pegs, self.moves)
            if self.pegs == [[],[],[],[1,2,3,4]]:
                print('''               __     __          __          ___       
               \ \   / /          \ \        / (_)      
                \ \_/ /__  _   _   \ \  /\  / / _ _ __  
                 \   / _ \| | | |   \ \/  \/ / | | '_ \ 
                  | | (_) | |_| |    \  /\  /  | | | | |
                  |_|\___/ \__,_|     \/  \/   |_|_| |_|\n''')
                self.wait()
                self.moves = []
                self.pegs = [[],[1,2,3,4],[],[]]
                self.screen.draw(self.pegs, self.moves)
            from_peg = 0
            command = self.get_input()
            match command.lower():
                case '1' | '2' | '3':
                    from_peg = command
                    print(Fore.YELLOW + f"Move from {from_peg} to which peg? :")
                    to_peg = self.get_input()
                    if to_peg in ('1', '2', '3'):
                        from_peg = int(from_peg)
                        to_peg = int(to_peg)
                        if self.try_move(from_peg, to_peg):
                            self.moves.append([from_peg, to_peg])
                        else:
                            print(f'Illegal move.')
                            self.wait()
                case 'u':
                    if len(self.moves) > 0:
                        from_peg, to_peg = self.moves.pop()
                        self.pegs[from_peg].insert(0, self.pegs[to_peg].pop(0))
                case 'l':
                    self.load()
                case 's':
                    self.save()
                case 'q':
                    self.screen.clear()
                    print("Goodbye!")
                    self.clear_input_buffer()
                    quit()
                case 'r':
                    self.moves = []
                    self.pegs = [[],[1,2,3,4],[],[]]
    def try_move(self, from_peg, to_peg):
        if len(self.pegs[from_peg]) == 0 or from_peg == to_peg:
            return False
        elif self.pegs[to_peg] and self.pegs[from_peg][0] > self.pegs[to_peg][0]:
            return False
        else:
            self.pegs[to_peg].insert(0, self.pegs[from_peg].pop(0))
            return True
    def wait(self):
        print('Press any key to continue.')
        self.get_input()
    def load(self):
        try:
            with open('.toh_save', 'rb') as file:
                self.pegs, self.moves = pickle.load(file)
                print('Game Loaded')
                self.wait()
        except Exception:
            print('No save file found')
            self.wait()
    def save(self):
        with open('.toh_save', 'wb') as file:
            pickle.dump((self.pegs, self.moves), file)
            print('Game Saved')
            self.wait()
    def get_input(self):
        key_pressed = None

        def on_press(key):
            nonlocal key_pressed
            try:
                key_pressed = key.char
            except AttributeError:
                key_pressed = 'zzz'
            return False
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        self.clear_input_buffer()
        return key_pressed
    def clear_input_buffer(self):
        if name == 'nt':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios, fcntl, os, sys
            fd = sys.stdin.fileno()
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            try:
                sys.stdin.read()
            except BlockingIOError:
                pass
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)
game = Game()