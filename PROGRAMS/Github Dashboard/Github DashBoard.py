import curses
import json
import os
import stat
import sys
import urllib.request
import urllib.error
import time
import math
import random
import threading
from datetime import datetime, timezone

CONFIG_PATH = os.path.expanduser("~/.github_widget_config.json")
API_BASE = "https://api.github.com"
TIMEOUT = 10

# Theme.root

THEME_ORDER = ["cyberpunk", "matrix", "amber", "ice"]

THEMES = {
    "cyberpunk": {
        "name": "CYBERPUNK",
        "border_primary": 2,
        "border_secondary": 6,
        "accent": 3,
        "dim": 4,
        "error": 1,
        "success": 2,
        "warning": 3,
        "title": 6,
        "value": 2,
        "muted": 4,
        "highlight": 3,
        "bar_fill": "█",
        "bar_empty": "░",
        "corner_tl": "╔",
        "corner_tr": "╗",
        "corner_bl": "╚",
        "corner_br": "╝",
        "h_line": "═",
        "v_line": "║",
        "t_down": "╦",
        "t_up": "╩",
        "t_right": "╠",
        "t_left": "╣",
        "cross": "╬",
        "dot": "◆",
        "arrow": "▶",
        "bullet": "◉",
        "star": "★",
        "fork": "⑂",
        "eye": "◈",
        "clock": "◷",
        "lock": "▣",
        "open": "□",
        "spark_chars": ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
        "spinner": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "wave": ["▔", "▀", "█", "▄", "▁"],
        "signal": ["▁▁▁", "▁▁▂", "▁▂▃", "▂▃▄", "▃▄▅", "▄▅▆", "▅▆▇", "▆▇█"],
    }
}

THEMES["matrix"] = dict(THEMES["cyberpunk"])
THEMES["matrix"]["name"] = "MATRIX"

THEMES["amber"] = dict(THEMES["cyberpunk"])
THEMES["amber"]["name"] = "AMBER"

THEMES["ice"] = dict(THEMES["cyberpunk"])
THEMES["ice"]["name"] = "ICE"

ACTIVE_THEME       = THEMES["cyberpunk"]
ACTIVE_THEME_INDEX = 0

PAIR_BORDER       = 1
PAIR_ACCENT       = 2
PAIR_DIM          = 3
PAIR_ERROR        = 4
PAIR_SUCCESS      = 5
PAIR_WARNING      = 6
PAIR_TITLE        = 7
PAIR_VALUE        = 8
PAIR_MUTED        = 9
PAIR_HIGHLIGHT    = 10
PAIR_BAR_FULL     = 11
PAIR_BAR_EMPTY    = 12
PAIR_HEADER_BG    = 13
PAIR_SCANLINE     = 14
PAIR_GLOW         = 15


# Theme.switch.root

def apply_theme_colors():
    global ACTIVE_THEME
    name = ACTIVE_THEME["name"]
    try:
        if name == "MATRIX":
            curses.init_pair(PAIR_BORDER,    curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_ACCENT,    curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_DIM,       curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_ERROR,     curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_SUCCESS,   curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_WARNING,   curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_TITLE,     curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_VALUE,     curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_MUTED,     curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_HIGHLIGHT, curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_BAR_FULL,  curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_BAR_EMPTY, curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_GLOW,      curses.COLOR_WHITE,  -1)
        elif name == "AMBER":
            curses.init_pair(PAIR_BORDER,    curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_ACCENT,    curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_DIM,       curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_ERROR,     curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_SUCCESS,   curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_WARNING,   curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_TITLE,     curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_VALUE,     curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_MUTED,     curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_HIGHLIGHT, curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_BAR_FULL,  curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_BAR_EMPTY, curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_GLOW,      curses.COLOR_WHITE,  -1)
        elif name == "ICE":
            curses.init_pair(PAIR_BORDER,    curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_ACCENT,    curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_DIM,       curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_ERROR,     curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_SUCCESS,   curses.COLOR_CYAN,   -1)
            curses.init_pair(PAIR_WARNING,   curses.COLOR_CYAN,   -1)
            curses.init_pair(PAIR_TITLE,     curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_VALUE,     curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_MUTED,     curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_HIGHLIGHT, curses.COLOR_CYAN,   -1)
            curses.init_pair(PAIR_BAR_FULL,  curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_BAR_EMPTY, curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_GLOW,      curses.COLOR_CYAN,   -1)
        else:
            curses.init_pair(PAIR_BORDER,    curses.COLOR_CYAN,   -1)
            curses.init_pair(PAIR_ACCENT,    curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_DIM,       curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_ERROR,     curses.COLOR_RED,    -1)
            curses.init_pair(PAIR_SUCCESS,   curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_WARNING,   curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_TITLE,     curses.COLOR_CYAN,   -1)
            curses.init_pair(PAIR_VALUE,     curses.COLOR_WHITE,  -1)
            curses.init_pair(PAIR_MUTED,     curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_HIGHLIGHT, curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_BAR_FULL,  curses.COLOR_GREEN,  -1)
            curses.init_pair(PAIR_BAR_EMPTY, curses.COLOR_BLUE,   -1)
            curses.init_pair(PAIR_GLOW,      curses.COLOR_WHITE,  -1)
    except Exception:
        pass


def next_theme():
    global ACTIVE_THEME, ACTIVE_THEME_INDEX
    ACTIVE_THEME_INDEX = (ACTIVE_THEME_INDEX + 1) % len(THEME_ORDER)
    ACTIVE_THEME = THEMES[THEME_ORDER[ACTIVE_THEME_INDEX]]
    apply_theme_colors()
    return ACTIVE_THEME["name"]


# Config

