#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "ppmCU.h"

#define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true) {
    if (code != cudaSuccess) {
        fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
        if (abort) exit(code);
    }
}

// Image from:
// http://7-themes.com/6971875-funny-flowers-pictures.html

__global__ void performNewIdeaIterationGPU(int width, int height, float* imageOut, float* imageIn, int size) {
    int thread_x = blockIdx.x * blockDim.x + threadIdx.x;
    int thread_y = blockIdx.y * blockDim.y + threadIdx.y;
    if (thread_x >= width || thread_y >= height) {
        return;
    }

    float sumR = 0.;
    float sumG = 0.;
    float sumB = 0.;
    int countIncluded = 0;
    for(int x = -size; x <= size; x++) {
    
        for(int y = -size; y <= size; y++) {
            int currentX = thread_x + x;
            int currentY = thread_y + y;
            
            // Check if we are outside the bounds
            if(currentX < 0)
                continue;
            if(currentX >= width)
                continue;
            if(currentY < 0)
                continue;
            if(currentY >= height)
                continue;
            
            // Now we can begin
            int offset = (width * currentY * 3) + (currentX * 3);
            sumR += imageIn[offset];
            sumG += imageIn[offset+1];
            sumB += imageIn[offset+2];
        
            // Keep track of how many values we have included
            countIncluded++;
        }
    
    }
    
    // Now we compute the final value for all colours
    float valueR = sumR / countIncluded;
    float valueG = sumG / countIncluded;
    float valueB = sumB / countIncluded;
    
    // Update the output image
    int offset = (width * thread_y * 3) + (thread_x * 3);
    imageOut[offset] = valueR;
    imageOut[offset+1] = valueG;
    imageOut[offset+2] = valueB;
}

__global__ void performNewIdeaFinalizationGPU(int width, int height, float* imageInSmall, float* imageInLarge, unsigned char* imageOut) {
    int thread_x = blockIdx.x * blockDim.x + threadIdx.x;
    int thread_y = blockIdx.y * blockDim.y + threadIdx.y;
    if (thread_x >= width || thread_y >= height) {
        return;
    }

    int offset = width * thread_y * 3 + thread_x * 3;

    float value = (imageInLarge[offset] - imageInSmall[offset]);
    if(value > 255.0f)
        imageOut[offset] = 255;
    else if (value < -1.0f) {
        value = 257.0f+value;
        if(value > 255.0f)
            imageOut[offset] = 255;
        else
            imageOut[offset] = floorf(value);
    } else if (value > -1.0f && value < 0.0f) {
        imageOut[offset] = 0;
    } else {
        imageOut[offset] = floorf(value);
    }
    
    value = (imageInLarge[offset+1] - imageInSmall[offset+1]);
    if(value > 255.0f)
        imageOut[offset+1] = 255;
    else if (value < -1.0f) {
        value = 257.0f+value;
        if(value > 255.0f)
            imageOut[offset+1] = 255;
        else
            imageOut[offset+1] = floorf(value);
    } else if (value > -1.0f && value < 0.0f) {
        imageOut[offset+1] = 0;
    } else {
        imageOut[offset+1] = floorf(value);
    }
    
    value = (imageInLarge[offset+2] - imageInSmall[offset+2]);
    if(value > 255.0f)
        imageOut[offset+2] = 255;
    else if (value < -1.0f) {
        value = 257.0f+value;
        if(value > 255.0f)
            imageOut[offset+2] = 255;
        else
            imageOut[offset+2] = floorf(value);
    } else if (value > -1.0f && value < 0.0f) {
        imageOut[offset+2] = 0;
    } else {
        imageOut[offset+2] = floorf(value);
    }
}

