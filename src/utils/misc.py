''' Colors '''
MAIN = '\033[38;5;50m'
GREEN = '\033[38;5;82m'
BLUE = '\033[0;38;5;12m'
LPURPLE = '\033[0;38;5;201m'
ORANGE = '\033[0;38;5;214m'
ORANGEB = '\033[1;38;5;214m'
PURPLE = '\033[0;38;5;141m'
B_PURPLE = '\033[45m'
YELLOW="\033[0;38;5;11m"
RED = '\033[1;31m'
B_RED = '\033[41m'
END = '\033[0m'
B_END = '\033[49m'
BOLD = '\033[1m'
ULINE = '\033[4m'


''' MSG Prefixes '''
INFO = f'{MAIN}Info {END}'
KEY = f'{ORANGE}Keystroke{END}'
PASTE = f'{BLUE}Paste{END}'
WARN = f'{ORANGE}Warning{END}'
IMPORTANT = WARN = f'{ORANGE}Important{END}'
FAILED = f'{RED}Fail{END}'
FORM = f'{RED}Form-Submission-Intercepted{END}'
FILE = f'{RED}File-Selection-Intercepted{END}'
TABLE = f'{RED}Table-Data-Intercepted{END}'
LINK = f'{RED}Link{END}'
RESPONSE = f'{RED}Server-Response-Intercepted{END}'
REQ = f'{BOLD}Request{END}'
SPIDER = f'{B_PURPLE}{BOLD}Spider{END}{B_END}'
CHANGE = f'{ORANGE}Input-Value-Changed{END}'
STATUS_CODE = f'{ORANGE}{BOLD}Status code: [{END}{B_END}'

def status_msg(s):
	print(STATUS_CODE + s + ORANGE + BOLD + "]" + END + B_END)

def info_msg(s):
	print(INFO + s)