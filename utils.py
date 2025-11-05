import cv2
import sys
import time
import os
import numpy as np
from functools import partial
from numba import njit

"""
Since Windows 10 Anniversary Update, console can use ANSI/VT100 color codes
You need set flag ENABLE_VIRTUAL_TERMINAL_PROCESSING(0x4) by SetConsoleMode
Use sequences:
"\x1b[48;5;" + s + "m" - set background color by index in table (0-255)
"\x1b[38;5;" + s + "m" - set foreground color by index in table (0-255)
"\x1b[48;2;" + r + ";" + g + ";" + b + "m" - set background by r,g,b values
"\x1b[38;2;" + r + ";" + g + ";" + b + "m" - set foreground by r,g,b values
Important notice: Internally Windows have only 256 (or 88) colors in table and Windows will used nearest to (r,g,b) value from table.
"""

def seconds_to_text(seconds):
    seconds=round(seconds)
    return f"{(seconds//3600) % 60:02d}:{(seconds//60) % 60:02d}:{seconds%60:02d}"

@njit
def show_frame_char(frame,window_size,char_set=" .~08#"):
    res = ""
    sep = 256 // len(char_set) + 1
    for x in range(window_size[1]):
        for y in range(window_size[0]):
            colour = round(0.299 * frame[x,y,2] + 0.587 * frame[x,y,1] + 0.114 * frame[x,y,0])
            res += char_set[colour//sep]
        res += "\n"
    return res

@njit
def show_frame_char_color(frame,window_size,char_set=" .~08#"):
    res = ""
    last_color = np.array([0,0,0],dtype=np.uint8)
    sep = 256 // len(char_set) + 1
    for x in range(window_size[1]):
        for y in range(window_size[0]):
            colour = round(0.299 * frame[x,y,2] + 0.587 * frame[x,y,1] + 0.114 * frame[x,y,0])
            if np.all(frame[x,y] == last_color):res += char_set[colour//sep]
            else:
                res += f"\x1b[38;2;{frame[x,y,2]};{frame[x,y,1]};{frame[x,y,0]}m"+char_set[colour//sep]
                last_color = frame[x,y]
        res += "\n"
    res += f"\x1b[38;2;255;255;255m"
    return res


@njit
def show_frame_color(frame,window_size):
    res = ""
    last_color = np.array([0,0,0],dtype=np.uint8)
    for x in range(window_size[1]):
        for y in range(window_size[0]):
            if np.all(frame[x,y] == last_color):res += " "
            else:
                res += f"\x1b[48;2;{frame[x,y,2]};{frame[x,y,1]};{frame[x,y,0]}m "
                last_color = frame[x,y]
        res += "\n"
    res += f"\x1b[48;2;0;0;0m"
    return res

@njit
def show_frame_bw(frame,window_size):
    res = ""
    last_color = 0
    for x in range(window_size[1]):
        for y in range(window_size[0]):
            colour = round(0.299 * frame[x,y,2] + 0.587 * frame[x,y,1] + 0.114 * frame[x,y,0])
            if colour == last_color:res += " "
            else:
                res += f"\x1b[48;2;{colour};{colour};{colour}m "
                last_color = colour
        res += "\n"
    res += f"\x1b[48;2;0;0;0m"
    return res

def video_bar(frame_num,time_now,video_length,duration,window_size):
    percent_len = int(frame_num / video_length * (window_size[0]-17))
    return time_now + "="*(percent_len) + ">" + "·"*(window_size[0]-17-percent_len) + duration + '\r'

def cap_bar(frame_num,time_now,window_size):
    return " "*((window_size[0]-8)//2) + time_now + " "*((window_size[0]-8)//2) + '\r'

def show(path,size=(96,54),shower=show_frame_bw):
    print("\033c") # 清屏
    window_size = (size[0],size[1]-1)
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:fps = 30
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if video_length <= 0:
        bar = partial(cap_bar,window_size=window_size)
        time_limit = np.inf
    else:
        duration = seconds_to_text(video_length / fps)
        bar = partial(video_bar, video_length=video_length,duration=duration,window_size=window_size)
        time_limit = 0

    frame_num = 0
    T = 1 / fps
    start_view_time = time.time()
    next_time = start_view_time
    
    while cap.isOpened():
        next_time += T
        frame_num += 1
        ret, frame = cap.read()
        if not ret:break
        elif time.time() - next_time > time_limit:
            time_now = seconds_to_text(time.time() - start_view_time)
            sys.stdout.write(bar(frame_num,time_now))
            sys.stdout.flush()
            continue # 渲染速率跟不上时跳帧
        frame = cv2.resize(frame, window_size)
        ascii_frame = shower(frame,window_size)
        sys.stdout.write("\033[H") # 光标移到头部但不清屏
        sys.stdout.write(ascii_frame)
        time_now = seconds_to_text(time.time() - start_view_time)
        sys.stdout.write(bar(frame_num,time_now))
        sys.stdout.flush()
        # cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        while time.time() < next_time:pass

if __name__ == '__main__':
    pass
    terminal_size = os.get_terminal_size()
    #os.system('mode con: cols=240 lines=80')
    # print(terminal_size.columns,terminal_size.lines)
    chars = "@%#*+=!-:. "
    my_chars = partial(show_frame_char_color, char_set=chars[::-1])
    show("./bda_colour.mp4",(terminal_size.columns,terminal_size.lines),my_chars)
    # show("./bda_colour.mp4",(terminal_size.columns,terminal_size.lines),show_frame_color) # 05:13
    # show(0,(terminal_size.columns,terminal_size.lines),my_chars)
    # show(0,(terminal_size.columns,terminal_size.lines),show_frame_color)