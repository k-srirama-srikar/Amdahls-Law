import time
from multiprocessing import Pool
import matplotlib.pyplot as plt


def parallel_task(n):
    # Simulate a parallelizable task
    return sum(i * i for i in range(n))

def measure_time(task_size, num_processes):
    sequential_size = task_size // 10  # 10% sequential part
    parallel_size = task_size - sequential_size

    # Sequential part
    start = time.time()
    sum(i * i for i in range(sequential_size))
    
    # Parallel part
    with Pool(num_processes) as pool:
        chunks = [parallel_size // num_processes] * num_processes
        pool.map(parallel_task, chunks)
    
    end = time.time()
    return end - start

if __name__ == "__main__":
    task_size = 10**7
    processors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    times = []

    for p in processors:
        time_taken = measure_time(task_size, p)
        times.append(time_taken)
        print(f"Processors: {p}, Time: {time_taken:.2f}s")

    # Calculate and print speedups
    speedups = [times[0] / t for t in times]
    print("Speedups:", speedups)



plt.figure(figsize=(10, 5))

# Execution time plot
plt.subplot(1, 2, 1)
plt.plot(processors, times, marker='o', label='Execution Time')
plt.xlabel('Number of Processors')
plt.ylabel('Time (s)')
plt.title('Execution Time vs Processors')
plt.grid(True)
plt.legend()

# Speedup plot
plt.subplot(1, 2, 2)
plt.plot(processors, speedups, marker='o', color='green', label='Speedup')
plt.xlabel('Number of Processors')
plt.ylabel('Speedup')
plt.title('Speedup vs Processors')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
