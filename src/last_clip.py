from moviepy.editor import *
import random

fonts = ('ComicSans', 'CourierNew', 'Arial')


def last_clip(text="", release_date="", teaser="", format=1, font=1):
    relative_start = 0.3
    relative = 0.4
    font_size = 60
    teaser_relative = 0.50
    if format:
        clip = ColorClip((1920, 1080), color=(0, 0, 0), duration=7)
    else:
        clip = ColorClip((864, 1080), color=(0, 0, 0), duration=7)

    composite = [clip]

    if text:
        txt_clip = TextClip(text, font=fonts[font], fontsize=font_size, color='white')
        txt_clip = txt_clip.set_position(('center', relative_start), relative=True).set_duration(7)
        composite.append(txt_clip.set_start(1).crossfadein(1.5))

    if release_date:
        date_font_size = font_size - 8
        date_clip = TextClip(release_date, font=fonts[font], fontsize=date_font_size, color='white')
        date_clip = date_clip.set_position(('center', relative), relative=True).set_duration(7)
        composite.append(date_clip.set_start(2).crossfadein(1.5))

    if teaser:
        rotate = random.randrange(-32, 32)
        teaser_font_size = 230 - (len(teaser) * 13)
        buy_clip = TextClip(teaser, font=fonts[font], fontsize=teaser_font_size, color='white')
        buy_clip = buy_clip.set_position(('center', teaser_relative), relative=True).set_duration(7)
        buy_clip = buy_clip.add_mask().rotate(rotate)
        composite.append(buy_clip.set_start(2.5).crossfadein(1.5))

    final = CompositeVideoClip(composite).set_duration(7)
    final.write_videofile("test.mp4", fps=25)
    return final