__global__ void convertImageToNewFormatGPU(int width, int height, float* imageUnchanged, unsigned char* originalData) {
    // Determine unique thread ID
    int thread_x = blockIdx.x * blockDim.x + threadIdx.x;
    int thread_y = blockIdx.y * blockDim.y + threadIdx.y;
    // Bounds check due to all-in-one formula for minimum block amount
    if (thread_x >= width || thread_y >= height) {
        return;
    }
    // Calculate offset
    int offset = width * thread_y * 3 + thread_x * 3;

    // Transform to float
    imageUnchanged[offset]   = __uint2float_rd(originalData[offset]);
    imageUnchanged[offset+1] = __uint2float_rd(originalData[offset+1]);
    imageUnchanged[offset+2] = __uint2float_rd(originalData[offset+2]);
}

typedef struct {
     float red,green,blue;
} AccuratePixel;

typedef struct {
     int x, y;
     AccuratePixel *data;
} AccurateImage;

// Convert a PPM image to a high-precision format 
AccurateImage *convertImageToNewFormat(PPMImage *image) {
    // Make a copy
    AccurateImage *imageAccurate;
    imageAccurate = (AccurateImage *)malloc(sizeof(AccurateImage));
    imageAccurate->data = (AccuratePixel*)malloc(image->x * image->y * sizeof(AccuratePixel));
    for(int i = 0; i < image->x * image->y; i++) {
        imageAccurate->data[i].red   = (float) image->data[i].red;
        imageAccurate->data[i].green = (float) image->data[i].green;
        imageAccurate->data[i].blue  = (float) image->data[i].blue;
    }
    imageAccurate->x = image->x;
    imageAccurate->y = image->y;
    
    return imageAccurate;
}

// Convert a high-precision format to a PPM image
PPMImage *convertNewFormatToPPM(AccurateImage *image) {
    // Make a copy
    PPMImage *imagePPM;
    imagePPM = (PPMImage *)malloc(sizeof(PPMImage));
    imagePPM->data = (PPMPixel*)malloc(image->x * image->y * sizeof(PPMPixel));
    for(int i = 0; i < image->x * image->y; i++) {
        imagePPM->data[i].red   = (unsigned char) image->data[i].red;
        imagePPM->data[i].green = (unsigned char) image->data[i].green;
        imagePPM->data[i].blue  = (unsigned char) image->data[i].blue;
    }
    imagePPM->x = image->x;
    imagePPM->y = image->y;
    
    return imagePPM;
}

AccurateImage *createEmptyImage(PPMImage *image){
    AccurateImage *imageAccurate;
    imageAccurate = (AccurateImage *)malloc(sizeof(AccurateImage));
    imageAccurate->data = (AccuratePixel*)malloc(image->x * image->y * sizeof(AccuratePixel));
    imageAccurate->x = image->x;
    imageAccurate->y = image->y;
    
    return imageAccurate;
}

// free memory of an AccurateImage
void freeImage(AccurateImage *image){
    free(image->data);
    free(image);
}

void performNewIdeaIteration(AccurateImage *imageOut, AccurateImage *imageIn, int size) {
    
    // Iterate over each pixel
    for(int senterX = 0; senterX < imageIn->x; senterX++) {
    
        for(int senterY = 0; senterY < imageIn->y; senterY++) {
            
            // For each pixel we compute the magic number
            float sumR = 0;
            float sumG = 0;
            float sumB = 0;
            int countIncluded = 0;
            for(int x = -size; x <= size; x++) {
            
                for(int y = -size; y <= size; y++) {
                    int currentX = senterX + x;
                    int currentY = senterY + y;
                    
                    // Check if we are outside the bounds
                    if(currentX < 0)
                        continue;
                    if(currentX >= imageIn->x)
                        continue;
                    if(currentY < 0)
                        continue;
                    if(currentY >= imageIn->y)
                        continue;
                    
                    // Now we can begin
                    int numberOfValuesInEachRow = imageIn->x; 
                    int offsetOfThePixel = (numberOfValuesInEachRow * currentY + currentX);
                    sumR += imageIn->data[offsetOfThePixel].red;
                    sumG += imageIn->data[offsetOfThePixel].green;
                    sumB += imageIn->data[offsetOfThePixel].blue;
                
                    // Keep track of how many values we have included
                    countIncluded++;
                }
            
            }
            
            // Now we compute the final value for all colours
            float valueR = sumR / countIncluded;
            float valueG = sumG / countIncluded;
            float valueB = sumB / countIncluded;
            
            // Update the output image
            int numberOfValuesInEachRow = imageOut->x; // R, G and B
            int offsetOfThePixel = (numberOfValuesInEachRow * senterY + senterX);
            imageOut->data[offsetOfThePixel].red = valueR;
            imageOut->data[offsetOfThePixel].green = valueG;
            imageOut->data[offsetOfThePixel].blue = valueB;
        }
    }
}

