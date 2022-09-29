import os, sys, shlex, subprocess, random
from tkinter import image_names

folder = './tmp'   
video_prefix = 'video_init_'
file_list = 'filelist.txt'
output = 'video_final_draft.mp4'

# processing user inputs
if len(sys.argv) >= 2:
    folder = sys.argv[1] 
# change folder path
os.chdir(folder)

def exe_command(command):
    command_array = shlex.split(command, posix=True)
    print('Runing command: {0}'.format(command))
    result = subprocess.Popen(command_array, text=True, stdout=sys.stdout, stderr=sys.stderr)
    result.communicate()     
    if result.returncode != 0: 
        print("Running command '{}' failed.".format(command))
        return False
    else:
        print("Running command '{}' successfull.".format(command))
        return True

count = 0
# count splited mp4 files
for path in os.listdir('./'):
    # check if current path is a file
    if os.path.isfile(os.path.join('./', path)):
        if path.startswith(video_prefix):
            count += 1
print('There are total {} splited videos.'.format(count))

# Add each splited video with background
digit_format = '{:02d}'
img_prefix = 'bg{:02d}'
with open(file_list, 'w') as f:
    for i in range(0, count):        
        video_name = video_prefix + digit_format.format(i) + '.mp4'
        video_output = video_prefix + digit_format.format(i) + '_b.mp4'
        img_name = img_prefix.format(i) + '.jpg'  
        if not os.path.exists(img_name):
            j = random.randint(0,3)
            img_name = img_prefix.format(j) + '.jpg'
        ffmpeg_cmd = "ffmpeg -y -i {0} -i {1} -filter_complex '[0:v]colorkey=0x00ff00:0.2:0.3[ckout];[1:v]scale=1920:1080[bg],[bg][ckout]overlay[out]' -map '[out]' -map 0:a:0 -c:a copy {2}"
        ffmpeg_cmd = ffmpeg_cmd.format(video_name, img_name, video_output)
        result = exe_command(ffmpeg_cmd)
        if result:
            f.write('file \'' + video_output + '\'' + '\n')
    
# combine splited video into the final one    
ffmpeg_cmd_final_draft = "ffmpeg -y -f concat -safe 0 -i {0} -c copy {1}".format(file_list, output)
result = exe_command(ffmpeg_cmd_final_draft)

