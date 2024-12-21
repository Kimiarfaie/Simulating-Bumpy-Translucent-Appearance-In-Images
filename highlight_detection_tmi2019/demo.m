% clear old variables
clear all;
close all;
clc;

if ~exist('mask')
    mkdir('mask')
end

img_folder = 'img';

% Get a list of all image files in the folder
img_files = dir(fullfile(img_folder, '*.png'));  % Change extension if needed (e.g., '*.jpg')

% The two parameters are key to obtain better masks.
% Different values of Ts and Tv are often set to produce good results.
% Ts is the threshold value for Saturation channel; Tv is the threshold value for Value channel.
% If you want to obtain better results, please modify the following parameters by yourself.

Ts=0.35;
Tv=0.75  ; % decreasing this would result in more highlights being detected

% 0.75 for all 
% some other 0.9, very bright images -> 1, 4, 5, 7, 16, 29, 34, 41, 44,
% Golden materials were good but this couldn't detect the highlight for
% other materials that well
% Loop through each image in the folder
% for materials that didn''t detect much highlight we eperiment 0.5
for i = 1:length(img_files)
    % Read the image
    img_name = img_files(i).name;
    img_path = fullfile(img_folder, img_name);
    img = im2double(imread(img_path));
    
    % Generate the mask using the sh_detection function
    mask = sh_detection(img, Ts, Tv);
    
    % Display the input image and mask
    %figure;
    %subplot(1, 2, 1); imshow(img); title('Input Image');
    %subplot(1, 2, 2); imshow(mask); title('Mask Map');
    
    % Save the mask
    [~, img_base_name, ~] = fileparts(img_name);  % Get the base image name without extension
    mask_filename = fullfile('mask', ['mask_' img_base_name '.png']);
    imwrite(mask, mask_filename);
    
    % Optionally, display progress
    fprintf('Processed and saved mask for: %s\n', img_name);
end