def get_value(readings, confidence_level, constant):
    """
    This function calculates the minimum number of observations required for a given level of confidence
    based on the input readings and confidence level.

    Args:
        readings (list): A list of readings
        confidence_level (float): The level of confidence in percentage
        constant (float): A constant value

    Returns:
        float: The minimum number of observations required for the given level of confidence
    """
    reading_sum = 0
    reading_squared_sum = 0
    for reading in readings:
        reading_sum += reading
        reading_squared_sum += reading ** 2

    N_linha = ((constant * len(readings) / reading_sum) * (((reading_squared_sum) -
                                                            (reading_sum**2 / len(readings))) / (len(readings) - 1))**(1/2))**2

    print(
        f"O número mínimo de leituras para uma confiabilidade de {confidence_level} é igual a {N_linha}")

    if N_linha < len(readings):
        print(
            f"Como {N_linha} < {len(readings)}, o tamanho da amostra está correto")
    else:
        print(
            f"O número de amostras é menor do que {N_linha} ({len(readings)} amostras)")


readings = [6, 5, 7, 7, 6, 6, 6, 6, 7, 5, 5,
            6, 6, 6, 6, 7, 6, 5, 5, 6, 6, 6, 6, 7, 7]

num_leituras = get_value(readings, 5, 40)
num_leituras = get_value(readings, 10, 20)
