# -*- coding: utf-8 -*-
"""Cópia de Cópia de Knight's independence.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F-biMmRdGU6rT9VeC4eFMrMZPDww5dWP
"""

# Independencia dos cavalos no tabuleiro de xadrez
# Matheus Ribeiro Alencar - 494711
import random
import copy

#inicializar tabuleiro
def initialize_chessboard(dim):
    matrix = []
    row = [0]*dim
    for i in range(dim):
        matrix.append(row[:]) #copy of row, no indexing problems later on
    return matrix

#Função que fará a restrição das casas atacadas por cavalos.
def place_attacks(pos_x,pos_y,chessboard):
    if pos_x+2<dim and pos_y +1<dim:
      chessboard[pos_x+2][pos_y +1] = 'X'
    if pos_x+2<dim and pos_y -1 >=0:
      chessboard[pos_x+2][pos_y -1] = 'X'
    if pos_x+1<dim and pos_y +2<dim:
      chessboard[pos_x+1][pos_y +2] = 'X'
    if pos_x+1<dim and pos_y -2>=0:
      chessboard[pos_x+1][pos_y -2] = 'X'
    if pos_x-2>=0 and pos_y+1<dim:
      chessboard[pos_x-2][pos_y +1] = 'X'
    if pos_x-2>=0 and pos_y-1>=0:
      chessboard[pos_x-2][pos_y -1] = 'X'
    if pos_x-1>=0 and pos_y-2>=0:
      chessboard[pos_x-1][pos_y -2] = 'X'
    if pos_x-1>=0 and pos_y+2<dim:
      chessboard[pos_x-1][pos_y +2] = 'X'

def check_attacks(chessboard):
  pos_x = None
  pos_y = None
  less_restrictions = -9        #Maior número de casas restritas pelos movimentos dos cavalos são 8
  A = copy.deepcopy(chessboard) # Cópia do chessboard
                                # Insere cópias do objeto original, fonte: https://docs.python.org/dev/library/copy.html#module-copy
  for i in range(0,len(A)):
    for j in range(0,len(A)):
      restricted_fields = 0

      if A[i][j] != 'X' and A[i][j] == 0: #Casa disponível, checaremos se nos leva a uma boa solução.
          if i+2<(len(A)) and j+1<(len(A)):
            if A[i+2][j +1] != 'X' and A[i+2][j +1] <= 0:
              restricted_fields = restricted_fields - 1

          if i+2<(len(A)) and j -1 >=0:
            if A[i+2][j -1] != 'X' and A[i+2][j -1] <= 0:
              restricted_fields = restricted_fields - 1

          if i+1<(len(A)) and j +2<(len(A)):
            if A[i+1][j +2] != 'X' and A[i+1][j +2] <= 0:
              restricted_fields = restricted_fields - 1

          if i+1<(len(A)) and j -2>=0:
            if A[i+1][j -2] != 'X' and A[i+1][j -2] <= 0:
              restricted_fields = restricted_fields - 1

          if i-2>=0 and j+1<(len(A)):
            if A[i-2][j +1] != 'X' and A[i-2][j +1] <= 0:
              restricted_fields = restricted_fields - 1

          if i-2>=0 and j-1>=0:
            if A[i-2][j -1]!= 'X' and A[i-2][j -1] <= 0:
              restricted_fields = restricted_fields - 1

          if i-1>=0 and j-2>=0:
            if A[i-1][j -2]!= 'X' and  A[i-1][j -2] <= 0:
              restricted_fields = restricted_fields - 1

          if i-1>=0 and j+2<len(A):
            if A[i-1][j +2]!= 'X' and A[i-1][j +2] <= 0:
              restricted_fields = restricted_fields - 1


          A[i][j] = restricted_fields

          if less_restrictions <= restricted_fields: #guardamos a melhor solução (maior número, mínimo -8, máximo 0(melhor caso))
            less_restrictions = restricted_fields
            pos_x = i
            pos_y = j
  return (pos_x,pos_y,A)

#Colocando os cavalos
def place_knights(chessboard):
  global current_knight

  if current_knight == 1:
    first_move = True
  else:
    first_move = False
  dim = len(chessboard)

  if first_move: #No primeiro movimento não temos restrições ainda. Soluções ótimas devem começar em algum dos 4 cantos (pois apenas restringimos no máximo 2 casas).

    #Vamos escolher aleatoriamente a primeira casa a ser ocupada

    corners = [0,dim-1]
    pos_x = random.choice(corners)
    pos_y = random.choice(corners)
    chessboard[pos_x][pos_y] = current_knight


    #Restringimos nosso tabuleiro nas posições que são atacadas pelo cavalo posto.
    place_attacks(pos_x,pos_y,chessboard)

    current_knight = current_knight + 1


  #Depois do primeiro movimento
  else:
    for i in range(dim*dim - 1):

        pos = check_attacks(chessboard)
        if pos[0] == None:
          break
        chessboard[pos[0]][pos[1]] = current_knight  #Alocamos o i-ésimo cavaleiro a melhor posição possível (segundo nossa heurística).
        place_attacks(pos[0],pos[1],chessboard)

        current_knight = current_knight + 1
        #return chessboard

    return reset_chessboard()
  return

