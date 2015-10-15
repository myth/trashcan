#define _GNU_SOURCE

#include <CL/opencl.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <tgmath.h>
#include <math.h>

#include "lodepng.h"
#include "pinkfloyd.h"

#define DEBUG 0

#ifndef max
#define max(a,b) (((a) >= (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))
#endif

void print_error(cl_int error_code);
const char *analyze_cl_error(cl_int error);

const char *analyze_cl_error(cl_int error) {
    switch (error) {
                // Run-time and JIT compiler errors
        case 0: return "CL_SUCCESS";
        case -1: return "CL_DEVICE_NOT_FOUND";
        case -2: return "CL_DEVICE_NOT_AVAILABLE";
        case -3: return "CL_COMPILER_NOT_AVAILABLE";
        case -4: return "CL_MEM_OBJECT_ALLOCATION_FAILURE";
        case -5: return "CL_OUT_OF_RESOURCES";
        case -6: return "CL_OUT_OF_HOST_MEMORY";
        case -7: return "CL_PROFILING_INFO_NOT_AVAILABLE";
        case -8: return "CL_MEM_COPY_OVERLAP";
        case -9: return "CL_IMAGE_FORMAT_MISMATCH";
        case -10: return "CL_IMAGE_FORMAT_NOT_SUPPORTED";
        case -11: return "CL_BUILD_PROGRAM_FAILURE";
        case -12: return "CL_MAP_FAILURE";
        case -13: return "CL_MISALIGNED_SUB_BUFFER_OFFSET";
        case -14: return "CL_EXEC_STATUS_ERROR_FOR_EVENTS_IN_WAIT_LIST";
        case -15: return "CL_COMPILE_PROGRAM_FAILURE";
        case -16: return "CL_LINKER_NOT_AVAILABLE";
        case -17: return "CL_LINK_PROGRAM_FAILURE";
        case -18: return "CL_DEVICE_PARTITION_FAILED";
        case -19: return "CL_KERNEL_ARG_INFO_NOT_AVAILABLE";
        // Compile-time errors
        case -30: return "CL_INVALID_VALUE";
        case -31: return "CL_INVALID_DEVICE_TYPE";
        case -32: return "CL_INVALID_PLATFORM";
        case -33: return "CL_INVALID_DEVICE";
        case -34: return "CL_INVALID_CONTEXT";
        case -35: return "CL_INVALID_QUEUE_PROPERTIES";
        case -36: return "CL_INVALID_COMMAND_QUEUE";
        case -37: return "CL_INVALID_HOST_PTR";
        case -38: return "CL_INVALID_MEM_OBJECT";
        case -39: return "CL_INVALID_IMAGE_FORMAT_DESCRIPTOR";
        case -40: return "CL_INVALID_IMAGE_SIZE";
        case -41: return "CL_INVALID_SAMPLER";
        case -42: return "CL_INVALID_BINARY";
        case -43: return "CL_INVALID_BUILD_OPTIONS";
        case -44: return "CL_INVALID_PROGRAM";
        case -45: return "CL_INVALID_PROGRAM_EXECUTABLE";
        case -46: return "CL_INVALID_KERNEL_NAME";
        case -47: return "CL_INVALID_KERNEL_DEFINITION";
        case -48: return "CL_INVALID_KERNEL";
        case -49: return "CL_INVALID_ARG_INDEX";
        case -50: return "CL_INVALID_ARG_VALUE";
        case -51: return "CL_INVALID_ARG_SIZE";
        case -52: return "CL_INVALID_KERNEL_ARGS";
        case -53: return "CL_INVALID_WORK_DIMENSION";
        case -54: return "CL_INVALID_WORK_GROUP_SIZE";
        case -55: return "CL_INVALID_WORK_ITEM_SIZE";
        case -56: return "CL_INVALID_GLOBAL_OFFSET";
        case -57: return "CL_INVALID_EVENT_WAIT_LIST";
        case -58: return "CL_INVALID_EVENT";
        case -59: return "CL_INVALID_OPERATION";
        case -60: return "CL_INVALID_GL_OBJECT";
        case -61: return "CL_INVALID_BUFFER_SIZE";
        case -62: return "CL_INVALID_MIP_LEVEL";
        case -63: return "CL_INVALID_GLOBAL_WORK_SIZE";
        case -64: return "CL_INVALID_PROPERTY";
        case -65: return "CL_INVALID_IMAGE_DESCRIPTOR";
        case -66: return "CL_INVALID_COMPILER_OPTIONS";
        case -67: return "CL_INVALID_LINKER_OPTIONS";
        case -68: return "CL_INVALID_DEVICE_PARTITION_COUNT";
        // Extension errors
        case -1000: return "CL_INVALID_GL_SHAREGROUP_REFERENCE_KHR";
        case -1001: return "CL_PLATFORM_NOT_FOUND_KHR";
        case -1002: return "CL_INVALID_D3D10_DEVICE_KHR";
        case -1003: return "CL_INVALID_D3D10_RESOURCE_KHR";
        case -1004: return "CL_D3D10_RESOURCE_ALREADY_ACQUIRED_KHR";
        case -1005: return "CL_D3D10_RESOURCE_NOT_ACQUIRED_KHR";
        default: return "Unknown OpenCL error";
        }
}

