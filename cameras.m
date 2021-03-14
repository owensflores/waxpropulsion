%% 8 MP Sony IMX219 camera module with CS lens 2718 for Raspberry Pi V2
% source: https://www.arducam.com/product/arducam-8mp-raspberry-pi-camera-v2-cs-b0102/

focalLength = 3.04 % mm
pixelHeight = 3280 % pixels
pixelWidth = 2464 % pixels
fov = 70 % degrees
sensorHeight = 3.674 % mm
sensorWidth = 2.760 % mm
pixelDiameter = 1.12 *10^(-3) % mm

%% instantaneous field of view iFOV
% iFOV = 2*arctan(r_p/f)
% r_p = pixel radius (half the pixel pitch, I know it's weird)
% f = focal length

r_p = pixelDiameter/2
f = focalLength
iFOV = 2*atan(r_p/f)

%% resolution at a distance
% this is calculated as ground sample distance in satellite design
% and is found by iFOV * distance of sensor to surface captured by image
% small angle approximate gives tan(x) ~= x

distance = 100 % mm, upper limit, whole distance of 2U along long axis
res = iFOV*distance

%% how many pixels is that?
% that res is the amount of resolved distance *per pixel* at 20 cm
% since the holes are 5 mm across, we can find out how many pixels across
% they will be 

target = 5 % mm
pixelCount = target/res


