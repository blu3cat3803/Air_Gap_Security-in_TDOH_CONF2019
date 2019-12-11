from playsound import playsound
import winsound
import time

msg = 't'
nowtime = 0
for i in msg:
	char = format(ord(i), 'b')
	if len(char) < 8:
		char = '0' * (8 - len(char)) + char
	for j in char:
		print(j, end=" ")
		if j == '0':
			#playsound('18kHz-2.wav', block=False)
			winsound.Beep(18000, 500)
			prevtime, nowtime = nowtime, time.perf_counter()
			proc_time = nowtime - prevtime
			print(proc_time)
		else:
			#playsound('20kHz-2.wav', block=False)
			winsound.Beep(20000, 500)
			prevtime, nowtime = nowtime, time.perf_counter()
			proc_time = nowtime - prevtime
			print(proc_time)

	print()