/*
 * Takes in an error code and prints it to stderr and exits
 */
void print_error(cl_int error_code) {
    fprintf(stderr, "%s\n", analyze_cl_error(error_code));
    exit(1);
}

float point_distance(float x1, float x2, float y1, float y2) {
    return pow(x2-x1, 2) + pow(y2-y1, 2);
}

bool inside_circle(float x, float y, float c_x, float c_y, float r) {
    return point_distance(x, c_x, y, c_y) <= pow(r, 2);
}

bool on_line(float ax, float bx, float cx, float ay, float by, float cy, float t) {
    return -(t) < (cy - ay) * (bx - ax) * (cx - ax) * (by - ay) < t && min(ax, bx) <= max(ax, bx) && min(ay, by) <= cy <= max(ay, by);
}

char *readText(const char *filename) {
	FILE *file = fopen( filename, "r");
	fseek(file, 0, SEEK_END);
	size_t length = ftell(file);
	(void) fseek(file, 0L, SEEK_SET);
	char *content = calloc(length + 1, sizeof(char));
	int itemsread = fread(content, sizeof(char), length, file);
	if (itemsread != length ) {
		printf("Error, reeadText(const char *), failed to read file");
		exit(1);
	}
	return content;
}


void parseLine(char *line, struct LineInfo li[], cl_int *lines, int height, int width) {
	float x1, x2, y1, y2, thickness, angle, intensity;
	int items = sscanf(line, "line %f,%f %f,%f %f %f,%f", &x1, &y1, &x2, &y2, &thickness, &angle, &intensity);
	if (7 == items ){
		li[*lines].x1 = x1 * width;
		li[*lines].x2 = x2 * width;
		li[*lines].y1 = y1 * height;
		li[*lines].y2 = y2 * height;
		li[*lines].thickness = thickness * width;
		li[*lines].color.angle = angle;
		li[*lines].color.intensity = intensity;
		(*lines)++;
	}
}


void parseCircle(char *line, struct CircleInfo ci[], cl_int *circles, int height, int width) {
	float x, y, radius;
	struct Color c;
	int items = sscanf(line, "circle %f,%f %f %f,%f", &x, &y, &radius, &c.angle, &c.intensity);
	if (5 == items){
		ci[*circles].x = x * width;
		ci[*circles].y = y * height;
		ci[*circles].radius = radius * width;
		ci[*circles].color.angle = c.angle;
		ci[*circles].color.intensity = c.intensity;
		(*circles)++;
	}
}


