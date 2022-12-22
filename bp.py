ultimas_peliculas_agregadas=[1,6,5,4,8,9,0,7,5,1]
for i in range(9,-1,-1):
    ultimas_peliculas_agregadas[i]=ultimas_peliculas_agregadas[i-1]
ultimas_peliculas_agregadas[0]=6
print(ultimas_peliculas_agregadas)