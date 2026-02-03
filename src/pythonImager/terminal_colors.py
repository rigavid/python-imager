new_line, space='\n', ' '
BLACK, RED, GREEN, BROWN, BLUE, PURPLE, CYAN, LIGHT_GRAY, DARK_GRAY="\033[30m", "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m", "\033[30m"
LIGHT_RED, LIGHT_GREEN, YELLOW, LIGHT_BLUE, LIGHT_PURPLE, LIGHT_CYAN, LIGHT_WHITE="\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"
BOLD, UNDERLINED, NORMAL='\033[1m', '\033[4m', '\033[00m'
BOLD_RED, BOLD_GREEN, BOLD_BLUE = f'{RED}{BOLD}', f'{GREEN}{BOLD}', f'{BLUE}{BOLD}'
# Append NORMAL at the end of the message to clear the format