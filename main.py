import pygame
import os

WIDTH, HEIGHT = 800, 800
PIECE_WIDTH, PIECE_HEIGHT = 50, 50
FPS = 60
#colours
DARK_BROWN = (249, 172, 113)
LIGHT_BROWN = (103, 51, 20)
LIGHT_GREEN = (80, 165, 4)



class Control :
    def __init__(self, WIN) :
        self.WIN = WIN
        self.SQ = pygame.Rect(0, 0, 100, 100)
        self.selected = None, None
        self.load_assets()
        self.set_board(0)


    def set_board(self, orient) :
        if orient == 0 :
            self.pieces_pos = {
                self.b_king: (1, [[0, 4]]),
                self.b_bishop: (2, [[0, 2], [0, 5]]),
                self.b_knight: (2, [[0, 1], [0, 6]]),
                self.b_pawn: (8, [[1, i] for i in range(8)]),
                self.b_queen: (1, [[0, 3]]),
                self.b_rook: (2, [[0, 0], [0, 7]]),

                self.w_king: (1, [[7, 4]]),
                self.w_bishop: (2, [[7, 2], [7, 5]]),
                self.w_knight: (2, [[7, 1], [7, 6]]),
                self.w_pawn: (8, [[6, i] for i in range(8)]),
                self.w_queen: (1, [[7, 3]]),
                self.w_rook: (2, [[7, 0], [7, 7]])
            }
        elif orient == -1 :
            pass


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
        for i in self.pieces_pos :
            if [r, c] in self.pieces_pos[i][1] :
                ret = i
        return ret


    def piece_move(self, piece, pos) :
        def limit(seq) :
            return [i for i in seq if i[0] in range(0, 8) and i[1] in range(0, 8) and i != pos]
        if piece in [self.b_king, self.w_king] :
            return limit([[i, j]for i in range(pos[0]-1, pos[0]+2) for j in range(pos[1]-1, pos[1]+2)])
        # elif piece == self.b_pawn :
        #     return limit([[i, j] for ])


    def click_handle(self, loc) :
        ret = self.scan_board(loc[0], loc[1])
        if ret :
            self.selected = (ret, loc)


    def draw_window(self) :
        self.WIN.fill(LIGHT_BROWN)
        
        for i in range(8) :
            for j in range(8) :
                colour = LIGHT_GREEN
                self.SQ.update(j*100, i*100, 100, 100)
                if (i+j)%2 == 0 and self.selected[1] != [i, j] :
                    colour = LIGHT_BROWN
                elif self.selected[1] != [i, j] :
                    colour = DARK_BROWN
                pygame.draw.rect(self.WIN, colour, self.SQ)
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