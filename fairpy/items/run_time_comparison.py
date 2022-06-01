import timeit  # Check performance of functions by running them many times
import matplotlib.pyplot as plt
import time
import numpy as np
import concurrent.futures
from py_undercut import undercut
import matplotlib.patches as mpatches

###################################################### Cython ######################################################

py_arr = []
cy_arr = []


#ABC= "abcdefghijklmnopqrstuvwxyz"
ABC= "abcdefghijklmn"
Alice = {}
Bob = {}
items=[]


for index, char in enumerate(ABC):
    Alice[char]= index
    Bob[char]= index+1
    items.append(char)
    agents = [(Alice),(Bob)]
    cy = timeit.timeit(f'cy_undercut.undercut({agents},{items})',
                    setup='import cy_undercut', number = 20 )
    py = timeit.timeit(f'undercut_procedure.undercut({agents},{items})',
                    setup='import undercut_procedure',
                    number = 20 )
    py_arr.append(py)
    cy_arr.append(cy)

print(f'cy = {cy}')
print(f'py = {py}')
print(f'Cython is {py/cy} times faster')
fig, ax = plt.subplots()
plt.title("Comparison between Cython and Python")
plt.xlabel("Number of items")
plt.ylabel("Time (seconds)")
for i, j in enumerate(range(len(py_arr)-1)):
    plt.plot([j+len(py_arr), j+len(py_arr)+1], [cy_arr[i], cy_arr[i+1]], 'green')
    plt.plot([j+len(py_arr), j+len(py_arr)+1], [py_arr[i], py_arr[i+1]], 'orange')
cy_ = mpatches.Patch(color='green', label='Cython')
py_ = mpatches.Patch(color='orange', label='Python')
ax.legend(handles=[cy_, py_])
plt.show()

###################################################### Threads ######################################################

if __name__ == "__main__":
    
    without_threads_arr = []
    with_threads_arr = []
    
    ABC= "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
    Alice = {}
    Bob = {}
    items=[]
    for index, char in enumerate(ABC):
        Alice[char]= index
        Bob[char]= index+1
        items.append(char)
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for _ in range(1000):
                executor.submit(undercut([Alice, Bob],items))
        finish = time.perf_counter()
        with_threads_arr.append(finish)

    Alice = {}
    Bob = {}
    items=[]
    for index, char in enumerate(ABC):
        Alice[char]= index
        Bob[char]= index+1
        items.append(char)
        start = time.perf_counter()
        for _ in range(1000):
                undercut([Alice, Bob],items)
        finish = time.perf_counter()
        without_threads_arr.append(finish)
        

a = np.array(without_threads_arr)
b = np.array(with_threads_arr)
a_ = np.mean(a)
b_=np.mean(b)
print(f'with_threads_arr is {a_/b_} times faster')
   
#print(with_threads_arr)  
#print(without_threads_arr)
fig, ax = plt.subplots()
plt.title("Comparison between with thread and without threads")
plt.xlabel("Number of items")
plt.ylabel("Time (seconds)")
for i, j in enumerate(range(len(without_threads_arr)-1)):
    plt.plot([j+len(without_threads_arr), j+len(without_threads_arr)+1], [with_threads_arr[i], with_threads_arr[i+1]], 'green')
    plt.plot([j+len(without_threads_arr), j+len(without_threads_arr)+1], [without_threads_arr[i], without_threads_arr[i+1]], 'orange')
cy_ = mpatches.Patch(color='green', label='Threads')
py_ = mpatches.Patch(color='orange', label='Without Threads')
ax.legend(handles=[cy_, py_])
plt.show()