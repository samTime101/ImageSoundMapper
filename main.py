from converter.image_sound_mapper import SoundImageMapper

converter = SoundImageMapper(
    image_path="src_image/image.png",
    grayscale_path="images/grayscale_image.png",
    resized_path="images/resized_image.png",
    sound_path="sounds/frequency.wav",
    save_path="outputs/frequency_image.png",
)

converter.compress_image_with_new_dimension((50, 50))
converter.image_to_grayscale()
pixels = converter.pixel_value_extractor()
freqs = converter.pixel_to_frequency(pixels)
converter.frequency_to_sound(freqs)
detected_chunks , detected_sr = converter.audio_file_to_chunks()
detected_freqs = converter.sound_to_frequency(detected_chunks , detected_sr)
converter.sound_to_image(detected_freqs)
