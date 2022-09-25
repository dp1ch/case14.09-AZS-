"""Case-study "Dictionaries (Fuel Station)"
Developers - Percentage:
 Pichuev Denis - 60.49%   
 Dyakovich Alexander - 60%
 Trushkin Nikita - 35.51%
"""
from random import randint
from math import ceil
prices = {'АИ-95':50,'АИ-80':42,'АИ-92':46,'АИ-98':58}
revenue = 0
azs = []
que = []
N_AZS = 3
file_input = open("input.txt", encoding="utf-8")
def sorting(elem):
    m = float("inf")
    q = 0
    for x in elem:
        q += 1
        for i, j in x.items():
            if i <= m:
                si = j
                m = i
                l = q
    return m, si, l - 1


def define_azs(fuel, t):
    minq = 1000
    res=None
    for a in azs:
        if fuel in a.get("fuel") and len(que[a["number"]][t]) < a["maxlen"]:
            if len(que[a["number"]][t]) <= minq:
                minq = len(que[a["number"]][t])
                res = a
								
    try:
      return res["number"]
    except TypeError:
      global leavers
      leavers+=1
      return


leaving_que = [[], [], []]


def run_time(t, t2=24 * 60):
		v = put_in(t)
		rec_list = []
		m = float("inf")
		time_next_car, consumed_time, fuel, stroke = v
		leaving_que = []
		for i in range(N_AZS):
			leaving_que.append([])
		for curt in range(t, t2):
				#if leaving_que!=[[],[],[]]:
				ho, mi = minToTime(curt)
				#homi = str(ho) + ":" + str(mi)
				#if m < 1000:
					#print("cr",curt,"(" + homi + ")","next",time_next_car,"next_leave",m,end="\n")
				#else:
					#print("cr", curt, "(" + homi + ")", "next", time_next_car)
				#if leaving_que!=[[],[],[]]:
				#	print("lq", leaving_que)
				for ticket in range(len(azs)):
					m = float("inf")
					if len(leaving_que[ticket]) > 0:
						leaving_que[ticket][0] -= 1
						#m = min(m, leaving_que[ticket][0])
						if leaving_que[ticket][0] <= 0:
							#print("FIX HERE!")#Fix here
							leaving_que[ticket].pop(0)
							m, s, n = sorting(rec_list)
							car_leaves_que(curt+1, s)
							#print(curt,s,rec_list)
							rec_list.pop(n)
							
					if curt >= time_next_car:
						if v!=0:
							az = define_azs(fuel, curt)
						if az == None:
							
							#print("водитель не нашёл места на азс")
							
							v = put_in(curt)
							if v == 0:
								continue
							time_next_car, consumed_time, fuel, stroke = v
							continue
						sumt = 0
						for i in leaving_que[az]:
							sumt += i
						for i in range(curt, int(curt + consumed_time + sumt)):
							if i <= t2:
								que[az][i] += "*"
						if v!=0:
							rec_list.append({curt + consumed_time + sumt: stroke})
							car_enters_que(curt, az, stroke, curt + consumed_time + sumt)
						#print("az", az)
							leaving_que[az].append(consumed_time)
						
						#print("Взял некст строку")
						v = put_in(curt)
						if v == 0:
							continue
						time_next_car, consumed_time, fuel, stroke = v


            #rec_dict[stroke]=time_next_car,consumed_time,fuel
            #rec_list.append(stroke)
def car_enters_que(t, az, stroke, leaving_time):  #az- номер колонки выбранной
    #t текущее время
    #global revenue += prices * stroke.split()[2]
		h , m = minToTime(t)
		h1, m1 = minToTime(leaving_time)
		print("В", str(h)+ ':' + str(m), "новый клиент:", stroke,"встал в очередь к автомату",az+1,"и покинет станцию в",str(h1)+ ':' + str(m1))
		for i in range(len(que)):
			print("Автомат", i+1,"максимальная очередь:", azs[i]['maxlen'], "Марки бензина:", azs[i]['fuel'],"->", que[i][t])


