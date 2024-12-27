from factory import errors
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound


class AsyncFactory(SQLAlchemyModelFactory):
    @classmethod
    async def _get_or_create(cls, model_class, session, args, kwargs):
        key_fields = {}
        for field in cls._meta.sqlalchemy_get_or_create:
            if field not in kwargs:
                raise errors.FactoryError(
                    "sqlalchemy_get_or_create - "
                    "Unable to find initialization value for '%s' in factory %s" %
                    (field, cls.__name__))
            key_fields[field] = kwargs.pop(field)

        obj = (await session.execute(
            select(model_class).
            filter_by(*args, **key_fields)
        )).scalar()

        if not obj:
            try:
                obj = await cls._save(model_class, session, args, {**key_fields, **kwargs})
            except IntegrityError as e:
                await session.rollback()

                if cls._original_params is None:
                    raise e

                get_or_create_params = {
                    lookup: value
                    for lookup, value in cls._original_params.items()
                    if lookup in cls._meta.sqlalchemy_get_or_create
                }
                if get_or_create_params:
                    try:
                        obj = (await session.execute(select(model_class).filter_by(
                                **get_or_create_params))).one()

                    except NoResultFound:
                        # Original params are not a valid lookup and triggered a create(),
                        # that resulted in an IntegrityError.
                        raise e
                else:
                    raise e

        return obj

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        return await super()._create(model_class, *args, **kwargs)

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        obj = model_class(*args, **kwargs)
        session.add(obj)
        await session.commit()
        return obj
