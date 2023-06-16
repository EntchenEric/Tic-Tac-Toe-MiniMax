import pygame
import copy

pygame.init()

# colors
GRAY = (129, 133, 137)
DARK_GRAY = (90, 90, 90)
RED = (220, 20, 60)

GAME_ACTIVE = True
FPS = 60

PADDING = 50

SCREEN_RES = (800, 800)

screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()


BLOCK_HEIGHT = (SCREEN_RES[0]-(PADDING*2))/3
BLOCK_WIDTH = (SCREEN_RES[1]-(PADDING*2))/3

SECTIONS = [
    ((SCREEN_RES[0] - PADDING/2)/3, (SCREEN_RES[1] - PADDING/2)/3),
    (((SCREEN_RES[0] - PADDING/2)/3) * 2, (SCREEN_RES[1] - PADDING/2)/3),
    (((SCREEN_RES[0] - PADDING/2)/3) * 3, (SCREEN_RES[1] - PADDING/2)/3),
    ((SCREEN_RES[0] - PADDING/2)/3, (SCREEN_RES[1] - PADDING/2)/3 * 2),
    (((SCREEN_RES[0] - PADDING/2)/3) * 2, (SCREEN_RES[1] - PADDING/2)/3 * 2),
    (((SCREEN_RES[0] - PADDING/2)/3) * 3, (SCREEN_RES[1] - PADDING/2)/3 * 2),
    ((SCREEN_RES[0] - PADDING/2)/3, (SCREEN_RES[1] - PADDING/2)/3 * 3),
    (((SCREEN_RES[0] - PADDING/2)/3) * 2, (SCREEN_RES[1] - PADDING/2)/3 * 3),
    (((SCREEN_RES[0] - PADDING/2)/3) * 3, (SCREEN_RES[1] - PADDING/2)/3 * 3),
]

# 0 = FREE, 1 = PLAYER, 2 = BOT
BOARD = [
    0, 0, 0,
    0, 0, 0,
    0, 0, 0
]

CurrentTurn = 1


def getClickSection(pos: tuple):
    for sectionid, section in enumerate(SECTIONS):
        if (pos[0] < section[0] and pos[1] < section[1]):
            return sectionid
    return None


def checkIfGameOver(board: list):
    for blockid, block in enumerate(board):
        if block != 0:
            if blockid < 6:
                if (blockid % 3 == 0):
                    if (block == board[blockid + 1] and block == board[blockid + 2]):
                        return block
            if blockid < 3:
                if (block == board[blockid + 3] and block == board[blockid + 6]):
                    return block
            if blockid in [0, 2]:
                if (block == board[blockid + (4 - blockid)] and block == board[blockid + (8 - blockid*2)]):
                    return block
    return 0

def getWinningBlocks(board: list):
    for blockid, block in enumerate(board):
        if block != 0:
            if blockid < 6:
                if (blockid % 3 == 0):
                    if (block == board[blockid + 1] and block == board[blockid + 2]):
                        return (blockid, blockid + 1, blockid + 2)
            if blockid < 3:
                if (block == board[blockid + 3] and block == board[blockid + 6]):
                    return (blockid, blockid + 3, blockid + 6)
            if blockid in [0, 2]:
                if (block == board[blockid + (4 - blockid)] and block == board[blockid + (8 - blockid * 2)]):
                    return (blockid, blockid + (4 - blockid), blockid + (8 - blockid * 2))
    return 0


def drawX(pos: tuple, screen):
    pygame.draw.line(surface=screen, color=DARK_GRAY, start_pos=(pos[0] - (BLOCK_WIDTH/10), pos[1] - (
        BLOCK_HEIGHT/10)), end_pos=(pos[0] - BLOCK_WIDTH, pos[1] - BLOCK_HEIGHT), width=5)
    pygame.draw.line(surface=screen, color=DARK_GRAY, start_pos=(pos[0] - (BLOCK_WIDTH/10), pos[1] - (
        BLOCK_HEIGHT)), end_pos=(pos[0] - BLOCK_WIDTH, pos[1] - BLOCK_HEIGHT/10), width=5)

def drawO(pos: tuple, screen):
    pygame.draw.circle(surface=screen, color=DARK_GRAY, center=(
        pos[0] - BLOCK_WIDTH/2, pos[1] - BLOCK_HEIGHT/2), radius=SCREEN_RES[0]/9, width=5)


while GAME_ACTIVE:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_ACTIVE = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            clickedSection = getClickSection(mousePos)
            if (clickedSection != None and BOARD[clickedSection] == 0):
                BOARD[clickedSection] = CurrentTurn
                if(not checkIfGameOver(BOARD) and (0 in BOARD)):
                    if(CurrentTurn == 1): CurrentTurn = 2
                    else: CurrentTurn = 1


    for blockid, symbol in enumerate(BOARD):
        if symbol == 1:
            drawX(SECTIONS[blockid], screen)
        if symbol == 2:
            drawO(SECTIONS[blockid], screen)

    for x in range(2):
        STARTWIDTH = ((SCREEN_RES[0] - int(PADDING / 2)) / 3) * (x+1)
        STARTHEIGHT = int(PADDING / 2)
        ENDWIDTH = ((SCREEN_RES[0] - int(PADDING / 2)) / 3) * (x+1)
        ENDHEIGHT = SCREEN_RES[1] - int(PADDING / 2)
        pygame.draw.line(color=DARK_GRAY, surface=screen, width=3, start_pos=(
            (STARTWIDTH, STARTHEIGHT)), end_pos=(ENDWIDTH, ENDHEIGHT))

        STARTWIDTH = int(PADDING / 2)
        STARTHEIGHT = ((SCREEN_RES[0] - int(PADDING / 2)) / 3) * (x+1)
        ENDWIDTH = SCREEN_RES[1] - int(PADDING / 2)
        ENDHEIGHT = ((SCREEN_RES[0] - int(PADDING / 2)) / 3) * (x+1)
        pygame.draw.line(color=DARK_GRAY, surface=screen, width=3, start_pos=(
            (STARTWIDTH, STARTHEIGHT)), end_pos=(ENDWIDTH, ENDHEIGHT))

    if(checkIfGameOver(BOARD)):
        winningBlocks = getWinningBlocks(BOARD)
        startPos = (SECTIONS[winningBlocks[0]][0] - BLOCK_WIDTH / 2, SECTIONS[winningBlocks[0]][1] - BLOCK_HEIGHT / 2)
        endPos = (SECTIONS[winningBlocks[2]][0] - BLOCK_WIDTH / 2, SECTIONS[winningBlocks[2]][1] - BLOCK_HEIGHT / 2)
        pygame.draw.line(surface=screen, color=RED, start_pos=startPos, end_pos=endPos, width=10)

    # Fenster Aktualisieren
    pygame.display.flip()
    clock.tick(FPS)
