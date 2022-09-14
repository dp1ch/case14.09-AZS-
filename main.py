from random import randint
from math import ceil
azs=[]
que = []
# azs = [{},{},{}]
file_input = open("input.txt", encoding="utf-8")
	#print(que)
# azs 
def define_azs(fuel,t):
	minq=1000
	for a in azs:
		if a.get("fuel") and len(que[a["number"]][t])<a["maxlen"]:
			if len(que[a["number"]][t]) <= minq:
				minq=len(que[a["number"]][t])
				res=a
			return res["number"]
	print("Car could not que TRIGGER")
	for i in range(len(azs)):
		print(que[i][t])
	print(azs)
	return
leaving_que=[[],[],[]]
def run_time(t):
	#join que
	#00:01 10 АИ-80
	leaving_dict={}
	v=put_in()
	if v==0:
		return
	time_next_car,consumed_time,fuel,stroke=v
  if time_next_car == 0:
    return 0
	for ts in range(t,24*60):
		if stroke == "":
			return
		#az-  номер автозаправки
		print("Current TS: ",ts,"Time next car arrives: ",time_next_car)
		if ts>=time_next_car:
			#print(3)
			az=define_azs(fuel,ts)
			if (az==None):
					v=put_in()
					if v==0:
						return
					time_next_car,consumed_time,fuel,stroke=v
					
					continue#skip this ts Водитель уехал и не смог ждать
			sum_t=0
			#print("az",az)
			
			for i in leaving_que[az]:
				sum_t+=i
				print(123456)
			for ts_up in range(ts,int(ts+sum_t+consumed_time)):
				que[az][ts_up]+="*"
				#print(que)
				#print("\n\n123\n")
				leaving_que[az].append(consumed_time)
				try:
					if leaving_dict[int(ts+sum_t+consumed_time)]:
						leaving_dict[int(ts+sum_t+consumed_time)]+=stroke
				except KeyError:		
					leaving_dict[int(ts+sum_t+consumed_time)]=stroke
			#TODO trigger entering event v
			
			car_enters_que(ts,az,stroke)		
			v=put_in()
			if v==0:
				return
			time_next_car,consumed_time,fuel,stroke=v
		for az in range(len(leaving_que)):
			if len(leaving_que[az])>0:
				leaving_que[az][0]=leaving_que[az][0]-1
				if leaving_que[az][0]<=0:
					leaving_que[az].pop(0)
					#TODO trigger leaving event v
					for i in leaving_dict.items():
						print(i)
					try:
						car_leaves_que(ts,leaving_dict[ts])
					except KeyError:
						try: 
							car_leaves_que(ts,leaving_dict[ts+1])
						except KeyError:
							try:
								car_leaves_que(ts,leaving_dict[ts-1])
							except KeyError:
								try:
									car_leaves_que(ts,leaving_dict[ts-2])
								except KeyError:
									car_leaves_que(ts,leaving_dict[ts+2])
				#que[az]=que[az][ts][:-1:]
				
			
		
		
		
	
	
	#leave_que
def car_enters_que(t,az,stroke):
	#az- номер колонки выбранной
	#t текущее время
	print("Водитель встал в очередь на аз",az)
	for i in range(len(que)):
		print(i,"->",que[i][t])
	
"""
В  01:25  новый клиент:  01:25 АИ-98 50 4 встал в очередь к автомату №3 
Автомат №1  максимальная очередь: 3 Марки бензина: АИ-80 -> 
Автомат №2  максимальная очередь: 2 Марки бензина: АИ-92 -> 
Автомат №3  максимальная очередь: 4 Марки бензина: АИ-92 АИ-95 АИ-98 ->*
"""
def car_leaves_que(t,stroke):
	#azs- глобальная
	#t текущее время
	#que - глобальная
	# из dict берется stroke, ключ время
	print("Водитель покинул АЗС")
	for i in range(len(que)):
		print(i,"->",que[i][t])
	
"""
В  01:44  клиент  01:39 АИ-80 40 5  заправил свой автомобиль и покинул АЗС. 
Автомат №1  максимальная очередь: 3 Марки бензина: АИ-80 -> 
Автомат №2  максимальная очередь: 2 Марки бензина: АИ-92 -> 
Автомат №3  максимальная очередь: 4 Марки бензина: АИ-92 АИ-95 АИ-98 -> 
"""
	
def timeToMin(h,m):
	print(int(h)*24+int(m),"\n")
	return int(h)*24+int(m)

def minToTime(t):
	return t//24,t%60

def input_azs():
  with open("azs.txt", encoding="utf-8") as file_azs:
    try:
      while True:
            s = file_azs.readline()
            number, count_que, fuel = s.split(" ", 2)
            azs.append({"number": int(number) - 1, "maxlen": int(count_que), "fuel": fuel})
    except ValueError:
      pass
  len_azs = len(azs)
  for i in range(len_azs):
	  que.append({})
  for n in range(len_azs):
	  for t in range (24*60-1):
		que[n][t]=""
  return azs, que

def put_in():
  try:
	  stroke=file_input.readline()
	  time, count_l, fuel = stroke.split()
  except ValueError:
    return 0
  time=timeToMin(time.split(":")[0],time.split(":")[1])
  count_t = ceil(int(count_l) / 10) + randint(-1,1)
  if count_t == 0:
    count_t = 1
		#TODO добавить строку их всех этих элементов = название клиента в выводе
		#далее  - stroke))
		# stroke == "01:39 АИ-80 40 5"  
  return time, count_t, fuel, stroke

def main():
	azs, que = input_azs()
	azs = [{"number":0,"maxlen":2,"fuel":"АИ-92 АИ-95 АИ-98"},{"number":1,"maxlen":4,"fuel":"АИ-95 АИ-98"},{"number":2,"maxlen":3,"fuel":" АИ-98"}]
	run_time(0)

main()
file_input.close()