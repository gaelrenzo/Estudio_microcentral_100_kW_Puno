from scripts.procesamiento_hidraulico import AuditorCalidadCSV


def test_auditoria_csv_valido(tmp_path):
    path = tmp_path / "topografia_valida.csv"
    path.write_text(
        "# METADATOS: Datum=WGS84, Zona=19S, Datum_Vertical=IGN_PERU, Metodo=GNSS_RTK\n"
        "ID,Punto,Este_m,Norte_m,Cota_m,Tipo_Cota\n"
        "1,P1,385250.40,8245220.10,3850.00,Eje_Tuberia\n"
        "2,P2,385350.40,8245220.10,3800.00,Eje_Tuberia\n",
        encoding="utf-8",
    )

    resultado = AuditorCalidadCSV.auditar_csv_topografia(path)

    assert resultado["valido"] is True
    assert resultado["observaciones"] == []
    assert resultado["filas_totales"] == 2


def test_auditoria_csv_detecta_inconsistencias(tmp_path):
    path = tmp_path / "topografia_corrupta.csv"
    path.write_text(
        "# METADATOS: Datum=WGS84, Zona=19S\n"
        "ID,Punto,Este_m,Norte_m,Cota_m,Tipo_Cota\n"
        "1,P1,385250.40,8245220.10,3850.00,NAV\n"
        "2,P2,385250.40,8245220.10,3700.00,Eje\n"
        "3,P3,385400.10,8245350.40,,Eje\n",
        encoding="utf-8",
    )

    resultado = AuditorCalidadCSV.auditar_csv_topografia(path)
    observaciones = resultado["observaciones"]

    assert resultado["valido"] is False
    assert any("Falta el metadato obligatorio" in obs for obs in observaciones)
    assert any("valores nulos" in obs for obs in observaciones)
    assert any("Mismas coordenadas planar" in obs for obs in observaciones)
