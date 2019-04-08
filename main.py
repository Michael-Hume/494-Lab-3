import time
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import serial

#s = serial.Serial("/dev/cu.usbmodem14501")
#s = serial.Serial("/dev/tty.usbmodem14301")
s = serial.Serial("/dev/tty.usbmodem14501")
data = []
rawHR_Readings = []
time_Readings = []
readingNumber = 0
HR_Readings = []
varReadings = []

print("Starting collection in 3")
print("")
sleep(.5)
print(" . ")
sleep(.5)
print(" . ")
sleep(.5)
print(" .\n")
sleep(.5)
print(" 2\n")
sleep(.5)
print(" . ")
sleep(.5)
print(" . ")
sleep(.5)
print(" .\n")
sleep(.5)
print(" 1\n")
sleep(.5)
print(" . ")
sleep(.5)
print(" . ")
sleep(.5)
print(" .\n")
sleep(.5)
print(" Collecting\n\n")

t_end = time.time() + 30  # <-- RUN FOR 2 MIN
startTime = int(time.time())
oldElapsed = 0
avgReading = 384.00
heartBeat = False
hbCount = 0
hbBaseline = 0
prevHBTime = time.time()
newHBTime = 0.0
avgTimeBetweenBeats = 0.0
totalTimeBetweenBeats = 0.0
heartRate = 0

f=open("lab3Readings.txt", "w+")
f=open("lab3Variability.txt", "w+")

while time.time() < t_end:
    readingNumber += 1
    currentTime = int(time.time())
    newElapsed = currentTime-startTime





    # Get data reading
    dataPoint = s.readline().decode('utf-8').strip()
    # Add it to list of readings
    rawHR_Readings.append(int(dataPoint))

    # Anything inside this loop will run once per second
    if newElapsed > oldElapsed:
        oldElapsed = newElapsed
        print("Time Elapsed: " + str(oldElapsed))
        avgReading = int(sum(rawHR_Readings)/len(rawHR_Readings))
        print("Avg: " + str(avgReading))

    f=open("lab3Readings.txt", "a+")
    f.write(str(dataPoint) + ",")
    f.close()
    f=open("lab3RVariability.txt", "a+")
    f.write(str(dataPoint) + ",")
    f.close()

    # If reading it 115% of avgReading it it a heart beat
    if int(dataPoint) > (avgReading * 1.2):
        if not heartBeat:
            heartBeat = True
            hbCount += 1
            print("\n* * * * * * * * * *")
            print("HeartBeat" + str(hbCount))
            print("* * * * * * * * * *\n")

            hbBaseline = int(dataPoint)

            # Calculate time between heartbeats
            newHBTime = time.time()
            timeSinceLastHB = newHBTime - prevHBTime
            totalTimeBetweenBeats = totalTimeBetweenBeats + timeSinceLastHB
            avgTimeBetweenBeats = totalTimeBetweenBeats/hbCount
            if hbCount > 1:
                print("Time since last beat: " + str(round(timeSinceLastHB, 3)))
                print("HB Count: " + str(hbCount))
                #print("Avg time between beats: " + str(round(avgTimeBetweenBeats, 3)) + "\n")
                print("Heart Rate Variability: " + str(round(avgTimeBetweenBeats*1000, 3)) + "ms" + "\n")
            prevHBTime = newHBTime
            if newElapsed > 0:
                heartRate = int((hbCount/newElapsed)*60)
                print("Current Heart Rate: " + str(heartRate) + " BPM")

    #varReadings.append(round(avgTimeBetweenBeats*1000, 3))
    varReadings.append(timeSinceLastHB)


    if int(dataPoint) < (hbBaseline*.70):
        if heartBeat:
            heartBeat = False
            #print("Flipped")


    time_Readings.append(oldElapsed)



    # APPLY MOVING AVG
    HR_Readings = rawHR_Readings
    #



outputFileName = "lab3.txt"
fd = open(outputFileName, "w+")

# Write to .txt file
fd.write("\nReadings\n")
for i in rawHR_Readings:
    fd.write("%d," % i)

print(hbCount*2)

print("Collection Complete")
print("HB Count: " + str(hbCount))
print("Heart Rate Variability: " + str(round(avgTimeBetweenBeats*1000, 3)) + " ms" + "\n")
print("Heart Rate: " + str(heartRate))
plt.plot(varReadings)
plt.ylabel("Seconds Between Beets")
plt.show()

