import numpy as np
import pygame
import sys
import math
import random
from button import Button

class Games:
  def __init__(self,depth2):
    self.depth2 = depth2

  def run1(self,depth2):


    ROWS = 6
    COLUMNS = 7

    BLUE = (64,224,208)
    BLACK = (0,0,0)
    PINK = (255,105,180)
    YELLOW = (240,240,0)

    PLAYER = 0
    AI = 1

    PLAYER_PIECE = 1
    AI_PIECE = 2

    WINDOW = 4
    EMPTY = 0

    COLUMN2 = 0

    SQUARE = 100


    def create_board(): 
      board = np.zeros((ROWS,COLUMNS))
      return board

    def drop_piece(board,row,column,piece): 
      board[row][column] = piece

    def is_valid_location(board,column):
      return board[ROWS-1][column] == 0 #

    def next_open_row(board,column): 
      for r in range(ROWS):
        if board[r][column] == 0:
          return r

    def print_board(board): 
      print(np.flip(board,0))

    def winning_move(board,piece):

      #horizontal
      for c in range(COLUMNS-3): 
        for r in range(ROWS):
          if board[r][c] == piece and board[r][c+1] == piece and board [r][c+2] == piece and board[r][c+3] == piece:
            return True

      #vertical
      for c in range(COLUMNS):
        for r in range(ROWS-3):
          if board[r][c] == piece and board[r+1][c] == piece and board [r+2][c]== piece and board[r+3][c] == piece:
            return True

      #positive diagonal
      for c in range(COLUMNS-3):
        for r in range(ROWS-3):
          if board[r][c] == piece and board[r+1][c+1] == piece and board [r+2][c+2]== piece and board[r+3][c+3] == piece:
            return True

      #negative diagonal
      for c in range(COLUMNS-3):
        for r in range(3,ROWS):
          if board[r][c] == piece and board[r-1][c+1] == piece and board [r-2][c+2]== piece and board[r-3][c+3] == piece:
            return True

    def evaluate_window(window,piece):
          score = 0
          opponent_piece = PLAYER_PIECE
          if piece == PLAYER_PIECE:
            opponent_piece = AI_PIECE


          if window.count(piece) == 4:
            score += 100 # returns if its a connect 4
    
          elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5 # returns if connect 3

          elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score +=2

          elif window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
            score -=4
          
          return score


    def score_position(board,piece):
      score = 0
        
      centre_array = [int(i) for i in list(board[:,COLUMNS//2])]
      centre_count = centre_array.count(piece)
      score += centre_count * 3  # preferences centre

      #horizontal
      for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMNS - 3):
          window = row_array[c:c+WINDOW]
          score += evaluate_window(window, piece)

      #vertical
      for c in range(COLUMNS):
        column_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
          window = column_array[r:r+ WINDOW]
          score += evaluate_window(window, piece)

      #diagnoal positive
      for r in range(ROWS - 3):
        for c in range(COLUMNS-3):
          window = [board[r+i][c+i] for i in range(WINDOW)]

          score += evaluate_window(window, piece)

      for r in range(ROWS - 3):
        for c in range(COLUMNS-3):
          window = [board[r+3-i][c+i] for i in range(WINDOW)]

          score += evaluate_window(window, piece)



      return score 

    def is_terminal_node(board):
      return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

    def minimax(board,depth,alpha,beta, maximisingPlayer):
      valid_locations = get_valid_locations(board)
      is_terminal = is_terminal_node(board)
      if depth == 0 or is_terminal: # terminal node is someone winning or no pieces left
        if is_terminal:
          if winning_move(board, AI_PIECE):
            return (None,100000000000000)
          elif winning_move(board,PLAYER_PIECE):
            return (None,-1000000000)
          else:
            return (None,0) # game over
        else: 
          return (None,score_position(board,AI_PIECE))
        
      if maximisingPlayer:
        value = -math.inf
        column2 = random.choice(valid_locations)
        for column in valid_locations:
          row = next_open_row(board,column)
          board_copy = board.copy() # so it doesnt use the same memory when doing repeadtedly
          drop_piece(board_copy,row,column,AI_PIECE)
          new_score = minimax(board_copy,depth-1,alpha,beta,False)[1]
          if new_score > value:
            value = new_score
            column2 = column
          alpha = max(alpha,value)
          if alpha >= beta:
            break
          
        return column2,value
        
      else: #minimising player
        value = math.inf
        column2 = random.choice(valid_locations)
        for column in valid_locations:
          row = next_open_row(board,column)
          board_copy = board.copy()
          drop_piece(board_copy,row,column,PLAYER_PIECE)
          new_score = minimax(board_copy,depth-1,alpha,beta,True)[1]# true and false switches between players
          if new_score < value:
            value = new_score
            column2 = column
          beta = min(beta,value)
          if alpha >= beta:
            break # dont need to look further in the tree
        return column2,value


        


    def get_valid_locations(board):
      valid_locations = []
      for column in range (COLUMNS):
        if is_valid_location(board,column):
          valid_locations.append(column)
      return valid_locations

    def pick_best_move (board,piece):

      best_score = -10000

      valid_locations = get_valid_locations(board)

      best_column = random.choice(valid_locations)

      for column in valid_locations:
        row = next_open_row(board,column)
        # we need to simulate this location

        temp_board = board.copy()
        drop_piece(temp_board,row,column,piece)
        score = score_position(temp_board, piece)
        if score > best_score:
          best_score = score
          best_column = column
        
      return best_column






    def draw_board(board):
      for c in range(COLUMNS):
        for r in range(ROWS):
          pygame.draw.rect(screen,BLUE,(c*SQUARE, r*SQUARE+ SQUARE, SQUARE, SQUARE))
          pygame.draw.circle(screen, BLACK, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), RADIUS)
      
      for c in range(COLUMNS):
        for r in range(ROWS):
          if board[r][c] == PLAYER_PIECE:
            pygame.draw.circle(screen, PINK, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
          elif board[r][c]== AI_PIECE:
            pygame.draw.circle(screen,YELLOW, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
      pygame.display.update()

    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()


    width = COLUMNS * SQUARE
    height = (ROWS+1) * SQUARE

    size = (width,height)

    RADIUS = int(SQUARE/2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace",75)

    turn = random.randint(PLAYER, AI)

    while not game_over:
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()

        if event.type == pygame.MOUSEMOTION:
          pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE))
          posx = event.pos[0]
          if turn == PLAYER:
            pygame.draw.circle(screen, PINK, (posx, int(SQUARE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
          pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE))
          #print(event.pos)

          #player 1 input

          if turn == PLAYER:
            posx = event.pos[0]
            column = int(math.floor(posx/SQUARE))
            
            if is_valid_location(board,column):
              row = next_open_row(board,column)
              drop_piece(board,row,column,PLAYER_PIECE)

              if winning_move(board,PLAYER_PIECE):
                message = myfont.render("Player 1 wins.",1,PINK)
                screen.blit(message,(40,10))
                game_over = True

              turn += 1
              turn = turn % 2 #changes turns

              print_board(board)
              draw_board(board)
          
          
      #AI input
      if turn == AI and not game_over:
        pygame.time.wait(500)

        #column = random.randint(0, (COLUMN_COUNT-1))

        #column = pick_best_move(board,AI_PIECE)

        column,minimax_score = minimax(board,self.depth2 ,-math.inf,math.inf,True)#want more of a depth you increase and it looks further into the future

                
        if is_valid_location(board,column):
          #pygame.time.wait(500)
          row = next_open_row(board,column)
          drop_piece(board,row,column,AI_PIECE)
        
          if winning_move(board,AI_PIECE):
            message = myfont.render("Player 2 wins.",1,YELLOW)
            screen.blit(message,(40,10))
            game_over = True
            
          print_board(board)
          draw_board(board)

          turn += 1
          turn = turn % 2 #changes turns

      if game_over:
        pygame.time.wait(3000)

def multiplayer1():
  ROWS = 6
  COLUMNS = 7

  BLUE = (64,224,208)
  BLACK = (0,0,0)
  PINK = (255,105,180)
  YELLOW = (240,240,0)


  def create_board():
    board = np.zeros((ROWS,COLUMNS))
    return board

  def drop_piece(board,row,column,piece):
    board[row][column] = piece

  def is_valid_location(board,column):
    return board[ROWS-1][column] == 0 #checks top row is empty

  def next_open_row(board,column): # finds which row to next place it on
    for r in range(ROWS):
      if board[r][column] == 0:
        return r

  def print_board(board):
    print(np.flip(board,0))

  def winning_move(board,piece):

    #horizontal
    for c in range(COLUMNS-3):
      for r in range(ROWS):
        if board[r][c] == piece and board[r][c+1] == piece and board [r][c+2]== piece and board[r][c+3] == piece:
          return True

    #vertical
    for c in range(COLUMNS):
      for r in range(ROWS-3):
        if board[r][c] == piece and board[r+1][c] == piece and board [r+2][c]== piece and board[r+3][c] == piece:
          return True

    #positive diagonal
    for c in range(COLUMNS-3):
      for r in range(ROWS-3):
        if board[r][c] == piece and board[r+1][c+1] == piece and board [r+2][c+2]== piece and board[r+3][c+3] == piece:
          return True

    #negative diagonal
    for c in range(COLUMNS-3):
      for r in range(3,ROWS):
        if board[r][c] == piece and board[r-1][c+1] == piece and board [r22][c+2]== piece and board[r-3][c+3] == piece:
          return True

  def draw_board(board):
    for c in range(COLUMNS):
      for r in range(ROWS):
        pygame.draw.rect(screen,BLUE,(c*SQUARE, r*SQUARE+ SQUARE, SQUARE, SQUARE))
        pygame.draw.circle(screen, BLACK, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), RADIUS)
    
    for c in range(COLUMNS):
      for r in range(ROWS):
        if board[r][c] == 1:
          pygame.draw.circle(screen, PINK, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
        elif board[r][c]== 2:
          pygame.draw.circle(screen,YELLOW, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RADIUS)
    pygame.display.update()

  board = create_board()
  print_board(board)
  game_over = False
  turn = 0

  pygame.init()

  SQUARE = 100

  width = COLUMNS * SQUARE
  height = (ROWS+1) * SQUARE

  size = (width,height)

  RADIUS = int(SQUARE/2 - 5)

  screen = pygame.display.set_mode(size)
  draw_board(board)
  pygame.display.update()

  myfont = pygame.font.SysFont("monospace",20)

  while not game_over:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      if event.type == pygame.MOUSEMOTION:
        pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE))
        posx = event.pos[0]
        if turn == 0:
          pygame.draw.circle(screen, PINK, (posx, int(SQUARE/2)), RADIUS)
        else:
          pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE/2)), RADIUS)
        pygame.display.update()

      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE))
        #print(event.pos)

        #player 1 input

        if turn == 0:
          posx = event.pos[0]
          column = int(math.floor(posx/SQUARE))
          
          if is_valid_location(board,column):
            row = next_open_row(board,column)
            drop_piece(board,row,column,1)

            if winning_move(board,1):
              label = myfont.render("Player 1 wins. Well done Player 1, that is an amazing achievement, keep going. Well done Player 2, you have worked very hard, keep trying.",1,PINK)
              screen.blit(label,(40,10))
              game_over = True
        
      
        #player 2 input
        else:
          posx = event.pos[0]
          column = int(math.floor(posx/SQUARE))
              
          if is_valid_location(board,column):
            row = next_open_row(board,column)
            drop_piece(board,row,column,2)
      
            if winning_move(board,2):
              label = myfont.render("Player 1 wins. Well done Player 1, that is an amazing achievement, keep going. Well done Player 2, you have worked very hard, keep trying.",1,YELLOW)
              screen.blit(label,(40,10))
              game_over = True
          
        print_board(board)
        draw_board(board)

        turn += 1
        turn = turn % 2 #changes turns

        if game_over:
          pygame.time.wait(3000)


