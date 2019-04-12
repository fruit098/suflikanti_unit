from moviepy.editor import *
import moviepy.video.fx.all as vfx


def intro_logo_with_background(background_animation, logo):
    clip = VideoFileClip(background_animation)
    clip = clip.resize(0.5)
    # TODO resize for platform

    sub = clip.subclip(0, 16)

    clip2 = sub.speedx(final_duration=2)

    clip3 = clip2.fx(vfx.time_mirror)

    final = concatenate_videoclips([clip2, clip3])

    image_clip = ImageClip(logo, duration=final.duration)
    image_clip = image_clip.resize(0.3).set_position("center", "center")

    final_video = CompositeVideoClip([final, image_clip.resize(lambda t: 1 + 0.1 * t)])

    final_reverse = final_video.fx(vfx.time_mirror)

    return final_reverse


def product_previews(products, text_content="Realase TODAY", duration_of_product=4, font="Amiri-Bold",
                     text_color="black"):
    image_clips = [ImageClip(image, duration=duration_of_product) for image in products]

    text_clip = TextClip(text_content, color=text_color, font=font).set_duration(duration_of_product * len(products))

    clips_with_text = [
        CompositeVideoClip([image_clip, text_clip]) for image_clip in image_clips
    ]

    clips_with_text = [clipo.set_duration(4) for clipo in clips_with_text]

    final_clip = concatenate_videoclips(clips_with_text)

    return final_clip


def anim_pictures(pic1):
    image_clip = ImageClip(pic1)

    image_clip = image_clip.set_duration(4)

    new_clip = image_clip.fx(vfx.scroll, w=1280, x_speed=500)

    new_clip.set_duration(float(image_clip.w - 640 * 2) / 500)
    return new_clip


def one_on_each_other(clip_list):
    imclips = []
    for item in clip_list:
        imclips.append(ImageClip(item).set_duration(2).crossfadein(2))

    imclipsstart = []
    start = 0
    for clip in imclips:
        if start == 0:
            start += 2
            imclipsstart.append(clip)
            continue

        imclipsstart.append(clip.set_start(start))
        start += 2

    final_clip = CompositeVideoClip(imclipsstart)

    final_clip.set_duration(len(imclipsstart) * 2)

    return final_clip


def logo_faid(logo):
    image_clip = ImageClip(logo, duration=4).crossfadein(3)

    final = CompositeVideoClip([image_clip])

    return final


if __name__ == '__main__':
    pass
