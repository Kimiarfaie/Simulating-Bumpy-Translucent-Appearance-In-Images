from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import math
import params as prm

def modulation_gray(filename, mask_filename):
    # Load the original image and the highlight mask
    img, _, _ = Image.open("./img2/" + filename).convert(prm.color_space).split()
    highlight_mask = Image.open("./mask2/" + mask_filename).convert("L")

    # Convert images to arrays
    f_xy = np.asarray(img)
    f_uv = np.fft.fft2(f_xy)
    shifted_f_uv = np.fft.fftshift(f_uv)


    # Apply Gaussian smoothing to the highlight mask (Optional)
    #highlight_mask = highlight_mask.filter(ImageFilter.GaussianBlur(radius=1.5))  # Adjust 'radius' for smoothing
    
    # Convert highlight mask to array and normalize values between 0 and 1
    highlight_mask = np.asarray(highlight_mask) / 255.0
    
    # Create the frequency domain filter
    x_pass_filter = Image.new(mode="L", size=(shifted_f_uv.shape[0], shifted_f_uv.shape[1]), color=0)
    draw = ImageDraw.Draw(x_pass_filter)
    center = (shifted_f_uv.shape[0] // 2, shifted_f_uv.shape[1] // 2)
    ellipse_pos = (center[0] - prm.outside_r, center[1] - prm.outside_r, center[0] + prm.outside_r, center[1] + prm.outside_r)
    draw.ellipse(ellipse_pos, fill=255)
    ellipse_pos = (center[0] - prm.inside_r, center[1] - prm.inside_r, center[0] + prm.inside_r, center[1] + prm.inside_r)
    draw.ellipse(ellipse_pos, fill=0)
    filter_array = np.asarray(x_pass_filter)

    # Output directory
    out_dir = "./results/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Apply bumpiness suppression (Only for scalefactor < 1)
    gray_signal = []
    shifted_f_uv_ms = shifted_f_uv.copy()
    
    for f in prm.scalefactor:
        # Apply modulation for both suppression and amplification
        for j in range(filter_array.shape[0]):
            for i in range(filter_array.shape[1]): 
                if highlight_mask[j][i] < 0.5:  # Apply modulation only to non-highlight areas
                    if filter_array[j][i] == 255:
                        shifted_f_uv_ms[j][i] = shifted_f_uv[j][i] * f
                    else:
                        shifted_f_uv_ms[j][i] = shifted_f_uv[j][i]
                else:
                    # For highlights, keep the original values
                    shifted_f_uv_ms[j][i] = shifted_f_uv[j][i]

        # Invert FFT to get the processed image back
        unshifted_f_uv = np.fft.fftshift(shifted_f_uv_ms)
        i_f_xy = np.fft.ifft2(unshifted_f_uv).real
        
        # After returning to spatial domain, overlay the highlights from the original image back into the modulated image
        result_image = (highlight_mask * f_xy) + ((1 - highlight_mask) * i_f_xy)

        # Convert to image and store
        gray_signal.append((Image.fromarray(result_image).convert("L"), "{:.2f}".format(f), 1))
    
    return gray_signal

def modulation_color_using_gray(filename, gray) -> None:
    _, cb, cr = Image.open("./images/" + filename).convert(prm.color_space).split()

    out_dir = "./results/"
    image_base_name = os.path.splitext(filename)[0]

    for (signal, string, method) in gray:
        out = Image.merge(prm.color_space, (signal, cb, cr)).convert("RGB")
        if method == 1:
            out.save(out_dir + f"{image_base_name}_masked_{string}.png")

if __name__ == "__main__":
    img_files = os.listdir("./images")
    for file in img_files:
        img_id = os.path.splitext(file)[0]  # Get the number from '1.png', '2.png', etc.
        mask_file = f"mask_{img_id}.png"  # Corresponding mask file 'mask_1.png', 'mask_2.png', etc.

        if os.path.exists(f"./masks/{mask_file}"):
            print(f"Processing {file} with {mask_file}")
            gray = modulation_gray(file, mask_file)
            modulation_color_using_gray(file, gray)
        else:
            print(f"Mask {mask_file} not found, skipping {file}")
