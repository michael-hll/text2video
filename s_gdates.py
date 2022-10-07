import datetime
import sxtwl
import sys

file = './d_date_detail.txt'

if len(sys.argv) >= 2:
    file = sys.argv[1]

#today = datetime.date.today().strftime('%Y-%m-%d')
today = datetime.date.today()
day = sxtwl.fromSolar(today.year, today.month, today.day)
#day = sxtwl.fromSolar(2022, 10, 22)
 
## 一些常量文字的定义。
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
Gan  = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];
Zhi =  ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX =  ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
XiZ = ('摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手')
 
# 公历的年月日
gongli = "%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
print(gongli)

# 星期
dayOfWeek = WeekCn[day.getWeek()]
print(dayOfWeek)

# 星座
xingZuo = XiZ[day.getConstellation()] + '座'
print("星座:", xingZuo)

# 农历
#nongli = "%d年%s%d月%d日" % (day.getLunarYear(), '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
nongli = "年%s%d月%d日" % ('闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
print(nongli)

# 以春节为界的天干地支 
yTG = day.getYearGZ(True)
yTG_DG = Gan[yTG.tg] + Zhi[yTG.dz]
print(yTG_DG) 
shengXiao = Zhi[yTG.dz] + ShX[yTG.dz]
print(shengXiao)

# 当日是否有节气
jieQi = ''
jieQi_Date = ''
if day.hasJieQi():
    jieQi = jqmc[day.getJieQi()]
    print('节气：%s'% jieQi)
    #获取节气的儒略日数
    jd = day.getJieQiJD()
    # 将儒略日数转换成年月日时秒
    t = sxtwl.JD2DD(jd )
    
    # 注意，t.s是小数，需要四舍五入
    jieQi_Date = "%d-%d-%d %d:%d:%d" % (t.Y, t.M, t.D, t.h, t.m, round(t.s))
    print("节气时间:" + jieQi_Date)
else:
    # 查找某日前后的节气
    while True:
        # 这里可以使用after或者before，不用担心速度，这里的计算在底层仅仅是+1这么简单
        day = day.after(1)
        # hasJieQi的接口比getJieQiJD速度要快，你也可以使用getJieQiJD来判断是否有节气。
        if day.hasJieQi():
            jieQi = jqmc[day.getJieQi()]
            print('节气：%s'% jqmc[day.getJieQi()])
            #获取节气的儒略日数， 如果说你要计算什么时间的相距多少，直接比对儒略日要方便，相信我。
            jd = day.getJieQiJD()
        
            # 将儒略日数转换成年月日时秒
            t = sxtwl.JD2DD(jd )
            
            # 注意，t.s是小数，需要四舍五入
            jieQi_Date = "%d-%d-%d %d:%d:%d" % (t.Y, t.M, t.D, t.h, t.m, round(t.s))
            print("节气时间:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
            
            break
    

    
with open(file, 'w') as f:
    line = 'gongli=' + gongli + '\n'
    line += 'xingqi=' + dayOfWeek + '\n'
    line += 'xingzuo=' + xingZuo + '\n'
    line += 'nongli=' + nongli + '\n'
    line += 'yTG_DZ=' + yTG_DG + '\n'
    line += 'shengXiao=' + shengXiao + '\n'
    line += 'jieQi=' + jieQi + '\n'
    line += 'jieQi_Date=' + jieQi_Date.replace(':', '\\:') + '\n'
    f.write(line)
    

'''
https://blog.csdn.net/lifulinghan/article/details/81484332

# 星期几
print(WeekCn[day.getWeek()])
 
# 这个月的第几周
print('该日属于这个月的第%d周'%(day.getWeekIndex(),))
 
# 星座(有bug?待修复)
print("星座:", XiZ[day.getConstellation()])
 
# 以春节为界的农历(注getLunarYear如果没有传参，或者传true，是以春节为界的)
s = "农历:%d年%s%d月%d日" % (day.getLunarYear(), '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
print(s)
 
# 不以立春为界的农历
s = "农历:%d年%s%d月%d日" % (day.getLunarYear(False), '闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
print(s)
 
 
# 以春节为界的天干地支 
yTG = day.getYearGZ(True)
print("以春节为界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
print("以春节为界的生肖:", ShX[yTG.dz])
 
# 以立春为界的天干地支 （注，如果没有传参，或者传false，是以立春为界的。刚好和getLunarYear相反）
yTG = day.getYearGZ()
print("以立春为界的年干支", Gan[yTG.tg] + Zhi[yTG.dz]) 
print("以立春为界的生肖:", ShX[yTG.dz])
 
#月干支
mTG = day.getMonthGZ()
print("月干支", Gan[mTG.tg] + Zhi[mTG.dz]) 
 
#日干支
dTG  = day.getDayGZ()
print("日干支", Gan[dTG.tg] + Zhi[dTG.dz]) 
 
#时干支
for hour in range(24):
    # 第一个参数为该天的天干，第二个参数为小时
    hTG  = sxtwl.getShiGz(dTG.tg, hour)
    print("%d时天干地支:"%(hour), Gan[hTG.tg] + Zhi[hTG.dz])
 
 
# 当日是否有节气
if day.hasJieQi():
    print('节气：%s'% jqmc[day.getJieQi()])
    #获取节气的儒略日数
    jd = day.getJieQiJD()
    # 将儒略日数转换成年月日时秒
    t = sxtwl.JD2DD(jd )
    
    # 注意，t.s是小数，需要四舍五入
    print("节气时间:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
else:
    print("当天不是节气日")
 
 
# 四注反查 分别传的是年天干，月天干，日天干，时天干， 开始查询年，结束查询年  返回满足条件的儒略日数
jds = sxtwl.siZhu2Year(yTG, mTG, dTG, sxtwl.GZ(5, 5), 2003, 2029);
for jd in jds:
    t = sxtwl.JD2DD(jd )
    print("符合条件的时间:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
 
 
# 获取一年中的闰月
year = 2020
month = sxtwl.getRunMonth(year)
if month >= 0:
    print("%d年的闰月是%d"%(year, month) )
else:
    print("没有闰月")
 
 
# 一个农历月的天数
year = 2020 #农历年
month  = 4 #农历月
isRun = False #是否是闰月
daynum = sxtwl.getLunarMonthNum(year, month, isRun)
print("农历%d年%s%d月的天数:"%(year, '闰'if isRun else '', month), daynum)
 
 
#儒略日数转公历
jd = sxtwl.J2000
t = sxtwl.JD2DD(jd )
 
#公历转儒略日
jd = sxtwl.toJD(t)
 
# 获取某天的后面几天
num = 1    #你喜欢写多少天 也多少天，可以写负数，相当于往前
day = day.after(num)  #获取num天后的日信息
s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
print(s)
 
# 同上
day = day.before(num)
s = "公历:%d年%d月%d日" % (day.getSolarYear(), day.getSolarMonth(), day.getSolarDay())
print(s)
 
 
# 查找某日前后的节气
while True:
    # 这里可以使用after或者before，不用担心速度，这里的计算在底层仅仅是+1这么简单
    day = day.after(1)
    # hasJieQi的接口比getJieQiJD速度要快，你也可以使用getJieQiJD来判断是否有节气。
    if day.hasJieQi():
        print('节气：%s'% jqmc[day.getJieQi()])
        #获取节气的儒略日数， 如果说你要计算什么时间的相距多少，直接比对儒略日要方便，相信我。
        jd = day.getJieQiJD()
    
        # 将儒略日数转换成年月日时秒
        t = sxtwl.JD2DD(jd )
        
        # 注意，t.s是小数，需要四舍五入
        print("节气时间:%d-%d-%d %d:%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))
        
        break
        
输出：
历:2022年10月6日
星期四
该日属于这个月的第2周
星座: 天秤
农历:2022年9月11日
农历:2022年9月11日
以春节为界的年干支 壬寅
以春节为界的生肖: 虎
以立春为界的年干支 壬寅
以立春为界的生肖: 虎
月干支 己酉
日干支 壬辰
0时天干地支: 庚子
1时天干地支: 辛丑
2时天干地支: 辛丑
3时天干地支: 壬寅
4时天干地支: 壬寅
5时天干地支: 癸卯
6时天干地支: 癸卯
7时天干地支: 甲辰
8时天干地支: 甲辰
9时天干地支: 乙巳
10时天干地支: 乙巳
11时天干地支: 丙午
12时天干地支: 丙午
13时天干地支: 丁未
14时天干地支: 丁未
15时天干地支: 戊申
16时天干地支: 戊申
17时天干地支: 己酉
18时天干地支: 己酉
19时天干地支: 庚戌
20时天干地支: 庚戌
21时天干地支: 辛亥
22时天干地支: 辛亥
23时天干地支: 壬子
当天不是节气日
2020年的闰月是4
农历2020年4月的天数: 30
公历:2022年10月7日
公历:2022年10月6日
节气：寒露
节气时间:2022-10-8 15:22:16        
'''        