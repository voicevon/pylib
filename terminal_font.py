
# https://www.devdungeon.com/content/colorize-terminal-output-python
# https://www.geeksforgeeks.org/print-colors-python-terminal/

class TerminalFont:
    class Color:
        class Control:  
            '''
            Full name: Perfect_color_text
            '''
            reset='\033[0m'
            bold='\033[01m'
            disable='\033[02m'
            underline='\033[04m'
            reverse='\033[07m'
            strikethrough='\033[09m'
            invisible='\033[08m'

        class Fore:
            '''
            Full name: Perfect_fore_color
            ''' 
            black='\033[30m'
            red='\033[31m'
            green='\033[32m'
            orange='\033[33m'
            blue='\033[34m'
            purple='\033[35m'
            cyan='\033[36m'
            lightgrey='\033[37m'
            darkgrey='\033[90m'
            lightred='\033[91m'
            lightgreen='\033[92m'
            yellow='\033[93m'
            lightblue='\033[94m'
            pink='\033[95m'
            lightcyan='\033[96m'

        class Background: 
            '''
            Full name: Perfect_background_color
            ''' 
            black='\033[40m'
            red='\033[41m'
            green='\033[42m'
            orange='\033[43m'
            blue='\033[44m'
            purple='\033[45m'
            cyan='\033[46m'
            lightgrey='\033[47m'

class CvColor:
    line = (0,255,0)  
    circle = (255,255,0)

if __name__ == "__main__":
    print (TerminalFont.Color.Fore.yellow + 'Hello world.   ' +TerminalFont.Color.Fore.red + 'Hey!')