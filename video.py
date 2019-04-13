import transition
from moviepy.editor import *
import moviepy.video.fx.all as vfx

list = []
list.append('/home/filipcaladi/Desktop/suflikanti_unit/fotak.jpg')
list.append('/home/filipcaladi/Desktop/suflikanti_unit/zena.jpg')
list.append('/home/filipcaladi/Desktop/suflikanti_unit/02.jpg')

video = transition.one_on_each_other(list)#intro_logo_with_background('/home/filipcaladi/Desktop/suflikanti_unit/Dense_fog_ahead_of_Forest.mp4','/home/filipcaladi/Desktop/suflikanti_unit/logo6.png')
video = transition.audio_to_clip('zvuk.mp3',video)
logo = transition.generate_intro('logo2.png')

conc = transition.concate_two(logo,video)

conc.write_videofile("test.mp4", fps=24)