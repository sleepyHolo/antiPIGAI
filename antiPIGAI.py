# -*- coding: utf-8 -*-

"""
Fucking the pigai.org
"""

import re
import pyautogui
import pygetwindow as gw
import argparse
from time import sleep
from math import ceil

import ctypes
# load user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)


HKL_NEXT = 1


def load_keyboard_layout(layout_name):
    return user32.LoadKeyboardLayoutW(layout_name, 1)


def activate_keyboard_layout(hkl):
    return user32.ActivateKeyboardLayout(hkl, 0)


def get_current_keyboard_layout():
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    return user32.GetKeyboardLayout(thread_id)


def switch_keyboard_layout(layout_name):
    hkl = load_keyboard_layout(layout_name)
    activate_keyboard_layout(hkl)


def get_target_title(target_key: str = '') -> list:
    """return all titles with target key"""
    all_titles = gw.getAllTitles()
    if target_key == '':
        return all_titles
    titles = []
    for title in all_titles:
        if re.search(target_key, title):
            titles.append(title)
    return titles


def switch_title(title_list: list, page_size: int = 9,
                 output_func=lambda x: print(x, end=''),
                 input_func=input) -> str:
    """let user choose target window"""
    if not title_list:
        input_ = input_func('No valid input. Search all titles? [Y/n]: ')
        if (input_.lower() != 'n'):
            title_list = get_target_title()
        else:
            return

    list_size = len(title_list)
    page = 1
    while True:
        title, page = show_list_to(title_list, list_size, page, page_size,
                                   output_func, input_func)
        if title:
            return title


def show_list_to(list_: list, list_size: int,
                 page: int = 1, page_size: int = 9,
                 output_func=lambda x: print(x, end=''),
                 input_func=input) -> str:
    """return index user choose"""
    page_max = ceil(list_size / page_size)
    from_ = (page - 1) * page_size
    size = page_size if page < page_max else min(page_size, list_size - from_)

    # print title
    output_func('\n' + '-'*20 + '\n')
    output_func(' [ < ') if page != 1 else output_func(' [   ')
    output_func(f'Page {page} / {page_max}')
    output_func(' > ]\n') if page != page_max else output_func('   ]\n')
    output_func('  0 \t- Next Page -\n')
    for i in range(1, size + 1):
        output_func(f'  {i} \t') if i != 1 else output_func(f'> {i} \t')
        output_func(str(list_[from_ + i - 1]) + '\n')
    input_ = input_func("Order (default with '>'): ")
    if input_ == '0':
        # page ++
        page = page + 1 if page < page_max else 1
        return '', page
    for i in range(1, size + 1):
        if input_ == str(i):
            return str(list_[from_ + i - 1]), page
    # default
    return str(list_[from_]), page


def set_active_window(title: str) -> None:
    window = gw.getWindowsWithTitle(title)[0]
    window.activate()
    window.maximize()
    return


def auto_type(filename: str, interval: float = 0.01,
              set_eng=True, text_only=False) -> None:
    """auto-type text from a file"""
    if set_eng:
        switch_keyboard_layout('00000409')
    if text_only:
        pyautogui.typewrite(filename, interval=interval)
        return
    with open(filename, 'r') as file:
        while True:
            if not (line := file.readline()):
                break
            pyautogui.typewrite(line, interval=interval)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='Your input. Default seen as file name.')
    parser.add_argument('--key', type=str, default='批改网',
                        help='Key word of your target. Default: 批改网.')
    parser.add_argument('-i', '--interval', type=float, default=0.01,
                        help='Set typing interval (s). Default: 0.01')
    parser.add_argument('--text_input', action='store_true', default=False,
                        help='input as text instead of file. Default: False')
    parser.add_argument('-e', '--english', action='store_true', default=False,
                        help='make sure using English. Default: False')
    parser.add_argument('--check_time', type=float, default=0,
                        help='Sleep time before typing (s). Default: 0')

    args = parser.parse_args()
    
    title = switch_title(get_target_title(args.key))
    if title == None:
        exit()
    set_active_window(title)
    
    sleep(args.check_time)

    auto_type(args.filename, interval=args.interval,
              set_eng=args.english, text_only=args.text_input)
    print('Done.')
