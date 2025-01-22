import subprocess
import matplotlib.pyplot as plt
import numpy as np

sequential_percentages = np.round(np.arange(0.0, 1.01, 0.01), 2)
# generates a sequential percentages list for 1% to 100%
execution_times = []
speedup_values  = []

cuda_program = "./matrix_multiplication"

for percentage in sequential_percentages:
    print(f"Running for sequential percentage: {percentage*100:.2f}%")
    try:
        # executing the cuda program
        result =  subprocess.run(
            [cuda_program, f"{percentage:.2f}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # now we get the execution time from the output
        for line in result.stdout.splitlines():
            if "Execution time:" in line:
                exec_time = float(line.split(":")[1].strip().split()[0])
                execution_times.append(exec_time)
                break
    
    except subprocess.CalledProcessError as e:
        print(f"Error in running the program: {e}")
        execution_times.append(None)

# plotting the results

# plt.figure(figsize=(10,6))
# plt.plot(
#     [p*100 for p in sequential_percentages],
#     execution_times,
#     marker='o',
#     linestyle='-',
#     color='blue'
# )
# plt.title("Execution Time vs Sequential Percentage")
# plt.xlabel("Sequential Percentage (%)")
# plt.ylabel("Execution time (seconds)")
# plt.grid(True)
# plt.show()



# Calculate Speedup
if execution_times[0] is not None:  # Ensure there's a valid reference (100% sequential case)
    T_CPU = execution_times[-1]  # Last value corresponds to 100% sequential
    speedup_values = [T_CPU / t if t else None for t in execution_times]

# Plot Execution Time
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)  # First plot
plt.plot(
    [p * 100 for p in sequential_percentages],
    execution_times,
    marker='o',
    linestyle='-',
    color='blue',
    label="Execution Time"
)
plt.title("Execution Time vs Sequential Percentage")
plt.xlabel("Sequential Percentage (%)")
plt.ylabel("Execution Time (seconds)")
plt.grid(True)
plt.legend()

# Plot Speedup
plt.subplot(1, 2, 2)  # Second plot
plt.plot(
    [p * 100 for p in sequential_percentages][1:],
    speedup_values[1:],
    marker='o',
    linestyle='-',
    color='green',
    label="Speedup"
)
plt.title("Speedup vs Sequential Percentage")
plt.xlabel("Sequential Percentage (%)")
plt.ylabel("Speedup")
plt.grid(True)
plt.legend()

# Show both plots
plt.tight_layout()
plt.show()