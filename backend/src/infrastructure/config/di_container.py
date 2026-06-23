import logging

logger = logging.getLogger(__name__)


class DIContainer:
    """Contenedor simple de dependencias.

    Se inicializa en create_app() con las instancias concretas de
    los adaptadores. Los Services lo consultan para obtener las
    dependencias compartidas, evitando la creación directa de
    instancias en controladores.
    """

    def __init__(self):
        self._repository = None
        self._nlp_service = None
        self._analytics = None

    def init_app(self, repository=None, nlp_service=None, analytics=None):
        self._repository = repository
        self._nlp_service = nlp_service
        self._analytics = analytics
        logger.info("DIContainer inicializado")

    @property
    def repository(self):
        return self._repository

    @property
    def nlp_service(self):
        return self._nlp_service

    @property
    def analytics(self):
        return self._analytics


container = DIContainer()
