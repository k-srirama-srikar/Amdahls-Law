#include <iostream>
#include <cuda.h>
#include <chrono>

using namespace std;

#define N 1024
// We use it for a matrix of dimension N x N

// Kernel for parallel matrix multiplication
__global__ void matMulParallel(float *A, float *B, float *C, int start, int end){
    /*
    Note: A kernal function is a function that is executed on the GPU...
    The __global__ keyword in CUDA marks this function as a kernel, 
    meaning it can be called from the host (CPU) and executed on the device (GPU)... 
    */
    int row = blockIdx.y*blockDim.y + threadIdx.y;
    int col = blockIdx.x*blockDim.x + threadIdx.x;
    /*
    blockIdx, blockDim, and threadIdx are special variables in CUDA that provide the index of the block and thread within that block...
    blockIdx gives the index of the block in the grid.
    blockDim gives the number of threads per block.
    threadIdx gives the index of the thread within the block.
    */
    if(row>=start && row< end && col<N){
        float value = 0;
        for (int k=0; k<N; k++){
            value+=A[row*N+k]*B[k*N+col];
        }
        C[row*N+col]=value;
    }
}

// sequential matrix multiplication
void matMulSequential(float *A, float *B, float *C, int start, int end){
    for (int i = start; i < end; i++) {
        for (int j = 0; j < N; j++) {
            float value = 0;
            for (int k = 0; k < N; k++) {
                value += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = value;
        }
    }
}

int main(int argc, char **argv){
    if(argc!=2){
        cerr << "Usage: "<< argv[0] << " <sequential_percentage>" << endl;
        return -1;
    }

    float sequentialPercentage = atof(argv[1]);

    if(sequentialPercentage<0.0f || sequentialPercentage>1.0f){
        // the break cases
        cerr << "Error: sequential percentage must be between 0.0 and 1.0" << endl;
        return -1;
    }

    // host matrices -  the matrices accessible by the cpu
    float *h_A, *h_B, *h_C;
    // device matrices - the matrices accessible by the gpu
    float *d_A, *d_B, *d_C;

    // note that we are considering the matrices as a 1 dimentional array here

    size_t bytes = N*N*sizeof(float);

    // allocate host memory
    h_A = (float *)malloc(bytes);
    h_B = (float *)malloc(bytes);
    h_C = (float *)malloc(bytes);

    // initializing matrices
    // note that i've initialised matrices in a basic manner it can be made better (like randomizing it) if need be
    for (int i = 0; i < N * N; i++) {
        h_A[i] = 1.0f;
        h_B[i] = 1.0f;
    }

    // allocate device memory
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    // copying data from host to device
    cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);

    // now definig the sequential and parallel split
    int sequentialRows = N*sequentialPercentage;
    int parallelRows = N - sequentialRows;

    // measuring the execution time
    auto start = chrono::high_resolution_clock::now();

    // sequential computation
    matMulSequential(h_A, h_B, h_C, 0, sequentialRows);


    // parallel computation
    dim3 threads(16,16);
    dim3 blocks((N + threads.x-1)/threads.x, (N+threads.y-1)/threads.y);
    matMulParallel<<<blocks, threads>>>(d_A, d_B, d_C, sequentialRows, N);
    // the above line launches the cuda kernel with the specified grid and block dimenstions
    
    cudaDeviceSynchronize();
    cudaMemcpy(h_C+sequentialRows*N, d_C+sequentialRows*N, parallelRows*N*sizeof(float), cudaMemcpyDeviceToHost);
    // copies the memory in the fromat (destination, source, size, direction)
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "Execution time: " << elapsed.count() << " seconds" << endl;

    // freedom #erenYaegar
    free(h_A);
    free(h_B);
    free(h_C);
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;

}