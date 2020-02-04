from flask import Flask, render_template, redirect, url_for, request
import chess
import chess.polyglot

# initialization

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    response.cache_control.max_age = 604800
    return(response)

# MAIN PAGE

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/ai', methods = ['GET', 'POST'])
def ai():
    if (request.method == 'POST'):

        board = chess.Board(request.form['fen'])

        pawntable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10,-20,-20, 10, 10,  5,
        5, -5,-10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0]

        knightstable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50]

        bishopstable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20]

        rookstable = [
        0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

        queenstable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
        0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

        kingstable = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30]

        piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING ]
        tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
        piecevalues = [100,320,330,500,900]

        ###

        def init_evaluate_board():

            global boardvalue

            wp = len(board.pieces(chess.PAWN, chess.WHITE))
            bp = len(board.pieces(chess.PAWN, chess.BLACK))
            wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
            bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
            wb = len(board.pieces(chess.BISHOP, chess.WHITE))
            bb = len(board.pieces(chess.BISHOP, chess.BLACK))
            wr = len(board.pieces(chess.ROOK, chess.WHITE))
            br = len(board.pieces(chess.ROOK, chess.BLACK))
            wq = len(board.pieces(chess.QUEEN, chess.WHITE))
            bq = len(board.pieces(chess.QUEEN, chess.BLACK))

            material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)

            pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
            pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.PAWN, chess.BLACK)])
            knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
            knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.KNIGHT, chess.BLACK)])
            bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
            bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.BISHOP, chess.BLACK)])
            rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
            rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.ROOK, chess.BLACK)])
            queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
            queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.QUEEN, chess.BLACK)])
            kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
            kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                                            for i in board.pieces(chess.KING, chess.BLACK)])

            boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

            return(boardvalue)

        def evaluate_board():

            global boardvalue

            if board.is_checkmate():

                if board.turn:
                    return(-9999)
                else:
                    return(9999)

            if board.is_stalemate():
                return(0)

            if board.is_insufficient_material():
                return(0)

            eval = boardvalue
            if board.turn:
                return(eval)
            else:
                return(-eval)

        def update_eval(mov, side):

            global boardvalue

            movingpiece = board.piece_type_at(mov.from_square)

            if side:
                boardvalue = boardvalue - tables[movingpiece - 1][mov.from_square]

                if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                    boardvalue = boardvalue - rookstable[chess.H1]
                    boardvalue = boardvalue + rookstable[chess.F1]
                elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                    boardvalue = boardvalue - rookstable[chess.A1]
                    boardvalue = boardvalue + rookstable[chess.D1]

            else:
                boardvalue = boardvalue + tables[movingpiece - 1][mov.from_square]

                if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                    boardvalue = boardvalue + rookstable[chess.H8]
                    boardvalue = boardvalue - rookstable[chess.F8]
                elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                    boardvalue = boardvalue + rookstable[chess.A8]
                    boardvalue = boardvalue - rookstable[chess.D8]

            if side:
                boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square]
            else:
                boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square]

            if board.is_capture(mov):
                if side:
                    boardvalue = boardvalue + piecevalues[board.piece_type_at(mov.to_square)-1]
                else:
                    boardvalue = boardvalue - piecevalues[board.piece_type_at(mov.to_square)-1]

            if mov.promotion != None:
                if side:
                    boardvalue = boardvalue + piecevalues[mov.promotion-1] - piecevalues[movingpiece-1]
                    boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square] \
                        + tables[mov.promotion - 1][mov.to_square]
                else:
                    boardvalue = boardvalue - piecevalues[mov.promotion-1] + piecevalues[movingpiece-1]
                    boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square] \
                        - tables[mov.promotion - 1][mov.to_square]

            return(mov)

        def make_move(mov):
            global boardvalue

            update_eval(mov, board.turn)
            board.push(mov)

            return(mov)

        def unmake_move():
            global boardvalue

            mov = board.pop()
            update_eval(mov, not board.turn)

            return(mov)

        def quiesce(alpha, beta):

            stand_pat = evaluate_board()

            if (stand_pat >= beta):
                return beta

            if (alpha < stand_pat):
                alpha = stand_pat

            for move in board.legal_moves:

                if board.is_capture(move):

                    make_move(move)
                    score = -quiesce(-beta, -alpha)
                    unmake_move()

                    if (score >= beta):
                        return beta
                    if (score > alpha):
                        alpha = score

            return(alpha)

        def alphabeta(alpha, beta, depthleft):

            bestscore = -9999

            if (depthleft == 0):
                return quiesce(alpha, beta)

            for move in board.legal_moves:

                make_move(move)
                score = -alphabeta(-beta, -alpha, depthleft - 1)
                unmake_move()

                if (score >= beta):
                    return score
                if (score > bestscore):
                    bestscore = score
                if (score > alpha):
                    alpha = score

            return(bestscore)

        def selectmove(depth):

            try:
                move = chess.polyglot.MemoryMappedReader("bookfish.bin").weighted_choice(board).move

                print(str(move), "BOOK")
                return(str(move))

            except:
                bestMove = chess.Move.null()
                bestValue = -99999
                alpha = -100000
                beta = 100000

                for move in board.legal_moves:

                    print("boardvalue =", boardvalue)
                    print("Move ->", move)

                    make_move(move)

                    boardValue = -alphabeta(-beta, -alpha, depth - 1)

                    if (boardValue > bestValue):
                        bestValue = boardValue;
                        bestMove = move

                    if (boardValue > alpha):
                        alpha = boardValue

                    unmake_move()


                print(str(bestMove), "AI")
                return(str(bestMove))

        ###

        boardvalue = init_evaluate_board()
        mov = selectmove(1)
        return(mov)

###

if __name__ == '__main__':
    app.run(debug=True)
