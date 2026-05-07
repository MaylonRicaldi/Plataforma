class NivelCognitivo:

    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"

    @staticmethod
    def is_valid(value):
        return value in [
            NivelCognitivo.BAJO,
            NivelCognitivo.MEDIO,
            NivelCognitivo.ALTO
        ]
