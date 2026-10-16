"""Prueba de ingesta y cálculo con datos sintéticos; no representa mediciones del proyecto."""

import numpy as np
import pandas as pd

from scripts.procesamiento_hidraulico import (
    EvaluadorHidraulicoMCH,
    leer_csv_topografia,
)


def test_ingesta_sintetica_topografia_aforo_y_hidraulica(tmp_path):
    topo = tmp_path / "topografia.csv"
    topo.write_text(
        "# METADATOS: Datum=WGS84, Zona=19S, Datum_Vertical=EJEMPLO, Metodo=GNSS_RTK\n"
        "ID,Punto,Este_m,Norte_m,Cota_m,Tipo_Cota,Incertidumbre_m,Progresiva_m,Descripcion\n"
        "1,CAM_EJE,385250.4,8245220.1,3850.0,Eje_Tuberia,0.015,0,Inicio eje sintético\n"
        "2,ANC_01,385310.2,8245290.8,3810.0,Eje_Tuberia,0.020,100,Anclaje sintético\n"
        "3,ANC_02,385400.1,8245350.4,3770.0,Eje_Tuberia,0.020,250,Anclaje sintético\n"
        "4,CM_EJE,385480.8,8245410.5,3735.0,Eje_Tuberia,0.015,425.8,Eje de turbina sintético\n",
        encoding="utf-8",
    )
    metadatos, puntos = leer_csv_topografia(topo)
    evaluador = EvaluadorHidraulicoMCH()

    assert metadatos["Zona"] == "19S"
    longitud = evaluador.longitud_trazado_3d(puntos)
    cuerda = evaluador.calcular_geometria_3d(
        *puntos.iloc[0][["Este_m", "Norte_m", "Cota_m"]],
        *puntos.iloc[-1][["Este_m", "Norte_m", "Cota_m"]],
    )["cuerda_3d_minima_m"]
    assert longitud >= cuerda

    aforo = pd.DataFrame(
        {
            "Distancia_m": [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "Profundidad_m": [0.0, 0.25, 0.45, 0.50, 0.40, 0.20, 0.0],
            "V_06_m_s": [0.0, 0.42, 0.68, 0.75, 0.61, 0.35, 0.0],
        }
    )
    dx = aforo["Distancia_m"].diff().iloc[1:].to_numpy()
    d = aforo["Profundidad_m"].to_numpy()
    v = aforo["V_06_m_s"].to_numpy()
    parciales = pd.DataFrame(
        {
            "area_parcial_m2": dx * (d[:-1] + d[1:]) / 2,
            "velocidad_media_m_s": (v[:-1] + v[1:]) / 2,
        }
    )
    _, res_aforo = evaluador.calcular_aforo(parciales)
    assert res_aforo["area_total_m2"] > 0
    assert res_aforo["Q_m3_s"] > 0

    perdidas = evaluador.calcular_perdidas_darcy(
        Q_m3_s=res_aforo["Q_m3_s"],
        D_interior_m=0.40,
        L_eje_m=longitud,
        rugosidad_absoluta_m=0.000045,
        K_total=2.0,
    )
    potencia = evaluador.calcular_potencia(
        Q_disponible_m3_s=res_aforo["Q_m3_s"],
        nivel_aguas_arriba_m=3854.2,
        nivel_aguas_abajo_m=3733.7,
        h_perdidas_m=perdidas["h_perdidas_m"],
        eta_turbina=0.86,
        eta_generador=0.92,
        eta_transformador=0.97,
    )
    assert np.isfinite(perdidas["h_perdidas_m"])
    assert 0 < potencia["salto_neto_m"] < potencia["salto_bruto_m"]
    assert potencia["potencia_electrica_kw"] > 0
