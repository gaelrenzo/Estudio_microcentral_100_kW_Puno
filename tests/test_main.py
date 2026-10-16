import pandas as pd

from main import procesar_paquete


def crear_paquete(data_dir, metadata=True):
    data_dir.mkdir(parents=True)
    meta = "# METADATOS: Datum=WGS84, Zona=19S, Datum_Vertical=IGN_PERU, Metodo=GNSS_RTK\n" if metadata else ""
    (data_dir / "levantamiento.csv").write_text(
        meta
        + "ID,Punto,Este_m,Norte_m,Cota_m,Tipo_Cota,Incertidumbre_m,Progresiva_m,Descripcion\n"
        + "1,NAV_UP,385240.4,8245220.1,3854.2,NAV,0.02,0,Nivel aguas arriba\n"
        + "2,CAM_EJE,385250.4,8245220.1,3850.0,Eje_Tuberia,0.02,10,Eje\n"
        + "3,ANC_01,385310.2,8245290.8,3810.0,Eje_Tuberia,0.02,100,Eje\n"
        + "4,ANC_02,385400.1,8245350.4,3770.0,Eje_Tuberia,0.02,250,Eje\n"
        + "5,CM_EJE,385480.8,8245410.5,3735.0,Eje_Tuberia,0.02,425.8,Eje\n"
        + "6,NAV_DOWN,385490.8,8245410.5,3733.7,NAV,0.02,440,Nivel aguas abajo\n",
        encoding="utf-8",
    )
    pd.DataFrame(
        {
            "Distancia_m": [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "Profundidad_m": [0.0, 0.25, 0.45, 0.50, 0.40, 0.20, 0.0],
            "V_06_m_s": [0.0, 0.42, 0.68, 0.75, 0.61, 0.35, 0.0],
        }
    ).to_csv(data_dir / "aforo.csv", index=False)


def ejecutar(data_dir, report):
    return procesar_paquete(
        data_dir,
        report,
        punto_aguas_arriba="NAV_UP",
        punto_aguas_abajo="NAV_DOWN",
        diametro_interior_m=0.40,
        rugosidad_m=0.000045,
        k_total=2.0,
        eta_turbina=0.86,
        eta_generador=0.92,
        eta_transformador=0.97,
    )


def test_main_procesa_paquete_y_escribe_reporte(tmp_path):
    data_dir = tmp_path / "data_campo"
    crear_paquete(data_dir)

    resultado = ejecutar(data_dir, tmp_path / "reporte.md")

    assert resultado["ok"] is True
    assert resultado["results"]["longitud_desarrollada_3d_m"] > 300
    assert resultado["results"]["aforo"]["Q_m3_s"] > 0
    assert resultado["results"]["perdidas"]["hf_m"] > 0
    assert resultado["results"]["potencia"]["potencia_electrica_kw"] > 0
    assert "PROCESADO" in (tmp_path / "reporte.md").read_text(encoding="utf-8")


def test_main_rechaza_topografia_con_metadatos_incompletos(tmp_path):
    data_dir = tmp_path / "data_campo"
    crear_paquete(data_dir, metadata=False)

    resultado = ejecutar(data_dir, tmp_path / "reporte.md")

    assert resultado["ok"] is False
    assert resultado["results"] == {}
    reporte = (tmp_path / "reporte.md").read_text(encoding="utf-8")
    assert "RECHAZADO" in reporte
    assert "Falta el metadato obligatorio" in reporte