#Mantemos o tabuleiro e o número de cavalos daquele tabuleiro.
#Resetamos o tabuleiro para começar outro, caso necessário.
def reset_chessboard():
  global chessboard_solutions
  global solutions
  global current_knight
  global chessboard

  chessboard_solutions.append(chessboard)
  n_knights = current_knight - 1
  solutions.append(n_knights)
  current_knight = 1

  dim= len(chessboard)
  chessboard = []
  row = [0]*dim
  for i in range(dim):
      chessboard.append(row[:])

  return chessboard_solutions,solutions

def branch(P): #iremos ramificar nosso tabuleiro P em P0(sem colocar cavalo na próxima posição, marcar com X) e em P1 (colocando um cavalo na próxima posição)
  P1 = copy.deepcopy(P)

#----------------------------------------PODA-------------------------------------------------------
  next = 1 #variável para possibilitar a continuação das ramificações
  #checar se podemos podar P e, consequentemente P1.
  #verificar poda comparando o melhor resultado(colocando 'C' nas casas restantes) com o resultado da heuristica
  max_knights = 0
  for i in range(len(P)):
    for j in range(len(P)):
      if P[i][j] != 'X' and (P[i][j] == 'C' or P[i][j] == 0):
        max_knights = max_knights + 1
  if max_knights < solutions[0]: #se numero maximo possivel for menor, não valerá a pena, retornamos None
    P = None
    P1 = None
    return (P,P1,next)
#-------------------------------------------------------------------------------------------------------


  global final_solutions #vetor onde iremos adicionar nossas soluções

  next = 0
  for i in range(len(P)):
    for j in range(len(P)):
      if P[i][j] == 0: #se existir ao menos 1 elemento 0, ou seja uma casa disponível, colocaremos nossas marcações.
        next = 1
        P[i][j] = 'X'
        P1[i][j] = 'C'
        place_attacks(i,j,P1)
        break
    if next == 1:
      break
    else:
      if P not in final_solutions: #Para evitarmos soluções repetidas
        final_solutions.append(P)
  return (P,P1,next)

#--------------------------------------------------------- MAIN   ---------------------------------------------------------

#inicializar variáveis e variáveis globais (chessboard)
dim = int(input("Chessboard dimension: \n"))
#n = int(input("Quantas vezes iremos rodar o algoritmo? \n")) # A única diferença das soluções será a posição do cavalo inicial, que será sempre em algum dos 4 cantos
chessboard = initialize_chessboard(dim)
current_knight = 1
chessboard_solutions = []
solutions = [] #numero de cavalos no board
first_knight = True #para uso de heuristicas após a primeira jogada, ver posteriormente

#--------------------------------------------------------- MAIN HEURÍSTICA  ---------------------------------------------------------

#Utilização da heurística para estabelecer a solução ótima (ou uma boa solução)
print("\n-------------------------------------------------------\n")
test_solutions = []
while len(solutions) < 1:
  test_solutions.append(place_knights(chessboard)) #armazenar todas as soluções de boards, e numero de cavalos.
  #Como estamos trabalhando com algumas variáveis globais, não chamaremos test_solutions em mais nenhum momento, apenas para executar nosso programa e funções.
print("Pela heurística temos:")
for i in chessboard_solutions[0]:
    print(i)
print('Número máximo de cavalos pela heurística: ',solutions[0],'\n')

#Inicializar nossa fila, e vetor com soluções.
queue = [initialize_chessboard(dim)]
q_solutions = []
final_solutions = []

while len(queue) > 0:
  P = queue.pop(0)
  #print(queue)
  v = branch(P)
  #print(queue)
  if v[2] == 1:
    if v[0]!= None:
      queue.append(v[0])
    if v[1]!= None:
      queue.append(v[1])

solutions_size = len(final_solutions) #armazena o número de soluções possíveis
for i in range(solutions_size):
    count = 0
    for j in range(dim):
      for k in range(dim):
        if final_solutions[i][j][k] == 'C':
          count = count + 1
    q_solutions.append(count) #contar número de cavalos por solução
    #break #otimização não necessitaremos de retirar todas as listas da fila, no momento que não existem mais casas, paramos o processo.

print("Soluções possíveis: ", solutions_size)
max = idx = 0
for i in range(solutions_size):
  if q_solutions[i] >= max:
    max = q_solutions[i]
    idx = i

print("Maior número de cavalos possíveis: ",max)
print("Configuração possível do tabuleiro: ")
for i in final_solutions[idx]:
  print(i)
