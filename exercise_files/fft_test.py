import numpy as np
from matplotlib import pyplot as plt

from scipy.fft import rfft, rfftfreq

FREQ1=1000
FREQ2=5000
SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds
def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Generate a 2 hertz sine wave that lasts for 5 seconds
#x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
#plt.plot(x, y)
#plt.show()
_, nice_tone = generate_sine_wave(FREQ1, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(FREQ2, SAMPLE_RATE, 1)
noise_tone = noise_tone * 1
for x in range(0,len(noise_tone)):
    nice_tone[x] = nice_tone[x] + noise_tone[x]
normalized_tone = np.int16((nice_tone / nice_tone.max()) * 32767)

#plt.plot(normalized_tone[:1000])
#plt.show()
N = SAMPLE_RATE * DURATION
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()


# Note the extra 'r' at the front
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()