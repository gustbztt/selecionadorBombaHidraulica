def get_float(dic, key, default=0.0):
    value = dic[key]
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def get_diametro_economico(vazao_desejada, funcionamento_diario):
    import bisect
    # lista de diametros comerciais possíveis
    diametros = [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 150, 200, 250, 300]
    # parâmetros para diâmetro ideal

    # get diametro economico em mm
    diametro_ideal = (1.3*((funcionamento_diario/24)**0.25) *
                      (vazao_desejada/60000)**0.5)*1000

    i = bisect.bisect_left(diametros, diametro_ideal)
    if i == 0:
        return diametros[0], diametros[1]
    if i == len(diametros):
        return diametros[-2], diametros[-1]

    diametro_succao = diametros[i]
    diametro_recalque = diametros[i-1]
    return diametro_succao, diametro_recalque
