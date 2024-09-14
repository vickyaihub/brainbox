import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib.widgets import Button
from piece_highlighter import highlighter
from ai_simulator_1 import ai_chess_player
from variabless import defeate_highlighted_pieces, user_vs_ai_turn

from piece_highlighter import highlighted_boxes, highlighted_boxes_coordinates, image_position,\
     users_turn, ai_turn, players_turn_color, ai_player_color, defeate_highlighted_box_coordinted
    # defeate_highlighted_pieces,

captured_variable = None

class chess_game_class:

    def __init__(self):

        self.ax, self.fig, self.button_white, self.button_black, self.text, self.ax_button_white, self.ax_button_black = self.displaying_chessboard()
        self.piece_positions, self.piece_images, self.artists = self.placing_initialImages()
        self.defeat_highlighted_pieces = []
        


        self.highlighter_n_move = highlighter(self.piece_positions, self.ax, self.artists, self.piece_images)
        
        

    def create_chessboard(self):
        chessboard = np.zeros((8,8))
        chessboard[1::2,::2] = 1
        chessboard[::2,1::2] = 1
        return chessboard
    
    def displaying_chessboard(self):
        chessboard = self.create_chessboard()
        fig, ax = plt.subplots(figsize=(4.7,6.5))
        ax.imshow(chessboard, cmap='gray', interpolation='nearest')

        # Remove the ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Add player selection text
        text = ax.text(3, 8, 'Choose Your Player:', fontsize=14, ha='center')

        # Add buttons for White and Black
        ax_button_white = plt.axes([0.25, 0.1, 0.15, 0.05])  # position x, y, width, height
        ax_button_black = plt.axes([0.6, 0.1, 0.15, 0.05])
        button_white = Button(ax_button_white, 'White')
        button_black = Button(ax_button_black, 'Black')

        return ax, fig, button_white, button_black, text, ax_button_white, ax_button_black
    
    
    def placing_initialImages(self):
        piece_images = {
            'wr' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_rook.jpg'),
            'wn' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_knight.jpg'),
            'wq' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_queen.jpg'),
            'wk' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_king.jpg'),
            'wp' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_pawn.jpg'),
            'wb' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/white_bishop.jpg'),
            'br' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_rook.jpg'),
            'bn' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_knight.jpg'),
            'bq' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_queen.jpg'),
            'bk' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_king.jpg'),
            'bp' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_pawn.jpg'),
            'bb' : mpimg.imread('/home/vicky/Documents/ailearning/vickyaihub/chess_pieces_images_reduced/black_bishop.jpg'),
        }

        piece_positions = {
            (0,0):'wr', (0,1):'wb', (0,2):'wn', (0,3):'wq', (0,4):'wk', (0,5):'wn', (0,6):'wb', (0,7):'wr',
            **{(1,i):'wp' for i in range(8)},
            **{(6,i):'bp' for i in range(8)},
            (7,0):'br', (7,1):'bb', (7,2):'bn', (7,3):'bq', (7,4):'bk', (7,5):'bn', (7,6):'bb', (7,7):'br'
        }
        
        artists = {}  # To keep track of the positions of pieces and their corresponding artists
        
        # Overlay the piece positions on the chessboard
        for position, piece in piece_positions.items():
            row, col = position
            img = piece_images[piece]
            
            imagebox = OffsetImage(img, zoom=0.51)
            ab = AnnotationBbox(imagebox, (col, row), frameon=False)
            self.ax.add_artist(ab)
            artists[position] = ab

        return piece_positions, piece_images, artists
    def remove_buttons_and_text(self):
        ax = self.ax
        self.button_white.ax.remove()
        self.button_black.ax.remove()
        self.text.remove()
        plt.draw()
        print('self.ai_player_color=', ai_player_color)
    def on_white_button_click(self, event):
        players_turn_color[0] = 'w'
        ai_player_color[0] = 'b'
        print('white_button_clicked!!')
        self.remove_buttons_and_text()
    def on_black_button_click(self, event):
        players_turn_color[0] = 'b'
        ai_player_color[0] = 'w'
        print('Black_button_clicked!!')
        self.remove_buttons_and_text()

    def selecting_color(self, button_white, button_black):                
        # Selecting color
        button_white.on_clicked(self.on_white_button_click)
        button_black.on_clicked(self.on_black_button_click)
        
        
    def check_player_turn(self, pos):
        if pos not in self.piece_positions:
            print('you clicked on empty box______')
            return True
        elif players_turn_color[0] == self.piece_positions[pos][0]:
            return True
        else:
            return False
    def handling_highlightening_and_moving_by_ai(self):
        print('AI is selecting piece')
        ai_decided_piece_coordinates = (1,1)
        ai_decided_piece_move_coordinates = (3,1)
        chess_ai = ai_chess_player(self.piece_positions, self.piece_images, self.artists, self.ax, self.fig, ai_player_color)
        ai_decided_piece_coordinates, ai_decided_piece_move_coordinates = chess_ai.simulating_positions_bu_ai()


        # check if it is clicked on piece
        if ai_decided_piece_coordinates in self.piece_positions:
            print('Showing possible highlights')

            # if clicked on piece then show possible moves
            self.highlight_possible_moves(ai_decided_piece_coordinates)
            plt.pause(0.5)
            # if ai_decided_piece_move_coordinates in self.piece_positions and self.piece_positions[ai_decided_piece_move_coordinates][0] != players_turn_color[0]:
            # self.highlighter_n_move.outline_possible_defeat_pieces([ai_decided_piece_move_coordinates])
            self.move_piece_to_selected_box(ai_decided_piece_move_coordinates)

        # check if it is clicked on empty space
        else:
            print('you clicked on the empty space')
        
        # ax.add_patch(plt.Rectangle(ai_decided_coordinates, 1, 1, fill=False, edgecolor='blue', linewidth=3))
        return 
    def check_ai_turn_or_user_turn(self):
        if user_vs_ai_turn == 'ai':
            self.handling_highlightening_and_moving_by_ai()
        else:
            return
    def move_piece_to_selected_box(self, click_position):
        global user_vs_ai_turn
        print('You are moving the chess piece now')

        # Initial setup
        img_position = image_position[0]
        image_position.clear()
        new_row, new_col = click_position
        old_row, old_col = img_position
        piece = self.piece_positions[img_position]
        img = self.piece_images[piece]
        n_frames = 10   

        # Remove the artist from old position
        self.artists[img_position].set_visible(False)
        self.artists[img_position].remove()  # Remove artist from the axis
        del self.artists[img_position] 
        # artist = self.artists.pop(img_position)
        # artist.set_visible(False)
        # artist.remove()  
        plt.draw() 

        # Animate the piece movement
        for i in range(n_frames + 1):
            x = old_row + (new_row - old_row) * i / n_frames
            y = old_col + (new_col - old_col) * i / n_frames

            # Remove the previous artist at the plot
            if i > 0:
                if img_position in self.artists:
                    self.artists[img_position].set_visible(False)
                    self.artists[img_position].remove()                   
                    plt.draw()

            # Add and update the artist at the new position 
            imagebox = OffsetImage(img, zoom=0.51)
            ab = AnnotationBbox(imagebox, (y,x), frameon=False)
            self.ax.add_artist(ab)
            self.artists[img_position] = ab       
            plt.pause(0.01) # Animation effect 

        # Finalize the move
        self.piece_positions[click_position] = piece
        del self.piece_positions[img_position]
        self.artists[click_position] = self.artists.pop(img_position)

        # Update player turn
        if players_turn_color[0] == 'b':
            players_turn_color[0] = 'w'
        else:
            players_turn_color[0] = 'b'
        
        print('move completed')

        if user_vs_ai_turn == 'user':
            user_vs_ai_turn = 'ai'
        # allowing turn for another player
        self.check_ai_turn_or_user_turn()

        
    def handling_highlightening_and_moving(self, click_position):
        # if highlighted moves exists
        if highlighted_boxes: # Clear previous highlights
            
            # check the click, if it is inside the highlighted moves or not
            if click_position in highlighted_boxes_coordinates:
                print('you clicked inside highlighted box')
                for highlight in highlighted_boxes:
                    highlight.remove()
                highlighted_boxes.clear()
                highlighted_boxes_coordinates.clear()
                # move the piece to the selected box
                self.move_piece_to_selected_box(click_position)           
            else:
                print('you clicked outside highlighted area')
                for highlight in highlighted_boxes:
                    highlight.remove()
                highlighted_boxes.clear()

                # check if it is clicked on piece
                if click_position in self.piece_positions:
                    print('Showing possible highlights')

                    # if clicked on piece then show possible moves
                    self.highlight_possible_moves(click_position)            

                # check if it is clicked on empty space
                else:
                    print('you clicked on the empty space')

        # check the click, if it is not inside highlighted moves
        else:
            # check if it is clicked on piece then show possible highlights
            if click_position in self.piece_positions:
                self.highlight_possible_moves(click_position)          

            # check if it is clicked on empty space
            else:
                print('you clicked on the empty space')

    def highlight_possible_moves(self, position):
                                              
        # Checking which piece is selected
        print('self.piece_positions[position]==', self.piece_positions[position])
        if self.piece_positions[position].startswith('w'):
            print("White is selected")
            if self.piece_positions[position].endswith('p'):
                print('White pawn is selected')
                self.highlighter_n_move.pawn_highlighter(position)
            elif self.piece_positions[position].endswith('r'):
                print('white rook is selected')
                self.highlighter_n_move.highlight_possible_moves_rook(position)
            elif self.piece_positions[position].endswith('b'):
                print('White bishop is selected')
                self.highlighter_n_move.highlight_possible_moves_bishop(position)
            elif self.piece_positions[position].endswith('n'):
                print('White Knight is selected')
                self.highlighter_n_move.highlight_possible_moves_knight(position)
                # self.highlight_possible_moves_knight(position)
            elif self.piece_positions[position].endswith('q'):
                print('White queen is selected')
                self.highlighter_n_move.highlight_possible_moves_queen(position)
            elif self.piece_positions[position].endswith('k'):
                print('White king is selected')

        else:
            print('Black is selected')
            if self.piece_positions[position].endswith('p'):
                print('Black pawn is selected')
                self.highlighter_n_move.pawn_highlighter(position)
            elif self.piece_positions[position].endswith('r'):
                print('Black rook is selected')
                self.highlighter_n_move.highlight_possible_moves_rook(position)
            elif self.piece_positions[position].endswith('b'):
                print('Black bishop is selected')
                self.highlighter_n_move.highlight_possible_moves_bishop(position)
            elif self.piece_positions[position].endswith('n'):
                print('Black Knight is selected')
                self.highlighter_n_move.highlight_possible_moves_knight(position)
            elif self.piece_positions[position].endswith('q'):
                print('Black queen is selected')
                self.highlighter_n_move.highlight_possible_moves_queen(position)
            elif self.piece_positions[position].endswith('k'):
                print('Black king is selected')
            
    # def removing_outline_defeat_highlight_pieces(self):
    #     for pos in defeate_highlighted_pieces:

    
    def remove_defeat_highlightes_from_pieces(self, pos):
        self.artists[pos].remove()
        del self.artists[pos]
        
        for highlight in highlighted_boxes:
            highlight.remove()
        highlighted_boxes.clear()
        highlighted_boxes_coordinates.clear()
    
    def remove_outlines(self):
        for pos in defeate_highlighted_pieces:
            self.artists[pos].remove()
            del self.artists[pos]

            row, col = pos
            piece = self.piece_positions[pos]
            img = self.piece_images[piece]            
            imagebox = OffsetImage(img, zoom=0.51)
            ab = AnnotationBbox(imagebox, (col, row), frameon=False)
            self.ax.add_artist(ab)
            self.artists[pos] = ab
            

    def handling_defeat_highlighted_pieces(self, click_position):
        if defeate_highlighted_pieces:
            self.remove_outlines()
            if click_position in defeate_highlighted_pieces:
                print("removing captured piece")
                self.remove_defeat_highlightes_from_pieces(click_position)
                
                self.move_piece_to_selected_box(click_position)
        # self.remove_outlines()
        defeate_highlighted_pieces.clear()
        plt.draw()

        
    
    def onclick(self, event):
        if event.inaxes in [self.ax_button_white, self.ax_button_black]:
            print('buttons clicked')
            return 
        
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            print(" Click was outside the axes")
            return
        col = int(round(x))
        row = int(round(y))
        click_position = (row, col)
        
        self.handling_defeat_highlighted_pieces(click_position)            

        # # Chacking turn and avoid unnecessary clicking
        check_turn = self.check_player_turn(click_position)
        # print('captured_variable=', captured_variable)
        # print('check_trun=', check_turn)
        if check_turn is False:
            return        
        
        self.handling_defeat_highlighted_pieces(click_position)        
        self.handling_highlightening_and_moving(click_position) # Highlighting possible moves and moving the pieces

    def main(self):
        print('Chess Game Begun!')
        self.selecting_color(self.button_white, self.button_black)

               
        # connect the click event to the handler
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()
     
# Execution of script
if __name__ == "__main__":
    a = chess_game_class()
    a.main()

