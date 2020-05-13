# This Tetris was made during COVID lockdown in May 2020. Created mostly from scratch with a little online help
# on how to organize and work with game field. Code is written in WingIDE, blocks are drawn in GIMP.

# Since I'm not a very skilled programmer and don't have much knowledge of 'right' programming practices and code style,
# this code may contain poorly written parts. But nevertheless it works and (as far as I've tested) doesn't have critical errors.

import pygame as pg
from random import choice

pg.init()

WHITE = (255, 255, 255)  # text color
BLACK = (0, 0, 0)        # game background
DARKGREY = (30, 30, 30)  # info bar background
GREY5 = (12, 12, 12)     # start window background
CELL_SIZE = 30           # can be changed, but then you have to redraw blocks.png

class MainWindow:
    def __init__(self):
        self.game_width = CELL_SIZE * game_field.width
        self.game_height = CELL_SIZE * game_field.height
        self.screen = pg.display.set_mode((480, 600))
        pg.key.set_repeat(50, 200)
        self.font = pg.font.SysFont('tahoma', 16)
        self.big_font = pg.font.SysFont('tahoma', 50, bold=True)
        self.small_font = pg.font.SysFont('tahoma', 10)

    def show_score(self):
        rows = game_field.total_rows_deleted
        score = game_field.score
        level = game_field.level
        rows_label = self.font.render(f'Lines removed: {rows}', True, WHITE)
        score_label = self.font.render(f'Score: {score}', True, WHITE)
        level_label = self.font.render(f'Level: {level}', True, WHITE)
        self.screen.blit(rows_label, (self.game_width + 30, 10))
        self.screen.blit(score_label, (self.game_width + 30, 30))
        self.screen.blit(level_label, (self.game_width + 30, 50))

    def show_next(self, next_piece):
        next_label = self.font.render('Next piece:', True, WHITE)
        self.screen.blit(next_label, (self.game_width + 30, 90))
        
        next_piece_window = pg.Surface((120, 150))   # create window that will be blitted into the main window
        block_color = next_piece.shape[0][0]
        if block_color == 0:
            block_color = next_piece.shape[0][1]
        block = piece.blocks.subsurface((block_color - 1) * 30, piece.tileset, 30, 30)
        for j in range(len(next_piece.shape)):
            for i in range(len(next_piece.shape[j])):
                if next_piece.shape[j][i] != 0:   # draw next piece centered in next piece window
                    next_piece_window.blit(block, (i * CELL_SIZE + 15 * (4 - len(next_piece.shape[0])),
                                                   j * CELL_SIZE + 15 * (5 - len(next_piece.shape))))

        self.screen.blit(next_piece_window, (self.game_width + 30, 115))

    def show_start_menu(self):
        pg.display.set_caption('Tetris')
        bg = pg.image.load('bg.png')
        self.screen.blit(bg, (0, 0))        
        win_size_x, win_size_y = self.screen.get_size()
        font = pg.font.SysFont('tahoma', 30, bold=True)
        bigger_font = pg.font.SysFont('tahoma', 60, bold=True)
        label_text = 'Press Enter to start'
        label = font.render(label_text, True, WHITE)
        tetris_label = bigger_font.render('TETRIS', True, WHITE)
        label_size = font.size(label_text)
        tetris_label_size = bigger_font.size('TETRIS')

        self.screen.blit(tetris_label, ((win_size_x - tetris_label_size[0]) // 2, (win_size_y - 250 - tetris_label_size[1]) // 2))
        self.screen.blit(label, ((win_size_x - label_size[0]) // 2, (win_size_y - label_size[1]) // 2 - 50))

    def create_menu_buttons(self):
        win_size_x, win_size_y = self.screen.get_size()
        btnStart = Button(150, 35, DARKGREY, 'New game', solid=False)
        btnResume = Button(150, 35, DARKGREY, 'Resume game', solid=False)
        btnQuit = Button(150, 35, DARKGREY, 'Quit game', solid=False)
        btnSettings = Button(150, 35, DARKGREY, 'Settings', solid=False)
        
        if not game_started:
            btnResume.text_color = GREY5
        btnStart.draw(window.screen, (win_size_x - btnQuit.width) // 2, win_size_y - 265)
        btnResume.draw(window.screen, (win_size_x - btnQuit.width) // 2, win_size_y - 220)
        btnSettings.draw(window.screen, (win_size_x - btnQuit.width) // 2, win_size_y - 175)
        btnQuit.draw(window.screen, (win_size_x - btnQuit.width) // 2, win_size_y - 130)
        return btnStart, btnResume, btnSettings, btnQuit
    
    def game_over(self):
        win_size_x, win_size_y = self.screen.get_size()
        game_over = self.big_font.render('GAME OVER', True, WHITE)
        press_space = self.font.render('Press space to restart', True, WHITE)
        label1_size = self.big_font.size('GAME OVER')
        label2_size = self.font.size('Press space to restart')
        bg = pg.Surface((win_size_x, win_size_y), pg.SRCALPHA)
        bg.fill((0, 0, 0, 200))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(game_over, ((win_size_x - label1_size[0]) // 2, (win_size_y - label1_size[1]) // 2))
        self.screen.blit(press_space, ((win_size_x - label2_size[0]) // 2, (win_size_y - label2_size[1]) // 2 + 50))
        pg.time.set_timer(pg.USEREVENT, 0)

    def pause(self):
        win_size_x, win_size_y = self.screen.get_size()
        bg = pg.Surface((win_size_x, win_size_y), pg.SRCALPHA)
        bg.fill((0, 0, 0, 200))

        self.screen.blit(bg, (0, 0))        
        game_over = self.big_font.render('GAME PAUSED', True, WHITE)
        label_size = self.big_font.size('GAME PAUSED')
        self.screen.blit(game_over, ((win_size_x - label_size[0]) // 2, (win_size_y - label_size[1]) // 2))

class SettingsWindow:
    def __init__(self):
        self.width = 480   # equal to MainWindow default dimensions
        self.height = 600
        self.screen = pg.display.set_mode((self.width, self.height))
        self.cap_font = pg.font.SysFont('tahoma', 25, bold=True)
        self.lbl_font = pg.font.SysFont('verdana', 18, bold=True)
        self.text_font = pg.font.SysFont('verdana', 12)

    def show_settings(self):
        pg.display.set_caption('Tetris / Settings')
        self.screen.fill(GREY5)

        caption = self.cap_font.render('Settings', True, WHITE, GREY5)
        caption_size = self.cap_font.size('Settings')
        self.screen.blit(caption, ((self.width - caption_size[0]) // 2, 15))

    def create_set_menu_buttons(self):
        win_size_x, win_size_y = self.screen.get_size()
        btnLevel = Button(155, 30, DARKGREY, 'Starting level')
        btnWidth = Button(155, 30, DARKGREY, 'Field width')
        btnTiles = Button(155, 30, DARKGREY, 'Change tile set')
        btnShowNext = Button(155, 30, DARKGREY, 'Show next piece')
        btnIncreaseSpeed = Button(155, 30, DARKGREY, 'Increase speed')
        btnDone = Button(90, 30, DARKGREY, 'OK')

        if show_next == True:
            text_show_next = 'On'
        else:
            text_show_next = 'Off'

        if increase_speed == True:
            text_inc_speed = 'On'
        else:
            text_inc_speed = 'Off'
            
        lblLevel = self.lbl_font.render(str(game_field.init_level), True, WHITE)
        lblWidth = self.lbl_font.render(str(game_field.width), True, WHITE)
        lblShowNext = self.lbl_font.render(text_show_next, True, WHITE)
        lblIncreaseSpeed = self.lbl_font.render(text_inc_speed, True, WHITE)
        
        lblWidthComment1 = self.text_font.render('Left mouse button to increase,', True, WHITE)
        lblWidthComment2 = self.text_font.render('Right mouse button to decrease', True, WHITE)
        lblIncrSpeedComment1 = self.text_font.render('If On, game speed will increase', True, WHITE)
        lblIncrSpeedComment2 = self.text_font.render('every 25 score points', True, WHITE)

        info_controls = ['Controls:', 'Left and right arrows to move pieces', 'Up and down arrows to rotate', 'Del to drop',
                         'Tab to quick restart game']
        
        for i in range(len(info_controls)):
            lblInfo = self.text_font.render(info_controls[i], True, WHITE)
            self.screen.blit(lblInfo, (30, 370 + i * 17))

        info1 = 'This Tetris is written in Python 3.6 with PyGame'
        info2 = 'in May 2020 during COVID-19 lockdown'
        info_ponies = 'All rights reserved by ponies'
        lblInfoText1 = self.text_font.render(info1, True, WHITE)
        lblInfoText2 = self.text_font.render(info2, True, WHITE)
        lblPonies = window.small_font.render(info_ponies, True, WHITE)
        info1_size = self.text_font.size(info1)
        info2_size = self.text_font.size(info2)
        info_ponies_size = window.small_font.size(info_ponies)

        btnLevel.draw(self.screen, 30, 100)
        btnWidth.draw(self.screen, 30, 140)
        btnTiles.draw(self.screen, 30, 180)
        btnShowNext.draw(self.screen, 30, 220)
        btnIncreaseSpeed.draw(self.screen, 30, 260)
        btnDone.draw(self.screen, 195, 320)
        self.screen.blit(lblLevel, (205, 103))
        self.screen.blit(lblWidth, (205, 143))
        self.screen.blit(lblShowNext, (205, 223))
        self.screen.blit(lblIncreaseSpeed, (205, 263))
        self.screen.blit(lblWidthComment1, (250, 140))
        self.screen.blit(lblWidthComment2, (250, 153))
        self.screen.blit(lblIncrSpeedComment1, (250, 260))
        self.screen.blit(lblIncrSpeedComment2, (250, 273))

        self.screen.blit(piece.blocks.subsurface(0, piece.tileset, 210, 30), (205, 180))

        self.screen.blit(lblInfoText1, ((win_size_x - info1_size[0]) // 2, 500))
        self.screen.blit(lblInfoText2, ((win_size_x - info2_size[0]) // 2, 520))
        self.screen.blit(lblPonies, ((win_size_x - info_ponies_size[0]) // 2, 575))

        return btnLevel, btnWidth, btnTiles, btnShowNext, btnIncreaseSpeed, btnDone

class Button:
    def __init__(self, width, height, color, text, text_color=WHITE, solid=True):
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pg.font.SysFont('verdana', 16, bold=True)

        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        if solid == True:
            self.surface.fill(self.color)
        else:
            pg.draw.rect(self.surface, self.color, (0, 0, self.width, self.height), 1)

    def draw(self, target_surface, target_x, target_y):
        self.label = self.font.render(self.text, True, self.text_color)
        self.label_size = self.font.size(self.text)
        target_surface.blit(self.surface, (target_x, target_y))
        target_surface.blit(self.label, (target_x + (self.width - self.label_size[0]) // 2,
                                         target_y + (self.height - 2 - self.label_size[1]) // 2))

        self.rect = (target_x, target_y, self.width, self.height)  # where to click

    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if (mouse_x in range(self.rect[0], self.rect[0] + self.rect[2])
        and mouse_y in range(self.rect[1], self.rect[1] + self.rect[3])):
            return True

class Field:
    def __init__(self, width, height, init_level=1):  # in cells, not in pixels; level is starting difficulty, customizable
        self.width = width
        self.height = height
        self.init_level = init_level                     # starting difficulty
        self.level = init_level                          # current difficulty (1 to 10)
        self.game_speed = 1000 - (self.level - 1) * 100  # delay in ms between piece moves down
        self.cells = [([1] + [0 for w in range(self.width)] + [1]) for h in range(self.height)] + [[1] * (self.width + 2)]
        self.field = pg.Surface((CELL_SIZE * self.width, CELL_SIZE * self.height))   # field has columns of ones at sides
        pg.time.set_timer(pg.USEREVENT, self.game_speed)                             # for easier checking if a piece
        self.total_rows_deleted = 0                                                  # can be moved; also the bottom row
        self.score = 0                                                               # of ones for the same purpose

    def draw(self):  # vertical line of ones causes shift in x coordinates, so draw everything moved one cell to the left
        for y in range(len(self.cells)):
            for x in range(1, len(self.cells[y])):
                if self.cells[y][x] == 0:
                    color = BLACK
                    pg.draw.rect(self.field, color, ((x - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    block = piece.blocks.subsurface((self.cells[y][x] - 1) * CELL_SIZE, piece.tileset, CELL_SIZE, CELL_SIZE)
                    game_field.field.blit(block, ((x - 1) * CELL_SIZE, y * CELL_SIZE))

    def delete_row(self):
        rows_deleted_now = 0
        for row in range(len(self.cells) - 1):
            if 0 not in self.cells[row]:
                self.cells = ([[1] + [0 for w in range(self.width)] + [1]]) + self.cells[:row] + self.cells[(row + 1):]
                rows_deleted_now += 1
                self.total_rows_deleted += 1

        if rows_deleted_now == 1:
            self.score += 1
        elif rows_deleted_now == 2:
            self.score += 3
        elif rows_deleted_now == 3:
            self.score += 6
        elif rows_deleted_now == 4:
            self.score += 10

        if increase_speed:    # if increase_speed was initially False and at some point during the game was set to True,
            if self.score // 25 + 1 > self.level and self.level < 10:     # level still will be set as (total score // 25)
                self.level += 1                                           # and if level should be higher by more than 1,
                self.game_speed -= 100                                    # it will increase by 1 with every new piece.
                                                                          # maybe do something with it later.
class Piece:
    def __init__(self, x, y, tileset):  # x and y in cells
        self.x = x
        self.y = y
        self.blocks = pg.image.load('blocks.bmp')
        self.tileset = tileset
        self.tileset_changed = False
        self.shape = choice((((0, 1, 0),    # piece color depends on numbers in shape
                              (0, 1, 0),    # line has additional zeros for better rotation
                              (0, 1, 0),
                              (0, 1, 0)),

                             ((2, 2, 2),
                              (0, 2, 0)),

                             ((3, 3),
                              (3, 3)),

                             ((4, 4, 4),
                              (4, 0, 0)),

                             ((5, 5, 5),
                              (0, 0, 5)),

                             ((6, 6, 0),
                              (0, 6, 6)),

                             ((0, 7, 7),
                              (7, 7, 0)),

                             ))

        self.block_color = self.shape[0][0]
        if self.block_color == 0:
            self.block_color = self.shape[0][1]

    def draw(self, field):  # field here is Surface to draw on
        self.block = self.blocks.subsurface((self.block_color - 1) * CELL_SIZE, self.tileset, CELL_SIZE, CELL_SIZE)
        for j in range(len(self.shape)):
            for i in range(len(self.shape[j])):
                if self.shape[j][i] != 0:
                    game_field.field.blit(self.block, ((self.x + i) * CELL_SIZE, (self.y + j) * CELL_SIZE))

    def can_move_left(self):
        for i in range(len(self.shape)):                        # self.x is actually one block to the left of a piece
            if self.shape[i][0] != 0 and game_field.cells[self.y + i][self.x] != 0:
                return False
            elif self.shape[i][0] == 0:
                if self.shape[i][1] != 0 and game_field.cells[self.y + i][self.x + 1] != 0:
                    return False
                elif self.shape[i][1] == 0:
                    if self.shape[i][2] != 0 and game_field.cells[self.y + i][self.x + 2] != 0:
                        return False
        return True

    def can_move_right(self):
        for i in range(len(self.shape)):
            if self.shape[i][-1] != 0 and game_field.cells[self.y + i][self.x + 1 + len(self.shape[i])] != 0:
                return False
            elif self.shape[i][-1] == 0:
                if self.shape[i][-2] != 0 and game_field.cells[self.y + i][self.x + len(self.shape[i])] != 0:
                    return False
                elif self.shape[i][-2] == 0:
                    if self.shape[i][-3] != 0 and game_field.cells[self.y + i][self.x - 1 + len(self.shape[i])] != 0:
                        return False
        return True

    def can_move_down(self):
        for i in range(len(self.shape[-1])):
            if self.shape[-1][i] != 0 and game_field.cells[self.y + len(self.shape)][self.x + 1 + i] != 0:
                return False
            elif self.shape[-1][i] == 0:
                if self.shape[-2][i] != 0 and game_field.cells[self.y + len(self.shape) - 1][self.x + 1 + i] != 0:
                    return False
                elif self.shape[-2][i] == 0:
                    if self.shape[-3][i] != 0 and game_field.cells[self.y + len(self.shape) - 2][self.x + 1 + i] != 0:
                        return False
        return True

    def move(self, direction):
        if direction == 'down':
            self.y += 1
        if direction == 'left':
            if self.can_move_left():
                self.x -= 1
        if direction == 'right':
            if self.can_move_right():
                self.x += 1

    def rotate_ccw(self):
        rotated = []
        if len(self.shape[0]) + self.y <= game_field.height:  # check if piece isn't at the bottom line of the field
            for x in range(len(self.shape[0]) - 1, -1, -1):
                rotated_line = []
                for line in self.shape:
                    rotated_line.append(line[x])
                rotated.append(rotated_line)

        blocked = False
        for y in range(len(rotated)):
            for x in range(len(rotated[y])):
                try:
                    if rotated[y][x] != 0 and game_field.cells[self.y + y][self.x + x + 1] != 0:
                        blocked = True
                except IndexError:  # for 4-line, which is too long for this check (but if check breaks, blocked is also True)
                    blocked = True
        if blocked != True and rotated != []:
            self.shape = tuple(rotated)

    def rotate_cw(self):
        rotated = []
        if len(self.shape[0]) + self.y <= game_field.height:
            for x in range(len(self.shape[0])):
                rotated_line = []
                for line in self.shape:
                    rotated_line.append(line[x])
                rotated_line.reverse()
                rotated.append(rotated_line)

        blocked = False
        for y in range(len(rotated)):
            for x in range(len(rotated[y])):
                try:
                    if rotated[y][x] != 0 and game_field.cells[self.y + y][self.x + x + 1] != 0:
                        blocked = True
                except IndexError:
                    blocked = True
        if blocked != True and rotated != []:
            self.shape = tuple(rotated)

    def drop(self):
        pg.time.set_timer(pg.USEREVENT, 10)

# --------- end defs ------------------------------

game_field = Field(10, 20)
window = MainWindow()
w_settings = SettingsWindow()
pause_button = Button(140, 25, (0, 0, 50), 'Pause game')
piece = Piece(game_field.width // 2 - 1, 0, 0)
next_piece = Piece(game_field.width // 2 - 1, 0, 0)
done = False           # closes setings window
gameover = False
paused = False
game = False           # True when a game is in process, False in menus
game_started = False   # False until first game after launch is started; when True, the Resume button will be active
settings = False       # show settings window
show_next = True       # show next piece
increase_speed = True  # if True, game speed increases when certain score is reached

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            game = True
            game_started = True

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            game = False
            window = MainWindow()   # redraw main window with its normal width
            window.screen = pg.display.set_mode((480, 600))

        if game:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    piece.move('left')
                if event.key == pg.K_RIGHT:
                    piece.move('right')

                if event.key == pg.K_DOWN:
                    piece.rotate_ccw()
                if event.key == pg.K_UP:
                    piece.rotate_cw()

                if event.key == pg.K_DELETE:
                    piece.drop()

                if event.key == pg.K_TAB:   # immediate restart
                    game_field = Field(game_field.width, 20, game_field.init_level)
                    piece = Piece(game_field.width // 2 - 1, 0, piece.tileset)
                    next_piece = Piece(game_field.width // 2 - 1, 0, piece.tileset)

                if event.key == pg.K_PAUSE:
                    paused = not paused
                    if paused:
                        pg.time.set_timer(pg.USEREVENT, 0)
                    else:
                        pg.time.set_timer(pg.USEREVENT, game_field.game_speed)

                if event.key == pg.K_SPACE and gameover:   # restart
                    game_field = Field(10, 20)
                    pg.time.set_timer(pg.USEREVENT, game_field.game_speed)
                    gameover = False

            if event.type == pg.USEREVENT:        # timer event to move piece down
                if piece.can_move_down():
                    piece.move('down')
                else:
                    for j in range(len(piece.shape)):          # redraw field with added piece
                        for i in range(len(piece.shape[j])):
                            if piece.shape[j][i] != 0:
                                game_field.cells[piece.y + j][piece.x + 1 + i] = piece.shape[j][i]
                    game_field.delete_row()                    # check and delete if neccesary
                    if not gameover:
                        pg.time.set_timer(pg.USEREVENT, game_field.game_speed)  # reset timer after drop
                        piece = next_piece
                        next_piece = Piece(game_field.width // 2 - 1, 0, piece.tileset)
                    for color in range(1, 8):
                        if color in game_field.cells[1][1:-1]:
                            gameover = True

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if pause_button.is_clicked():
                    paused = not paused
                    if paused:
                        pg.time.set_timer(pg.USEREVENT, 0)
                    else:
                        pg.time.set_timer(pg.USEREVENT, game_field.game_speed)

            # ------ draw everything --------------------------------

            window.screen.fill(DARKGREY)
            game_field.field.fill(BLACK)   # game_field is class instance, field is Surface
            game_field.draw()
            piece.draw(game_field.field)
            window.screen.blit(game_field.field, (0, 0))

            if show_next:
                window.show_next(next_piece)

            pause_button.draw(window.screen, window.screen.get_size()[0] - 160, window.screen.get_size()[1] - 55)

            if gameover:
                window.game_over()

            if paused:
                window.pause()
                pause_button.text = 'Resume game'
            else:
                pause_button.text = 'Pause game'

            window.show_score()

        elif not game and not settings:       # main menu
            window.show_start_menu()
            btnStart, btnResume, btnSettings, btnQuit = window.create_menu_buttons()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                if btnStart.is_clicked():
                    game_field = Field(game_field.width, 20, game_field.init_level)
                    window = MainWindow()
                    window.screen = pg.display.set_mode((window.game_width + 180, window.game_height))

                    piece = Piece(game_field.width // 2 - 1, 0, piece.tileset)
                    next_piece = Piece(game_field.width // 2 - 1, 0, piece.tileset)
                    game = True
                    game_started = True
                    paused = False   # in case if old game was paused before starting new game

                if btnResume.is_clicked() and game_started:   # resume game if it was already started
                    game = True
                    window = MainWindow()
                    window.screen = pg.display.set_mode((window.game_width + 180, window.game_height))

                if btnQuit.is_clicked():
                    done = True

                if btnSettings.is_clicked():
                    settings = True

        elif settings:
            w_settings.show_settings()
            btnLevel, btnWidth, btnTiles, btnShowNext, btnIncreaseSpeed, btnDone = w_settings.create_set_menu_buttons()
            mouse_x, mouse_y = pg.mouse.get_pos()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                settings = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if btnDone.is_clicked():
                    settings = False

                if btnLevel.is_clicked():
                    game_field.init_level = game_field.init_level % 10 + 1

                if btnWidth.is_clicked():
                    if pg.mouse.get_pressed()[0] and game_field.width < 30:
                        game_field.width += 1
                    if pg.mouse.get_pressed()[2] and game_field.width > 6:
                        game_field.width -= 1
                    game_started = False

                if btnTiles.is_clicked():       # y pixel shift in blocks.png
                    piece.tileset = next_piece.tileset = piece.tileset + 30
                    if piece.tileset == 90:
                        piece.tileset = next_piece.tileset = 0
                    piece.tileset_changed = True

                if btnShowNext.is_clicked():         # show next piece
                    show_next = not show_next

                if btnIncreaseSpeed.is_clicked():    # if True, game speed increases when certain score is reached
                    increase_speed = not increase_speed

    pg.display.flip()
