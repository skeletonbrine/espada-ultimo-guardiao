import pygame
import random

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Inicialização pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Espada do Último Guardião")
font = pygame.font.SysFont("serif", 24)
clock = pygame.time.Clock()

# Funções utilitárias
def draw_text(surface, text, pos, font, color=WHITE):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        surface.blit(rendered, (pos[0], pos[1] + i * 30))

def draw_hud(screen, font, player, enemy):
    pygame.draw.rect(screen, (40, 40, 60), (30, 20, 740, 100), border_radius=12)
    pygame.draw.rect(screen, (100, 100, 120), (30, 20, 740, 100), 2, border_radius=12)
    alignment_colors = {"light": (180, 200, 255), "dark": (120, 0, 120), "neutral": (120, 120, 120)}
    pygame.draw.rect(screen, alignment_colors.get(player.alignment, (255, 255, 255)), (40, 30, 30, 30), border_radius=6)
    pygame.draw.rect(screen, (255, 255, 255), (40, 30, 30, 30), 2, border_radius=6)
    draw_text(screen, f"{player.name} - HP: {player.current_hp}/{player.max_hp} | ATK: {player.atk} | DEF: {player.defense}", (90, 30), font)
    draw_text(screen, f"{enemy['name']} - HP: {enemy['hp']}/{enemy['max_hp']} | ATK: {enemy['atk']} | DEF: {enemy['def']}", (90, 60), font)

# Classe base
class Scene:
    def render(self, screen): raise NotImplementedError
    def handle_event(self, event, game): raise NotImplementedError

# Player
class Player:
    def __init__(self, name):
        self.name = name
        self.alignment = "neutral"
        self.max_hp = 100
        self.current_hp = 100
        self.atk = 15
        self.defense = 5

    def change_alignment(self, new_alignment):
        self.alignment = new_alignment

# Espada
class Sword:
    def __init__(self):
        self.name = "Espada do Último Guardião"
        self.spirit = "neutro"

    def speak(self, alignment):
        if alignment == "light":
            return "Lembre-se: o verdadeiro poder é o sacrifício."
        elif alignment == "dark":
            return "Poder absoluto exige mãos firmes e sem culpa."
        elif alignment == "neutral":
            return "Você ainda está encontrando seu caminho."
        return "..."

