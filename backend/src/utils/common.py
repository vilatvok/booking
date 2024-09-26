from fastapi import HTTPException, status


async def generate_image_path(path, image):
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid content type',
        )

    path = path + image.filename

    # save avatar in media
    with open('src/' + path, 'wb') as f:
        f.write(await image.read())

    return path
