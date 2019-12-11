import pyaudio
import wave
import numpy as np
import time

np.set_printoptions(suppress=True)

def prepare_data(msg):
	chunk = 1024
	f = wave.open('Voice/18kHz-0.24+0.01.wav', 'rb')
	bit_zero_data = b''
	tmp = b'tmp'
	while tmp != b'':
		tmp = f.readframes(chunk)
		bit_zero_data += tmp

	f = wave.open('Voice/20kHz-0.24+0.01.wav', 'rb')
	bit_one_data = b''
	tmp = b'tmp'
	while tmp != b'':
		tmp = f.readframes(chunk)
		bit_one_data += tmp

	send_data = b''
	for i in msg:
		char = format(ord(i), 'b')
		if len(char) < 8:
			char = '0' * (8 - len(char)) + char
		for j in char:
			if j == '0':
				send_data += bit_zero_data
			else:
				send_data += bit_one_data
	return send_data

def send(msg):
	rate = 96000
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, output = True) 
	for char in msg:
		print(char,end='')
		send_data = prepare_data(char)
		stream.write(send_data)
	data = prepare_data('a')
	stream.write(send_data)	
	stream.stop_stream()
	stream.close()

def main():
	m = 'tdohconf2019'
	send(m)
if __name__ == '__main__':
	main()