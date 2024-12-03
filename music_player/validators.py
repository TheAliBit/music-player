from PIL import Image
from mutagen import File as MutagenFile
from rest_framework.exceptions import ValidationError


def validate_image_file(image_file, max_size_mb=3, allowed_formats=('JPEG', 'PNG', 'JPG')):
    """
    Validates an image file.

    :param image_file: The uploaded image file to validate.
    :param max_size_mb: Maximum allowed file size in megabytes.
    :param allowed_formats: Tuple of allowed image formats (e.g., 'JPEG', 'PNG').
    :raises ValidationError: If the file is invalid, too large, or not in an allowed format.
    :return: None
    """
    try:
        img = Image.open(image_file)
        img.verify()  # Verify the file is an image
    except Exception:
        raise ValidationError("The uploaded file is not a valid image.")

    # Validate the image format
    if img.format not in allowed_formats:
        raise ValidationError(f"The image format must be one of {', '.join(allowed_formats)}.")

    # Validate image size
    if image_file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"The image size must not exceed {max_size_mb} MB.")


def validate_audio_file(audio_file, max_size_mb=10, allowed_formats=('MP3', 'WAV', 'FLAC', 'AAC')):
    """
    Validates an audio file.

    :param audio_file: The uploaded audio file to validate.
    :param max_size_mb: Maximum allowed file size in megabytes.
    :param allowed_formats: Tuple of allowed audio formats (e.g., 'MP3', 'WAV').
    :raises ValidationError: If the file is invalid, too large, or not in an allowed format.
    :return: None
    """
    try:
        audio = MutagenFile(audio_file)
        if audio is None:
            raise ValidationError("The uploaded file is not a valid audio file.")
    except Exception:
        raise ValidationError("The uploaded file could not be processed as audio.")

    # Validate the audio format (check file extension in mutagen tags)
    file_format = audio_file.name.split('.')[-1].upper()
    if file_format not in allowed_formats:
        raise ValidationError(f"The audio format must be one of {', '.join(allowed_formats)}.")

    # Validate file size
    if audio_file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"The audio size must not exceed {max_size_mb} MB.")
