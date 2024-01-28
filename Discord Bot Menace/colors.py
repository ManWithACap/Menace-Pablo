# kamito / console-color on GitHub
class Colors:
    def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"
    def backrgb(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"

    # foreground color
    BLACK  = rgb(0, 0, 0)
    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    PURPLE = rgb(111, 0, 201)
    CYAN   = "\033[36m"
    WHITE  = "\033[37m"
    MAGENTA = rgb(244, 3, 252)

    # background color
    BLACKB  = "\033[40m"
    REDB    = "\033[41m"
    GREENB  = "\033[42m"
    YELLOWB = "\033[43m"
    BLUEB   = "\033[44m"
    PURPLEB = "\033[45m"
    CYANB   = "\033[46m"
    WHITEB  = "\033[47m"

    # bold
    B    = "\033[1m"
    BOFF = "\033[22m"

    # italics
    I = "\033[3m"
    IOFF = "\033[23m"

    # underline
    U = "\033[4m"
    UOFF = "\033[24m"

    # invert
    R = "\033[7m"
    ROFF = "\033[27m"

    # reset
    RESET  = "\033[0m"