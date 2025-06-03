import pygame
import sys
import random

pygame.init()
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)
GREEN = (0, 150, 0)
RED = (180, 0, 0)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)

# -------------- Constants ----------------
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)
GREEN = (0, 150, 0)
RED = (180, 0, 0)
BLUE = (30, 144, 255)

FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monetary Policy Simulator")

# -------------- Game State ----------------
rounds = 5
current_round = 1
interest_rate = 2.0
money_supply = 100
history = []

# -------------- Simulation Function ----------------
def simulate_economy(interest, money):
    inflation = 1.5 + (money - 100) * 0.05 - interest * 0.4 + random.uniform(-0.5, 0.5)
    unemployment = 6.0 - (money - 100) * 0.03 + interest * 0.6 + random.uniform(-0.5, 0.5)
    growth = 2.0 + (money - 100) * 0.04 - interest * 0.3 + random.uniform(-0.3, 0.3)

    inflation = max(0.0, round(inflation, 2))
    unemployment = max(0.0, round(unemployment, 2))
    growth = round(growth, 2)

    return inflation, unemployment, growth

# -------------- UI Functions ----------------
def draw_slider(x, y, label, value, min_val, max_val):
    pygame.draw.rect(screen, GRAY, (x, y + 30, 200, 5))
    pos = int((value - min_val) / (max_val - min_val) * 200)
    pygame.draw.circle(screen, BLUE, (x + pos, y + 32), 10)
    text = FONT.render(f"{label}: {value:.2f}", True, DARK_GRAY)
    screen.blit(text, (x, y))

def draw_results(round_num, inf, unemp, gdp):
    y = 350
    screen.blit(FONT.render(f"Quarter {round_num} Results:", True, DARK_GRAY), (100, y))
    screen.blit(FONT.render(f"Inflation Rate: {inf:.2f}%", True, RED), (120, y + 40))
    screen.blit(FONT.render(f"Unemployment Rate: {unemp:.2f}%", True, BLUE), (120, y + 80))
    screen.blit(FONT.render(f"GDP Growth: {gdp:.2f}%", True, GREEN), (120, y + 120))

# -------------- Main Loop ----------------
def game_loop():
    global current_round, interest_rate, money_supply
    clock = pygame.time.Clock()
    dragging_interest = False
    dragging_money = False
    last_result = None
    game_over = False

    while True:
        screen.fill(WHITE)
        if current_round <= rounds:
            title = BIG_FONT.render(f"Quarter {current_round} - Set Your Policy", True, DARK_GRAY)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

            draw_slider(100, 120, "Interest Rate (%)", interest_rate, 0.0, 10.0)
            draw_slider(100, 220, "Money Supply", money_supply, 80, 120)

            btn = pygame.Rect(400, 260, 200, 50)
            pygame.draw.rect(screen, GREEN, btn)
            screen.blit(FONT.render("Submit Policy", True, WHITE), (btn.x + 40, btn.y + 10))

            if last_result:
                draw_results(current_round - 1, *last_result)

        else:
            game_over = True
            screen.blit(BIG_FONT.render("Simulation Complete", True, DARK_GRAY), (300, 50))
            y = 130
            score = 0
            for r, data in enumerate(history, 1):
                inf, unemp, gdp = data
                score += max(0, 100 - abs(inf - 2) * 10 - abs(unemp - 5) * 10)
                screen.blit(FONT.render(f"Q{r}: Inflation={inf:.2f}%  Unemployment={unemp:.2f}%  GDP={gdp:.2f}%", True, BLACK), (100, y))
                y += 40
            final = FONT.render(f"Final Policy Score: {int(score/rounds)} / 100", True, BLUE)
            screen.blit(final, (100, y + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over:
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 100 <= mx <= 300:
                    if 150 <= my <= 170:
                        dragging_interest = True
                    elif 250 <= my <= 270:
                        dragging_money = True
                elif 400 <= mx <= 600 and 260 <= my <= 310:
                    # Submit policy
                    result = simulate_economy(interest_rate, money_supply)
                    history.append(result)
                    last_result = result
                    current_round += 1

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_interest = dragging_money = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if dragging_interest:
                    pos = max(0, min(mx - 100, 200))
                    interest_rate = round(0 + (pos / 200) * 10.0, 2)
                elif dragging_money:
                    pos = max(0, min(mx - 100, 200))
                    money_supply = round(80 + (pos / 200) * 40, 2)

        clock.tick(30)

if __name__ == "__main__":
    game_loop()
