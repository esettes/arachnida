''' Colors '''
BLUEAQUA = '\033[38;5;50m'
BLUELIGHT = '\033[38;5;45m'
GREENWEED = '\033[38;5;10m'

LILA = '\033[38;5;104m'
PINKDARK = '\033[38;5;05m'
GREENLOAD = '\033[38;5;77m'
DOTLOAD =  '\033[38;5;237m'

GREY = '\033[38;5;110m'
GREY246 = '\033[38;5;246m'

LIME = '\033[38;5;118m'
BLACK = '\033[38;5;16m'
BLUEDARK = '\033[38;5;22m'
GREENLIGHTBRIGHT = '\033[38;5;120m'
WHITE = '\033[38;5;15m'

PURPLEDARK = '\033[38;5;99m'
PURPLEDARK1 = '\033[38;5;98m'
GREENLIGHT = '\033[38;5;82m'
BLUE = '\033[0;38;5;12m'
LPURPLE = '\033[0;38;5;201m'
ORANGE = '\033[0;38;5;214m'
ORANGEDARK = '\033[0;38;5;208m'
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
INFO = f'{BLUEAQUA}Info {END}'
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

DOT = f'{DOTLOAD}#{END}'
LOAD = f'{BOLD}{GREENLOAD}#{END}{B_END}'
STATUS_CODE = f'{ORANGE}{BOLD}>Status code: [{END}{B_END}'
RECOLECT_IMG =  f'{LILA}Recolecting images:\t{END}'
DOWNLOAD = f'{LILA}Downloading:\t{END}'
DONE = f'{GREENLOAD}\nDone!{END}'

def status_msg(s):
	print(STATUS_CODE + s + ORANGE + BOLD + "]" + END + B_END)

def info_msg(s):
	print(GREY246 + s + END)