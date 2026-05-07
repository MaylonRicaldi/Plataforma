from abc import ABC, abstractmethod

class AnalyticsPort(ABC):

    @abstractmethod
    def analizar(self):
        pass