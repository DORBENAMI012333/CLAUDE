#!/usr/bin/env python3
import sys
import json
import datetime
import hashlib
from pathlib import Path

WORDS = [
    "crane", "slate", "audio", "raise", "arose", "stare", "snare", "irate",
    "stale", "arise", "least", "alert", "later", "alter", "regal", "glare",
    "large", "lager", "lager", "oater", "resat", "tears", "tares", "rates",
    "aster", "earns", "nears", "saner", "snare", "learn", "renal", "lance",
    "clean", "ocean", "canoe", "alone", "atone", "oaken", "knave", "naive",
    "avail", "villa", "rival", "viral", "trial", "trail", "grail", "grail",
    "brail", "braid", "brain", "train", "grain", "drain", "spain", "plain",
    "plaid", "plait", "plant", "bland", "brand", "grand", "grind", "grins",
    "bring", "brink", "drink", "rinks", "rings", "reign", "feign", "feline",
    "angel", "angle", "glean", "panel", "penal", "plane", "planer", "repay",
    "repeal", "pearl", "early", "layer", "relay", "leary", "lathe", "lithe",
    "tithe", "title", "tidal", "ideal", "ideas", "stead", "beads", "reads",
    "reeds", "creed", "greed", "treed", "freed", "breed", "bleed", "speed",
    "spade", "blade", "grade", "trade", "brave", "crave", "grave", "gravel",
    "ravel", "raven", "maven", "haven", "haves", "shave", "shave", "slave",
    "stave", "starve", "carve", "curve", "curse", "purse", "nurse", "terse",
    "verse", "avert", "overt", "inert", "inter", "enter", "cento", "scent",
    "cents", "dents", "rents", "tents", "vents", "event", "seven", "scene",
    "green", "greet", "sleet", "fleet", "sweet", "tweet", "swept", "crept",
    "creep", "sleep", "steep", "steer", "sheer", "cheer", "sneer", "spear",
    "smear", "swear", "sweat", "treat", "tread", "bread", "dread", "spread",
    "beady", "ready", "heady", "leads", "beads", "meads", "heads",
    "stead", "steam", "cream", "dream", "seam", "realm", "reams", "teams",
    "trams", "clams", "claps", "clasp", "crash", "crass", "brass", "grace",
    "trace", "brace", "place", "space", "spice", "slice", "twice", "price",
    "pride", "bride", "brine", "shrine", "spine", "swine", "shine", "whine",
    "white", "write", "quite", "quiet", "queen", "queer", "quest", "guest",
    "gusto", "gust", "gruff", "bluff", "fluff", "stuff", "stung", "sting",
    "sling", "cling", "fling", "flung", "plumb", "plume", "flume", "flute",
    "brute", "prune", "prude", "pride", "gripe", "tripe", "trice", "price", "prick",
    "trick", "track", "crack", "stack", "snack", "slack", "black", "bland",
    "blank", "clank", "plank", "frank", "flank", "thank", "think", "thine",
    "thing", "thick", "chick", "chuck", "cluck", "stuck", "pluck", "truck",
    "track", "trace", "truce", "prize", "prose", "probe",
    "globe", "grove", "prove", "crave", "shove", "above", "glove",
    "clove", "drove", "trove", "stove", "stone", "phone", "prone", "prong",
    "wrong", "among", "along", "aloft", "aloof", "about", "stout", "snout",
    "trout", "grout", "scout", "shout", "clout", "count", "mount", "fount",
    "blunt", "grunt", "front", "frost", "trust", "truss", "crush", "brush",
    "blush", "flush", "plush", "slush", "froth", "broth", "cloth", "cloth",
    "sloth", "broil", "coils", "foils", "roils", "toils", "boils", "spoil",
    "spill", "skill", "swill", "trill", "grill", "drill", "frill", "quill",
    "guilt", "built", "quilt", "wilt", "jolt", "bolt", "molt", "dolt",
    "colt", "volt", "folk", "yolk", "hulk", "sulk", "bulk", "silk", "bilk",
    "milk", "melt", "felt", "belt", "dealt", "knelt", "whelp", "yelp",
    "kelp", "help", "helm", "realm", "qualm", "psalm", "balm", "palm",
    "calm", "alms", "arms", "harm", "farm", "form", "fort", "fork", "fore",
    "force", "forge", "gorge", "purge", "surge", "verge", "merge", "serge",
    "stern", "fern", "kern", "yearn", "learn", "earth", "hearth", "dearth",
    "worth", "north", "birth", "berth", "mirth", "girth", "filth", "fifth",
    "swift", "shift", "drift", "sift", "gift", "gust", "dusk", "dust",
    "bust", "rust", "must", "musk", "tusk", "desk", "flask", "mask", "task",
    "whisk", "brisk", "frisk", "risk", "disk", "disc", "drip", "grip",
    "trip", "clip", "chip", "skip", "ship", "whip", "drips", "grips",
    "trips", "crisp", "wispy", "misty", "dusty", "rusty", "lusty", "gusty",
    "busty", "musty", "nasty", "hasty", "pasty", "tasty", "vasty", "waist",
    "heist", "twist", "wrist", "exist", "moist", "hoist", "foist", "joist",
    "joust", "burst", "first", "thirst", "worst", "horst", "ghost", "boast",
    "coast", "roast", "toast", "feast", "beast", "least", "yeast", "leash",
    "peach", "beach", "reach", "teach", "bleach", "preach", "breach", "perch",
    "lurch", "church", "birch", "march", "parch", "starch", "harsh", "marsh",
    "flash", "clash", "crash", "trash", "brash", "gnash", "slash", "plash",
]

