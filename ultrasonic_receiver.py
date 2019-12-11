import pyaudio
import wave
import numpy as np
import time

np.set_printoptions(suppress=True)

def determine_frequency():
	rate = 44100
	chunk = 1024
	threshold = 50000
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
	binary_data = ''
	#prevtime = time.time()

	while True:
		data = np.frombuffer(stream.read(chunk), np.int16)
		fft = abs(np.fft.fft(data).real)
		fft = fft[:int(len(fft)/2)]
		freq = np.fft.fftfreq(chunk, 1.0/rate)
		freq = freq[:int(len(freq)/2)]
		high_val = max([fft[np.where(freq > 19990)[0][i]] for i in range(0, 20)])
		low_val = max([fft[np.where(freq > 17990)[0][i]] for i in range(0, 20)])
		#print('high_value: {0}, low_value:{1}'.format(high_val, low_val))
		#proc_time, prevtime = time.time() - prevtime, time.time()
		#print(proc_time)
		high_bool = high_val > threshold
		low_bool = low_val > threshold
		if high_bool and low_bool:
			if high_val > low_val:
				low_bool = False
			else:
				high_bool = False
		if high_bool:
			#print('High value' + str(high_val))
			binary_data += '1'
			#print('1  '+str(high_val))
			#print(proc_time)
			if len(binary_data) == 8:
				print(chr(int(binary_data, 2)))
				binary_data = ''

		elif low_bool:
			#print('Low value' + str(low_val))
			binary_data += '0'
			#print('0  '+str(low_val))
			#print(proc_time)
			if len(binary_data) == 8:
				print(chr(int(binary_data, 2)))
				binary_data = ''
		time.sleep(0.249)
	stream.stop_stream()
	stream.close()
	p.terminate()

def main():
	determine_frequency()
if __name__ == '__main__':
	main()