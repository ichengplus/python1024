# coding=utf-8
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

path = pathlib.Path(
    '~/dev/python/python1024/data/automate/008video').expanduser()
if not path.is_dir():
    path.mkdir()

x = np.linspace(-2, 2, 200)
duration = 2
fig, ax = plt.subplots()


def make_frame(t):
    ax.clear()
    ax.plot(x, np.sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)
    ax.set_ylim(-1.5, 2.5)
    return mplfig_to_npimage(fig)


out_path = path.joinpath('008video_matplotlib.gif')
animation = VideoClip(make_frame, duration=duration)
animation.write_gif(out_path, fps=20)
