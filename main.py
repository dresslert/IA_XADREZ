import chess

class ChessAI:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        try:
            if depth == 0 or board.is_game_over():
                return self.evaluate(board)

            legal_moves = list(board.legal_moves)

            if maximizing_player:
                max_eval = -float('inf')
                for move in legal_moves:
                    board.push(move)
                    eval = self.alphabeta(board, depth - 1, alpha, beta, False)
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
                    eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                    board.pop()
                    min_eval = min(min_eval, eval)
                    if beta <= alpha:
                        break
                return min_eval
        except Exception as e:
            print(f"Erro durante a avaliação do tabuleiro: {e}")
            return 0  # retorna uma pontuação neutra em caso de erro

    def evaluate(self, board):
        try:
            total_evaluation = 0

            # Avalia cada peça no tabuleiro
            for square, piece in zip(chess.SQUARES, board.piece_map().values()):
                if piece.color == chess.WHITE:
                    total_evaluation += self.piece_values[piece.piece_type]
                else:
                    total_evaluation -= self.piece_values[piece.piece_type]

            # adiciona bônus dinâmico para a posição do rei no final do jogo
            if board.is_variant_draw() or board.is_variant_end():
                total_evaluation += self.evaluate_king_position(board)

            return total_evaluation
        except Exception as e:
            print(f"Erro durante a avaliação do tabuleiro: {e}")
            return 0  # retorna uma pontuação neutra em caso de erro

    def evaluate_king_position(self, board):
        try:
            king_square = board.king(chess.WHITE)
            file, rank = chess.square_file(king_square), chess.square_rank(king_square)

            center_bonus = 1 if 3 <= file <= 4 and 3 <= rank <= 4 else 0

            return center_bonus
        except Exception as e:
            print(f"Erro durante a avaliação da posição do rei: {e}")
            return 0  # retorna uma pontuação neutra em caso de erro

    def get_best_move(self, board, depth):
        try:
            legal_moves = list(board.legal_moves)
            best_move = None
            best_eval = -float('inf')
            alpha = -float('inf')
            beta = float('inf')

            for move in legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval > best_eval:
                    best_eval = eval
                    best_move = move

            return best_move
        except Exception as e:
            print(f"Erro durante a escolha da melhor jogada: {e}")
            return None  # retorna None em caso de erro

    def play_game(self):
        try:
            board = chess.Board()

            while not board.is_game_over():
                self.imprimir_tabuleiro_grafico(board)

                if board.turn:
                    move_uci = input("Digite o movimento (UCI): ")
                    while chess.Move.from_uci(move_uci) not in board.legal_moves:
                        print("Movimento inválido, tente novamente.")
                        move_uci = input("Digite o movimento (UCI): ")

                    board.push(chess.Move.from_uci(move_uci))
                else:
                    print("A IA está pensando...")
                    depth = 3
                    best_move = self.get_best_move(board, depth)
                    if best_move is not None:
                        board.push(best_move)
                        print(f"A IA moveu: {best_move.uci()}")
                    else:
                        print("Erro ao escolher a melhor jogada da IA.")

            self.imprimir_tabuleiro_grafico(board)
            print("Fim do jogo")
        except Exception as e:
            print(f"Erro durante a execução do jogo: {e}")

    def imprimir_tabuleiro_grafico(self, board):
        print("   a b c d e f g h")
        print(" +------------------")
        for i in range(7, -1, -1):
            print(f"{i + 1}|", end=" ")
            for j in range(8):
                piece = board.piece_at(chess.square(j, i))
                if piece is not None:
                    print(piece.symbol(), end=" ")
                else:
                    print(".", end=" ")
            print()

# instancia a classe e inicia o jogo
if __name__ == "__main__":
    chess_ai = ChessAI()
    chess_ai.play_game()