// Perform the final step, and save it as a ppm in imageOut
void performNewIdeaFinalization(AccurateImage *imageInSmall, AccurateImage *imageInLarge, PPMImage *imageOut) {

    
    imageOut->x = imageInSmall->x;
    imageOut->y = imageInSmall->y;
    
    for(int i = 0; i < imageInSmall->x * imageInSmall->y; i++) {
        float value = (imageInLarge->data[i].red - imageInSmall->data[i].red);
        if(value > 255.0f)
            imageOut->data[i].red = 255;
        else if (value < -1.0f) {
            value = 257.0f+value;
            if(value > 255.0f)
                imageOut->data[i].red = 255;
            else
                imageOut->data[i].red = floorf(value);
        } else if (value > -1.0f && value < 0.0f) {
            imageOut->data[i].red = 0;
        } else {
            imageOut->data[i].red = floorf(value);
        }
        
        value = (imageInLarge->data[i].green - imageInSmall->data[i].green);
        if(value > 255.0f)
            imageOut->data[i].green = 255;
        else if (value < -1.0f) {
            value = 257.0f+value;
            if(value > 255.0f)
                imageOut->data[i].green = 255;
            else
                imageOut->data[i].green = floorf(value);
        } else if (value > -1.0f && value < 0.0f) {
            imageOut->data[i].green = 0;
        } else {
            imageOut->data[i].green = floorf(value);
        }
        
        value = (imageInLarge->data[i].blue - imageInSmall->data[i].blue);
        if(value > 255.0f)
            imageOut->data[i].blue = 255;
        else if (value < -1.0f) {
            value = 257.0f+value;
            if(value > 255.0f)
                imageOut->data[i].blue = 255;
            else
                imageOut->data[i].blue = floorf(value);
        } else if (value > -1.0f && value < 0.0f) {
            imageOut->data[i].blue = 0;
        } else {
            imageOut->data[i].blue = floorf(value);
        }
    }
}

