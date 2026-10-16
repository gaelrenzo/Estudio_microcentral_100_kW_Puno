"""
Orquestador Principal del Sistema Modular: Hydro AI Engineering.
Ejecuta secuencialmente la hidrología, dimensionamiento hidráulico, selección de turbina,
análisis de transitorios, evaluación económica, gráficos y generación del informe PDF formal.
"""

import os
import sys

# Asegurar que la raíz del proyecto esté en el sys.path para importaciones relativas
RUTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_RAIZ not in sys.path:
    sys.path.insert(0, RUTA_RAIZ)

from src.hydrology import (
    cargar_caudales,
    validar_datos,
    estadisticas_caudales,
    graficar_cdc
)
from src.hydraulics import (
    dimensionamiento_canal,
    dimensionamiento_tuberia,
    calcular_grupo_turbina_generador
)
from src.turbines import seleccionar_turbina, velocidad_especifica, kurier
from src.electrical import (
    calcular_transformador,
    tensionConexion,
    energia_anual
)
from src.transient import (
    calcular_celeridad,
    calcular_sobrepresion,
    espesor_requerido,
    perfil_presiones,
    graficar_perfil
)
from src.economics import evaluacion_completa
from src.reports import generar_informe_pdf
from src.cad_bridge.export_pipeline import exportar_todos_los_planos
from ai.agent import HydroAgent


