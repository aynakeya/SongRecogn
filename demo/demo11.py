import threading,random,time

class _insertFingerprints(threading.Thread):
    def __init__(self, threadID,data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
    def run(self):
        a = random.randrange(0,5)
        print(self.threadID,a)
        time.sleep(a)
num = 10
st = 0
total_threads=[]
running_threads = []
for i in range(0,20):
    total_threads.append(_insertFingerprints(i,""))
while st < len(total_threads):
    if len(running_threads) < num:
        print(st,"start")
        total_threads[st].start()
        running_threads.append(total_threads[st])
        st += 1
        continue
    for t in running_threads:
        if not t.is_alive():
            print(t.threadID, "stop")
            running_threads.remove(t)
for t in total_threads:
    t.join()
