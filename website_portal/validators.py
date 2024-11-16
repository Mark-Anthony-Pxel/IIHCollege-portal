def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError(_('Image file too large ( > 5MB )'))

def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValidationError(_('File size too large ( > 10MB )'))