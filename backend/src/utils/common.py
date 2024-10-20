from fastapi import HTTPException, status, UploadFile


async def generate_image_path(path: str, image: UploadFile) -> str:
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid content type',
        )

    path = path + image.filename

    # save avatar in media folder
    with open('src/' + path, 'wb') as f:
        f.write(await image.read())

    return path