# Cenas do jogo
class IntroScene(Scene):
    def __init__(self, font):
        self.font = font

    def render(self, screen):
        draw_text(screen,
                  "Diante de você está uma espada cravada em uma pedra ancestral.\n"
                  "Você sente que este momento definirá seu destino.",
                  (60, 80), self.font)
        draw_text(screen, "1. Empunhar a espada.", (70, 320), self.font)
        draw_text(screen, "2. Ignorar e seguir seu caminho.", (70, 380), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game.change_scene("accepted")
            elif event.key == pygame.K_2:
                game.change_scene("ignored")

class AcceptedScene(Scene):
    def __init__(self, font):
        self.font = font

    def render(self, screen):
        draw_text(screen,
                  "Ao pegar a espada, uma voz antiga ressoa em sua mente:\n"
                  "\"Guardião... seu destino começa agora.\"",
                  (60, 80), self.font)
        draw_text(screen, "1. Escutar a voz da espada.", (70, 320), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            game.change_scene("alignment_choice")

class IgnoredScene(Scene):
    def __init__(self, font):
        self.font = font

    def render(self, screen):
        draw_text(screen,
                  "Você vira as costas para a espada.\n"
                  "O destino, no entanto, não costuma aceitar silêncio.",
                  (60, 80), self.font)
        draw_text(screen, "1. Continuar seu caminho...", (70, 320), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            game.change_scene("village")

class AlignmentChoiceScene(Scene):
    def __init__(self, font):
        self.font = font

    def render(self, screen):
        draw_text(screen,
                  "Ao empunhar a Espada do Último Guardião,\n"
                  "uma torrente de emoções transborda em sua alma...\n"
                  "O que você sente?",
                  (60, 80), self.font)
        draw_text(screen, "1. Ser esperança para os que não têm mais fé.", (70, 320), self.font)
        draw_text(screen, "2. Ter poder a qualquer custo.", (70, 380), self.font)
        draw_text(screen, "3. Criar um legado — nem herói, nem vilão.", (70, 440), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game.player.change_alignment("light")
                game.change_scene("village")
            elif event.key == pygame.K_2:
                game.player.change_alignment("dark")
                game.change_scene("village")
            elif event.key == pygame.K_3:
                game.player.change_scene("neutral")
                game.change_scene("village")
class VillageScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        self.phase = 0

    def render(self, screen):
        if self.phase == 0:
            draw_text(screen,
                "Você chega à vila. Um ancião corre até você:\n"
                "\"Guardião! Bandidos estão vindo, ajude-nos!\"",
                (60, 80), self.font)
            draw_text(screen, "1. Lutar contra os bandidos.", (70, 320), self.font)
            draw_text(screen, "2. Fugir da vila.", (70, 380), self.font)
        else:
            draw_text(screen, "Você parte para enfrentar o inimigo!", (60, 150), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 0:
                if event.key == pygame.K_1:
                    game.change_scene("combat")
                elif event.key == pygame.K_2:
                    game.change_scene("final")

class CombatScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        self.reset_combat()

    def reset_combat(self):
        self.enemy = {
            'name': 'Bandido',
            'hp': 80,
            'max_hp': 80,
            'atk': 12,
            'def': 3
        }
        self.phase = 'player_turn'
        self.message = ""
        self.defending = False

    def render(self, screen):
        screen.fill((15, 15, 30))
        draw_hud(screen, self.font, self.player, self.enemy)
        draw_text(screen, self.message, (50, 150), self.font)

        if self.phase == 'player_turn':
            draw_text(screen, "1. Atacar | 2. Ataque Especial | 3. Defender", (50, 300), self.font)
        elif self.phase == 'end':
            draw_text(screen, "Pressione qualquer tecla para continuar...", (50, 350), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 'player_turn':
                if event.key == pygame.K_1:
                    damage = max(self.player.atk - self.enemy['def'], 1)
                    self.enemy['hp'] -= damage
                    self.message = f"Você causou {damage} de dano!"
                    self.phase = 'enemy_turn' if self.enemy['hp'] > 0 else 'end'
                elif event.key == pygame.K_2:
                    bonus = int(self.enemy['hp'] * 0.25) if self.player.alignment == "light" else int((self.enemy['max_hp'] - self.enemy['hp']) * 0.25)
                    damage = max((self.player.atk + bonus) - self.enemy['def'], 1)
                    self.enemy['hp'] -= damage
                    self.message = f"Ataque especial! {damage} de dano!"
                    self.phase = 'enemy_turn' if self.enemy['hp'] > 0 else 'end'
                elif event.key == pygame.K_3:
                    self.defending = True
                    self.message = "Você se prepara para defender!"
                    self.phase = 'enemy_turn'
            elif self.phase == 'enemy_turn':
                damage = self.enemy['atk']
                if self.defending:
                    self.message = f"O {self.enemy['name']} ataca, mas você defende o golpe!"
                    damage = 0
                else:
                    self.message = f"O {self.enemy['name']} ataca e causa {damage} de dano!"
                self.player.current_hp -= damage
                self.phase = 'player_turn'
                self.defending = False
            elif self.phase == 'end':
                game.change_scene("post_combat")

class PostCombatScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        if player.alignment == "dark":
            self.player.atk += 5
            self.message = "Um homem misterioso te dá uma adaga negra. [+5 ATK]"
        elif player.alignment == "light":
            self.player.defense += 2
            self.message = "Uma criança te dá um anel da esperança. [+2 DEF]"
        else:
            self.message = "Você observa os escombros. Tudo ainda é incerto."

    def render(self, screen):
        draw_text(screen, self.message, (60, 100), self.font)
        draw_text(screen, "Pressione qualquer tecla para seguir até o castelo.", (60, 400), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            game.change_scene("king")

class KingScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        self.phase = 0

    def render(self, screen):
        if self.phase == 0:
            draw_text(screen,
                "Você é levado até o rei. Ele diz:\n"
                "\"Um orc ancestral ameaça nossas terras. Você aceita o desafio?\"",
                (60, 80), self.font)
            draw_text(screen, "1. Aceitar o desafio", (70, 320), self.font)
        else:
            draw_text(screen, "Você segue rumo à floresta sombria...", (60, 100), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 0 and event.key == pygame.K_1:
                self.phase = 1
            elif self.phase == 1:
                game.change_scene("forest")
                
class ForestCrossingScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        self.phase = 0
        self.selection = None
        self.message = ""

    def render(self, screen):
        screen.fill((15, 25, 15))
        if self.phase == 0:
            draw_text(screen,
                "A caminho do covil do orc, você cruza uma floresta antiga.\n"
                "Há algo místico ali. Você encontra um altar de pedras\n"
                "com três símbolos brilhando à sua frente...",
                (60, 60), self.font)
            draw_text(screen, "Pressione qualquer tecla para se aproximar.", (60, 340), self.font)
        elif self.phase == 1:
            draw_text(screen, "Qual símbolo você toca?", (60, 80), self.font)
            draw_text(screen, "1. A folha sagrada (cura total)", (70, 140), self.font)
            draw_text(screen, "2. A lâmina ardente (+3 ATK)", (70, 200), self.font)
            draw_text(screen, "3. A rocha eterna (+3 DEF)", (70, 260), self.font)
        elif self.phase == 2:
            draw_text(screen, self.message, (60, 100), self.font)
            draw_text(screen, "Pressione qualquer tecla para continuar...", (60, 400), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 0:
                self.phase = 1
            elif self.phase == 1:
                if event.key == pygame.K_1:
                    self.player.current_hp = self.player.max_hp
                    self.message = "Você sente sua energia se restaurar completamente."
                elif event.key == pygame.K_2:
                    self.player.atk += 3
                    self.message = "Sua lâmina brilha em chamas. [+3 ATK]"
                elif event.key == pygame.K_3:
                    self.player.defense += 3
                    self.message = "Sua pele se endurece como pedra. [+3 DEF]"
                self.phase = 2
            elif self.phase == 2:
                game.change_scene("final_combat")
                

class FinalCombatScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        self.reset_combat()

    def reset_combat(self):
        self.enemy = {
            'name': 'Orc Bravio',
            'hp': 150,
            'max_hp': 150,
            'atk': 20,
            'def': 5
        }
        self.phase = 'player_turn'
        self.message = ""
        self.defending = False

    def render(self, screen):
        screen.fill((10, 10, 25))
        draw_hud(screen, self.font, self.player, self.enemy)
        draw_text(screen, self.message, (50, 150), self.font)

        if self.phase == 'player_turn':
            draw_text(screen, "1. Atacar | 2. Ataque Especial | 3. Defender", (50, 300), self.font)
        elif self.phase == 'end':
            draw_text(screen, "Pressione qualquer tecla para ver o desfecho...", (50, 350), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 'player_turn':
                if event.key == pygame.K_1:
                    damage = max(self.player.atk - self.enemy['def'], 1)
                    self.enemy['hp'] -= damage
                    self.message = f"Você golpeia o orc e causa {damage}!"
                    self.phase = 'enemy_turn' if self.enemy['hp'] > 0 else 'end'
                elif event.key == pygame.K_2:
                    bonus = int(self.enemy['hp'] * 0.3) if self.player.alignment == "light" else int((self.enemy['max_hp'] - self.enemy['hp']) * 0.3)
                    damage = max((self.player.atk + bonus) - self.enemy['def'], 1)
                    self.enemy['hp'] -= damage
                    self.message = f"Ataque especial devastador! {damage} de dano!"
                    self.phase = 'enemy_turn' if self.enemy['hp'] > 0 else 'end'
                elif event.key == pygame.K_3:
                    self.defending = True
                    self.message = "Você se coloca em guarda!"
                    self.phase = 'enemy_turn'
            elif self.phase == 'enemy_turn':
                damage = self.enemy['atk']
                if self.defending:
                    self.message = f"O {self.enemy['name']} ataca, mas você se defende!"
                    damage = 0
                else:
                    self.message = f"O orc ataca com fúria! Causa {damage} de dano!"
                self.player.current_hp -= damage
                self.defending = False
                self.phase = 'player_turn'
            elif self.phase == 'end':
                game.change_scene("final")

class FinalScene(Scene):
    def __init__(self, font, player):
        self.font = font
        self.player = player
        if player.alignment == "light":
            self.message = (
                "O orc cai derrotado, e a paz retorna às terras.\n"
                "Você é a luz que afastou as trevas. Seu nome será lembrado como lenda."
            )
        elif player.alignment == "dark":
            self.message = (
                "O orc cai. Você ergue sua espada sobre os escombros...\n"
                "Não como herói, mas como conquistador. O mundo agora é seu."
            )
        else:
            self.message = (
                "Nem herói, nem vilão. Você enfrentou o destino e venceu.\n"
                "E por isso, será lembrado como aquele que escolheu seu próprio caminho."
            )

    def render(self, screen):
        screen.fill((10, 10, 10))
        draw_text(screen, self.message, (60, 100), self.font)
        draw_text(screen, "Pressione qualquer tecla para sair...", (60, 400), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            exit()

# Game controller
class Game:
    def __init__(self):
        self.player = Player("Kael")
        self.sword = Sword()
        self.font = font
        self.current_scene = IntroScene(font)

    def change_scene(self, name):
        scenes = {
        "intro": IntroScene(self.font),
        "accepted": AcceptedScene(self.font),
        "ignored": IgnoredScene(self.font),
        "alignment_choice": AlignmentChoiceScene(self.font),
        "village": VillageScene(self.font, self.player),
        "combat": CombatScene(self.font, self.player),
        "post_combat": PostCombatScene(self.font, self.player),
        "king": KingScene(self.font, self.player),
        "forest": ForestCrossingScene(self.font, self.player),
        "final_combat": FinalCombatScene(self.font, self.player),
        "final": FinalScene(self.font, self.player)
    }
        self.current_scene = scenes[name]


# Loop principal
game = Game()
running = True

while running:
    screen.fill((20, 20, 20))
    pygame.draw.rect(screen, {"light": (180, 200, 255), "dark": (60, 0, 100), "neutral": (120, 120, 120)}[game.player.alignment], (20, 20, 40, 40))
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 40, 40), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.current_scene.handle_event(event, game)

    game.current_scene.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
