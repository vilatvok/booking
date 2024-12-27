from abc import ABC, abstractmethod

from src.application.interfaces.services.tokens import ITokenService


class IBackgroundTasksService(ABC):
    @abstractmethod
    def send_mail(self, subject: str, text: str, recipient: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_confirmation_letter(
        self,
        token_service: ITokenService,
        recipient: str,
        token_data: dict,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def send_reset_password(
        self,
        token_service: ITokenService,
        recipient: str,
        token_data: dict,
    ) -> str:
        raise NotImplementedError
