import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from variabless import defeate_highlighted_pieces

# from variabless import highlighted_boxes, highlighted_boxes_coordinates, image_position, defeate_highlighted_pieces,\
#         users_turn, ai_turn, user_vs_ai_turn, players_turn_color, ai_player_color
highlighted_boxes = []
highlighted_boxes_coordinates = []
defeate_highlighted_box_coordinted = []
image_position = []
# defeate_highlighted_pieces = []
users_turn = []
ai_turn = []
# user_vs_ai_turn = ['user']
players_turn_color = ['beginning']
ai_player_color = [None]

class highlighter:
    def __init__(self,piece_positions, ax, artists, piece_images):
        
        self.piece_positions = piece_positions
        self.ax = ax
        self.piece_images = piece_images
        self.artists = artists
    def remove_outline_defeat_highlight_boxes(self):        
        for position in defeate_highlighted_pieces:
            piece = self.piece_positions[position]
            img = self.piece_images[piece]            
            imagebox = OffsetImage(img, zoom=0.51)
            ab = AnnotationBbox(imagebox, (position[1], position[0]), frameon=False)
            self.ax.add_artist(ab)
            self.artists[position] = ab
            

    def plotting_yellow_rectangles(self,possible_moves):
        print('possible_moves=', possible_moves)
        for move in possible_moves:
            highlight = plt.Rectangle((move[1] - 0.5, move[0] - 0.5), 1, 1, color='yellow', alpha=0.5)
            self.ax.add_patch(highlight)
            highlighted_boxes.append(highlight)
        plt.draw()
        highlighted_boxes_coordinates.extend(possible_moves)
        possible_moves.clear()

    def outline_possible_defeat_pieces(self):
        global defeate_highlighted_box_coordinted
        # Remove and hide defeated pieces
        for pos in defeate_highlighted_pieces:
            if pos in self.artists:
                self.artists[pos].remove()
                del self.artists[pos]
            plt.draw()

            # Get the piece and its image at the given position
            piece = self.piece_positions.get(pos)
            if piece:
                img = self.piece_images[piece]
                
                # Create an image annotation with reduced brightness and red border
                imagebox = OffsetImage(img, zoom=0.51)
                ab = AnnotationBbox(imagebox, (pos[1], pos[0]), frameon=True, bboxprops=dict(edgecolor='red', linewidth=2))
                
                # Add the annotation to the plot and store it in artists
                self.ax.add_artist(ab)
                self.artists[pos] = ab
        

        

    def pawn_highlighter(self,position):
        print("highlightinh possible pawn moves")
        image_position.clear()
        image_position.append(position)

        possible_moves = []
        row, col = position
        place = self.piece_positions[position]

        if place.startswith('w') and row < 7:
            if (row + 1, col) not in self.piece_positions:
                possible_moves.append((row + 1, col))
            if (row + 1, col) in self.piece_positions and self.piece_positions[(row+1, col)][0] != place[0]:
                print('possible_defeate_peaces_found')
                possible_moves.append((row + 1, col))
                defeate_highlighted_pieces.append((row + 1, col))
            if row == 1 and (row + 2, col) not in self.piece_positions:
                possible_moves.append((row + 2, col))
            if row == 1 and (row + 2, col) in self.piece_positions and self.piece_positions[(row+2, col)][0] != place[0]:
                print('possible_defeate_peaces_found')
                possible_moves.append((row + 2, col))
                defeate_highlighted_pieces.append((row + 2, col))
                
        elif place.startswith('b') and row > 0:
            if (row - 1, col) not in self.piece_positions:
                possible_moves.append((row - 1, col))
            if (row -1, col) in self.piece_positions and self.piece_positions[(row-1, col)][0] != place[0]:
                print('possible_defeate_peaces_found')
                possible_moves.append((row -1, col))
                defeate_highlighted_pieces.append(((row -1, col)))
            if row == 6 and (row - 2, col) not in self.piece_positions:
                possible_moves.append((row - 2, col))
            if row == 6 and (row -2, col) in self.piece_positions and self.piece_positions[(row-2, col)][0] != place[0]:
                print('possible_defeate_peaces_found')
                possible_moves.append((row -2, col))
                defeate_highlighted_pieces.append((row -2, col))

        self.plotting_yellow_rectangles(possible_moves)
        self.outline_possible_defeat_pieces()
    def highlight_possible_moves_rook(self, position):
        image_position.clear()
        image_position.append(position)
        possible_moves = []
        global defeate_highlighted_pieces
        row, col = position

        # Define a helper function to handle rook movement
        def explore_moves(start, end, step, fixed, is_row=True):
            for i in range(start, end, step):
                pos = (i, fixed) if is_row else (fixed, i)
                if pos in self.piece_positions:
                    if self.piece_positions[pos][0] == players_turn_color[0]:
                        break  # Stop if a smae team piece is encountered
                    else:
                        possible_moves.append(pos)
                        defeate_highlighted_pieces.append(pos)
                        break  # Stop after capturing a opponent piece
                else:
                    possible_moves.append(pos)

        # Explore all four directions
        explore_moves(row + 1, 8, 1, col, is_row=True)    # Upward
        explore_moves(row - 1, -1, -1, col, is_row=True)  # Downward
        explore_moves(col + 1, 8, 1, row, is_row=False)   # Right
        explore_moves(col - 1, -1, -1, row, is_row=False) # Left

        print('defeate_highlighted_pieces=', defeate_highlighted_pieces)
        self.plotting_yellow_rectangles(possible_moves)
        self.outline_possible_defeat_pieces()
       
    def highlight_possible_moves_knight(self, position):
        image_position.clear()
        image_position.append(position)
        possible_moves = []
        global defeate_highlighted_pieces
        defeate_highlighted_pieces.clear()

        row, col = position
        knight_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        for move in knight_moves:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:  # Ensure the move is within the board
                if move in self.piece_positions:
                    if players_turn_color[0] != self.piece_positions[move][0]:  # Opponent's piece
                        defeate_highlighted_pieces.append(move)
                        possible_moves.append(move)
                else:  # Empty square
                    possible_moves.append(move)

        print('defeate_highlighted_pieces=', defeate_highlighted_pieces)
        self.plotting_yellow_rectangles(possible_moves)
        self.outline_possible_defeat_pieces()

    def highlight_possible_moves_bishop(self, position):
        image_position.clear()
        image_position.append(position)
        possible_moves = []
        defeate_highlighted_pieces.clear()
        row, col = position

        # Directions for bishop moves (diagonals)
        directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        for direction in directions:
            d_row, d_col = direction
            for i in range(1, 8):
                move = (row + i * d_row, col + i * d_col)
                if not (0 <= move[0] < 8 and 0 <= move[1] < 8):  # Stay within board bounds
                    break
                if move in self.piece_positions:
                    if players_turn_color[0] == self.piece_positions[move][0]:  # Same color
                        break
                    defeate_highlighted_pieces.append(move)  # Opponent's piece
                    possible_moves.append(move)
                    break
                possible_moves.append(move)

        self.plotting_yellow_rectangles(possible_moves)
        self.outline_possible_defeat_pieces()


    # def highlight_possible_moves_bishop(self, position):
    #     image_position.clear()
    #     image_position.append(position)
    #     possible_moves = []
    #     defeate_highlighted_pieces.clear()
    #     row, col = position
    #     # Four separate moves, 1. upward left, 2. upward right, 3. Downward left, 4. downward right
    #     # 1. Diagonal 1- down right
    #     for i in range(1,8):
    #         move = (row+i, col+i)
    #         if move[0] > 7 or move[1] >7:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)
    #     # Diagonal 2- down left
    #     for i in range(1,8):
    #         move = (row+i, col-i)
    #         if move[0] > 7  or move[1] <  0 :
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #         else:
    #             possible_moves.append(move)
    #     # Diigonal 3 - up left
    #     for i in range(1,8):
    #         move = (row-i, col-i)
    #         if move[0] < 0 or move[1] < 0:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #         else:
    #             possible_moves.append(move)
    #     # Diagonal 4 - up right
    #     for i in range(1,8):
    #         move = (row-i, col+i)
    #         if move[0] < 0 or move[1] > 7:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #         else:
    #             possible_moves.append(move)

    #     self.plotting_yellow_rectangles(possible_moves)
    #     self.outline_possible_defeat_pieces()

    def highlight_possible_moves_queen(self, position):
        image_position.clear()
        image_position.append(position)
        possible_moves = []
        defeate_highlighted_pieces.clear()
        row, col = position

        # Directions for both rook and bishop moves
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),   # Rook directions (vertical & horizontal)
                    (1, 1), (-1, 1), (-1, -1), (1, -1)]  # Bishop directions (diagonal)

        for direction in directions:
            d_row, d_col = direction
            for i in range(1, 8):
                move = (row + i * d_row, col + i * d_col)
                if not (0 <= move[0] < 8 and 0 <= move[1] < 8):  # Stay within board bounds
                    break
                if move in self.piece_positions:
                    if players_turn_color[0] == self.piece_positions[move][0]:  # Same color
                        break
                    defeate_highlighted_pieces.append(move)  # Opponent's piece
                    possible_moves.append(move)
                    break
                possible_moves.append(move)

        self.plotting_yellow_rectangles(possible_moves)
        self.outline_possible_defeat_pieces()

    # def highlight_possible_moves_queen(self, position):
    #     image_position.clear()
    #     image_position.append(position)
    #     possible_moves = []
    #     defeate_highlighted_pieces.clear()
    #     row, col = position
        
    #     # Queen's movement combines rook and bishop logic

    #     # Rook-like moves (horizontal and vertical)
        
    #     # Moving up (row increasing)
    #     for i in range(row + 1, 8):
    #         move = (i, col)
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)
        
    #     # Moving down (row decreasing)
    #     for i in range(row - 1, -1, -1):
    #         move = (i, col)
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Moving right (column increasing)
    #     for i in range(col + 1, 8):
    #         move = (row, i)
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Moving left (column decreasing)
    #     for i in range(col - 1, -1, -1):
    #         move = (row, i)
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Bishop-like moves (diagonal)
        
    #     # Diagonal 1: Moving up-right
    #     for i in range(1, 8):
    #         move = (row + i, col + i)
    #         if move[0] > 7 or move[1] > 7:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Diagonal 2: Moving down-right
    #     for i in range(1, 8):
    #         move = (row - i, col + i)
    #         if move[0] < 0 or move[1] > 7:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Diagonal 3: Moving down-left
    #     for i in range(1, 8):
    #         move = (row - i, col - i)
    #         if move[0] < 0 or move[1] < 0:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     # Diagonal 4: Moving up-left
    #     for i in range(1, 8):
    #         move = (row + i, col - i)
    #         if move[0] > 7 or move[1] < 0:
    #             break
    #         if move in self.piece_positions:
    #             if players_turn_color[0] == self.piece_positions[move][0]:
    #                 break
    #             else:
    #                 defeate_highlighted_pieces.append(move)
    #                 possible_moves.append(move)
    #                 break
    #         else:
    #             possible_moves.append(move)

    #     self.plotting_yellow_rectangles(possible_moves)
    #     self.outline_possible_defeat_pieces()


            
            
            
        
        
