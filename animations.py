from PIL import Image
import imageio
import numpy as np

class ImageManipulator:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.frames = []
        self.original_size = self.image.size  # Save the original size

    def zoom_in(self, start_factor, end_factor, steps):
        for zoom_factor in np.linspace(start_factor, end_factor, steps):
            width, height = self.image.size
            new_width = int(width // zoom_factor)
            new_height = int(height // zoom_factor)
            left = int((width - new_width)/2)
            top = int((height - new_height)/2)
            right = int((width + new_width)/2)
            bottom = int((height + new_height)/2)
            
            frame = self.image.crop((left, top, right, bottom))
            frame = frame.resize(self.original_size)  # Resize to original size
            self.frames.append(frame)

    def zoom_out(self, start_factor, end_factor, steps):
        for zoom_factor in np.linspace(start_factor, end_factor, steps):
            width, height = self.image.size
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)
            left = int((width - new_width)/2)
            top = int((height - new_height)/2)
            right = int((width + new_width)/2)
            bottom = int((height + new_height)/2)

            # Crop the image first
            cropped = self.image.crop((left, top, right, bottom))

            # Then resize the cropped image back to original size
            frame = cropped.resize(self.original_size)

            self.frames.append(frame)


    def pan_left_to_right(self, start, end, length, steps):
        width, height = self.image.size
        top = 0
        bottom = height
        for left in np.linspace(start, end-length, steps):
            left = int(left)
            right = left+length
            
            frame = self.image.crop((left, top, right, bottom))
            #frame = frame.resize(self.original_size)  # Resize to original size
            self.frames.append(frame)

    def pan_right_to_left(self, start, end, length, steps):
        width, height = self.image.size
        top = 0
        bottom = height
        for right in np.linspace(end, start+length, steps):
            right = int(right)
            left = right-length
            
            frame = self.image.crop((left, top, right, bottom))
            #frame = frame.resize(self.original_size)  # Resize to original size
            self.frames.append(frame)

    def save_gif(self, filepath):
        images = [np.array(frame) for frame in self.frames]
        imageio.mimsave(filepath, images, format='mp4')  # 50 milliseconds per frame


manipulator = ImageManipulator("imgs/zizek.jpeg")

# Apply operations
#manipulator.zoom_in(1, 2, 50)  # Zoom in gradually from factor 1 to 2, over 50 frames
#manipulator.pan_left_to_right(0, manipulator.image.size[1], 400, 100)  # Pan from left to right gradually, over 50 frames
manipulator.pan_right_to_left(0, manipulator.image.size[1], 300, 100)  # Pan from right to left gradually, over 50 frames
#manipulator.zoom_out(0.25, 1.0, 50)  # Zoom out gradually from factor 1 to 0.5, over 50 frames
#manipulator.zoom_in(1.0, 2, 50)  # Zoom in gradually from factor 0.5 to 1, over 50 frames

# Save as GIF
manipulator.save_gif("outputs/output.mp4")
