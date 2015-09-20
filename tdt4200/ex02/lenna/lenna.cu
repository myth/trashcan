#include <iostream>
#include <stdio.h>
#include "lodepng.h"

// Pixel invert kernel
__global__ void invertPixels(unsigned char* img){
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  img[i] = ~img[i];
}

int main( int argc, char ** argv) {

  int N;
  size_t pngsize;
  unsigned char *png = NULL;
  const char * filename = "lenna512x512_inv.png";
  /* Read in the image */
  lodepng_load_file(&png, &pngsize, filename);
 
  unsigned char *image = NULL;
  unsigned int width, height;
  /* Decode it into a RGB 8-bit per channel vector */
  unsigned int error = lodepng_decode24(&image, &width, &height, png, pngsize);

  /* Check if read and decode of .png went well */
  if(error != 0){
      std::cout << "error " << error << ": " << lodepng_error_text(error) << std::endl;
  }

  // Set the number of elements
  N = height * width * 3;
  // Set the needed memory
  size_t size = N * sizeof(unsigned char);
  
  // Allocate vector space in dev memory
  unsigned char* d_Array;
  cudaMalloc(&d_Array, size);

  // Initialize the events
  cudaEvent_t e1, e2;
  float kernel_ms, device_ms, host_ms;

  // Start first timer
  cudaEventCreate(&e1);
  cudaEventCreate(&e2);

  // Copy vector data to dev memory
  cudaEventRecord(e1, 0);
  cudaMemcpy(d_Array, image, size, cudaMemcpyHostToDevice),
  cudaEventRecord(e2, 0);
  cudaEventSynchronize(e2);
  cudaEventElapsedTime(&host_ms, e1, e2);


  // Invoke kernel
  int threadsPerBlock = 256;
  cudaEventRecord(e1, 0);
  invertPixels<<<N / threadsPerBlock, threadsPerBlock>>>(d_Array);
  cudaEventRecord(e2, 0);
  cudaEventSynchronize(e2);
  cudaEventElapsedTime(&kernel_ms, e1, e2);


  // Copy from device to host
  cudaEventRecord(e1, 0);
  cudaMemcpy(image, d_Array, size, cudaMemcpyDeviceToHost),
  cudaEventRecord(e2, 0);
  cudaEventSynchronize(e2);
  cudaEventElapsedTime(&device_ms, e1, e2);


  // Free device memory and events
  cudaFree(d_Array);
  cudaEventDestroy(e1);
  cudaEventDestroy(e2);

  // Print results
  printf("Kernel: %fms\nH->D: %fms\nD->H: %fms\nTot transfer: %fms\n",
          kernel_ms, device_ms, host_ms, device_ms + host_ms);

  /* Save the result to a new .png file */
  lodepng_encode24_file("lenna512x512_orig.png", image, width, height);

  return 0;
}

