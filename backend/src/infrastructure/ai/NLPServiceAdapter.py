import os
import json

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


class NLPServiceAdapter:

    def __init__(self):

        api_key = os.getenv(
            "TU API KEY"
        )

        self.gemini_available = False

        try:

            if api_key:

                genai.configure(
                    api_key=api_key
                )

                self.model = genai.GenerativeModel(
                    "models/gemini-1.5-flash-8b"
                )

                self.gemini_available = True

        except Exception as e:

            print(
                "Gemini no disponible:",
                str(e)
            )

    # -------------------------
    # MOTOR LOCAL DE RESPALDO
    # -------------------------

    def local_ai_engine(
        self,
        question_text
    ):

        text = question_text.lower()

        # nivel alto

        if (
            "por qué" in text or
            "analiza" in text or
            "compare" in text or
            "justifique" in text or
            "proponga" in text
        ):

            return {

                "level": "alto",

                "feedback":
                "Pregunta de alto nivel cognitivo que fomenta análisis y razonamiento crítico.",

                "improved_question":
                f"Justifique y analice: {question_text}"
            }

        # nivel bajo

        if (
            "qué es" in text or
            "define" in text or
            "mencione" in text
        ):

            return {

                "level": "bajo",

                "feedback":
                "Pregunta conceptual básica. Puede profundizarse solicitando aplicación o análisis.",

                "improved_question":
                f"¿Cómo aplicarías en un caso real: {question_text}?"
            }

        # nivel medio

        return {

            "level": "medio",

            "feedback":
            "Pregunta adecuada que requiere comprensión y explicación.",

            "improved_question":
            f"Explique con mayor profundidad: {question_text}"
        }

    # -------------------------
    # GEMINI + FALLBACK
    # -------------------------

    def analyze_question(
        self,
        question_text
    ):

        if not self.gemini_available:

            return self.local_ai_engine(
                question_text
            )

        prompt = f"""
Evalúa esta pregunta y responde SOLO JSON:

Pregunta:
{question_text}

Formato:
{{
 "level":"bajo|medio|alto",
 "feedback":"máximo 20 palabras",
 "improved_question":"versión mejorada"
}}
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            raw = response.text.strip()

            raw = raw.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            result = json.loads(
                raw
            )

            return {

                "level":
                result.get(
                    "level",
                    "medio"
                ),

                "feedback":
                result.get(
                    "feedback",
                    ""
                ),

                "improved_question":
                result.get(
                    "improved_question",
                    question_text
                )
            }

        except Exception as e:

            print(
                "Gemini fallback activado:",
                str(e)
            )

            return self.local_ai_engine(
                question_text
            )
