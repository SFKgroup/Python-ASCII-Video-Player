# Python ASCII Video Player

[中文](./Readme.md) [English](./Readme_en.md)

Due to Python's relatively low execution efficiency and the limitations of `print()` for console output, many assume that Python cannot produce dynamic ASCII art videos—a view that is overly pessimistic. In fact, Python’s performance potential is far greater than commonly imagined. By replacing `print()` with `sys.stdout`, console output speed can reach impressive levels. Combined with JIT compilation techniques to optimize loop performance, it becomes straightforward to achieve frame rates of 60 FPS or higher under standard terminal character sizes. Even when reducing font size (increasing the number of characters displayed per line), the playback can typically maintain around 24 FPS on most systems.

### Command-line Arguments

```bash
python main.py -s /your/video/dir
```

`-s`, `--source`: Path to the video file. Default is **"0"**, which activates the computer's primary (index 0) camera. Network URLs are also supported.  
`--width`: Frame width in characters. Default **0** means fill the entire terminal window width.  
`--height`: Frame height in characters. Default **0** means fill the entire terminal window height.  
`--style`: Rendering style. Default is **"char_bw"**. Available styles include:

 - `"char_bw"`           : Uses black and white only; brightness is represented by characters. Offers the highest frame rate.
 - `"char_color"`    : Uses multiple colors; brightness is represented by character type, while character color represents actual pixel color. Lower frame rate.
 - `"color"`               : Uses multiple colors; pixel colors are represented by background color. Moderate frame rate.
 - `"bw"`                     : Uses grayscale; pixel brightness is represented by background color. Moderate frame rate.

`--charset`: Character set used for rendering. Default is **" .:-!=+*#%@"**. Only applies to `"char_bw"` and `"char_color"` modes.