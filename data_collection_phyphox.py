import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from playsound import playsound

# phyphox configuration
PP_ADDRESS = "http://192.168.1.8" #change this based on whatever your phone says
PP_CHANNELS = ["accX", "accY", "accZ", "magX", "magY", "magZ"]
sampling_rate = 100

# animation and data collection config
PREV_SAMPLE = 50
INTERVALS = 1000 / sampling_rate

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

fig2 = plt.figure()
max = fig2.add_subplot(1,1,1)

# global var to save timestamp
xs = []

# global array to save acceleration
accX = []
accY = []
accZ = []

magX = []
magY = []
magZ = []

# make one of them true at a time
isAnimate = True
isCollectData = False

#instrument modes
c = 0
ints = ["DRUM", "PIANO"]
noises = [['Tom.mp3', 'Snare.mp3', 'Cymbal.mp3'], ['piano-g_G_major.wav', 'piano-c_C_major.wav', 'piano-b_B_major.wav']]


def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    accX = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    accY = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    accZ = data["buffer"][PP_CHANNELS[2]]["buffer"][0]
    magX = data["buffer"][PP_CHANNELS[3]]["buffer"][0]
    magY = data["buffer"][PP_CHANNELS[4]]["buffer"][0]
    magZ = data["buffer"][PP_CHANNELS[5]]["buffer"][0]
    # print (accX, ' ', accY, ' ', accY)
    return [accX, accY, accZ, magX, magY, magZ]

# In[11]:


# This function is called periodically from FuncAnimation
def animate(i, xs, accX, accY, accZ, magX, magY, magZ):
    [naccX, naccY, naccZ, nmagX, nmagY, nmagZ] = getSensorData()

    xs.append(dt.datetime.now().strftime('%S.%f'))  # %H:%M:%S.%f

    accX.append(naccX)
    accY.append(naccY)
    accZ.append(naccZ)

    magX.append(nmagX)
    magY.append(nmagY)
    magZ.append(nmagZ)

    # plot only the 50 (PREV_SAMPLE) previous smaples
    _accX = accX[-PREV_SAMPLE:]
    _accY = accY[-PREV_SAMPLE:]
    _accZ = accZ[-PREV_SAMPLE:]

    _magX = magX[-PREV_SAMPLE:]
    _magY = magY[-PREV_SAMPLE:]
    _magZ = magZ[-PREV_SAMPLE:]

    xs = xs[-PREV_SAMPLE:]

    ax.clear()
    max.clear()

    ax.plot(xs, _accX, label='AX')
    ax.plot(xs, _accY, label='AY')
    ax.plot(xs, _accZ, label='AZ')

    max.plot(xs, _magX, label='MagX')
    max.plot(xs, _magY, label='MagY')
    max.plot(xs, _magZ, label='MagZ')

    ax.legend(loc='upper left')
    max.legend(loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


def getData():
    [naccX, naccY, naccZ, nmagX, nmagY, nmagZ] = getSensorData()  # get nth sample
    t = dt.datetime.now().strftime('%M:%S.%f')  # %H:%M:%S.%f
    xs.append(t)
    accX.append(naccX)
    accY.append(naccY)
    accZ.append(naccZ)
    magX.append(nmagX)
    magY.append(nmagY)
    magZ.append(nmagZ)
    return [t, naccX, naccY, naccZ, nmagX, nmagY, nmagZ]


def instrumental(ax, ay, az, mx, my, mz):
    if ax > 10:
        print "Note C"
        print (ax, ' ', ay, ' ', az, ' ', mx, ' ', my, ' ', mz)
        playsound('piano-c_C_major.wav')
    elif ay > 10:
        print "Note B"
        print (ax, ' ', ay, ' ', az, ' ', mx, ' ', my, ' ', mz)
        playsound('piano-b_B_major.wav')
    elif az > 35:
        print "Note G"
        print (ax, ' ', ay, ' ', az, ' ', mx, ' ', my, ' ', mz)
        playsound('piano-g_G_major.wav')
    print (ax, ' ', ay, ' ', az, ' ', mx, ' ', my, ' ', mz)


def main():
    if isAnimate == True:
        # interval in milliseconds
        ani = anim.FuncAnimation(fig, animate, fargs=(xs, accX, accY, accZ, magX, magY, magZ), interval=INTERVALS, repeat=True)
        plt.show()
    if isCollectData == True:
        while True:
            [t, naccX, naccY, naccZ, nmagX, nmagY, nmagZ] = getData()
            instrumental(naccX, naccY, naccZ, nmagX, nmagY, nmagZ)
            # time.sleep(INTERVALS/1000)   # Delays for INTERVALS seconds.


if __name__ == '__main__':
    main()


