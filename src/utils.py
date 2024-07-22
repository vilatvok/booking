from typing import Annotated

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


pk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())"))
]