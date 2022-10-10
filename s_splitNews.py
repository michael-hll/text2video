import sys

print(sys.argv)
content = '你好欢迎观赏我的的视频谢谢大家的收看，你好“阿道夫：阿斯蒂芬”'
file = 'news.txt'
x = 10 # splited size

if sys.argv[1]:
    content = str(sys.argv[1])
if sys.argv[2]:
    file = sys.argv[2]
if sys.argv[3]:
    x = int(sys.argv[3])
 
lines = [content[y-x:y] for y in range(x, len(content)+x,x)]

with open(file, 'w') as f:
    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            f.write(line)
        else:
            f.write(line + '\n')