def main():
    """
    Función de ejecución principal de la ingeniería integral de la microcentral.
    """
    print("=" * 70)
    print("   HYDRO AI ENGINEERING - MICROCENTRAL HIDROELÉCTRICA 100 kW")
    print("   Localización: Río Blanco, Departamento de Puno, Perú")
    print("=" * 70)

    # Definir rutas relativas seguras
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_datos_csv = os.path.join(
        ruta_base, "data", "series_caudales_diarios_historicos_2014_2023.csv"
    )
    carpeta_reports = os.path.join(ruta_base, "reports")
    os.makedirs(carpeta_reports, exist_ok=True)

    ruta_grafico_cdc = os.path.join(carpeta_reports, "curva_duracion_caudales.png")
    ruta_grafico_ariete = os.path.join(carpeta_reports, "perfil_sobrepresion_ariete.png")
    ruta_informe_pdf = os.path.join(carpeta_reports, "informe_tecnico_mch_100kw_puno.pdf")

    # 1. Cargar y Validar Datos Hidrológicos
    print("\n[1/6] Procesando hidrología y serie histórica de caudales...")
    df_caudales = cargar_caudales(ruta_datos_csv)
    validacion = validar_datos(df_caudales)
    caudales_arr = df_caudales["Caudal_Rio_m3s"].values
    stats_hidro = estadisticas_caudales(caudales_arr)

    # Parámetros del proyecto
    hb = 115.0           # Salto bruto (m)
    qd = 0.125           # Caudal de diseño nominal (m³/s) = 125 L/s
    q_eco = 0.030        # Caudal ecológico de reserva (m³/s) = 30 L/s
    eficiencia = 0.82    # Rendimiento global referencial

    # Graficar Curva de Duración de Caudales (CDC)
    graficar_cdc(caudales_arr, ruta_grafico_cdc, q_diseno=qd, q_eco=q_eco)
    print(f"      - Serie cargada: {stats_hidro['total_observaciones']:,} días analizados")
    print(f"      - Caudal medio: {stats_hidro['caudal_medio']:.3f} m³/s | Q95: {stats_hidro['percentiles'][95]:.3f} m³/s")
    print(f"      - Gráfico CDC guardado en: {ruta_grafico_cdc}")

    # 2. Dimensionamiento Hidráulico
    print("\n[2/6] Ejecutando dimensionamiento hidráulico y de tubería forzada...")
    dim_canal = dimensionamiento_canal(Q=qd, n=0.014, S=0.0015, b=0.50)
    dim_tub = dimensionamiento_tuberia(
        Q=qd, Hb=hb, L=380.0, k_rug=0.000045, D_adoptado=0.250
    )
    hn_efectivo = dim_tub["salto_neto_m"]
    grupo_tg = calcular_grupo_turbina_generador(
        Q=qd, Hn=hn_efectivo, Hb=hb, z_inyectores=2, N_rpm=1200.0
    )

    print(f"      - Canal: Ancho {dim_canal['ancho_solera_m']} m | Tirante {dim_canal['tirante_normal_m']} m | Froude {dim_canal['numero_froude']} ({dim_canal['regimen_flujo']})")
    print(f"      - Tubería Forzada: D = {dim_tub['diametro_adoptado_m']*1000:.0f} mm | Salto neto Hn = {hn_efectivo:.2f} m (Pérdidas: {dim_tub['perdida_relativa_pct']}%)")
    print(f"      - Generador: Potencia neta a red = {grupo_tg['potencia_neta_red_kw']:.2f} kW")

    # 3. Selección y Análisis de Turbina
    print("\n[3/6] Seleccionando y modelando turbina...")
    turbina_sel = seleccionar_turbina(caudal=qd, salto=hb)
    ns_turb = velocidad_especifica(N=1200.0, Q=qd, H=hn_efectivo)
    torque_eje = kurier(N=1200.0, P=grupo_tg["potencia_mecanica_eje_kw"])
    print(f"      - Tecnología recomendada: Turbina {turbina_sel['tipo']} (Ns = {ns_turb:.1f} rpm)")
    print(f"      - Rodete primitivo: {grupo_tg['diametro_primitivo_rodete_m']*1000:.1f} mm | {grupo_tg['numero_cucharas']} cucharas")
    print(f"      - Torque en el eje motriz: {torque_eje:.2f} N·m")

    # 4. Análisis Eléctrico e Interconexión
    print("\n[4/6] Configurando interconexión y balance energético...")
    transformador = calcular_transformador(potencia_kw=100.0, tension_kv=10.0)
    nivel_tension = tensionConexion(100.0)
    balance_energia = energia_anual(
        caudales=caudales_arr,
        potencia_nominal_kw=100.0,
        q_diseno=qd,
        q_eco=q_eco,
        hb=hb
    )
    print(f"      - Interconexión: {nivel_tension} | Transformador: {transformador['potencia_nominal_transformador_kva']} kVA")
    print(f"      - Generación estimada: {balance_energia['energia_anual_mwh']:.2f} MWh/año | Factor de planta: {balance_energia['factor_planta_pct']}%")

    # 5. Análisis de Transitorios Hidráulicos (Golpe de Ariete)
    print("\n[5/6] Simulando transitorios hidráulicos y sobrepresión de cierre...")
    v_tubo = dim_tub["velocidad_m_s"]
    celeridad_a = calcular_celeridad(D=0.250, e=0.005)
    ariete = calcular_sobrepresion(L=380.0, v=v_tubo, tc=4.0, Hb=hb, D=0.250, e=0.005)
    espesor_tub = espesor_requerido(H_max=ariete["presion_maxima_H_max_m"], D=0.250)
    perfil = perfil_presiones(
        L=380.0, D=0.250, Hb=hb, delta_h=ariete["sobrepresion_delta_H_m"]
    )
    graficar_perfil(perfil, ruta_grafico_ariete)

    print(f"      - Celeridad de onda (a): {celeridad_a:.1f} m/s | Maniobra: {ariete['tipo_maniobra']}")
    print(f"      - Sobrepresión de diseño: {ariete['sobrepresion_delta_H_m']:.2f} m | Presión máx: {ariete['presion_maxima_H_max_m']:.2f} m ({ariete['presion_maxima_bar']:.1f} bar)")
    print(f"      - Espesor mínimo requerido: {espesor_tub:.2f} mm (Comercial especificado: 4.75 y 6.35 mm)")
    print(f"      - Gráfico de perfil de presiones: {ruta_grafico_ariete}")

    # 6. Evaluación Económica Integral
    print("\n[6/6] Realizando evaluación financiera a 25 años...")
    econ = evaluacion_completa(
        capex=245800.0,
        opex_pct=0.03,
        potencia_kw=100.0,
        factor_planta=balance_energia["factor_planta"],
        tarifa=0.075,
        horizonte=25,
        tasa_descuento=0.10
    )
    print(f"      - CAPEX: ${econ['capex_usd']:,.2f} USD | Flujo Anual: ${econ['flujo_neto_anual_usd']:,.2f} USD")
    print(f"      - VAN (@ 10%): ${econ['van_usd']:,.2f} USD | TIR: {econ['tir_pct']:.2f}% | Payback: {econ['payback_anios']:.2f} años")
    print(f"      - LCOE: ${econ['lcoe_usd_mwh']:.2f} USD/MWh | Relación B/C: {econ['relacion_beneficio_costo']:.2f}")

    # Consulta al Agente Normativo
    agente = HydroAgent()
    dictamen_agente = agente.consultar("Decreto Legislativo 1002 RER y requisitos de la ANA")

    # Estructurar resultados para el informe PDF
    resultados = {
        "hidrologia": {
            "validacion": validacion,
            "estadisticas": stats_hidro
        },
        "hidraulica": {
            "canal": dim_canal,
            "tuberia": dim_tub,
            "generador": grupo_tg
        },
        "turbinas": turbina_sel,
        "electrica": {
            "transformador": transformador,
            "balance": balance_energia,
            "nivel_tension": nivel_tension
        },
        "transitorio": ariete,
        "economia": econ,
        "grafico_cdc": ruta_grafico_cdc,
        "grafico_ariete": ruta_grafico_ariete,
        "dictamen_agente": dictamen_agente
    }

    # 7. Generación de Planos de Ingeniería en CAD Vectorial (DXF)
    print("\n[7/7] Generando suite de planos CAD vectoriales (.dxf) y vistas de revisión...")
    info_planos = exportar_todos_los_planos(ruta_base)

    # Generar Informe PDF
    print("\n[+] Compilando informe técnico final en formato PDF (ReportLab)...")
    ruta_pdf_generado = generar_informe_pdf(resultados, ruta_informe_pdf)
    print(f"    --> Informe PDF generado exitosamente en: {ruta_pdf_generado}")

    # Resumen final en consola
    print("\n" + "=" * 70)
    print("   RESUMEN EJECUTIVO - MICROCENTRAL HIDROELÉCTRICA PUNO 100 kW")
    print("=" * 70)
    print(f"   * Caudal de Diseño Nominal (Qd):      {qd*1000:.0f} L/s ({qd} m³/s)")
    print(f"   * Caudal Ecológico de Reserva (Qeco): {q_eco*1000:.0f} L/s ({q_eco} m³/s)")
    print(f"   * Salto Bruto / Salto Neto:           {hb:.1f} m / {hn_efectivo:.2f} m")
    print(f"   * Turbina Adoptada:                   Pelton de 2 inyectores (1200 RPM)")
    print(f"   * Potencia Neta Entregada a Red:      {grupo_tg['potencia_neta_red_kw']:.2f} kW")
    print(f"   * Generación Anual Estimada:          {econ['generacion_anual_mwh']:.2f} MWh/año")
    print(f"   * Inversión Total (CAPEX):            ${econ['capex_usd']:,.2f} USD")
    print(f"   * Indicadores de Rentabilidad:        VAN = ${econ['van_usd']:,.2f} USD | TIR = {econ['tir_pct']:.2f}%")
    print(f"   * Período de Recuperación (Payback):  {econ['payback_anios']:.2f} Años")
    print(f"   * Costo Nivelado de Energía (LCOE):   ${econ['lcoe_usd_mwh']:.2f} USD/MWh")
    print(f"   * Archivos Generados en reports/:")
    print(f"       1. {os.path.basename(ruta_grafico_cdc)}")
    print(f"       2. {os.path.basename(ruta_grafico_ariete)}")
    print(f"       3. {os.path.basename(ruta_pdf_generado)}")
    print("=" * 70)
    print("   EJECUCIÓN COMPLETADA EXITOSAMENTE.")
    print("=" * 70)


if __name__ == "__main__":
    main()
