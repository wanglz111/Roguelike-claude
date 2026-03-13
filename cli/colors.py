"""ANSI color codes for terminal output."""

import sys
import os


def _supports_color() -> bool:
    """Check if the terminal supports color output."""
    # Check if output is redirected
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return False

    # Check for common color-supporting terminals
    term = os.environ.get('TERM', '')
    if term in ('dumb', ''):
        return False

    # Windows terminal support
    if sys.platform == 'win32':
        # Windows 10+ supports ANSI colors
        return True

    return True


# Enable/disable colors based on terminal support
COLORS_ENABLED = _supports_color()


class Color:
    """ANSI color codes."""
    # Text colors
    RED = '\033[91m' if COLORS_ENABLED else ''
    GREEN = '\033[92m' if COLORS_ENABLED else ''
    YELLOW = '\033[93m' if COLORS_ENABLED else ''
    BLUE = '\033[94m' if COLORS_ENABLED else ''
    MAGENTA = '\033[95m' if COLORS_ENABLED else ''
    CYAN = '\033[96m' if COLORS_ENABLED else ''
    WHITE = '\033[97m' if COLORS_ENABLED else ''
    GRAY = '\033[90m' if COLORS_ENABLED else ''

    # Bright colors
    BRIGHT_RED = '\033[91;1m' if COLORS_ENABLED else ''
    BRIGHT_GREEN = '\033[92;1m' if COLORS_ENABLED else ''
    BRIGHT_YELLOW = '\033[93;1m' if COLORS_ENABLED else ''
    BRIGHT_BLUE = '\033[94;1m' if COLORS_ENABLED else ''
    BRIGHT_MAGENTA = '\033[95;1m' if COLORS_ENABLED else ''
    BRIGHT_CYAN = '\033[96;1m' if COLORS_ENABLED else ''

    # Styles
    BOLD = '\033[1m' if COLORS_ENABLED else ''
    DIM = '\033[2m' if COLORS_ENABLED else ''
    RESET = '\033[0m' if COLORS_ENABLED else ''

    # Store enabled state as class attribute
    COLORS_ENABLED = COLORS_ENABLED


def colorize(text: str, color: str) -> str:
    """Wrap text with color codes."""
    if not COLORS_ENABLED:
        return text
    return f"{color}{text}{Color.RESET}"


def hp_color(current: int, maximum: int) -> str:
    """Return appropriate color for HP based on percentage."""
    if maximum == 0:
        return Color.GRAY
    percentage = current / maximum
    if percentage > 0.6:
        return Color.GREEN
    elif percentage > 0.3:
        return Color.YELLOW
    else:
        return Color.RED


def mp_color(current: int, maximum: int) -> str:
    """Return appropriate color for MP based on percentage."""
    if maximum == 0:
        return Color.GRAY
    percentage = current / maximum
    if percentage > 0.5:
        return Color.CYAN
    elif percentage > 0.2:
        return Color.BLUE
    else:
        return Color.GRAY


def rarity_color(rarity: str) -> str:
    """Return color for item rarity."""
    rarity_colors = {
        'common': Color.WHITE,
        'rare': Color.BLUE,
        'epic': Color.MAGENTA,
        'legendary': Color.YELLOW
    }
    return rarity_colors.get(rarity, Color.WHITE)
