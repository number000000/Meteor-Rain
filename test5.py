import subprocess
p = subprocess.call('ffmpeg.exe -r 60 -f image2 -s 1000x740 -i ./frames/frame_%d.png -vcodec libx264 -crf 25  window_video.mp4', shell=True)