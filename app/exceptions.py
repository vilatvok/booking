from fastapi import HTTPException, status


not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Not found',
)

permission_required = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You dont have permission',
)