#test
pygame.init()

#create game window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font1 = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("arialblack", 30)


#define colours
TEXT_COL = (0, 0, 0)


#load button images
instructions_img = pygame.image.load("images/instructions.png").convert_alpha()
play_img = pygame.image.load("images/play.png").convert_alpha()
quit_img = pygame.image.load("images/quit.png").convert_alpha()
easy_img = pygame.image.load('images/easy.png').convert_alpha()
medium_img = pygame.image.load('images/medium.png').convert_alpha()
hard_img = pygame.image.load('images/hard.png').convert_alpha()
impossible_img = pygame.image.load('images/impossible.png').convert_alpha()
multiplayer_img = pygame.image.load('images/multiplayer.png').convert_alpha()
back_img = pygame.image.load('images/back.png').convert_alpha()
back2_img = pygame.image.load('images/back2.png').convert_alpha()
#create button instances

instructions_button = Button(200, 100, instructions_img, 0.2)
play_button = Button(100, 295, play_img, 0.2)
quit_button = Button(200, 550, quit_img, 0.19)
easy_button = Button(50, 250, easy_img, 0.3)
medium_button = Button(370, 250, medium_img, 0.195)
hard_button = Button(50, 400, hard_img, 0.3)
impossible_button = Button(400, 350, impossible_img, 0.21)
multiplayer_button = Button (370,400, multiplayer_img, 0.185)
back_button = Button (200,500, back_img, 0.2)
back2_button = Button (200,550, back_img, 0.18)

