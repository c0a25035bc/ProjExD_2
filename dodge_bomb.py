import os
import sys
import random
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """Rect が画面に収まっているかを判定する

    Parameters
    ----------
    rct : pg.Rect
        範囲判定対象の Rect

    Returns
    ----------
    tuple[bool, bool]
        (横方向の判定結果, 縦方向の判定結果) のタプル（内側なら True で外側なら False）
    """

    horizontal = rct.left >= 0 and rct.right <= WIDTH
    vertical = rct.top >= 0 and rct.bottom <= HEIGHT
    return horizontal, vertical


def gameover(screen: pg.Surface) -> None:
    """ゲームオーバー画面を表示する

    Parameters
    ----------
    screen : pg.Surface
        画面判定対象の Surface
    """

    # 黒い矩形 Surface (ゲームオーバー画面) を作成
    gameover_img = pg.Surface((WIDTH, HEIGHT))

    # ゲームオーバー画面の透明度
    gameover_img.set_alpha(200)

    # 白文字の Game Over をゲームオーバー画面に blit
    text_font = pg.font.Font(None, 80)
    text_surface = text_font.render("Game Over", True, (255, 255, 255))
    gameover_img.blit(text_surface, [405, 265])

    # こうかとんの画像をゲームオーバー画面に blit
    kk_img = pg.image.load("fig/8.png")
    gameover_img.blit(kk_img, [730, 260])
    gameover_img.blit(kk_img, [340, 260])

    # ゲームオーバー画面をスクリーンに blit
    screen.blit(gameover_img, [0, 0])

    # ちょっと待つ
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            print("GAME OVER")
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, (dx, dy) in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += dx
                sum_mv[1] += dy
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            sum_mv[0] *= -1
            sum_mv[1] *= -1
            kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        bb_rct_check = check_bound(bb_rct)
        if not bb_rct_check[0]:
            vx = -vx
        if not bb_rct_check[1]:
            vy = -vy
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
