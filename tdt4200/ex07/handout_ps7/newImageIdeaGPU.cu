#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "ppmCU.h"

// Image from:
// http://7-themes.com/6971875-funny-flowers-pictures.html

// TODO: You must implement this
// The handout code is much simpler than the MPI/OpenMP versions
//__global__ void performNewIdeaIterationGPU( ... ) { ... }

// TODO: You should implement this
//__global__ void performNewIdeaFinalizationGPU( ... ) { ... }

// TODO: You should implement this
//__global__ void convertImageToNewFormatGPU( ... ) { ... }

// Perhaps some extra kernels will be practical as well?
//__global__ void ...GPU( ... ) { ... }

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
        
	if(argc > 1) {
		image = readPPM("flower.ppm");
	} else {
		image = readStreamPPM(stdin);
	}

	AccurateImage *imageUnchanged = convertImageToNewFormat(image); // save the unchanged image from input image
	AccurateImage *imageBuffer = createEmptyImage(image);
	AccurateImage *imageSmall = createEmptyImage(image);
	AccurateImage *imageBig = createEmptyImage(image);
	
	PPMImage *imageOut;
	imageOut = (PPMImage *)malloc(sizeof(PPMImage));
	imageOut->data = (PPMPixel*)malloc(image->x * image->y * sizeof(PPMPixel));

	// Process the tiny case:
	performNewIdeaIteration(imageSmall, imageUnchanged, 2);
	performNewIdeaIteration(imageBuffer, imageSmall, 2);
	performNewIdeaIteration(imageSmall, imageBuffer, 2);
	performNewIdeaIteration(imageBuffer, imageSmall, 2);
	performNewIdeaIteration(imageSmall, imageBuffer, 2);
	
	// Process the small case:
	performNewIdeaIteration(imageBig, imageUnchanged,3);
	performNewIdeaIteration(imageBuffer, imageBig,3);
	performNewIdeaIteration(imageBig, imageBuffer,3);
	performNewIdeaIteration(imageBuffer, imageBig,3);
	performNewIdeaIteration(imageBig, imageBuffer,3);
	
	// save tiny case result
	performNewIdeaFinalization(imageSmall,  imageBig, imageOut);
	if(argc > 1) {
		writePPM("flower_tiny.ppm", imageOut);
	} else {
		writeStreamPPM(stdout, imageOut);
	}

	
	// Process the medium case:
	performNewIdeaIteration(imageSmall, imageUnchanged, 5);
	performNewIdeaIteration(imageBuffer, imageSmall, 5);
	performNewIdeaIteration(imageSmall, imageBuffer, 5);
	performNewIdeaIteration(imageBuffer, imageSmall, 5);
	performNewIdeaIteration(imageSmall, imageBuffer, 5);
	
	// save small case
	performNewIdeaFinalization(imageBig,  imageSmall,imageOut);
	if(argc > 1) {
		writePPM("flower_small.ppm", imageOut);
	} else {
		writeStreamPPM(stdout, imageOut);
	}

	// process the large case
	performNewIdeaIteration(imageBig, imageUnchanged, 8);
	performNewIdeaIteration(imageBuffer, imageBig, 8);
	performNewIdeaIteration(imageBig, imageBuffer, 8);
	performNewIdeaIteration(imageBuffer, imageBig, 8);
	performNewIdeaIteration(imageBig, imageBuffer, 8);

	// save the medium case
	performNewIdeaFinalization(imageSmall,  imageBig, imageOut);
	if(argc > 1) {
		writePPM("flower_medium.ppm", imageOut);
	} else {
		writeStreamPPM(stdout, imageOut);
	}
	
	// free all memory structures
	freeImage(imageUnchanged);
	freeImage(imageBuffer);
	freeImage(imageSmall);
	freeImage(imageBig);
	free(imageOut->data);
	free(imageOut);
	free(image->data);
	free(image);
	
	return 0;
}

