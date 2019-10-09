import vlc
import time
#i0 = vlc.Instance("--aout=alsa")
#m0 = i0.media_new("fullTheme.opus")
#
#mp0 = m0.player_new_from_media()
#mp0.play()
#
#time.sleep(10)

import mpv

player = mpv.MPV()

player.play("fullTheme.opus")