def car_leaves_que(t, stroke):
    #azs- глобальная
    #t текущее время
    #que - глобальная
    # из dict берется stroke, ключ время
    h , m = minToTime(t)
    print("В",str(h)+ ':' + str(m),"клиент", stroke," заправил свой автомобиль и покинул АЗС.")
    for i in range(len(que)):
        print("Автомат", i+1,"максимальная очередь:",azs[i]['maxlen'], "Марки бензина:",azs[i]['fuel'],"->", que[i][t])

def timeToMin(h, m):
    #print(int(h)*24+int(m),"\n")
    return int(h) * 60 + int(m)


def minToTime(t1):
	t1 = int(t1)#print( t1,t1//60,t1%60)
	h=str((t1 // 60)%24)
	m=str(t1 % 60)
	if len(h)==1:
		h="0"+h
	if len(m)==1:
		m="0"+m
	return h,m 


def input_azs():
    with open("azs.txt", encoding="utf-8") as file_azs:
        try:
            while True:
                st = file_azs.readline()
                number, count_que, fuel = st.split(" ", 2)
                azs.append({
                    "number": int(number) - 1,
                    "maxlen": int(count_que),
                    "fuel": fuel.replace("\n","")
                })
        except ValueError:
            pass
    len_azs = len(azs)
    for i in range(len_azs):
        que.append({})
    for n in range(len_azs):
        for t in range(24 * 60 + 1):
            que[n][t] = ""
    return azs, que


def put_in(curt):
	try:
		stroke = file_input.readline()
		time, count_l, fuel = stroke.split()
	except ValueError:
		return 0
	time = timeToMin(time.split(":")[0], time.split(":")[1])
	global revenue
	global litrs,leavers
	az = define_azs(fuel, time)
	if az!=None:
		revenue += int(prices[fuel])*int(count_l)
		litrs[fuel]+=int(count_l)
	else:
		leavers-=1
		h , m = minToTime(time)
		strin="В  "+str(h)+ ':' + str(m)+ " новый клиент:" +stroke.replace("\n","")+ " не смог заправить автомобиль и покинул АЗС. "
		print(strin)
		t=curt
		for i in range(len(que)):
			print("Автомат", i+1,"максимальная очередь:",azs[i]['maxlen'], "Марки бензина:",azs[i]['fuel'],"->", que[i][t])

#txt = "For only {price:.2f} dollars!"
	count_t = ceil(int(count_l) / 10) + randint(-1, 1)
	if count_t == 0:
		count_t = 1
	stroke=stroke.replace("\n","")
	return time, count_t, fuel, stroke
	
# stroke == "01:39 АИ-80 40 5"
def main():
  global azs  
  azs, que = input_azs()
  #azs = [{"number": 0,"maxlen": 2,"fuel": "АИ-92 "},{"number": 1,"maxlen": 3,"fuel": "АИ-95 АИ-98"},{"number": 2,"maxlen": 4,"fuel": " АИ-98"}]
  run_time(0)
    #print(sorting(f))
leavers=0
litrs={'АИ-95':0,'АИ-80':0,'АИ-92':0,'АИ-98':0}
main()
file_input.close()
litrsss=""
revenues=""
for litrss,i in litrs.items():
	litrsss+= litrss + ':' + str(i) + ' литров' + ', '
q=0
for z in str(revenue)[::-1]:
	if q % 3 == 0 and q!=0:
		revenues += '.'
	q += 1
	revenues += z

print('Количество литров, проданное за сутки по каждой марке бензина:',litrsss[:-2])
print('Общая сумма продаж за сутки:',revenues[::-1],'рублей')
print('Количество клиентов, которые покинули АЗС не заправив автомобиль из-за «скопившейся» очереди:',leavers)


