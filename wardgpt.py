
import json
import os
import sys
from datetime import datetime

# ========== ANSI COLOURS & STYLES (cross‑platform safe) ==========
class Style:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

class Color:
    # Basic foreground
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # Bright foreground
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    # Backgrounds
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def colored(text, color, style=None):
    """Return text wrapped in ANSI colour and optional style."""
    s = color
    if style:
        s += style
    return f"{s}{text}{Style.RESET}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ========== CONSTANTS ==========
HOURLY_RATE = 5
MAX_HOURS_PER_DAY = 24

import os
import sys

# --- Cross‑platform app data directory ---
if sys.platform == 'darwin':          # macOS
    BASE_DIR = os.path.expanduser('~/Library/Application Support/WardGPT')
elif sys.platform == 'win32':         # Windows
    BASE_DIR = os.path.join(os.environ.get('APPDATA', '.'), 'WardGPT')
else:                                 # Linux / other
    BASE_DIR = os.path.expanduser('~/.wardgpt')

os.makedirs(BASE_DIR, exist_ok=True)
DATA_FILE = os.path.join(BASE_DIR, 'wardgpt.json')

# ========== DATA HANDLING ==========
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return data.get('log', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(log):
    with open(DATA_FILE, 'w') as f:
        json.dump({'log': log}, f, indent=2)

# ========== VALIDATION ==========
def validate_date(date_str):
    date_str = date_str.replace(']', '').replace('[', '').strip()
    if not date_str:
        return None
    formats = [
        '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',
        '%b %d, %Y', '%B %d, %Y',
        '%d %b %Y', '%d %B %Y',
        '%d %b %y', '%d %B %y',
    ]
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime('%d %B %Y')
        except ValueError:
            continue
    print(colored('  ⚠️  Date format not recognized. Using DD/MM/YYYY', Color.YELLOW))
    return date_str

def validate_hours(hours):
    if hours < 0:
        return False, "Hours cannot be negative!"
    if hours == 0:
        return False, "Cannot log 0 hours!"
    if hours > MAX_HOURS_PER_DAY:
        return False, f"Cannot exceed {MAX_HOURS_PER_DAY} hours in a day!"
    if hours > 16:
        print(colored(f'  ⚠️  {hours}h is a long day. Confirm? (y/n)', Color.YELLOW), end=' ')
        if input().lower().strip() != 'y':
            return False, "Task cancelled."
    return True, ""

# ========== TASK LOGGING ==========
def log_task():
    clear_screen()
    print(colored('╔══════════════════════════╗', Color.CYAN))
    print(colored('║       LOG A TASK        ║', Color.CYAN))
    print(colored('╚══════════════════════════╝', Color.CYAN))
    print()

    date = validate_date(input('  📅 Date (DD/MM/YYYY): ').strip())
    if not date:
        print(colored('  ❌ Date cannot be empty!', Color.RED))
        input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
        return None

    task = input('  ✏️  Task Description : ').strip()
    if not task:
        print(colored('  ❌ Task cannot be empty!', Color.RED))
        input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
        return None
    if len(task) < 3:
        print(colored('  ❌ Description too short (min 3 chars)', Color.RED))
        input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
        return None

    print()
    print(colored('  How do you want to track time?', Color.BRIGHT_BLUE))
    print(colored('    1. Start Timer (live)', Color.BRIGHT_WHITE))
    print(colored('    2. Enter Start & End times', Color.BRIGHT_WHITE))
    print(colored('    3. Enter hours directly', Color.BRIGHT_WHITE))
    choice = input(colored('  Choose (1-3): ', Color.BRIGHT_CYAN)).strip()

    hours = None
    if choice == '1':
        print()
        input(colored('  ⏱  Press Enter to START...', Color.GREEN))
        start = datetime.now()
        print(colored(f'  ▶️  Started at {start.strftime("%H:%M:%S")}', Color.GREEN))
        input(colored('  ⏸  Press Enter to STOP...', Color.RED))
        end = datetime.now()
        print(colored(f'  ⏹  Stopped at {end.strftime("%H:%M:%S")}', Color.RED))
        hours = round((end - start).total_seconds() / 3600, 2)
        print(colored(f'  ⏱  Time recorded: {hours} hours', Color.BRIGHT_GREEN))

    elif choice == '2':
        print(colored('\n  Enter times in 24h format (HH:MM)', Color.BRIGHT_BLUE))
        try:
            start_time = input(colored('  Start (e.g., 09:00): ', Color.BRIGHT_WHITE)).strip()
            end_time = input(colored('  End   (e.g., 17:30): ', Color.BRIGHT_WHITE)).strip()
            start_h, start_m = map(int, start_time.split(':'))
            end_h, end_m = map(int, end_time.split(':'))

            if not (0 <= start_h <= 23 and 0 <= start_m <= 59):
                raise ValueError
            if not (0 <= end_h <= 23 and 0 <= end_m <= 59):
                raise ValueError

            start_dec = start_h + start_m / 60
            end_dec = end_h + end_m / 60
            if end_dec <= start_dec:
                end_dec += 24
            hours = round(end_dec - start_dec, 2)
            print(colored(f'  ⏱  Time recorded: {hours} hours', Color.BRIGHT_GREEN))
        except:
            print(colored('  ❌ Invalid time format! Use HH:MM', Color.RED))
            input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
            return None

    elif choice == '3':
        try:
            hours = float(input(colored('  Hours Spent: ', Color.BRIGHT_WHITE)).strip())
        except ValueError:
            print(colored('  ❌ Please enter a valid number!', Color.RED))
            input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
            return None
    else:
        print(colored('  ❌ Invalid choice!', Color.RED))
        input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
        return None

    ok, msg = validate_hours(hours)
    if not ok:
        print(colored(f'  ❌ {msg}', Color.RED))
        input(colored('  Press Enter to continue...', Color.WHITE, Style.DIM))
        return None

    input(colored('\n  ✅ Task logged! Press Enter to continue.', Color.GREEN))
    return {'Date': date, 'Task': task, 'Hours': hours}

# ========== LOG VIEW & MANAGEMENT ==========
def display_logs(log):
    clear_screen()
    print(colored('╔══════════════════════════╗', Color.CYAN))
    print(colored('║       WORK LOGS         ║', Color.CYAN))
    print(colored('╚══════════════════════════╝', Color.CYAN))
    if not log:
        print(colored('\n  📭 No tasks logged yet!', Color.WHITE, Style.DIM))
        return False

    print(colored(f'\n  📋 {len(log)} task(s) found\n', Color.BRIGHT_BLUE))
    for i, task in enumerate(log, 1):
        task_disp = task['Task'] if len(task['Task']) <= 55 else task['Task'][:52] + '...'
        print(colored(f'  [{i}]', Color.BRIGHT_WHITE), end=' ')
        print(colored(f"Date  : {task['Date']}", Color.BRIGHT_CYAN))
        print(colored(f'       Task  : {task_disp}', Color.WHITE))
        print(colored(f'       Hours : {task["Hours"]:.1f}h', Color.YELLOW))
        print()
    return True

def remove_task(log):
    if not display_logs(log):
        input(colored('  Press Enter to return.', Color.WHITE, Style.DIM))
        return

    try:
        num = int(input(colored('  Enter # to remove (0 to cancel): ', Color.BRIGHT_RED)).strip())
        if num == 0:
            print(colored('  ↩️  Cancelled.', Color.WHITE, Style.DIM))
            return
        if 1 <= num <= len(log):
            removed = log.pop(num - 1)
            print(colored(f'  ✅ Removed: {removed["Task"][:50]}', Color.GREEN))
        else:
            print(colored(f'  ❌ Enter between 1 and {len(log)}', Color.RED))
    except ValueError:
        print(colored('  ❌ Invalid number!', Color.RED))
    input(colored('\n  Press Enter to continue.', Color.WHITE, Style.DIM))

# ========== SUMMARY & PAYMENT ==========
def show_summary(log):
    clear_screen()
    print(colored('╔══════════════════════════╗', Color.CYAN))
    print(colored('║       WORK SUMMARY      ║', Color.CYAN))
    print(colored('╚══════════════════════════╝', Color.CYAN))
    if not log:
        print(colored('\n  📭 No tasks logged yet!', Color.WHITE, Style.DIM))
        return

    total_h = sum(t['Hours'] for t in log)
    avg_h = total_h / len(log)
    max_t = max(log, key=lambda x: x['Hours'])
    min_t = min(log, key=lambda x: x['Hours'])

    print(colored(f'\n  📊 Total Tasks    : {len(log)}', Color.BRIGHT_WHITE))
    print(colored(f'  ⏱  Total Hours    : {total_h:.1f}h', Color.BRIGHT_GREEN))
    print(colored(f'  📈 Average/Task   : {avg_h:.1f}h', Color.BRIGHT_BLUE))
    print(colored(f'  📈 Longest        : {max_t["Hours"]:.1f}h - {max_t["Task"][:35]}', Color.MAGENTA))
    print(colored(f'  📉 Shortest       : {min_t["Hours"]:.1f}h - {min_t["Task"][:35]}', Color.YELLOW))
    print(colored(f'  💰 Total Payment  : £{total_h * HOURLY_RATE:.2f}', Color.BRIGHT_YELLOW))
    print(colored(f'  📅 Days (8h)      : {total_h/8:.1f}', Color.WHITE, Style.DIM))
    print(colored(f'  📅 Weeks (40h)    : {total_h/40:.1f}', Color.WHITE, Style.DIM))

    print(colored('\n  📋 Recent Tasks:', Color.BRIGHT_WHITE))
    for t in log[-3:]:
        print(colored(f'    • {t["Date"]}: {t["Task"][:50]} ({t["Hours"]}h)', Color.WHITE))

def show_payment(log):
    clear_screen()
    print(colored('╔══════════════════════════╗', Color.CYAN))
    print(colored('║      PAYMENT DETAILS    ║', Color.CYAN))
    print(colored('╚══════════════════════════╝', Color.CYAN))
    if not log:
        print(colored('\n  📭 No tasks logged yet!', Color.WHITE, Style.DIM))
        return

    total_h = sum(t['Hours'] for t in log)
    gross = total_h * HOURLY_RATE
    tax = gross * 0.20
    net = gross - tax

    print(colored(f'\n  💷 Rate           : £{HOURLY_RATE}/hour', Color.BRIGHT_GREEN))
    print(colored(f'  ⏱  Total Hours    : {total_h:.1f}h', Color.BRIGHT_WHITE))
    print(colored(f'  💰 Gross Payment  : £{gross:.2f}', Color.BRIGHT_YELLOW))

    print(colored('\n  📊 Tax Estimate (if applicable):', Color.BRIGHT_BLUE))
    print(colored(f'  💰 Gross          : £{gross:.2f}', Color.WHITE))
    print(colored(f'  🏛  Tax (20%)      : £{tax:.2f}', Color.RED))
    print(colored(f'  💵 Net            : £{net:.2f}', Color.GREEN))

    print(colored('\n  📅 Time Breakdown:', Color.BRIGHT_BLUE))
    print(colored(f'  📅 Days (8h)      : {total_h/8:.1f}', Color.WHITE))
    print(colored(f'  📅 Weeks (40h)     : {total_h/40:.1f}', Color.WHITE))

    if total_h > 0:
        print(colored(f'\n  💡 Invoice-ready: £{gross:.2f}', Color.BRIGHT_CYAN))

# ========== MAIN MENU ==========
def main_menu(log):
    clear_screen()
    print(colored('╔══════════════════════════════════════╗', Color.BLUE + Style.BOLD))
    print(colored('║            WardGPT v2.0             ║', Color.BLUE + Style.BOLD))
    print(colored('╚══════════════════════════════════════╝', Color.BLUE + Style.BOLD))
    print()
    if log:
        total_h = sum(t['Hours'] for t in log)
        print(colored(f'  📊 {len(log)} tasks | ⏱ {total_h:.1f}h | 💰 £{total_h * HOURLY_RATE:.2f}', Color.GREEN))
    else:
        print(colored('  📭 No tasks logged yet', Color.WHITE, Style.DIM))
    print()
    print(colored('  1.', Color.BRIGHT_WHITE) + ' Log a Task          ')
    print(colored('  2.', Color.BRIGHT_WHITE) + ' View / Manage Logs  ')
    print(colored('  3.', Color.BRIGHT_WHITE) + ' Summary             ')
    print(colored('  4.', Color.BRIGHT_WHITE) + ' Payment Details     ')
    print(colored('  5.', Color.BRIGHT_WHITE) + ' Exit                ')
    print()

def main():
    log = load_data()
    while True:
        main_menu(log)
        choice = input(colored('  Choose (1-5): ', Color.CYAN + Style.BOLD)).strip()

        if choice == '1':
            task = log_task()
            if task:
                log.append(task)
                save_data(log)

        elif choice == '2':
            while True:
                clear_screen()
                print(colored('╔══════════════════════════╗', Color.BLUE))
                print(colored('║     MANAGE WORK LOGS    ║', Color.BLUE))
                print(colored('╚══════════════════════════╝', Color.BLUE))
                print()
                print(colored('  1.', Color.BRIGHT_WHITE) + ' View All Logs')
                print(colored('  2.', Color.BRIGHT_WHITE) + ' Remove a Task')
                print(colored('  3.', Color.BRIGHT_WHITE) + ' Back to Main Menu')
                print()
                sub = input(colored('  Choose: ', Color.CYAN)).strip()
                if sub == '1':
                    display_logs(log)
                    input(colored('\n  Press Enter to return.', Color.WHITE, Style.DIM))
                elif sub == '2':
                    remove_task(log)
                    save_data(log)
                elif sub == '3':
                    break
                else:
                    print(colored('  ❌ Invalid choice!', Color.RED))
                    input(colored('  Press Enter...', Color.WHITE, Style.DIM))

        elif choice == '3':
            show_summary(log)
            input(colored('\n  Press Enter to return.', Color.WHITE, Style.DIM))

        elif choice == '4':
            show_payment(log)
            input(colored('\n  Press Enter to return.', Color.WHITE, Style.DIM))

        elif choice == '5':
            save_data(log)
            clear_screen()
            print(colored('╔══════════════════════════╗', Color.GREEN))
            print(colored('║   👋 Goodbye! Take Care ║', Color.GREEN))
            print(colored('╚══════════════════════════╝', Color.GREEN))
            break

        else:
            print(colored('  ❌ Please choose 1-5!', Color.RED))
            input(colored('  Press Enter to continue.', Color.WHITE, Style.DIM))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n')
        try:
            save_data(load_data())
            print(colored('  💾 Data saved.', Color.GREEN))
        except:
            print(colored('  ❌ Could not save data.', Color.RED))
        print(colored('  👋 Goodbye!\n', Color.YELLOW))
        sys.exit(0)

  
