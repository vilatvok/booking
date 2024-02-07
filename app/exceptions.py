from fastapi import HTTPException, status


not_found = HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')
permission_required = HTTPException(
    status.HTTP_403_FORBIDDEN, 
    'You dont have permission'
)