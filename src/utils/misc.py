''' Colors '''
BLUEAQUA = '\033[38;5;50m'
GREENWEED = '\033[38;5;10m'

LILA = '\033[38;5;104m'
PINKDARK = '\033[38;5;05m'
GREENLOAD = '\033[38;5;77m'
DOTLOAD =  '\033[38;5;237m'

GREY = '\033[38;5;110m'
GREY246 = '\033[38;5;246m'

LIME = '\033[38;5;118m'
GREENLIGHTBRIGHT = '\033[38;5;120m'
WHITE = '\033[38;5;15m'

PURPLEDARK = '\033[38;5;99m'
PURPLEDARK1 = '\033[38;5;98m'
GREENLIGHT = '\033[38;5;82m'
BLUE = '\033[0;38;5;12m'
LPURPLE = '\033[0;38;5;201m'
ORANGE = '\033[0;38;5;214m'
PURPLE = '\033[0;38;5;141m'
B_PURPLE = '\033[45m'
YELLOW="\033[0;38;5;11m"
RED = '\033[1;31m'
B_RED = '\033[41m'
END = '\033[0m'
B_END = '\033[49m'
BOLD = '\033[1m'


''' MSG Prefixes '''
INFO = f'{BLUEAQUA}Info {END}'
KEY = f'{ORANGE}Keystroke{END}'
PASTE = f'{BLUE}Paste{END}'
WARN = f'{ORANGE}Warning{END}'
IMPORTANT = WARN = f'{ORANGE}Important{END}'
FAILED = f'{RED}Fail{END}'

DOT = f'{DOTLOAD}#{END}'
LOAD = f'{BOLD}{GREENLOAD}#{END}{B_END}'
STATUS_CODE = f'{ORANGE}{BOLD}>Status code: [{END}{B_END}'
BAD_STATUS_CODE = f'{B_RED}>Status code: [{END}{B_END}'
RECOLECT_IMG =  f'{LILA}Recolecting images:\t{END}'
RECOLECT_HREF =  f'{LILA}Recolecting links:\t{END}'
DOWNLOAD = f'{LILA}Downloading:\t{END}'
OBATAIN_URLS = f'{LILA}Obtaining hrefs:\t{END}'
DONE = f'{GREENLOAD}\nDone!{END}'
URL = f'{ORANGE}URL {END}'

def status_msg(s):
	print(flush=True)
	print(STATUS_CODE + s + ORANGE + BOLD + "]" + END + B_END)

def bad_status_code(s):
	print(BAD_STATUS_CODE + s + B_RED + "]" + END + B_END)

def info_msg(s):
	print(GREY246 + s + END)

def lightinfo_msg(s):
	print(f'{BLUEAQUA} {s}')