void printLines(struct LineInfo li[], cl_int lines) {
	for ( int i = 0 ; i < lines ; i++) {
		fprintf(stderr, "line:	from:%f,%f to:%f,%f thick:%f,	%f,%f\n", li[i].x1, li[i].y1, li[i].x2, li[i].y2, li[i].thickness,li[i].color.angle, li[i].color.intensity);
	}
}


void printCircles(struct CircleInfo ci[], cl_int circles) {
	for (int i = 0 ; i < circles ; i++) {
		fprintf(stderr, "circle %f,%f %f %f,%f\n", ci[i].x,ci[i].y,ci[i].radius, ci[i].color.angle, ci[i].color.intensity);
	}
}

int main() {
 
	// Parse input
	int numberOfInstructions;
	char* *instructions = NULL;
	size_t *instructionLengths;

	struct CircleInfo *circleinfo;
	cl_int circles = 0;
	struct LineInfo *lineinfo;
	cl_int lines = 0;

	char *line = NULL;
	size_t linelen = 0;
	int width = 0, height = 0;
	ssize_t read = getline(&line, &linelen, stdin);

	// Read size of canvas
	sscanf(line, "%d,%d" ,&width, &height);
	read = getline(&line, &linelen, stdin);

	// Read amount of primitives
	sscanf(line, "%d" , &numberOfInstructions);

	// Allocate memory for primitives
	instructions = calloc(sizeof(char*), numberOfInstructions);
	instructionLengths = calloc(sizeof(size_t), numberOfInstructions);
	circleinfo = calloc(sizeof(struct CircleInfo), numberOfInstructions);
	lineinfo = calloc(sizeof(struct LineInfo), numberOfInstructions);

	// Read in each primitive
	for (int i = 0 ; i < numberOfInstructions; i++) {
		ssize_t read = getline(&instructions[i], &instructionLengths[i], stdin);
		
        parseLine(instructions[i], lineinfo, &lines, height, width);
        parseCircle(instructions[i], circleinfo, &circles, height, width);
	}

    // Check that we have read it OK
    if (DEBUG) {
        printLines(lineinfo, lines);
        printCircles(circleinfo, circles);
    }

    // Declare needed OpenCL vars
    cl_int err;
    cl_uint num_platforms, num_devices;
    cl_platform_id platform_id;
    cl_device_id device_id;
    cl_context context;
    cl_command_queue commands;
    cl_program program;
    cl_kernel kernel;

    cl_mem input;
    cl_mem output;

    // Check platforms
    err = clGetPlatformIDs(1, &platform_id, &num_platforms);
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    // Connect to a compute device
    int gpu = 1;
    err = clGetDeviceIDs(
        platform_id,
        gpu ? CL_DEVICE_TYPE_GPU : CL_DEVICE_TYPE_CPU,
        1,
        &device_id,
        &num_devices
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    // Create the context
    cl_context_properties props[] = {
        CL_CONTEXT_PLATFORM,
        (cl_context_properties) platform_id,
        0
    };
    context = clCreateContext(
        props,
        1,
        &device_id,
        NULL,
        NULL,
        &err
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    // Create the command queue
    commands = clCreateCommandQueue(
        context,
        device_id,
        0,
        &err
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }

	// Create OpenCL program
	char *source = readText("kernel.cl");
	program = clCreateProgramWithSource(
		context,
        1,
		(const char **) &source,
		NULL,
        &err
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }
    
    // Build the program
    err = clBuildProgram(
        program,
        1,
        &device_id,
        NULL,
        NULL,
        NULL
    );
    if (err != CL_SUCCESS) {
        fprintf(stderr, "%s\n", analyze_cl_error(err));
        static char err_buffer[1024 * 1024];
        size_t err_length;
        clGetProgramBuildInfo(
            program,
            device_id,
            CL_PROGRAM_BUILD_LOG,
            sizeof(err_buffer),
            err_buffer,
            &err_length
        );
        fprintf(stderr, "%s\n", err_buffer);
        return 1;
    }

	// Create kernel
    kernel = clCreateKernel(
        program,
        "test",
        &err
    );
    if (!kernel || err != CL_SUCCESS) {
        print_error(err);
    }

    // Allocate memory for output array on device
    size_t data_length = sizeof(unsigned char) * width * height * 3;
    output = clCreateBuffer(context, CL_MEM_READ_WRITE, data_length, NULL, NULL);
    if (!output) {
        fprintf(stderr, "Failed to allocate device output memory");
    }

    // Allocate memory for the lineinfo and circleinfo struct arrays
    cl_mem dev_lineinfo = clCreateBuffer(
        context,
        CL_MEM_READ_ONLY,
        sizeof(struct LineInfo) * lines,
        NULL,
        NULL
    );
    if (!dev_lineinfo) {
        fprintf(stderr, "Failed to allocate device lineinfo memory");
    }
    cl_mem dev_circleinfo = clCreateBuffer(
        context,
        CL_MEM_READ_ONLY,
        sizeof(struct CircleInfo) * circles,
        NULL,
        NULL
    );
    if (!dev_circleinfo) {
        fprintf(stderr, "Failed to allocate device circleinfo memory");
    }
    
    // Copy our lineinfo and circleinfo data into device buffer memory
    err = clEnqueueWriteBuffer(
        commands,
        dev_lineinfo,
        CL_TRUE,
        0,
        sizeof(struct LineInfo) * lines,
        lineinfo,
        0,
        NULL,
        NULL
    );
    err |= clEnqueueWriteBuffer(
        commands,
        dev_circleinfo,
        CL_TRUE,
        0,
        sizeof(struct CircleInfo) * circles,
        circleinfo,
        0,
        NULL,
        NULL
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }



    
    // Set kernel args
    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &output);
    err |= clSetKernelArg(kernel, 1, sizeof(cl_mem), &dev_lineinfo);
    err |= clSetKernelArg(kernel, 2, sizeof(cl_mem), &dev_circleinfo);
    err |= clSetKernelArg(kernel, 3, sizeof(cl_int), &lines);
    err |= clSetKernelArg(kernel, 4, sizeof(cl_int), &circles);
    err |= clSetKernelArg(kernel, 5, sizeof(int), &width);
    err |= clSetKernelArg(kernel, 6, sizeof(int), &height);
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    // Execute kernel
    const size_t g_ws[2] = {width, height};
    err = clEnqueueNDRangeKernel(
        commands,
        kernel,
        2,
        NULL,
        g_ws,
        NULL,
        0,
        NULL,
        NULL
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    // Await calculations
    clFinish(commands);

    // Read back data
    unsigned char *result = malloc(data_length);
    err = clEnqueueReadBuffer(
        commands,
        output,
        CL_TRUE,
        0,
        data_length,
        result,
        0,
        NULL,
        NULL
    );
    if (err != CL_SUCCESS) {
        print_error(err);
    }

    if (DEBUG) {
        for (int i = 0; i < 1024; i++) {
            fprintf(stderr, "(%d,%d,%d)", result[i*3], result[i*3+1], result[i*3+2]);
        }
        fprintf(stderr, "\n");
    }

    /* 
     * IMAGE GENERATION
     */

    // Generate the PNG
	size_t png_length = 0;
	unsigned char *png = NULL;
	lodepng_encode24(
		&png,
		&png_length,
		result,
		width,
		height
    );

	// KEEP THIS LINE. Or make damn sure you replace it with something equivalent.
	// This "prints" your png to stdout, permitting I/O redirection
	fwrite(png, sizeof(unsigned char), png_length, stdout);

    /* 
     * CLEANUP
     */

    // Free CL allocated vars
    clReleaseMemObject(output);
    clReleaseMemObject(dev_lineinfo);
    clReleaseMemObject(dev_circleinfo);
    clReleaseProgram(program);
    clReleaseKernel(kernel);
    clReleaseCommandQueue(commands);
    clReleaseContext(context);

    // Free allocated primitives
	free(instructions);
	free(instructionLengths);
	free(circleinfo);
	free(lineinfo);
    free(result);

	return 0;
}