int main(int argc, char** argv) {
    
    PPMImage *image;
    
    // Determine which input stream to use
    if(argc > 1) {
        image = readPPM("flower.ppm");
    } else {
        image = readStreamPPM(stdin);
    }

    // Allocate space for final image
    PPMImage *imageOut;
    imageOut = (PPMImage *)malloc(sizeof(PPMImage));
    imageOut->data = (PPMPixel*)malloc(image->x * image->y * sizeof(PPMPixel));

    // Set up image dimensions
    int height, width;
    width = image->x;
    height = image->y;
    imageOut->x = width;
    imageOut->y = height;

    // Determine our thread block and thread grid size
    dim3 dimGrid(
        ceilf((width + 31) / 32),
        ceilf((height + 31) / 32)
    );
    dim3 dimBlock(
        32,
        32
    );

    // Cache our needed bytecounts for accurate and PPM images
    size_t imageSize = sizeof(float) * width * height * 3;
    size_t imageSizePPM = sizeof(unsigned char) * width * height * 3;

    // Declare device memory pointers
    float* devImageUnchanged;
    float* devImageBuffer;
    float* devImageSmall;
    float* devImageBig;
    unsigned char* devImageOut;

    // Allocate memory on the device
    gpuErrchk(cudaMalloc((void**)&devImageUnchanged, imageSize));
    gpuErrchk(cudaMalloc((void**)&devImageBuffer, imageSize));
    gpuErrchk(cudaMalloc((void**)&devImageSmall, imageSize));
    gpuErrchk(cudaMalloc((void**)&devImageBig, imageSize));
    gpuErrchk(cudaMalloc((void**)&devImageOut, imageSizePPM));
    gpuErrchk(cudaDeviceSynchronize());

    // Copy original image data
    cudaMemcpy(devImageOut, image->data, imageSizePPM, cudaMemcpyHostToDevice);
    gpuErrchk(cudaPeekAtLastError());

    // Transform to accurate format
    convertImageToNewFormatGPU<<<dimGrid, dimBlock>>>(width, height, devImageUnchanged, devImageOut);
    gpuErrchk(cudaPeekAtLastError());

    // Process the tiny case:
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageUnchanged, 2);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageSmall, 2);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBuffer, 2);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageSmall, 2);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBuffer, 2);
    gpuErrchk(cudaPeekAtLastError());

    // Process the small case:
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageUnchanged, 3);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageBig, 3);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageBuffer, 3);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageBig, 3);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageBuffer, 3);
    gpuErrchk(cudaPeekAtLastError());

    // Save tiny case result
    performNewIdeaFinalizationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBig, devImageOut);
    gpuErrchk(cudaPeekAtLastError());
    
    // Put finalized data in imageOut buffer for filewrite
    cudaMemcpy(imageOut->data, devImageOut, imageSizePPM, cudaMemcpyDeviceToHost);
    gpuErrchk(cudaPeekAtLastError());

    if(argc > 1) {
        writePPM("flower_tiny.ppm", imageOut);
    } else {
        writeStreamPPM(stdout, imageOut);
    }

    // Process the medium case
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageUnchanged, 5);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageSmall, 5);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBuffer, 5);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageSmall, 5);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBuffer, 5);
    gpuErrchk(cudaPeekAtLastError());
    
    // Save small case
    performNewIdeaFinalizationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageSmall, devImageOut);
    gpuErrchk(cudaPeekAtLastError());

    // Put finalized data in imageOut buffer for filewrite
    cudaMemcpy(imageOut->data, devImageOut, imageSizePPM, cudaMemcpyDeviceToHost);
    gpuErrchk(cudaPeekAtLastError());

    if(argc > 1) {
        writePPM("flower_small.ppm", imageOut);
    } else {
        writeStreamPPM(stdout, imageOut);
    }
    
    // Process the large case
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageUnchanged, 8);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageBig, 8);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageBuffer, 8);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBuffer, devImageBig, 8);
    gpuErrchk(cudaPeekAtLastError());
    performNewIdeaIterationGPU<<<dimGrid, dimBlock>>>(width, height, devImageBig, devImageBuffer, 8);
    gpuErrchk(cudaPeekAtLastError());

    // Save the medium case   
    performNewIdeaFinalizationGPU<<<dimGrid, dimBlock>>>(width, height, devImageSmall, devImageBig, devImageOut);
    gpuErrchk(cudaPeekAtLastError());

    // Put finalized data in imageOut buffer for filewrite
    cudaMemcpy(imageOut->data, devImageOut, imageSizePPM, cudaMemcpyDeviceToHost);
    gpuErrchk(cudaPeekAtLastError());

    if(argc > 1) {
        writePPM("flower_medium.ppm", imageOut);
    } else {
        writeStreamPPM(stdout, imageOut);
    }

    // Free GPU allocated memory structures
    cudaFree(devImageUnchanged);
    cudaFree(devImageBuffer);
    cudaFree(devImageSmall);
    cudaFree(devImageBig);
    cudaFree(devImageOut);

    // Free host memory structures
    free(imageOut->data);
    free(imageOut);
    free(image->data);
    free(image);
    
    return 0;
}

