from comp2 import IMU_Reader


trial=IMU_Reader()
x=trial.readAll()
print x	

count=1
while(1):
    trial.startReading()