def load_or_create_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║     GITHUB DASHBOARD SETUP WIZARD    ║")
    print("  ╚══════════════════════════════════════╝\n")
    username = input("  GitHub Username : ").strip()
    token    = input("  Personal Access Token (Classic) : ").strip()
    config   = {"username": username, "token": token}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
    os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)
    print("\n  ✓ Config saved to ~/.github_widget_config.json\n")
    return config


# API

def make_request(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("User-Agent", "github-terminal-widget/2.0-visual")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return None, "Bad credentials"
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"Network error"
    except Exception:
        return None, "Unknown error"


def fetch_all_data(username, token):
    profile,       profile_err  = make_request(f"{API_BASE}/users/{username}", token)
    notifications, notif_err    = make_request(f"{API_BASE}/notifications", token)
    repos,         repos_err    = make_request(
        f"{API_BASE}/users/{username}/repos?sort=updated&per_page=8", token
    )
    events,        events_err   = make_request(
        f"{API_BASE}/users/{username}/events?per_page=10", token
    )
    return (
        profile       or {},   profile_err,
        notifications or [],   notif_err,
        repos         or [],   repos_err,
        events        or [],   events_err,
    )


# Color

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    try:
        curses.init_pair(PAIR_HEADER_BG, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(PAIR_SCANLINE,  curses.COLOR_BLACK, -1)
    except Exception:
        pass
    apply_theme_colors()


# SDP

def safe_add(win, y, x, text, attr=0):
    if win is None:
        return
    try:
        max_y, max_x = win.getmaxyx()
        if y < 0 or y >= max_y or x < 0 or x >= max_x:
            return
        available = max_x - x - 1
        if available <= 0:
            return
        text = str(text)[:available]
        win.addstr(y, x, text, attr)
    except curses.error:
        pass


def safe_addch(win, y, x, ch, attr=0):
    try:
        max_y, max_x = win.getmaxyx()
        if y < 0 or y >= max_y or x < 0 or x >= max_x:
            return
        win.addch(y, x, ch, attr)
    except curses.error:
        pass


def hline(win, y, x, ch, n, attr=0):
    for i in range(n):
        safe_add(win, y, x + i, ch, attr)


def vline(win, y, x, ch, n, attr=0):
    for i in range(n):
        safe_add(win, y + i, x, ch, attr)


# Boxes

def draw_box(win, y, x, h, w, title="", title_attr=0, border_attr=0, style="double"):
    if h < 2 or w < 2:
        return
    T = ACTIVE_THEME
    if style == "double":
        tl, tr, bl, br = T["corner_tl"], T["corner_tr"], T["corner_bl"], T["corner_br"]
        hl, vl = T["h_line"], T["v_line"]
    else:
        tl, tr, bl, br = "┌", "┐", "└", "┘"
        hl, vl = "─", "│"

    safe_add(win, y,         x,         tl, border_attr)
    safe_add(win, y,         x + w - 1, tr, border_attr)
    safe_add(win, y + h - 1, x,         bl, border_attr)
    safe_add(win, y + h - 1, x + w - 1, br, border_attr)

    hline(win, y,         x + 1, hl, w - 2, border_attr)
    hline(win, y + h - 1, x + 1, hl, w - 2, border_attr)
    vline(win, y + 1, x,         vl, h - 2, border_attr)
    vline(win, y + 1, x + w - 1, vl, h - 2, border_attr)

    if title:
        label = f"  {title}  "
        max_label = w - 4
        if len(label) > max_label:
            label = label[:max_label]
        lx = x + (w - len(label)) // 2
        safe_add(win, y, lx, label, title_attr or border_attr | curses.A_BOLD)


def draw_box_glow(win, y, x, h, w, title="", glowing=False):
    attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    if glowing:
        attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    draw_box(win, y, x, h, w, title, attr, attr)


def draw_inner_separator(win, y, x, w, border_attr=0):
    T = ACTIVE_THEME
    safe_add(win, y, x,         T["t_right"], border_attr)
    safe_add(win, y, x + w - 1, T["t_left"],  border_attr)
    hline(win, y, x + 1, T["h_line"], w - 2, border_attr)


def draw_vertical_separator(win, y, x, h, border_attr=0):
    T = ACTIVE_THEME
    safe_add(win, y,         x, T["t_down"], border_attr)
    safe_add(win, y + h - 1, x, T["t_up"],   border_attr)
    vline(win, y + 1, x, T["v_line"], h - 2, border_attr)


# Animations

def get_spinner(tick):
    sp = ACTIVE_THEME["spinner"]
    return sp[tick % len(sp)]


def get_wave_char(tick, offset=0):
    wv = ACTIVE_THEME["wave"]
    return wv[(tick + offset) % len(wv)]


def pulse_attr(tick, base_attr):
    if (tick // 4) % 2 == 0:
        return base_attr | curses.A_BOLD
    return base_attr


def glitch_char(ch, tick, probability=0.03):
    glitch_pool = "!@#$%^&*<>?/\\|~`"
    if random.random() < probability and (tick % 7 == 0):
        return random.choice(glitch_pool)
    return ch


def animated_title(text, tick):
    result = ""
    for i, ch in enumerate(text):
        if random.random() < 0.02 and (tick % 5 == 0) and ch != " ":
            result += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        else:
            result += ch
    return result


# The line

def make_sparkline(values, width):
    if not values or width <= 0:
        return " " * width
    chars = ACTIVE_THEME["spark_chars"]
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    result = ""
    sample = values[-width:]
    for v in sample:
        idx = int((v - mn) / rng * (len(chars) - 1))
        result += chars[idx]
    return result.ljust(width)


def fake_sparkline(seed, width, tick):
    random.seed(seed + tick // 10)
    vals = [random.randint(1, 10) for _ in range(width)]
    return make_sparkline(vals, width)


# ProgressBar

def draw_bar(win, y, x, width, value, max_val, label="", show_pct=True):
    if max_val <= 0:
        max_val = 1
    ratio = min(value / max_val, 1.0)
    fill_w = int(ratio * width)
    empty_w = width - fill_w
    T = ACTIVE_THEME
    bar_full  = curses.color_pair(PAIR_BAR_FULL)  | curses.A_BOLD
    bar_empty = curses.color_pair(PAIR_BAR_EMPTY)
    for i in range(fill_w):
        safe_add(win, y, x + i, T["bar_fill"], bar_full)
    for i in range(empty_w):
        safe_add(win, y, x + fill_w + i, T["bar_empty"], bar_empty)
    if show_pct:
        pct_str = f" {int(ratio * 100)}%"
        safe_add(win, y, x + width + 1, pct_str, curses.color_pair(PAIR_MUTED))


def draw_mini_bar(win, y, x, width, value, max_val):
    if max_val <= 0:
        max_val = 1
    ratio = min(value / max_val, 1.0)
    fill_w = int(ratio * width)
    T = ACTIVE_THEME
    for i in range(fill_w):
        safe_add(win, y, x + i, T["bar_fill"], curses.color_pair(PAIR_BAR_FULL))
    for i in range(width - fill_w):
        safe_add(win, y, x + fill_w + i, T["bar_empty"], curses.color_pair(PAIR_BAR_EMPTY))


# Header

ASCII_LOGO = [
    "  ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗ ",
    " ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗",
    " ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝",
    " ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗",
    " ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝",
    "  ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ",
]

MINI_LOGO = [
    " ▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄▄  ",
    "█    █ █          █ █  █ █  █ █  █ █ █    █ ",
    "█       █ ▄ ▄ ▄ █   █   █  █ █  █ █ █    █ ",
    " ████    █▀▀▀▀▀▀█    █ █   █████████  ████  ",
]


def draw_header(win, max_y, max_x, tick, username, theme_name="CYBERPUNK"):
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    warn_attr   = curses.color_pair(PAIR_WARNING) | curses.A_BOLD
    T = ACTIVE_THEME

    header_h = 3
    safe_add(win, 0, 0, T["corner_tl"], border_attr)
    safe_add(win, 0, max_x - 1, T["corner_tr"], border_attr)
    hline(win, 0, 1, T["h_line"], max_x - 2, border_attr)
    vline(win, 1, 0, T["v_line"], header_h - 1, border_attr)
    vline(win, 1, max_x - 1, T["v_line"], header_h - 1, border_attr)

    spinner = get_spinner(tick)
    title_text = "  GITHUB TERMINAL DASHBOARD  "
    title_x = max(2, (max_x - len(title_text)) // 2)
    safe_add(win, 0, title_x, title_text, accent_attr)

    now = datetime.now().strftime("%H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    right_info = f"{spinner} {now} "
    safe_add(win, 1, max_x - len(right_info) - 2, right_info, dim_attr)

    user_label = f"  {T['bullet']} USER: "
    safe_add(win, 1, 2, user_label, dim_attr)
    safe_add(win, 1, 2 + len(user_label), username.upper(), accent_attr)

    theme_label = f" THEME:{theme_name} "
    theme_x = max_x - len(right_info) - len(theme_label) - 3
    if theme_x > 20:
        safe_add(win, 1, theme_x, theme_label, warn_attr)

    version_str = f"v2.0 [{date_str}]"
    version_x = max_x - len(version_str) - len(right_info) - 4
    if version_x > 20:
        safe_add(win, 1, version_x, version_str, dim_attr)

    wave_row = 2
    wave_period = 6
    for col in range(1, max_x - 1):
        phase = (col * 0.3 + tick * 0.5) % (math.pi * 2)
        val = math.sin(phase)
        if val > 0.6:
            ch = "▀"
            attr = accent_attr
        elif val > 0.2:
            ch = "·"
            attr = border_attr
        else:
            ch = T["h_line"]
            attr = dim_attr
        safe_add(win, wave_row, col, ch, attr)

    safe_add(win, wave_row, 0, T["t_right"], border_attr)
    safe_add(win, wave_row, max_x - 1, T["t_left"], border_attr)

    return header_h + 1


# Footer

def draw_footer(win, max_y, max_x, tick, status_msg=""):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    accent_attr = curses.color_pair(PAIR_ACCENT)
    warn_attr   = curses.color_pair(PAIR_WARNING)

    fy = max_y - 2
    safe_add(win, fy, 0, T["t_right"], border_attr)
    safe_add(win, fy, max_x - 1, T["t_left"], border_attr)
    hline(win, fy, 1, T["h_line"], max_x - 2, border_attr)

    safe_add(win, max_y - 1, 0, T["corner_bl"], border_attr)
    safe_add(win, max_y - 1, max_x - 1, T["corner_br"], border_attr)
    hline(win, max_y - 1, 1, T["h_line"], max_x - 2, border_attr)

    keys = [
        ("[Q]", "QUIT"),
        ("[R]", "REFRESH"),
        ("[T]", "THEME"),
        ("[↑↓]", "SCROLL"),
    ]
    kx = 2
    for key, label in keys:
        safe_add(win, max_y - 1, kx, key, accent_attr)
        kx += len(key)
        safe_add(win, max_y - 1, kx, f" {label}  ", dim_attr)
        kx += len(label) + 3

    uptime_str = f" {T['clock']} LIVE "
    safe_add(win, max_y - 1, max_x - len(uptime_str) - 2, uptime_str,
             pulse_attr(tick, curses.color_pair(PAIR_SUCCESS)))

    if status_msg:
        sm = f" {status_msg} "[:max_x - 4]
        sx = max(2, (max_x - len(sm)) // 2)
        safe_add(win, fy, sx, sm, warn_attr)


# Profile

def draw_profile_panel(win, y, x, h, w, profile, err, tick):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    val_attr    = curses.color_pair(PAIR_VALUE)
    warn_attr   = curses.color_pair(PAIR_WARNING) | curses.A_BOLD
    hi_attr     = curses.color_pair(PAIR_HIGHLIGHT) | curses.A_BOLD

    draw_box(win, y, x, h, w,
             f" {T['bullet']} PROFILE OVERVIEW ",
             accent_attr, border_attr)

    ix = x + 2
    row = y + 1

    if err:
        safe_add(win, row, ix, f"{T['dot']} ERROR: {err}"[:w-4], warn_attr)
        return

    login    = profile.get("login", "—")
    name     = profile.get("name") or login
    bio      = profile.get("bio") or "No bio provided"
    location = profile.get("location") or "Unknown"
    company  = profile.get("company") or ""
    blog     = profile.get("blog") or ""
    repos    = profile.get("public_repos", 0)
    gists    = profile.get("public_gists", 0)
    followers = profile.get("followers", 0)
    following = profile.get("following", 0)
    created  = profile.get("created_at", "")
    hireable = profile.get("hireable", False)
    t_repos  = profile.get("total_private_repos", 0)

    avatar_lines = build_avatar_art(login, tick)
    av_x = x + w - 12
    for i, al in enumerate(avatar_lines[:min(4, h-2)]):
        safe_add(win, row + i, av_x, al[:10], curses.color_pair(PAIR_BORDER))

    name_display = name[:w - 16]
    safe_add(win, row, ix, name_display, accent_attr | curses.A_BOLD)

    if hireable and row + 1 < y + h - 1:
        safe_add(win, row, ix + len(name_display) + 1,
                 " HIREABLE ", curses.color_pair(PAIR_SUCCESS) | curses.A_REVERSE)

    row += 1
    safe_add(win, row, ix, f"@{login}"[:w-4], dim_attr)
    row += 1

    if row < y + h - 2:
        bio_lines = wrap_text(bio, w - 4)
        for bl in bio_lines[:2]:
            if row < y + h - 2:
                safe_add(win, row, ix, bl, val_attr)
                row += 1

    if location and row < y + h - 2:
        safe_add(win, row, ix, f"⌖ {location}"[:w-4], dim_attr)
        row += 1

    if company and row < y + h - 2:
        safe_add(win, row, ix, f"▣ {company}"[:w-4], dim_attr)
        row += 1

    row += 1

    if row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1

    stats = [
        (T["star"],  "REPOS",     repos,     50),
        ("◎",        "FOLLOWERS", followers, 1000),
        ("◉",        "FOLLOWING", following, 500),
        ("◈",        "GISTS",     gists,     50),
    ]

    for icon, label, val, max_val in stats:
        if row >= y + h - 2:
            break
        bar_w = max(1, w - 18)
        safe_add(win, row, ix,     f"{icon} {label:<9}", dim_attr)
        safe_add(win, row, ix + 11, f"{val:>5}", hi_attr)
        if bar_w > 3:
            draw_mini_bar(win, row, ix + 17, min(bar_w, w - ix - 18), val, max_val)
        row += 1

    if created and row < y + h - 2:
        try:
            dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
            age_days = (datetime.utcnow() - dt).days
            age_years = age_days // 365
            safe_add(win, row, ix,
                     f"{T['clock']} Member for {age_years}y {age_days % 365}d"[:w-4],
                     dim_attr)
        except Exception:
            pass


def build_avatar_art(login, tick):
    seed = sum(ord(c) for c in login)
    random.seed(seed)
    chars = ["▓", "▒", "░", "█", "▄", "▀"]
    lines = []
    for r in range(4):
        row_str = ""
        for c in range(8):
            random.seed(seed + r * 8 + c + (tick // 20))
            row_str += random.choice(chars)
        lines.append(row_str)
    return lines


def wrap_text(text, width):
    if not text or width <= 0:
        return []
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= width:
            current = (current + " " + w).strip()
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


# Noifications

def draw_notifications_panel(win, y, x, h, w, notifications, err, tick):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    val_attr    = curses.color_pair(PAIR_VALUE)
    warn_attr   = curses.color_pair(PAIR_WARNING) | curses.A_BOLD
    err_attr    = curses.color_pair(PAIR_ERROR)   | curses.A_BOLD
    hi_attr     = curses.color_pair(PAIR_HIGHLIGHT)| curses.A_BOLD

    total = len(notifications)
    glow  = total > 0

    title_attr = warn_attr if glow else accent_attr
    draw_box(win, y, x, h, w,
             f" {T['bullet']} NOTIFICATIONS ",
             title_attr, border_attr)

    ix  = x + 2
    row = y + 1

    if err:
        safe_add(win, row, ix, f"{T['dot']} {err}"[:w-4], err_attr)
        return

    badge_w = 14
    badge_x = x + (w - badge_w) // 2
    if total == 0:
        safe_add(win, row, badge_x, f"  ✓ ALL CLEAR  ", accent_attr | curses.A_BOLD)
    else:
        badge = f"  {total} UNREAD  "
        safe_add(win, row, badge_x, badge[:w-4],
                 pulse_attr(tick, warn_attr) | curses.A_REVERSE)

    row += 1

    type_counts = {}
    repo_counts = {}
    for n in notifications:
        ntype = n.get("subject", {}).get("type", "Unknown")
        repo  = n.get("repository", {}).get("name", "")
        type_counts[ntype] = type_counts.get(ntype, 0) + 1
        repo_counts[repo]  = repo_counts.get(repo, 0) + 1

    if type_counts and row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1
        tc_x = ix
        for ntype, cnt in list(type_counts.items())[:4]:
            label = f"{ntype[:6]}:{cnt} "
            if tc_x + len(label) < x + w - 2:
                safe_add(win, row, tc_x, f"{cnt}", hi_attr)
                safe_add(win, row, tc_x + len(str(cnt)), f" {ntype[:6]}", dim_attr)
                tc_x += len(label) + 1
        row += 1

    if row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1

    type_icons = {
        "PullRequest": "⑂",
        "Issue":       "◎",
        "Release":     "▣",
        "Commit":      "◆",
        "Discussion":  "◉",
    }

    reason_colors = {
        "mention":    PAIR_WARNING,
        "assign":     PAIR_ACCENT,
        "review_requested": PAIR_HIGHLIGHT,
        "subscribed": PAIR_MUTED,
    }

    max_show = min(total, (h - (row - y) - 2))
    for i, notif in enumerate(notifications[:max_show]):
        if row >= y + h - 2:
            break
        subject = notif.get("subject", {})
        title   = subject.get("title", "(no title)")
        ntype   = subject.get("type", "")
        repo    = notif.get("repository", {}).get("name", "")
        reason  = notif.get("reason", "")
        unread  = notif.get("unread", True)

        icon = type_icons.get(ntype, T["dot"])
        reason_pair = reason_colors.get(reason, PAIR_VALUE)
        item_attr = curses.color_pair(reason_pair)
        if not unread:
            item_attr = dim_attr

        prefix = f"{icon} "
        avail  = w - 4 - len(prefix)
        if len(title) > avail:
            title = title[:avail - 1] + "…"
        safe_add(win, row, ix, prefix, item_attr | curses.A_BOLD)
        safe_add(win, row, ix + len(prefix), title, item_attr)
        row += 1

        if repo and row < y + h - 2:
            repo_str = f"   └ {repo}"[:w-4]
            safe_add(win, row, ix, repo_str, dim_attr)
            row += 1

    if total > max_show and row < y + h - 2:
        safe_add(win, row, ix, f"  … +{total - max_show} more", dim_attr)


# Repo panel

def draw_repos_panel(win, y, x, h, w, repos, err, tick, scroll_offset=0):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER)  | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT)  | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    val_attr    = curses.color_pair(PAIR_VALUE)
    warn_attr   = curses.color_pair(PAIR_WARNING) | curses.A_BOLD
    hi_attr     = curses.color_pair(PAIR_HIGHLIGHT)| curses.A_BOLD
    err_attr    = curses.color_pair(PAIR_ERROR)   | curses.A_BOLD

    draw_box(win, y, x, h, w,
             f" {T['star']} RECENTLY UPDATED REPOSITORIES ",
             accent_attr, border_attr)

    ix  = x + 2
    row = y + 1

    if err:
        safe_add(win, row, ix, f"{T['dot']} {err}"[:w-4], err_attr)
        return

    if not repos:
        safe_add(win, row, ix, "No repositories found.", dim_attr)
        return

    max_stars  = max((r.get("stargazers_count", 0) for r in repos), default=1) or 1
    max_forks  = max((r.get("forks_count", 0) for r in repos), default=1) or 1
    max_issues = max((r.get("open_issues_count", 0) for r in repos), default=1) or 1

    name_w   = min(28, w // 3)
    stats_w  = 22
    bar_w    = max(4, w - name_w - stats_w - 8)

    hdr_attr = dim_attr | curses.A_UNDERLINE
    hdr = f"{'REPOSITORY':<{name_w}} {'★':>4} {'⑂':>4} {'!':>4}  {'ACTIVITY':<{bar_w}}"
    safe_add(win, row, ix, hdr[:w-4], hdr_attr)
    row += 1

    if row < y + h - 1:
        hline(win, row, ix, "╌", w - 4, dim_attr)
        row += 1

    lang_colors = {
        "Python":     PAIR_WARNING,
        "JavaScript": PAIR_HIGHLIGHT,
        "TypeScript": PAIR_ACCENT,
        "Go":         PAIR_BORDER,
        "Rust":       PAIR_ERROR,
        "Java":       PAIR_WARNING,
        "C++":        PAIR_BORDER,
        "C":          PAIR_MUTED,
        "Ruby":       PAIR_ERROR,
        "Swift":      PAIR_ACCENT,
        "Kotlin":     PAIR_HIGHLIGHT,
        "Shell":      PAIR_SUCCESS,
    }

    for i, repo in enumerate(repos[scroll_offset:]):
        if row >= y + h - 2:
            break

        name     = repo.get("name", "—")
        stars    = repo.get("stargazers_count", 0)
        forks    = repo.get("forks_count", 0)
        issues   = repo.get("open_issues_count", 0)
        lang     = repo.get("language") or ""
        private  = repo.get("private", False)
        fork     = repo.get("fork", False)
        archived = repo.get("archived", False)
        desc     = repo.get("description") or ""
        updated  = repo.get("updated_at", "")
        topics   = repo.get("topics", [])

        is_highlighted = (tick // 8) % len(repos) == i

        prefix = ""
        if private:
            prefix = T["lock"] + " "
        elif fork:
            prefix = T["fork"] + " "
        elif archived:
            prefix = "⊘ "
        else:
            prefix = T["open"] + " "

        name_str = (prefix + name)[:name_w]
        row_attr = hi_attr if is_highlighted else val_attr

        safe_add(win, row, ix, name_str, row_attr | curses.A_BOLD)
        safe_add(win, row, ix + name_w + 1, f"{stars:>4}", curses.color_pair(PAIR_WARNING))
        safe_add(win, row, ix + name_w + 6, f"{forks:>4}", curses.color_pair(PAIR_BORDER))
        safe_add(win, row, ix + name_w + 11,
                 f"{issues:>4}",
                 curses.color_pair(PAIR_ERROR) if issues > 0 else dim_attr)

        spark_x = ix + name_w + 17
        spark_w = min(bar_w, w - spark_x - 3)
        if spark_w > 2:
            spark = fake_sparkline(i * 37 + sum(ord(c) for c in name), spark_w, tick)
            spark_attr = curses.color_pair(PAIR_ACCENT) if is_highlighted else dim_attr
            safe_add(win, row, spark_x, spark[:spark_w], spark_attr)

        row += 1

        if desc and row < y + h - 2:
            desc_str = f"   {desc}"[:w-4]
            safe_add(win, row, ix, desc_str, dim_attr)
            row += 1

        if (lang or topics) and row < y + h - 2:
            meta_x = ix + 3
            if lang:
                lang_pair = lang_colors.get(lang, PAIR_MUTED)
                lang_str = f"◈ {lang}"
                safe_add(win, row, meta_x, lang_str,
                         curses.color_pair(lang_pair) | curses.A_BOLD)
                meta_x += len(lang_str) + 2
            for topic in topics[:3]:
                if meta_x + len(topic) + 3 < x + w - 2:
                    safe_add(win, row, meta_x, f"[{topic}]", dim_attr)
                    meta_x += len(topic) + 3
            if updated:
                try:
                    dt = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")
                    age = (datetime.utcnow() - dt).days
                    age_str = f"  {T['clock']} {age}d ago" if age > 0 else f"  {T['clock']} today"
                    safe_add(win, row, x + w - len(age_str) - 3, age_str, dim_attr)
                except Exception:
                    pass
            row += 1

        if i < len(repos) - 1 and row < y + h - 2:
            hline(win, row, ix, "┄", w - 4, dim_attr)
            row += 1


# Activity

def draw_activity_panel(win, y, x, h, w, events, err, tick):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER)  | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT)  | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    val_attr    = curses.color_pair(PAIR_VALUE)
    warn_attr   = curses.color_pair(PAIR_WARNING) | curses.A_BOLD
    err_attr    = curses.color_pair(PAIR_ERROR)   | curses.A_BOLD
    hi_attr     = curses.color_pair(PAIR_HIGHLIGHT)

    draw_box(win, y, x, h, w,
             f" {T['clock']} RECENT ACTIVITY ",
             accent_attr, border_attr)

    ix  = x + 2
    row = y + 1

    if err:
        safe_add(win, row, ix, f"{T['dot']} {err}"[:w-4], err_attr)
        return

    event_icons = {
        "PushEvent":             ("▶", PAIR_ACCENT),
        "PullRequestEvent":      ("⑂", PAIR_HIGHLIGHT),
        "IssuesEvent":           ("◎", PAIR_WARNING),
        "WatchEvent":            ("★", PAIR_WARNING),
        "ForkEvent":             ("⑂", PAIR_BORDER),
        "CreateEvent":           ("◆", PAIR_SUCCESS),
        "DeleteEvent":           ("✕", PAIR_ERROR),
        "IssueCommentEvent":     ("◉", PAIR_MUTED),
        "PullRequestReviewEvent":("◈", PAIR_ACCENT),
        "ReleaseEvent":          ("▣", PAIR_HIGHLIGHT),
    }

    type_tally = {}
    for ev in events:
        etype = ev.get("type", "Unknown")
        type_tally[etype] = type_tally.get(etype, 0) + 1

    if type_tally and row < y + h - 3:
        bar_section_w = w - 4
        max_count = max(type_tally.values()) or 1
        top_types = sorted(type_tally.items(), key=lambda kv: -kv[1])[:4]
        for etype, cnt in top_types:
            if row >= y + h - 3:
                break
            icon, pair = event_icons.get(etype, (T["dot"], PAIR_MUTED))
            label = etype.replace("Event", "")[:10]
            safe_add(win, row, ix, f"{icon} {label:<10}", curses.color_pair(pair))
            bx = ix + 13
            bw = max(2, w - 18)
            draw_mini_bar(win, row, bx, bw, cnt, max_count)
            safe_add(win, row, bx + bw + 1, f"{cnt}", curses.color_pair(pair) | curses.A_BOLD)
            row += 1

    if row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1

    for ev in events[:max(0, h - (row - y) - 2)]:
        if row >= y + h - 2:
            break
        etype  = ev.get("type", "")
        repo   = ev.get("repo", {}).get("name", "")
        created = ev.get("created_at", "")
        icon, pair = event_icons.get(etype, (T["dot"], PAIR_MUTED))
        ev_attr = curses.color_pair(pair)

        label = etype.replace("Event", "")[:8]
        repo_short = repo.split("/")[-1][:w - 16]
        age_str = ""
        if created:
            try:
                dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
                mins = int((datetime.utcnow() - dt).total_seconds() / 60)
                if mins < 60:
                    age_str = f"{mins}m"
                elif mins < 1440:
                    age_str = f"{mins//60}h"
                else:
                    age_str = f"{mins//1440}d"
            except Exception:
                pass

        line = f"{icon} {label:<8} {repo_short}"
        safe_add(win, row, ix, line[:w-4-len(age_str)-2], ev_attr)
        if age_str:
            safe_add(win, row, x + w - len(age_str) - 3, age_str, dim_attr)
        row += 1


# Stats

def draw_stats_panel(win, y, x, h, w, repos, profile, tick):
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER)  | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT)  | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    val_attr    = curses.color_pair(PAIR_VALUE)
    hi_attr     = curses.color_pair(PAIR_HIGHLIGHT)| curses.A_BOLD
    warn_attr   = curses.color_pair(PAIR_WARNING)

    draw_box(win, y, x, h, w,
             f" {T['dot']} REPO STATS ",
             accent_attr, border_attr)

    ix  = x + 2
    row = y + 1

    lang_map = {}
    total_stars  = 0
    total_forks  = 0
    total_issues = 0
    total_size   = 0

    for repo in repos:
        lang = repo.get("language") or "Other"
        lang_map[lang] = lang_map.get(lang, 0) + 1
        total_stars  += repo.get("stargazers_count", 0)
        total_forks  += repo.get("forks_count", 0)
        total_issues += repo.get("open_issues_count", 0)
        total_size   += repo.get("size", 0)

    totals = [
        (T["star"],  "Stars",  total_stars),
        ("⑂",        "Forks",  total_forks),
        ("◎",        "Issues", total_issues),
    ]

    for icon, label, val in totals:
        if row >= y + h - 2:
            break
        safe_add(win, row, ix,      f"{icon} {label:<7}", dim_attr)
        safe_add(win, row, ix + 10, f"{val:>5}", hi_attr)
        spark = fake_sparkline(hash(label) % 999, w - 20, tick)
        safe_add(win, row, ix + 16, spark[:max(0, w-20)],
                 curses.color_pair(PAIR_BORDER))
        row += 1

    if row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1

    if lang_map and row < y + h - 2:
        safe_add(win, row, ix, "LANGUAGES", dim_attr | curses.A_BOLD)
        row += 1
        total_repos = sum(lang_map.values()) or 1
        sorted_langs = sorted(lang_map.items(), key=lambda kv: -kv[1])
        for lang, cnt in sorted_langs[:min(4, h - (row - y) - 2)]:
            if row >= y + h - 2:
                break
            pct = cnt / total_repos
            bar_w = max(2, w - 16)
            fill  = int(pct * bar_w)
            safe_add(win, row, ix, f"{lang[:8]:<8}", accent_attr)
            safe_add(win, row, ix + 9, f"{int(pct*100):>3}%", hi_attr)
            draw_mini_bar(win, row, ix + 14, fill, fill, fill or 1)
            row += 1

    if total_size and row < y + h - 2:
        draw_inner_separator(win, row, x, w, border_attr)
        row += 1
        if total_size >= 1024:
            size_str = f"{total_size/1024:.1f} MB"
        else:
            size_str = f"{total_size} KB"
        safe_add(win, row, ix, f"Total Size  {size_str}", dim_attr)


# rain effect

MATRIX_CHARS = "01アイウエオカキクケコサシスセソタチツテト"

class MatrixColumn:
    def __init__(self, x, max_y):
        self.x = x
        self.max_y = max_y
        self.y = random.randint(0, max_y)
        self.speed = random.uniform(0.3, 1.0)
        self.length = random.randint(3, 8)
        self.chars = [random.choice(MATRIX_CHARS) for _ in range(self.length)]
        self.phase = random.uniform(0, math.pi * 2)

    def update(self, tick):
        self.y = (self.y + self.speed) % (self.max_y + self.length)
        if random.random() < 0.1:
            idx = random.randint(0, self.length - 1)
            self.chars[idx] = random.choice(MATRIX_CHARS)

    def draw(self, win, tick):
        for i, ch in enumerate(self.chars):
            cy = int(self.y) - i
            if 0 <= cy < self.max_y:
                if i == 0:
                    attr = curses.color_pair(PAIR_GLOW) | curses.A_BOLD
                elif i < 2:
                    attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
                else:
                    attr = curses.color_pair(PAIR_MUTED)
                safe_add(win, cy, self.x, ch, attr)


# Load

def draw_loading(win, tick):
    win.clear()
    max_y, max_x = win.getmaxyx()
    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD
    accent_attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)
    warn_attr   = curses.color_pair(PAIR_WARNING)| curses.A_BOLD

    for col in range(0, max_x, 3):
        height = int(abs(math.sin((col * 0.1 + tick * 0.05))) * (max_y // 2))
        for row in range(max_y - height, max_y):
            ch_idx = int(abs(math.sin(row + tick * 0.1)) * (len(MATRIX_CHARS) - 1))
            safe_add(win, row, col, MATRIX_CHARS[ch_idx], dim_attr)

    cy = max_y // 2

    logo_y = cy - 5
    if max_x > 52:
        logo_x = max(0, (max_x - 50) // 2)
        for i, line in enumerate(ASCII_LOGO):
            if logo_y + i >= 0 and logo_y + i < max_y:
                safe_add(win, logo_y + i, logo_x, line[:max_x - logo_x - 1], accent_attr)

    spinner = get_spinner(tick)
    stages = [
        "Connecting to GitHub API",
        "Fetching user profile",
        "Loading notifications",
        "Scanning repositories",
        "Parsing activity feed",
        "Rendering dashboard",
    ]
    stage_idx = (tick // 6) % len(stages)
    stage_msg = f"  {spinner}  {stages[stage_idx]}...  "
    msg_x = max(0, (max_x - len(stage_msg)) // 2)
    safe_add(win, cy + 2, msg_x, stage_msg, warn_attr)

    bar_w  = min(40, max_x - 10)
    bar_x  = max(0, (max_x - bar_w) // 2)
    filled = int((tick % 30) / 30 * bar_w)
    safe_add(win, cy + 4, bar_x - 1, "[", border_attr)
    safe_add(win, cy + 4, bar_x + bar_w, "]", border_attr)
    for i in range(bar_w):
        if i < filled:
            safe_add(win, cy + 4, bar_x + i, T["bar_fill"],
                     curses.color_pair(PAIR_BAR_FULL) | curses.A_BOLD)
        else:
            safe_add(win, cy + 4, bar_x + i, T["bar_empty"],
                     curses.color_pair(PAIR_BAR_EMPTY))

    hint = "Press any key to cancel"
    hint_x = max(0, (max_x - len(hint)) // 2)
    safe_add(win, cy + 6, hint_x, hint, dim_attr)

    win.refresh()


# dih size of a peanut

def draw_too_small(win, max_y, max_x, tick):
    win.clear()
    T = ACTIVE_THEME
    accent_attr = curses.color_pair(PAIR_ACCENT) | curses.A_BOLD
    warn_attr   = curses.color_pair(PAIR_WARNING)| curses.A_BOLD
    dim_attr    = curses.color_pair(PAIR_MUTED)

    cy = max_y // 2
    cx = max_x // 2

    spinner = get_spinner(tick)
    msgs = [
        (f"{spinner} TERMINAL TOO SMALL {spinner}",  warn_attr),
        ("",                                          0),
        (f"Required : 80 cols × 24 rows",             dim_attr),
        (f"Current  : {max_x} cols × {max_y} rows",  accent_attr),
        ("",                                          0),
        ("Please resize your terminal window",        dim_attr),
        ("then press any key to continue",            dim_attr),
    ]

    for i, (msg, attr) in enumerate(msgs):
        mx = max(0, cx - len(msg) // 2)
        my = cy - len(msgs) // 2 + i
        if 0 <= my < max_y:
            safe_add(win, my, mx, msg[:max_x-1], attr)

    win.refresh()


# Main layout

def render_full_dashboard(win, data, tick, scroll_offset=0, theme_name="CYBERPUNK"):
    max_y, max_x = win.getmaxyx()
    win.clear()

    (profile, profile_err,
     notifications, notif_err,
     repos, repos_err,
     events, events_err) = data

    username = profile.get("login", "user")

    header_bottom = draw_header(win, max_y, max_x, tick, username, theme_name)

    content_y = header_bottom
    content_h = max_y - content_y - 2
    footer_y  = max_y - 2

    draw_footer(win, max_y, max_x, tick)

    T = ACTIVE_THEME
    border_attr = curses.color_pair(PAIR_BORDER) | curses.A_BOLD

    left_w    = max_x // 2
    right_w   = max_x - left_w
    top_h     = content_h // 2
    bottom_h  = content_h - top_h

    top_left_w  = left_w
    top_right_w = right_w

    bottom_left_w  = max_x * 2 // 3
    bottom_right_w = max_x - bottom_left_w

    draw_vertical_separator(win,
                            content_y, left_w,
                            top_h, border_attr)

    draw_vertical_separator(win,
                            content_y + top_h, bottom_left_w,
                            bottom_h, border_attr)

    draw_profile_panel(win,
                       content_y, 0,
                       top_h, top_left_w,
                       profile, profile_err, tick)

    draw_notifications_panel(win,
                             content_y, left_w,
                             top_h, top_right_w,
                             notifications, notif_err, tick)

    draw_repos_panel(win,
                     content_y + top_h, 0,
                     bottom_h, bottom_left_w,
                     repos, repos_err, tick, scroll_offset)

    stats_h = bottom_h // 2
    act_h   = bottom_h - stats_h

    draw_stats_panel(win,
                     content_y + top_h, bottom_left_w,
                     stats_h, bottom_right_w,
                     repos, profile, tick)

    draw_activity_panel(win,
                        content_y + top_h + stats_h, bottom_left_w,
                        act_h, bottom_right_w,
                        events, events_err, tick)

    win.refresh()

# Main Loop

def run_dashboard(stdscr, config):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(80)
    stdscr.keypad(True)
    init_colors()

    username = config["username"]
    token    = config["token"]

    data         = None
    loading      = True
    tick         = 0
    scroll       = 0
    last_refresh = 0
    refresh_interval = 300
    status_msg   = ""

    fetch_done   = threading.Event()
    fetch_result = [None]

    def do_fetch():
        fetch_result[0] = fetch_all_data(username, token)
        fetch_done.set()

    fetch_thread = threading.Thread(target=do_fetch, daemon=True)
    fetch_thread.start()

    while True:
        max_y, max_x = stdscr.getmaxyx()

        if max_y < 24 or max_x < 80:
            draw_too_small(stdscr, max_y, max_x, tick)
            key = stdscr.getch()
            tick += 1
            continue

        if loading:
            if not fetch_done.is_set():
                draw_loading(stdscr, tick)
            else:
                data         = fetch_result[0]
                loading      = False
                last_refresh = time.time()
                status_msg   = f"Last refreshed at {datetime.now().strftime('%H:%M:%S')}"
        else:
            now = time.time()
            if now - last_refresh > refresh_interval:
                fetch_done.clear()
                fetch_result[0] = None
                fetch_thread = threading.Thread(target=do_fetch, daemon=True)
                fetch_thread.start()
                loading    = True
                status_msg = "Auto-refreshing..."
                continue

            max_scroll = max(0, len(data[4]) - 3) if data else 0
            render_full_dashboard(stdscr, data, tick, scroll,
                                  ACTIVE_THEME["name"])

        key = stdscr.getch()
        if key != -1:
            if key in (ord('q'), ord('Q'), 27):
                break
            elif key in (ord('r'), ord('R')):
                loading = True
                fetch_done.clear()
                fetch_result[0] = None
                fetch_thread = threading.Thread(target=do_fetch, daemon=True)
                fetch_thread.start()
                status_msg = "Refreshing..."
                scroll = 0
            elif key in (ord('t'), ord('T')):
                new_name = next_theme()
                status_msg = f"Theme: {new_name}"
            elif key in (curses.KEY_DOWN, ord('j'), ord('J')):
                max_scroll = max(0, len(data[4]) - 3) if data else 0
                scroll = min(scroll + 1, max_scroll)
            elif key in (curses.KEY_UP, ord('k'), ord('K')):
                scroll = max(scroll - 1, 0)

        tick += 1


# Entry

def main():
    try:
        config = load_or_create_config()
    except (KeyboardInterrupt, EOFError):
        print("\n  Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Config error: {e}")
        sys.exit(1)

    try:
        curses.wrapper(run_dashboard, config)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n  GitHub Dashboard closed.\n")


if __name__ == "__main__":
    main()
