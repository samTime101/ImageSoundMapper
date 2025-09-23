# SEP 18 2025
# SAMIP REGMI

# IMPORTS
from PIL import Image
import numpy as np
import scipy.io.wavfile as wav
import os
from matplotlib import pyplot as plt
import librosa

# SOME DECLARATIONS
PIXEL_RANGE = (0, 255)
FREQ_RANGE = (200, 1000)
DURATION_PER_PIXEL = 0.01
SAMPLE_RATE = 44100

class ImageToSound:

    def __init__( self, image_path, grayscale_path, resized_path, sound_path) -> None :
        # FIRST CHECK IF IMAGE_FILE_PATH EXISTS
        try:
            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"IMAGE FILE NOT FOUND: {image_path}")
        except Exception as e:
            print(f"ERROR: {e}")
            return
        
        # CHECK IF DIRECTORIES EXIST, IF NOT CREATE THEM
        for path in [grayscale_path, resized_path, sound_path]:
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)

        # ASSIGN PATHS
        self.image_path = image_path
        self.grayscale_path = grayscale_path
        self.resized_path = resized_path
        self.sound_path = sound_path

    # GET IMAGE DIMENSIONS
    def get_image_dimensions(self) -> tuple | None:
        print("1. GETTING IMAGE DIMENSIONS...")
        try:
            with Image.open(self.image_path) as img:
                width, height = img.size
            return width, height
        except Exception as e:
            print(f"ERROR GETTING IMG DIMENSIONS: {e}")
            return None

    # RESIZE IMAGE
    def compress_image_with_new_dimension(self, new_dimensions: tuple) -> None:
        print("2. RESIZING IMAGE...")
        try:
            with Image.open(self.image_path) as img:
                img = img.resize(new_dimensions)
                img.save(self.resized_path)
        except Exception as e:
            print(f"ERROR COMPRESSING IMG: {e}")

    # CONVERT TO GRAYSCALE
    def image_to_grayscale(self) -> None:
        print("3. CONVERTING RESIZED IMAGE TO GRAYSCALE...")
        try:
            img = Image.open(self.resized_path).convert("L")
            img.save(self.grayscale_path)
        except Exception as e:
            print(f"ERROR LOADING IMAGE: {e}")
    
    # EXTRACT PIXELS
    def pixel_value_extractor(self) -> list:
        print("4. EXTRACTING PIXEL VALUES FROM GRAYSCALE IMAGE...")
        try:
            with Image.open(self.grayscale_path) as img:
                pixels = list(img.getdata())
            return pixels
        except Exception as e:
            print(f"ERROR EXTRACTING PIXELS: {e}")
            return []

    # MAP PIXELS TO FREQUENCIES
    def pixel_to_frequency(self, pixel_data: list) -> list:
        print("5. MAPPING PIXELS TO FREQUENCIES...")
        f_min, f_max = FREQ_RANGE
        p_min, p_max = PIXEL_RANGE

        # LINEAR MAPPING
        freqs = [
            f_min + ((px - p_min) / (p_max - p_min)) * (f_max - f_min)
            for px in pixel_data
        ]
        return freqs
    
    # CONVERT FREQUENCIES TO SOUND
    # https://glowingpython.blogspot.com/2011/09/sound-synthesis.html
    def frequency_to_sound(self, frequency_data: list,duration = DURATION_PER_PIXEL, sample_rate = SAMPLE_RATE) -> None:
        print("6. CONVERTING FREQUENCIES TO SOUND...")
        try:
            samples = []
            number_of_audo_samples = int(sample_rate * duration)
            for freq in frequency_data:
                t = np.linspace(0, duration, number_of_audo_samples)
                wave = np.sin(2 * np.pi * freq * t)
                # print(wave.dtype) # FLOAT 64
                samples.append(wave.astype(np.float32)) 
            full_wave = np.concatenate(samples)
            wav.write(self.sound_path, sample_rate, full_wave)
            print(f"SOUND FILE SAVED: {self.sound_path}")
        except Exception as e:
            print(f"ERROR GENERATING SOUND: {e}")

class SoundToImage:
    def __init__( self, sound_path, save_path) -> None :
        # FIRST CHECK IF SOUND_FILE_PATH EXISTS
        try:
            if not os.path.isfile(sound_path):
                raise FileNotFoundError(f"SOUND FILE NOT FOUND: {sound_path}")
        except Exception as e:
            print(f"ERROR: {e}")
            return
        
        # CHECK IF DIRECTORIES EXIST, IF NOT CREATE THEM
        dir_name = os.path.dirname(save_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # ASSIGN PATHS
        self.sound_path = sound_path
        self.save_path = save_path

    def audio_file_to_chunks(self, chunk_sample = int(SAMPLE_RATE * DURATION_PER_PIXEL)) -> tuple :
        try:
            print("1. LOADING AUDIO FILE AND EXTRACTING CHUNKS...")
            y , sr = librosa.load(self.sound_path, sr=SAMPLE_RATE)
            # print(f"LEN OF SAMPLES IN AUDIO FILE: {len(y)}")
            num_chunks = len(y) // chunk_sample
            
            # SPLIT ALL SAMPLES OF 'y' 1102500 SAMPLES INTO 'num_chunks':2500 CHUNKS
            # EACH CHUNK WILL HAVE 'chunk_sample':441 SAMPLES

            chunks = np.array_split(y, num_chunks)  
            return chunks , sr
        except Exception as e:
            print(f"ERROR: {e}")
            return [] , None        

    # EXTRACT FREQUENCIES FROM SOUND
    def sound_to_frequency(self, chunks: list , sr:int) -> list:
        print("2. EXTRACTING FREQUENCIES FROM AUDIO CHUNKS...")
        try:
            detected_frequencies = []
            for chunk in chunks:
                f0 = librosa.yin(chunk, fmin=FREQ_RANGE[0], fmax=FREQ_RANGE[1], sr=sr)
                # print(f0) # 1 ELEMENT ARRAY
                detected_frequencies.append(f0[0])
            return detected_frequencies
        except Exception as e:
            print(f"ERROR: {e}")
            return []

    # MAP FREQUENCIES BACK TO PIXELS
    def frequency_to_pixel(self, frequency_data: list) -> list:
        print("3. MAPPING FREQUENCIES BACK TO PIXELS...")
        f_min, f_max = FREQ_RANGE
        p_min, p_max = PIXEL_RANGE
        pixels = [
            p_min + ((freq - f_min) / (f_max - f_min)) * (p_max - p_min)
            for freq in frequency_data
        ]
        return pixels
    
    # CONVERT FREQUENCIES BACK TO IMAGE
    # https://stackoverflow.com/questions/71968442/convert-data-pixels-to-image
    def sound_to_image(self, frequency: list, image_size: tuple = (50, 50)) -> None:
        print("4. CONVERTING FREQUENCIES BACK TO IMAGE...")
        try:
            pixel_values = self.frequency_to_pixel(frequency)
            width, height = image_size
            if len(pixel_values) != len(frequency):
                raise ValueError("PIXEL COUNT MISMATCH") 

            img_array = np.array(pixel_values, dtype=np.uint8).reshape((height, width))
            img = Image.fromarray(img_array, mode='L')
            img.save(self.save_path)
            print(f"IMAGE SAVED: {self.save_path}") 
            # plt.imshow(img_array, cmap='gray', vmin=0, vmax=255)
            # plt.show()
        except Exception as e:
            print(f"ERROR SAVING IMAGE: {e}")



