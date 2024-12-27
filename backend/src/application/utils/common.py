
async def generate_image_path(path: str, image, content_type: str) -> str:
    if content_type not in ['image/jpeg', 'image/png']:
        raise TypeError('Invalid content type')

    # save avatar in media folder
    with open('src/' + path, 'wb') as f:
        f.write(await image.read())

    return path
