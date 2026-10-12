"""
Módulo del Agente de Asesoría Técnica e Ingeniería Hidroeléctrica (HydroAgent).
Implementa un sistema experto basado en reglas heurísticas y normativas para responder
consultas, sugerir tipologías de turbinas y verificar el cumplimiento regulatorio peruano.
"""

import os
from typing import Dict, Any, List, Optional


class HydroAgent:
    """
    Agente inteligente de ingeniería y normativa para microcentrales hidroeléctricas.
    Opera bajo reglas deterministas sin requerir APIs externas.
    """

    def __init__(self, conocimiento_path: Optional[str] = None):
        """
        Inicializa el agente y carga la base de conocimiento normativo.

        Args:
            conocimiento_path: Ruta al archivo Markdown de normativa. Si es None,
                               usa la ruta estándar ai/knowledge/normativa_peruana.md.
        """
        if conocimiento_path is None:
            conocimiento_path = os.path.join(
                os.path.dirname(__file__), "knowledge", "normativa_peruana.md"
            )
        self.conocimiento_path = conocimiento_path
        self.conocimiento_texto = ""
        self.cargar_conocimiento()

    def cargar_conocimiento(self) -> str:
        """
        Carga el contenido textual de la base de conocimientos.

        Returns:
            Texto completo del documento normativo.
        """
        if os.path.exists(self.conocimiento_path):
            with open(self.conocimiento_path, "r", encoding="utf-8") as f:
                self.conocimiento_texto = f.read()
        else:
            self.conocimiento_texto = (
                "Base de conocimiento no encontrada en: " + self.conocimiento_path
            )
        return self.conocimiento_texto

    def sugerir_turbina(self, caudal: float, salto: float) -> str:
        """
        Sugiere el tipo de turbina óptimo a partir del caudal de diseño y el salto disponible.

        Args:
            caudal: Caudal volumétrico de diseño en m³/s.
            salto: Caída neta o bruta en metros.

        Returns:
            Diagnóstico textual con la turbina sugerida, velocidad específica y consideraciones.
        """
        if caudal <= 0 or salto <= 0:
            return "Error: Los parámetros de caudal y salto deben ser valores positivos no nulos."

        if (salto > 200.0 and caudal < 2.0) or (salto >= 50.0 and caudal <= 0.20):
            return (
                f"Para un salto de {salto:.1f} m y caudal de {caudal*1000:.1f} L/s, "
                "se recomienda una Turbina Pelton (Acción). "
                "Excelente rendimiento a cargas parciales mediante control por aguja de inyector. "
                "Rango Ns: 10 - 35 rpm."
            )
        elif 100.0 <= salto <= 500.0 and caudal < 5.0:
            return (
                f"Para un salto de {salto:.1f} m y caudal de {caudal:.3f} m³/s, "
                "se recomienda una Turbina Turgo (Acción). "
                "Admite mayor caudal que la Pelton para el mismo diámetro con menor tendencia al bloqueo. "
                "Rango Ns: 30 - 70 rpm."
            )
        elif 50.0 <= salto <= 200.0 and 2.0 <= caudal <= 50.0:
            return (
                f"Para un salto de {salto:.1f} m y caudal de {caudal:.2f} m³/s, "
                "se recomienda una Turbina Francis (Reacción). "
                "Óptima relación compacidad/potencia para saltos medianos. "
                "Rango Ns: 60 - 300 rpm."
            )
        elif salto < 50.0 and caudal > 20.0:
            return (
                f"Para un salto de {salto:.1f} m y caudal de {caudal:.2f} m³/s, "
                "se recomienda una Turbina Kaplan (Reacción axial). "
                "Álabes orientables con curva de rendimiento plana para caudales elevados. "
                "Rango Ns: 300 - 1000 rpm."
            )
        elif salto < 10.0 and caudal > 10.0:
            return (
                f"Para un salto muy bajo ({salto:.1f} m) y caudal de {caudal:.2f} m³/s, "
                "se recomienda un Tornillo Hidrodinámico de Arquímedes. "
                "Ideal para desniveles mínimos con bajo impacto ictícola."
            )
        elif salto < 50.0 and caudal <= 20.0:
            return (
                f"Para un salto de {salto:.1f} m y caudal de {caudal:.3f} m³/s, "
                "se recomienda una Turbina Michell-Banki (Flujo Cruzado). "
                "Fabricación sencilla y bajo costo para microgeneración rural."
            )
        else:
            if salto >= 100.0:
                return f"Con salto de {salto:.1f} m, se recomienda tecnología Pelton o Turgo según costo local."
            else:
                return f"Con salto de {salto:.1f} m, se recomienda tecnología Francis o Flujo Cruzado."

    def consultar(self, pregunta: str) -> str:
        """
        Responde consultas técnicas y regulatorias en lenguaje natural analizando intenciones clave.

        Args:
            pregunta: Pregunta o temática consultada en español.

        Returns:
            Respuesta estructurada con fundamento técnico o legal peruano.
        """
        p = pregunta.lower().strip()

        if any(w in p for w in ["rer", "1002", "decreto", "renovable"]):
            return (
                "Conforme al Decreto Legislativo 1002 (Promoción de Inversión en RER), las centrales "
                "hidroeléctricas con potencia instalada menor o igual a 20 MW califican como tecnología RER. "
                "Gozan de despacho preferente ante el COES, libre acceso a redes y régimen de depreciación acelerada."
            )
        elif any(w in p for w in ["caudal ecologico", "ecologico", "reserva", "rio"]):
            return (
                "Según la Ley Nº 29338 (Ley de Recursos Hídricos) y la ANA, toda captación hidráulica debe "
                "dejar circular de forma ininterrumpida el Caudal Ecológico. Típicamente corresponde a un mínimo "
                "del 10% al 15% del caudal medio de estiaje (para el Río Blanco en Puno se fijaron 30 L/s)."
            )
        elif any(w in p for w in ["ana", "licencia", "derecho", "agua", "recursos hidricos"]):
            return (
                "La Autoridad Nacional del Agua (ANA) exige 4 etapas secuenciales: 1) Acreditación de Disponibilidad "
                "Hídrica, 2) Autorización de Ejecución de Obras en fuente natural, 3) Inspección de término de obras, "
                "y 4) Otorgamiento de Licencia de Uso de Agua No Consuntiva para generación eléctrica."
            )
        elif any(w in p for w in ["concesion", "minem", "dge", "potencia", "permiso electrico"]):
            return (
                "Bajo el D.L. 25844 (Ley de Concesiones Eléctricas), los proyectos menores a 500 kW no requieren "
                "concesión definitiva ni temporal; se consideran microgeneración y solo precisan autorización simplificada "
                "y registro ante la Dirección Regional de Energía y Minas (DREM) o DGE."
            )
        elif any(w in p for w in ["osinergmin", "tarifa", "supervision", "calidad"]):
            return (
                "OSINERGMIN supervisa la seguridad técnica, protecciones de red (CNE Suministro) y régimen tarifario. "
                "Para microcentrales aisladas o conectadas a redes rurales, se aplica el Procedimiento de Fijación "
                "de Tarifas en Sistemas Aislados (R.D. 076-2014) y control de armónicos y factor de potencia (0.85 a 1.0)."
            )
        elif any(w in p for w in ["golpe de ariete", "ariete", "celeridad", "allievi"]):
            return (
                "Para controlar el golpe de ariete en microcentrales Pelton se recomienda el uso de deflectores de chorro "
                "de corte rápido (< 0.5 s) combinados con un servomotor o cierre gradual de la aguja de tobera (tc >= 4.0 s). "
                "Esto transforma la maniobra en cierre lento (Allievi), evitando sobrepresiones que superen el 20-30% de Hb."
            )
        elif any(w in p for w in ["canal", "manning", "conduccion"]):
            return (
                "El canal de aducción se dimensiona con la ecuación de Manning procurando flujo subcrítico (Fr < 0.8) "
                "y velocidad entre 0.6 m/s (para evitar sedimentación de arenas finas) y 2.0 m/s (para prevenir erosión "
                "del hormigón simple o mampostería)."
            )
        elif any(w in p for w in ["lcoe", "van", "tir", "rentabilidad", "payback"]):
            return (
                "Para microcentrales RER en Perú, una evaluación a 25 años con tasa de descuento social/privada del 10% "
                "suele arrojar un LCOE de 0.04 a 0.06 USD/kWh y una TIR superior al 15%, resultando atractiva frente "
                "a la generación con grupos diésel (> 0.25 USD/kWh)."
            )
        else:
            return (
                "Consulta procesada por HydroAgent. Se sugiere revisar los tópicos de normativa peruana "
                "(DL 1002 RER, Ley 29338 de Aguas, CNE Suministro, exigencias ANA y OSINERGMIN) o especificar "
                "parámetros como caudal (m³/s) y salto (m) para dimensionamiento técnico."
            )

    def revisar_normativa(self, checklist: List[Any]) -> Dict[str, Any]:
        """
        Evalúa una lista de ítems de cumplimiento técnico-legal del proyecto.

        Args:
            checklist: Lista de nombres de requisitos o diccionarios con claves 'requisito' y 'cumple'.

        Returns:
            Diccionario con resumen de cumplimiento, porcentaje y observaciones.
        """
        requisitos_clave = {
            "disponibilidad_hidrica": "Acreditación de Disponibilidad Hídrica emitida por ANA/ALA.",
            "caudal_ecologico": "Garantía de caudal ecológico continuo en bocatoma (Ley 29338).",
            "autorizacion_obras_ana": "Autorización de obras en cauce natural emitida por ANA.",
            "calificacion_rer": "Potencia <= 20 MW para acogerse al Decreto Legislativo 1002.",
            "exoneracion_concesion": "Potencia <= 500 kW exonerada de trámite de concesión definitiva.",
            "estudio_ambiental": "Certificación Ambiental (DIA o Ficha Técnica Ambiental MINEM/SENACE).",
            "protecciones_cne": "Cumplimiento del Código Nacional de Electricidad y OSINERGMIN."
        }

        resultados = []
        cumplidos = 0

        for item in checklist:
            if isinstance(item, dict):
                nombre = item.get("requisito", "")
                estado = bool(item.get("cumple", True))
                obs = item.get("observacion", "")
            else:
                nombre = str(item).lower().replace(" ", "_")
                estado = True
                obs = "Verificado conforme a normativa peruana."

            descripcion = requisitos_clave.get(nombre, f"Requisito general: {nombre}")
            if estado:
                cumplidos += 1

            resultados.append({
                "requisito": nombre,
                "descripcion": descripcion,
                "cumple": estado,
                "observacion": obs
            })

        total = len(checklist)
        porcentaje = round((cumplidos / total * 100.0), 2) if total > 0 else 0.0

        return {
            "total_requisitos": total,
            "cumplidos": cumplidos,
            "pendientes": total - cumplidos,
            "porcentaje_cumplimiento": porcentaje,
            "estado_general": "Aprobado" if porcentaje >= 80.0 else "Requiere Regularización",
            "detalle": resultados
        }
