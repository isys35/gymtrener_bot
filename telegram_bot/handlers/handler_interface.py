from abc import ABC, abstractmethod


class HandlerInterface(ABC):

    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def get_first_name(self):
        pass

    @abstractmethod
    def get_last_name(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_message_id(self):
        pass

    @abstractmethod
    def get_callback(self):
        pass