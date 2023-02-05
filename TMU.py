import math


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


def mean_absolute_error(data, key1, key2):
    """Calculate the mean absolute error between true and predicted values in a list of dictionaries."""
    y_true = [d[key1] for d in data]
    y_pred = [d[key2] for d in data]
    return sum(abs(y_true[i] - y_pred[i]) for i in range(len(y_true))) / len(y_true)


data = [{'Caso': 1, 'Vazão encontrada': 0.00211, 'Vazão real': 0.002106, 'Hm encontrada': 55.671236, 'Hm real': 55.671236},
        {'Caso': 2, 'Vazão encontrada': 0.00223, 'Vazão real': 0.002232,
            'Hm encontrada': 57.602024, 'Hm real': 57.602024},
        {'Caso': 3, 'Vazão encontrada': 0.00103, 'Vazão real': 0.001029,
            'Hm encontrada': 43.7632, 'Hm real': 43.763199},
        {'Caso': 4, 'Vazão encontrada': 0.00228, 'Vazão real': 0.0022776,
            'Hm encontrada': 58.315351, 'Hm real': 58.315351},
        {'Caso': 5, 'Vazão encontrada': 0.00204, 'Vazão real': 0.00204, 'Hm encontrada': 54.707336, 'Hm real': 54.707336}]

print(mean_absolute_error(data, 'Hm encontrada', 'Hm real'))
