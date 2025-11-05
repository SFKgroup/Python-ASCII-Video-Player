import argparse
import os
from functools import partial
from utils import show,show_frame_char_color,show_frame_char,show_frame_color,show_frame_bw

parser = argparse.ArgumentParser("")
parser.add_argument('-s', '--source', type=str, default="0", help='Video source')
parser.add_argument('--width', type=int, default=0, help='Terminal columns (0 for full screen)')
parser.add_argument('--height', type=int, default=0, help='Terminal lines (0 for full screen)')
parser.add_argument('--style', type=str, default="char_bw", help='style of video')
parser.add_argument('--charset', type=str, default=" .:-!=+*#%@", help='charset for video (from empty to full)') # " `.':~!>=+/?[#%$&@"


if __name__ == '__main__':
    args = parser.parse_args()
    func_style = {
        "char_bw"    : partial(show_frame_char, char_set=args.charset),
        "char_color" : partial(show_frame_char_color,char_set=args.charset),
        "color"      : show_frame_color,
        "bw"         : show_frame_bw
    }
    assert args.style in func_style , "style not supported"

    video_source = args.source
    if video_source.isdigit():video_source = int(video_source)
    if args.width and args.height:size = (args.width, args.height)
    else:
        terminal_size = os.get_terminal_size()
        size = (terminal_size.columns, terminal_size.lines)

    show(video_source,size,func_style[args.style])