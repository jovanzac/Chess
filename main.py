import pygame
import os

WIDTH, HEIGHT = 800, 800
PIECE_WIDTH, PIECE_HEIGHT = 50, 50
FPS = 60
#colours
DARK_BROWN = (249, 172, 113)
LIGHT_BROWN = (103, 51, 20)
LIGHT_GREEN = (80, 165, 4)
BLACK = (0, 0, 0)



class Control :
    def __init__(self, WIN) :
        self.WIN = WIN
        self.SQ = pygame.Rect(0, 0, 100, 100)
        self.load_assets()
        self.set_board(0)
        self.selected = None, None
        self.possible_moves = []
        self.turn = self.white_pieces_pos
        self.opponent = self.black_pieces_pos
        self.pieces_lost = {
            "black" : [],
            "white" : [],
        }
        self.check_condition = False
        self.starting_pos = {
            (self.w_pawn, self.b_pawn) : [[[6, i], 0] for i in range(8)],
        }
        self.castle_count = {
            "white-left": 0,
            "white-right": 0,
            "black-left": 0,
            "black-right": 0
        }


    def set_board(self, orient) :
        if orient == 0 :
            self.black_pieces_pos = {
                self.b_king: [1, [[0, 4]]],
                self.b_bishop: [2, [[0, 2], [0, 5]]],
                self.b_knight: [2, [[0, 1], [0, 6]]],
                self.b_pawn: [8, [[1, i] for i in range(8)]],
                self.b_queen: [1, [[0, 3]]],
                self.b_rook: [2, [[0, 0], [0, 7]]],
            }
            self.white_pieces_pos = {
                self.w_king: [1, [[7, 4]]],
                self.w_bishop: [2, [[7, 2], [7, 5]]],
                self.w_knight: [2, [[7, 1], [7, 6]]],
                self.w_pawn: [8, [[6, i] for i in range(8)]],
                self.w_queen: [1, [[7, 3]]],
                self.w_rook: [2, [[7, 0], [7, 7]]]
            }
        elif orient == -1 :
            # Switch sides
            self.selected = None, None
            self.possible_moves = []
            for i in self.black_pieces_pos :
                self.black_pieces_pos[i][1] = [[7-i[0], 7-i[1]] for i in self.black_pieces_pos[i][1]]
            for i in self.white_pieces_pos :
                self.white_pieces_pos[i][1] = [[7-i[0], 7-i[1]] for i in self.white_pieces_pos[i][1]]
            self.turn, self.opponent = self.opponent, self.turn


    def load_assets(self) :
        def process_img(loc) :
            return pygame.transform.scale(
                pygame.image.load(loc), (PIECE_WIDTH, PIECE_HEIGHT)
            )
        # Black Chess pieces
        self.b_king = process_img(os.path.join("Assets", "Black", "king.png"))
        self.b_bishop = process_img(os.path.join("Assets", "Black", "bishop.png"))
        self.b_knight = process_img(os.path.join("Assets", "Black", "knight.png"))
        self.b_pawn = process_img(os.path.join("Assets", "Black", "pawn.png"))
        self.b_queen = process_img(os.path.join("Assets", "Black", "queen.png"))
        self.b_rook = process_img(os.path.join("Assets", "Black", "rook.png"))
        # White Chess pieces
        self.w_king = process_img(os.path.join("Assets", "White", "king.png"))
        self.w_bishop = process_img(os.path.join("Assets", "White", "bishop.png"))
        self.w_knight = process_img(os.path.join("Assets", "White", "knight.png"))
        self.w_pawn = process_img(os.path.join("Assets", "White", "pawn.png"))
        self.w_queen = process_img(os.path.join("Assets", "White", "queen.png"))
        self.w_rook = process_img(os.path.join("Assets", "White", "rook.png"))


    def scan_board(self, r, c) :
        ret = None
        for i in self.black_pieces_pos :
            if [r, c] in self.black_pieces_pos[i][1] :
                ret = i
        for i in self.white_pieces_pos :
            if [r, c] in self.white_pieces_pos[i][1] :
                ret = i
        return ret


    def piece_move(self, piece, pos, p) :
        def limit(seq) :
            return [i for i in seq if i[0] in range(0, 8) and i[1] in range(0, 8) and i != pos]
        def free_space(seq) :
            return [i for i in seq if self.scan_board(i[0], i[1]) not in own or self.scan_board(i[0], i[1]) == None]
        def loop(condition, i, j, a, b) :
            while(free_space(limit([[i, j]]))) :
                ret.append([i, j])
                if condition(i, j) in opp :
                    break
                i += a
                j += b

        ret = []
        own = self.turn if p else self.opponent
        opp = self.opponent if p else self.turn
        # If piece is a king
        if piece in [self.b_king, self.w_king] :
            ret = free_space(limit([[i, j]for i in range(pos[0]-1, pos[0]+2) for j in range(pos[1]-1, pos[1]+2)]))
        # If piece is a pawn
        elif piece in [self.b_pawn, self.w_pawn] :
            def pawn_remove(condition, i, j) :
                if condition(i, j) :
                    ret.remove([i, j])
            ret = free_space(limit([[pos[0]-1, pos[1]-1], [pos[0]-1, pos[1]], [pos[0]-1, pos[1]+1]]))
            pawn_remove(lambda i, j: not self.scan_board(i, j) and [i, j] in ret, pos[0]-1, pos[1]-1)
            pawn_remove(lambda i, j: not self.scan_board(i, j) and [i, j] in ret, pos[0]-1, pos[1]+1)
            pawn_remove(lambda i, j: self.scan_board(i, j) and [i, j] in ret, pos[0]-1, pos[1])
            t = (self.w_pawn, self.b_pawn)
            if piece in t and [i for i in range(2) if [pos, i] in self.starting_pos[t]] :
                ret.append([pos[0]-2, pos[1]])
                pawn_remove(lambda i, j: self.scan_board(i, j) and [i, j] in ret, pos[0]-2, pos[1])
        # If piece is a bishop
        elif piece in [self.b_bishop, self.w_bishop] :
            i, j = pos[0]-1, pos[1]-1
            loop(lambda i, j:self.scan_board(i, j), i, j, -1, -1)
            j = pos[1]+1
            loop(lambda i, j:self.scan_board(i, j), i, j, -1, 1)
            i, j = pos[0]+1, pos[1]-1
            loop(lambda i, j:self.scan_board(i, j), i, j, 1, -1)
            j = pos[1]+1
            loop(lambda i, j:self.scan_board(i, j), i, j, 1, 1)
        # If piece is a rook
        elif piece in [self.b_rook, self.w_rook] :
            i, j = pos[0]-1, pos[1]
            loop(lambda i, j:self.scan_board(i, j), i, j, -1, 0)
            i = pos[0]+1
            loop(lambda i, j:self.scan_board(i, j), i, j, 1, 0)
            i, j = pos[0], pos[1]-1
            loop(lambda i, j:self.scan_board(i, j), i, j, 0, -1)
            j = pos[1]+1
            loop(lambda i, j:self.scan_board(i, j), i, j, 0, 1)
        # If piece is a queen
        elif piece in [self.b_queen, self.w_queen] :
            ret += self.piece_move(self.b_bishop, pos, 3)
            ret += self.piece_move(self.b_rook, pos, 3)
        # If piece is a knight
        elif piece in [self.b_knight, self.w_knight] :
            ret = free_space(limit([
                [pos[0]-2, pos[1]+1], [pos[0]-2, pos[1]-1], [pos[0]-1, pos[1]+2], [pos[0]-1, pos[1]-2],
                [pos[0]+2, pos[1]+1], [pos[0]+2, pos[1]-1], [pos[0]+1, pos[1]+2], [pos[0]+1, pos[1]-2]
            ]))
        if self.check_condition and p and p != 3 :
            ret = self.stage_and_filter(ret, piece, pos)
        return ret


    def stage_and_filter(self, moves, piece, pos) :
        ret = []
        if piece not in self.turn :
            return moves
        self.turn[piece][1].remove(pos)
        for i in moves :
            native = self.scan_board(i[0], i[1])
            if native :
                self.opponent[native][1].remove(i)
            self.turn[piece][1].append(i)
            self.check()
            if not self.check_condition :
                ret.append(i)
            self.turn[piece][1].remove(i)
            if native :
                self.opponent[native][1].append(i)
        self.turn[piece][1].append(pos)
        return ret


    def attacked_loc(self) :
        ret = []
        for i in self.opponent :
            a = 0
            for j in self.opponent[i][1] :
                a += 1
                ret += self.piece_move(i, j, False)
        return ret


    def check(self) :
        attacked = self.attacked_loc()
        self.checkcount = 0
        king = self.b_king if self.turn == self.black_pieces_pos else self.w_king
        if self.turn[king][1][0] in attacked :
            self.check_condition = True
        else :
            self.check_condition = False


    def castle(self, king, rook, rook_pos) :
        """Implement castling"""
        def check_empty() :
            r = range(0, blocks+1) if direction == "left" else range(5, 7) if side == "white" else range(4, 7)
            l =list(set([self.scan_board(7, i) for i in r]))
            return True if len(l) == 1 and l[0] == None else False
        side = "white" if self.turn == self.white_pieces_pos else "black"
        direction = "right" if rook_pos == [7, 7] else "left"
        blocks = 3 if (direction=="left" and side=="white") or (direction=="right" and side=="black") else 2
        if self.castle_count[f"{side}-{direction}"] == 0 and check_empty() :
            if direction == "right" :
                self.turn[king][1][0] = [7, self.turn[king][1][0][1]+2]
                self.turn[rook][1].remove([7, 7])
                self.turn[rook][1].append([7, 7-blocks])
            elif direction == "left" :
                self.turn[king][1][0] = [7, self.turn[king][1][0][1]-2]
                self.turn[rook][1].remove([7, 0])
                self.turn[rook][1].append([7, blocks])
            self.castle_count[f"{side}-{direction}"] += 1
            self.set_board(-1)


    def click_handle(self, loc) :
        piece = self.scan_board(loc[0], loc[1])
        rook = self.w_rook if self.turn == self.white_pieces_pos else self.b_rook
        king = self.w_king if self.turn == self.white_pieces_pos else self.b_king
        if piece in self.turn and not (piece == rook and self.selected[0] == king) :
            self.check()
            self.selected = (piece, loc)
            self.possible_moves = self.piece_move(piece, loc, True)
        elif self.selected[1] and loc in self.possible_moves :
            # If there is a piece in the new location, it gets taken
            if piece :
                opp = "black" if self.opponent == self.black_pieces_pos else "white"
                self.opponent[piece][1].remove(loc)
                self.pieces_lost[opp].append(piece)
            t = (self.w_pawn, self.b_pawn)
            i = 2 if [self.selected[1], 1] in self.starting_pos[t] else 1 if [self.selected[1], 0] in self.starting_pos[t] else None
            if self.selected[0] in t and i :
                self.starting_pos[t][self.starting_pos[t].index([self.selected[1], i-1])][1] += 1
            self.turn[self.selected[0]][1].remove(self.selected[1])
            self.turn[self.selected[0]][1].append(loc)
            self.set_board(-1)
        elif self.selected[0] == king and piece == rook :
            self.castle(king, rook, loc)


    def draw_window(self) :
        self.WIN.fill(LIGHT_BROWN)
        
        for i in range(8) :
            for j in range(8) :
                colour = LIGHT_GREEN
                self.SQ.update(j*100, i*100, 100, 100)
                if (i+j)%2 == 0 and [i, j] not in [self.selected[1]] + self.possible_moves :
                    colour = LIGHT_BROWN
                elif [i, j] not in [self.selected[1]] + self.possible_moves  :
                    colour = DARK_BROWN
                pygame.draw.rect(self.WIN, colour, self.SQ)
                pygame.draw.rect(self.WIN, BLACK, self.SQ, 2)
                piece = self.scan_board(i, j)
                if piece :
                    self.WIN.blit(piece, (j*100+25, i*100+25))

        pygame.display.update()
        
        
    def main(self) :
        clock = pygame.time.Clock()
        run = True
        while run :
            clock.tick(FPS)

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN :
                    mouse_pos = [i//100 for i in pygame.mouse.get_pos()]
                    print(f"mouse button down values are: {mouse_pos[1], mouse_pos[0]}")
                    self.click_handle(mouse_pos[::-1])
                
            self.draw_window()

        pygame.quit()


if __name__ == "__main__" :
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess!")
    
    ctrl = Control(WIN)
    ctrl.main()