screen_img = pygame.image.load("images/screen.png").convert_alpha()
screen2_img = pygame.transform.scale(screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((64,224,208))
  

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if instructions_button.draw(screen):
        menu_state = "instructions"
      if quit_button.draw(screen):
        game_paused = False
      if easy_button.draw(screen):
        easy = Games(1)
        easy.run1(1)
      if medium_button.draw(screen):
        medium = Games(3)
        medium.run1(3)
      if hard_button.draw(screen):
        hard = Games(4)
        hard.run1(4)
      if multiplayer_button.draw(screen):
        multiplayer1()

    if menu_state == "instructions":
      draw_text("How to Play:", font1, TEXT_COL, 50, 50)
      draw_text("The game is simple - try to get four of", font2, TEXT_COL, 50, 120)
      draw_text("your colour pieces together in a row", font2, TEXT_COL, 50, 150)
      draw_text("This can be: horizontally, vertically or", font2, TEXT_COL, 50, 200)
      draw_text("even diagonally", font2, TEXT_COL, 50, 230)
      draw_text("The first person to get 4 in a row wins,", font2, TEXT_COL, 50, 280)
      draw_text("so make sure to block your opponents", font2, TEXT_COL, 50, 310)
      draw_text("pieces", font2, TEXT_COL, 50, 340)
      draw_text("Good Luck!", font2, TEXT_COL, 50, 390)

      if back_button.draw(screen):
        menu_state = "main"

  else:
    screen.blit(screen2_img, (0, 0))
   

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()