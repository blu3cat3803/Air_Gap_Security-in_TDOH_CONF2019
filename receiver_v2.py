import numpy as np
import pyaudio
import time
import os 

rate = 2 ** 16
frames_per_buffer = 2 ** 15
low_target = 17995
high_target = 19995
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
nowtime = 0
c = ''
while True:
	
	data = np.fromstring(stream.read(frames_per_buffer), dtype=np.int16)
	fft = abs(np.fft.fft(data).real)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(frames_per_buffer,1.0/rate)
	fft = 20 * np.log10(np.clip(np.abs(fft), 1e-20, 1e100))
	freq = freq[:int(len(freq)/2)]
	
	high_val = max([fft[np.where(freq > high_target)[0][i]] for i in range(0, 10)])
	low_val = max([fft[np.where(freq > low_target)[0][i]] for i in range(0, 10)])
	result = {'18000' : low_val, '20000' : high_val}
	#print(nowtime - prevtime)
	if result['18000'] > 120:
		c += '0'
		if len(c) == 8:
			character = chr(int(c, 2)) 
			print(character, end="")
			c = ''
		print('0')		
		#print('0  ' + str(proc_time))
		
	elif result['20000'] > 120:
		c += '1'
		if len(c) == 8:
			character = chr(int(c, 2))
			print(character, end="")
			c = ''
		print('1')
		#print('1  ' + str(proc_time))
		
	prevtime = time.perf_counter()
stream.stop_stream()
stream.close()
p.terminate()