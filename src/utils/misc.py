''' Colors '''
BLUEAQUA = '\033[38;5;50m'
GREENWEED = '\033[38;5;10m'

LILA = '\033[38;5;104m'
PINK = '\033[38;5;207m'
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
INFO2 = f'{ORANGE}Info {END}'
INFO3 = f'{PINK}Info {END}'
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
	print(f'{BLUEAQUA} {s} {END}')

def info_msg_purple(s):
	print(f'{LILA} {s} {END}')

def info_msg_orange(s):
	print(f'{ORANGE} {s} {END}')
    
def err_msg(s):
	print(f'{RED}[ERROR] {END}{s}')

CUSTOM_TAGS = {
	0x0100: "ImageWidth",
    0x0101: "ImageLength",
    0x0102: "BitsPerSample",
    0x0103: "Compression",
	0x010D: "DocumentName",
    0x010E: "ImageDescription",
    0x010F: "Make",
    0x0110: "Model",
	0x0115: "SamplesPerPixel",
    0x0117: "StripByteCounts",
	0x011A: "XResolution",
    0x011B: "YResolution",
	0x0128: "ResolutionUnit",
    0x0129: "PageNumber",
    0x012D: "TransferFunction",
    0x0131: "Software",
    0x0132: "DateTime",
    0x013B: "Artist",
	0x0157: "ClipPath",
    0x0158: "XClipPathUnits",
    0x0159: "YClipPathUnits",
	0x015B: "JPEGTables",
	0x8298: "Copyright",
	0x8833: "ISOSpeed",
	0x9212: "SecurityClassification",
    0x9213: "ImageHistory",
    0x9214: "SubjectLocation",
	0xC65C: "BestQualityScale",
    0xC65D: "RawDataUniqueID",
    0xC68B: "OriginalRawFileName",
    0xC68C: "OriginalRawFileData",
}

CUSTOM_TAGS = {
    
}