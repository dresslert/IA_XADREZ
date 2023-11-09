import chess
import random

# function to find the best move
def minimax(board, depth, alpha, beta, maximixing_player):

    # condição de parada: profundidade atingida ou jogo acabou 
    if depth == 0 or board.is_game_over():
        return evaluate(board) # retorna a avaliação do tabuleiro

    legal_moves = list(board.legal_moves)
    if maximixing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval 
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval 

# funcao de avaliação do tabuleiro
def evaluate(board):
    # funcao de avaliação simples (poderia ser mais sofisticada, implantar depois)
    return random.randint(-100, 100) # retorna uma pontuação aleatória 

# funcao para encontrar a melhor jogada 
def get_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

# func que roda o game
def main():
    board = chess.Board()

    while not board.is_game_over():
        if board.turn: # se for a vez do jogador
            move_uci = input("Digite o movimento (UCI): ")
            if chess.Move.from_uci(move_uci) in board.legal_moves:
                board.push(chess.Move.from_uci(move_uci))
            else:
                print("Movimento invalido, tente novamente")
                continue
        else: # vez da IA 
            depth = 3 # profundidade de busca
            best_move = get_best_move(board, depth)
            board.push(best_move)
            print(f"A IA moveu: {best_move.uci()}")
    
    print("Fim do game")

if __name__ == "__main__":
    main()
