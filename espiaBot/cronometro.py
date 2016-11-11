import time
finish = False
t = time.time()
Min = 0
Seg = 0
while not finish:
    Seg = Seg +1
    if Seg >= 60:
     Min = Min + 1
     Seg = 0
    if Min == 1: # Duracion maxima de cronometro
     finish = True
    if Seg < 10:
     print(str(Min) + ':0' + str(Seg))
    else:
     print(str(Min) + ':' + str(Seg))
    time.sleep(1)
