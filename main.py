from converter.image_sound_mapper import ImageToSound , SoundToImage

IMAGE_PATH = "src_image/image.png"
GRAYSCALE_PATH = "images/grayscale_image.png"
RESIZED_PATH = "images/resized_image.png"

SOUND_PATH = "sounds/frequency.wav"
SAVE_PATH = "reconstructed_image/reconstructed_image.png"


its = ImageToSound(IMAGE_PATH,GRAYSCALE_PATH,RESIZED_PATH,SOUND_PATH)

its.compress_image_with_new_dimension((50, 50))
its.image_to_grayscale()
pixels = its.pixel_value_extractor()
freqs = its.pixel_to_frequency(pixels)
its.frequency_to_sound(freqs)

sti = SoundToImage(SOUND_PATH,SAVE_PATH)

detected_chunks , detected_sr = sti.audio_file_to_chunks()
detected_freqs = sti.sound_to_frequency(detected_chunks , detected_sr)
sti.sound_to_image(detected_freqs)
