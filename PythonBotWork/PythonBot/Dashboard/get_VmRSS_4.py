import json
import subprocess
from   time              import sleep
import os
import time
import atexit
import json
from os.path             import exists
import numpy             as np
import matplotlib.pyplot as plt
import re



#TODO take arguements to
#1. Record
#2. Compare old recordings
#3. average/high
#4. ? Not sure if any more info is needed?
#% Maybe vault and other services?


file_exists = exists("myfile.json")
if file_exists:
    with open('myfile.json', 'r') as openfile: 
        lastPart = json.load(openfile)
        print(lastPart)


def exit_handler(): 
    
    with open("myfile.json", "w") as f: 
        json.dump(y_axis_ls[1], f)
    print('My application is ending!')

atexit.register(exit_handler)

def getVmRSS_stats(pid): return os.system("docker exec -it strato_strato_1 bash -c 'cat /proc/"+ str(pid) + "/status'")


def getVmRSS_stats_(pid):
    temp2_ =  os.popen("docker exec -it strato_strato_1 bash -c 'cat /proc/"+ str(pid) + "/status'").read()
    temp1 = (temp2_).split("VmRSS:")[1]
    temp3 = temp1.split("\n")[0]
    return temp3

def percentage_usage(x):
    temp =  os.popen("docker exec -it strato_strato_1 bash -c 'ps -p "+ str(x) + " -o %cpu,%mem'").read()
    #print(re.findall("\d+\.\d+", temp))
    [res1, res2] = re.findall("\d+\.\d+", temp)
    return [float(res1), float(res2)]



def getPids(x):
    temp = os.popen("docker exec -it strato_strato_1 bash -c 'ps axo pid,comm'").read()
    temp1 = (str(temp)).split(x)[0]
    temp2 = temp1 [-5:]
    return int(temp2)


#List of services to track
ls = ["strato-api", "vm-runner", "strato-p2p", "strato-sequence", "slipstream"]

#Store memory % for each service
ls_percent_mem = [ [] for _ in ls]

#Store cpu %
ls_percent_cpu    = [ [] for _ in ls]  

#list of Service's PID
ls_pids = [getPids(x)  for x in ls ]

for x in ls_pids : print(getVmRSS_stats_(str(x)))

#Set up 
plt.ion()
amount_of_graphs = len(ls) +1
fig, axs = plt.subplots(amount_of_graphs+1)
#fig.canvas.setWindowTitle('Strato cpu and mem Monitor')
fig.canvas.manager.set_window_title('Strato cpu and mem Monitor')


t   = []
y_axis_ls =  [ []  for i in range(0, len(ls))]


SomeLines = []

for i in range(0, amount_of_graphs-1): 

    something_ , = axs[i].plot( t , y_axis_ls[i], 'ko-' , markersize = 1 )
    axs[i].legend( [ ls[i] ] )
    axs[i].set_ylabel("Kib")
print("Something", something_)



some1, = axs[amount_of_graphs -1].plot(t, [], 'ko-',   color='blue',  markersize = 1)
some2, = axs[amount_of_graphs -1].plot(t, [], 'ko-',   color='green', markersize = 1)
some3, = axs[amount_of_graphs -1].plot(t, [],'ko-',    color='red',   markersize = 1)
some4, = axs[amount_of_graphs -1].plot(t, [], 'ko-', markersize = 1)
axs[amount_of_graphs-1].legend(list(map((lambda x : "cpu" + x), ls)))

#axs[1].set_ylabel("KiB")
axs[amount_of_graphs -1].set_ylabel("%")


lines_ls_cpu = [some1, some2, some3, some4]


some1_, = axs[amount_of_graphs].plot(t, [], 'ko-',   color='blue',  markersize = 1)
some2_, = axs[amount_of_graphs].plot(t, [], 'ko-',   color='green', markersize = 1)
some3_, = axs[amount_of_graphs].plot(t, [],'ko-',    color='red',   markersize = 1)
some4_, = axs[amount_of_graphs].plot(t, [], 'ko-', markersize = 1)
#axs[amount_of_graphs].legend(ls)
axs[amount_of_graphs].legend(list(map((lambda x : "mem" + x), ls)))
axs[amount_of_graphs].set_ylabel("%")

lines_ls_mem = [some1, some2, some3, some4]




print("Do we get here")
fig.show()

#from pprint import pprint
#pprint(vars(axs[amount_of_graphs -1 ]))

#for attr in dir(axs[amount_of_graphs -1 ]):
#    print("obj.%s = %r" % (attr, getattr(axs[amount_of_graphs -1 ], attr)))


#print(xs[amount_of_graphs -1 ].lines)

t0 = time.time()
while True:
    #y = np.random.random()

    current_vmRrss = []
    
    t.append( time.time()-t0 )


    for i, k in enumerate(ls_pids): 
        
        #Step 1, get % of use
        [cpu, mem]   = percentage_usage(int(k))
        print("cpu for service", ls[i], cpu, mem)
        ls_percent_cpu[i].append(cpu)
        ls_percent_mem[i].append(mem)

        y_axis_ls[i].append(int(re.findall(r'\d+', getVmRSS_stats_((str(ls_pids[i]))))[0])) 
        
        #if i == 1 and len(lastPart) >= len(y_axis_ls[i]): 
        #    print("i" , i , "we got here")
        #    axs[i].lines[1].set_data( t, lastPart[ : len(y_axis_ls[i]) ] )


        axs[i].lines[0].set_data( t,y_axis_ls[i] )
        #print("axs[i].lines", axs[i].lines)        
        
        #if i == 1:
        #    axs[amount_of_graphs -1 ].lines[0].set_data( t, ls_percent_cpu[0])
        #    test_this = ls_percent_cpu[1]
        #    axs[amount_of_graphs -1 ].lines[1].set_data( t, test_this)
        

        if i < 4: 
            #print("lines_ls", lines_ls[i]) 
            #print("time vs", t, ls_percent_cpu[i])
            #lines_ls[i].set_data(t, ls_percent_cpu[i])
            axs[amount_of_graphs -1 ].lines[i].set_data(t, ls_percent_cpu[i]) 
            axs[amount_of_graphs -1].relim()                  # recompute the data limits
            axs[amount_of_graphs -1].autoscale_view()
            
            axs[amount_of_graphs ].lines[i].set_data(t, ls_percent_mem[i])
            axs[amount_of_graphs].relim()                  # recompute the data limits
            axs[amount_of_graphs].autoscale_view()

        

        axs[i].relim()                  # recompute the data limits
        axs[i].autoscale_view()
    

    fig.canvas.flush_events()   # update the plot and take care of window events (like resizing etc.)
    time.sleep(1)               # wait for next loop iteration
     


plt.show()
