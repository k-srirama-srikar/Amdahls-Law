# Amdahl's Law
I wrote a program to test out the Amdahl's law that I came across... \
I tried to check the ideal speedup with different number of processors and differennt percentages of parallelizations...

Also, I've tried out a CUDA program to plot the values for different parallel percentages... 

## About Amdahl's Law
Gene Amdahl, one of the early pioneers of computing made a simple but insightful observation about the effectiveness of improving the performance of one part of a system.

The idea is that we speed up one part of the, the effect on the overall system performance depends on both how significant this part was and how much it sped up.

Consider a system executes an application program in time $T_{old}$ and a fraction $\alpha$ of this time is required by some part of the system and now we improve it's performance by a factor $k$. Now the overall execution time would be, 
<p align='center'>$\Large T_{new} = (1-\alpha)T_{old} + (\alpha T_{old})/k$ </p>
<p align='center'>$\Large = T_{old}[(1-\alpha)+\alpha/k]$ </p>
 

From this we compute the speed up as 
<p align='center'>$\Large S = T_{old}/T_{new}$ </p>
<p align='center'>$\Large S =  \frac{1}{(1-\alpha)+\alpha/k}$ </p>


Now, we can also look at it through this formula as well

<p align='center'>$\Large S = \frac{1}{(1 - P) + P/N}$ </p>

Where:
- S: Speedup of the system
- P: Proportion of the task that can be parallelized
- N: Number of processors or parallel resources

In short, the Amdahl's Law highlights the importance of minimizing the sequential portion of a task to achieve greater performance gains in parallel systems.


## Parallel Processor Computation Analysis

The `parallel_comp.py` program evaluates the performance of a parallel computation system using Python's `multiprocessing` module, focusing on how the number of processors affects execution time and speedup.

The parallel task I've chosen here is the summation of squares form $0$ to $n-1$ (with $n$ being $10^7$)

The below is the image of the plot...

![Screenshot from 2025-01-23 00-39-57](https://github.com/user-attachments/assets/f3992ae3-66ce-4832-8cf8-3a96b59a1e4b)

> [!NOTE]
> This program was run on a system with 6 cores, so as you can see, it was pretty close to the ideal case...
> And the change in the graph after 6, is beacuse of the overhead...
> Basically the operating system schedules multiple processes on the same core, resulting in context switching overhead and diminished performance

You can experiment with this by varing the percentages of the sequential and parallel processes and see...

## Matrix Multiplication using CUDA

I have simulated a 1024 x 1024 matrix multiplication with varying percentages of parallel processes (basically CPU and GPU) from 0 to 100 and the below is the plot for the same...

![image](https://github.com/user-attachments/assets/862aba2a-4d7b-4587-abc7-3c128de6e3cb)


> [!NOTE]
> When trying to run the `plot.py` make sure you are in the `matrix_multiplication_using_cuda` directory \
> Also, make sure to have the `nvidia-cuda-toolkit` installed

## The System Specs

> [!IMPORTANT]
> The specifications of the system from which the graphs are plotted... \
> OS : Linux Mint 21.3 \
> CPU : AMD Ryzen 5 5600H \
> GPU : Nvidia GeForce GTX 1650 \
> CUDA : Version 12.2
