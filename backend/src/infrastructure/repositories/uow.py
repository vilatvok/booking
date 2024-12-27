from src.application.interfaces.repositories.uow import IUnitOfWork


class SqlAlchemyUnitOfWork(IUnitOfWork):

    def __init__(self, session_factory):
        self.session = session_factory

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def rollback(self):
        if self.session:
            await self.session.rollback()