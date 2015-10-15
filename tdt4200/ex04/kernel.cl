/* OpenCL Kernel declarations */

struct Color {
	float angle;
	float intensity;
};

struct CircleInfo {
	float x;
	float y;
	float radius;
	struct Color color;
};

struct LineInfo {
	float x1, y1;
	float x2, y2;
	float thickness;
	struct Color color;
};

float truncf(float val) {
    float t = convert_float(trunc(val));
    if (val - t < 0.75f) { return t; }
    else { return t + 1.0f; }
}

float red(float deg) {
	float a1 = 1.f/60;
	float b1 = 2;
	float a2 = -1.f/60;
	float b2 = 2;
	float asc = deg * a2 + b2;
	float desc = deg * a1 + b1;
	return fmax(.0f , fmin(1.f, fmin(asc, desc)));
}

float green(float deg) {
	float a1 = 1.f/60;
	float b1 = 0;
	float a2 = -1.f/60;
	float b2 = 4;
	float asc = deg * a2 + b2;
	float desc = deg * a1 + b1;
	return fmax(.0f, fmin(1.f, fmin(asc, desc)));
}

float blue(float deg) {
	float a1 = 1.f/60;
	float b1 = -2;
	float a2 = -1.f/60;
	float b2 = 6;
	float asc = deg * a2 + b2;
	float desc = deg * a1 + b1;
	return fmax(.0f, fmin(1.f, fmin(asc, desc)));
}

float rgb_blue(float hue, float intensity) {
    return blue(hue) * intensity;
}

float rgb_red(float hue, float intensity) {
    return red(hue) * intensity;
}

float rgb_green(float hue, float intensity) {
    return green(hue) * intensity;
}

float delta_square(float x1, float x2, float y1, float y2) {
    return pow(x2-x1, 2) + pow(y2-y1, 2);
}
bool inside_circle(float x, float y, float c_x, float c_y, float r) {
    return delta_square(x, c_x, y, c_y) <= pow(r, 2);
}

// Distance from a point in 2D space to a line segment
float point_to_line(float x0, float x1, float x2, float y0, float y1, float y2) {
    float perpendicular = fabs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - x1 * y2);
    float line_length = sqrt(pow(y2 - y1, 2) + pow(x2 - x1, 2));
    float point_to_line = perpendicular / line_length;

    return point_to_line;
}

// Check if distance from point to line segment is less than half its thickness
bool on_line(float x0, float x1, float x2, float y0, float y1, float y2, float t) {

    float xmin, xmax, ymin, ymax;
    xmin = fmin(x1, x2);
    xmax = fmax(x1, x2);
    ymin = fmin(y1, y2) - t / 2.f;
    ymax = fmax(y1, y2) + t / 2.f;

    if (xmin <= x0 && x0 <= xmax && ymin <= y0 && y0 <= ymax) {
        return point_to_line(x0, x1, x2, y0, y1, y2) < t / 2.f;
    } else {
        return false;
    }
}

/* KERNELS */

__kernel
void test(__global uchar *output,
          __global struct LineInfo *li,
          __global struct CircleInfo *ci,
          int numLines,
          int numCircles,
          int width,
          int height) {

    const int TX = get_global_id(0);
    const int TY = get_global_id(1);

    int offset = TY * width * 3 + TX * 3;
    
    output[offset] = 0;
    output[offset + 1] = 0;
    output[offset + 2] = 0;
    
    for (int i = 0; i < numCircles; i++) {
        struct CircleInfo c = ci[i];
        if (inside_circle(TX, TY, c.x, c.y, c.radius)) {
            output[offset] = min(convert_uchar(255), convert_uchar(output[offset] + rgb_red(c.color.angle, c.color.intensity)));
            output[offset + 1] = min(convert_uchar(255), convert_uchar(output[offset + 1] + rgb_green(c.color.angle, c.color.intensity)));
            output[offset + 2] = min(convert_uchar(255), convert_uchar(output[offset + 2] + rgb_blue(c.color.angle, c.color.intensity)));
        }
    }
    
    for (int i = 0; i < numLines; i++) {
        struct LineInfo l = li[i];
        if (on_line(TX, l.x1, l.x2, TY, l.y1, l.y2, l.thickness)) {
            output[offset] = min(convert_uchar(255), convert_uchar(output[offset] + rgb_red(l.color.angle, l.color.intensity)));
            output[offset + 1] = min(convert_uchar(255), convert_uchar(output[offset + 1] + rgb_green(l.color.angle, l.color.intensity)));
            output[offset + 2] = min(convert_uchar(255), convert_uchar(output[offset + 2] + rgb_blue(l.color.angle, l.color.intensity)));
        }
    }
}

