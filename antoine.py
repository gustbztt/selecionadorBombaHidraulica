dados = [6, 5, 7, 7, 6, 6, 6, 6, 7, 5, 5,
         6, 6, 6, 6, 7, 6, 5, 5, 6, 6, 6, 6, 7, 7]

n = len(dados)
sum_x = sum(dados)
sum_x_sq = sum_x**2

sum_sq_x = 0
for i in dados:
    sum_sq_x += i**2

print(f' n={n} \n sum_x={sum_x} \n sum_x_sq={sum_x_sq} \n sum_sq_x={sum_sq_x}')

# para 5% confiabilidade
n_linha = ((40*n/sum_x)*((sum_sq_x-(sum_x_sq/n))/(n-1))**(1/2))**2
print(f'para 5% de confiabilidade = {n_linha}')
# para 10% confiabilidade
n_linha1 = ((20*n/sum_x)*((sum_sq_x-(sum_x_sq/n))/(n-1))**(1/2))**2
print(f'para 10% de confiabilidade = {n_linha1}')