# Filter to exactly 5-letter words, dedupe
WORDS = sorted(set(w.lower() for w in WORDS if len(w) == 5))

VALID_GUESSES = set(WORDS)

# ANSI colors
GREEN  = "\033[42m\033[30m"
YELLOW = "\033[43m\033[30m"
GRAY   = "\033[100m\033[37m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

STATS_FILE = Path.home() / ".wordle_stats.json"


def load_stats():
    if STATS_FILE.exists():
        return json.loads(STATS_FILE.read_text())
    return {"played": 0, "wins": 0, "streak": 0, "max_streak": 0, "dist": {str(i): 0 for i in range(1, 7)}}


def save_stats(stats):
    STATS_FILE.write_text(json.dumps(stats))


def daily_word():
    today = datetime.date.today().isoformat()
    h = int(hashlib.md5(today.encode()).hexdigest(), 16)
    return WORDS[h % len(WORDS)]


def score_guess(guess, answer):
    result = ["gray"] * 5
    answer_chars = list(answer)
    # First pass: greens
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "green"
            answer_chars[i] = None
    # Second pass: yellows
    for i in range(5):
        if result[i] == "green":
            continue
        if guess[i] in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(guess[i])] = None
    return result


def render_tile(ch, color):
    c = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}[color]
    return f"{c} {ch.upper()} {RESET}"


def render_guess(guess, result):
    return " ".join(render_tile(ch, col) for ch, col in zip(guess, result))


def render_keyboard(used):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    lines = []
    for row in rows:
        parts = []
        for ch in row:
            if ch in used:
                color = used[ch][0]
                c = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}[color]
                parts.append(f"{c}{ch.upper()}{RESET}")
            else:
                parts.append(f"{BOLD}{ch.upper()}{RESET}")
        lines.append("  ".join(parts))
    return "\n".join(lines)


def print_header():
    print(f"\n{BOLD}  W O R D L E{RESET}  {DIM}terminal edition{RESET}\n")


def print_board(guesses, results, current_row):
    for i in range(6):
        if i < len(guesses):
            print("  " + render_guess(guesses[i], results[i]))
        else:
            print(f"  {DIM}[ ] [ ] [ ] [ ] [ ]{RESET}")
    print()


def print_stats(stats):
    print(f"\n{BOLD}Your Stats{RESET}")
    print(f"  Played: {stats['played']}  Wins: {stats['wins']}  "
          f"Streak: {stats['streak']}  Best: {stats['max_streak']}")
    if stats['wins'] > 0:
        print(f"\n  {BOLD}Guess distribution:{RESET}")
        max_val = max(int(v) for v in stats['dist'].values()) or 1
        for k in "123456":
            bar_len = int(stats['dist'][k] / max_val * 20)
            bar = "█" * bar_len
            print(f"  {k}  {GREEN}{bar}{RESET} {stats['dist'][k]}")
    print()


def main():
    answer = daily_word()
    guesses = []
    results = []
    used = {}  # letter -> (best_color, ...)
    stats = load_stats()

    color_rank = {"green": 2, "yellow": 1, "gray": 0}

    print_header()

    won = False
    for attempt in range(6):
        print_board(guesses, results, attempt)
        print(render_keyboard(used))
        print()

        while True:
            try:
                raw = input(f"  Guess {attempt + 1}/6 › ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n  Goodbye!\n")
                sys.exit(0)

            if len(raw) != 5:
                print("  ✗ Must be 5 letters.\n")
                continue
            if not raw.isalpha():
                print("  ✗ Letters only.\n")
                continue
            # Accept any 5-letter word
            break

        result = score_guess(raw, answer)
        guesses.append(raw)
        results.append(result)

        for ch, col in zip(raw, result):
            if ch not in used or color_rank[col] > color_rank[used[ch][0]]:
                used[ch] = (col,)

        # Clear screen and redraw
        print("\033[2J\033[H", end="")
        print_header()

        if all(c == "green" for c in result):
            print_board(guesses, results, attempt + 1)
            msgs = ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"]
            print(f"  {BOLD}{GREEN} {msgs[attempt]} {RESET}  The word was {BOLD}{answer.upper()}{RESET}\n")
            won = True
            break

    if not won:
        print_board(guesses, results, 6)
        print(f"  The word was {BOLD}{GREEN} {answer.upper()} {RESET}\n")

    stats["played"] += 1
    if won:
        stats["wins"] += 1
        stats["streak"] += 1
        stats["max_streak"] = max(stats["max_streak"], stats["streak"])
        stats["dist"][str(len(guesses))] = stats["dist"].get(str(len(guesses)), 0) + 1
    else:
        stats["streak"] = 0
    save_stats(stats)
    print_stats(stats)


if __name__ == "__main__":
    main()
