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
pygame.display.set_caption("A Espada do Último Guardião")
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
def draw_background(screen, bg):
    if bg:
        screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
    else:
        screen.fill((0, 0, 0))
def draw_hud_box(screen, rect, font, text):
    hud_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, (20, 20, 40, 220), hud_surface.get_rect(), border_radius=12)
    screen.blit(hud_surface, rect.topleft)
    draw_text(screen, text, (rect.x + 20, rect.y + 20), font)


# classe "base" a se seguir para todas as cenas
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

# Espada (não foi implementado)
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

class MainMenuScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.title_font = pygame.font.Font(None, 72)  # Título maior
        self.background = background
        self.input_text = ""
        self.message = "Digite seu nome e pressione ENTER:"

    def render(self, screen):
        # Desenha o background, se houver
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))
    
        # Título com sombra
        title_text = "A Espada do Último Guardião"
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))   # texto branco
        shadow_surface = self.title_font.render(title_text, True, (200, 50, 50))     # sombra escura
    
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 60))
        shadow_rect = title_rect.copy()
        shadow_rect.move_ip(3, 3)  # desloca a sombra um pouco pra direita e pra baixo
    
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(title_surface, title_rect)
    
        # Caixa de HUD para input do nome
        hud_rect = pygame.Rect(50, 120, WIDTH - 100, 160)
        text = self.message + "\n\n" + self.input_text + "|"
        draw_hud_box(screen, hud_rect, self.font, text)


    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.player = Player(self.input_text if self.input_text else "Kael")
                game.change_scene("intro")
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 20 and event.unicode.isprintable():
                    self.input_text += event.unicode


class IntroScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.background = background

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 300)
        text = (
            "Diante de você está uma espada cravada em uma pedra ancestral.\n"
            "Você sente que este momento definirá seu destino.\n\n"
            "1. Empunhar a espada.\n"
            "2. Ignorar e seguir seu caminho."
        )
        draw_hud_box(screen, hud_rect, self.font, text)



    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game.change_scene("accepted")
            elif event.key == pygame.K_2:
                game.change_scene("ignored")

class AcceptedScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.background = background

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 250)
        text = (
            "Ao pegar a espada, uma voz antiga ressoa em sua mente:\n"
            "\"Guardião... seu destino começa agora.\"\n\n"
            "1. Escutar a voz da espada."
        )
        draw_hud_box(screen, hud_rect, self.font, text)


    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            game.change_scene("alignment_choice")

class IgnoredScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.background = background

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 300)
        text = (
            "Você vira as costas para a espada.\n"
            "Você sente um peso... como se tivesse perdido algo importante.\n"
            "O destino, no entanto, não costuma aceitar silêncio.\n\n"
            "1. Continuar seu caminho..."
        )
        draw_hud_box(screen, hud_rect, self.font, text)



    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            game.player.atk -= 14  # Penalidade por ignorar a espada
            if game.player.atk < 1:
                game.player.atk = 1  # Evita que fique com ataque zero ou negativo
            game.change_scene("village")


class AlignmentChoiceScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.background = background

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 350)
        text = (
            "Ao empunhar a Espada do Último Guardião,\n"
            "uma torrente de emoções transborda em sua alma...\n"
            "O que você sente?\n\n"
            "1. Ser esperança para os que não têm mais fé.\n"
            "2. Ter poder a qualquer custo.\n"
            "3. Criar um legado — nem herói, nem vilão."
        )
        draw_hud_box(screen, hud_rect, self.font, text)



    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game.player.change_alignment("light")
                game.change_scene("village")
            elif event.key == pygame.K_2:
                game.player.change_alignment("dark")
                game.change_scene("village")
            elif event.key == pygame.K_3:
                game.player.change_alignment("neutral")
                game.change_scene("village")

class VillageScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
        self.player = player
        self.phase = 0

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 300)
        if self.phase == 0:
            text = (
                "Você chega à vila. Um ancião corre até você:\n"
                "\"Guardião! Bandidos estão vindo, ajude-nos!\"\n\n"
                "1. Lutar contra os bandidos.\n"
                "2. Fugir da vila."
            )
        else:
            text = "Você parte para enfrentá-los! O mais forte deles lhe desafia para batalhar"

        draw_hud_box(screen, hud_rect, self.font, text)


    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 0:
                if event.key == pygame.K_1:
                    game.change_scene("combat")
                elif event.key == pygame.K_2:
                    game.change_scene("king")

class CombatScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
        self.player = player
        self.reset_combat()

    def reset_combat(self):
        self.enemy = {
            'name': 'Bandido Chefe',
            'hp': 80,
            'max_hp': 80,
            'atk': 12,
            'def': 3
        }
        self.phase = 'player_turn'
        self.message = ""
        self.defending = False

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((15, 15, 30))

        draw_hud(screen, self.font, self.player, self.enemy)

        hud_rect = pygame.Rect(40, 140, WIDTH - 80, 200)
        draw_hud_box(screen, hud_rect, self.font, self.message)

        if self.phase == 'player_turn':
            draw_text(screen, "1. Atacar | 2. Ataque Especial | 3. Defender", (50, 340), self.font)
        elif self.phase == 'end':
            draw_text(screen, "Pressione qualquer tecla para continuar...", (50, 390), self.font)
        elif self.phase == 'defeat':
            draw_text(screen, "Pressione qualquer tecla para ver seu destino...", (50, 440), self.font)


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
                # Calcula chance de ataque especial
                base_chance = 33.3
                defense_modifier = self.player.defense * 1.5  # 1.5% a menos por ponto de defesa
                final_chance = max(5, base_chance - defense_modifier)
                
                if random.random() * 100 < final_chance:
                    # Ataque especial do inimigo
                    damage = self.enemy['atk'] + 7  # ou outro bônus
                    attack_type = "especial"
                else:
                    damage = self.enemy['atk']
                    attack_type = "normal"
                
                if self.defending:
                    self.message = f"O {self.enemy['name']} tentou um ataque {attack_type}, mas você se defendeu!"
                    damage = 0
                else:
                    self.message = f"O {self.enemy['name']} usa um ataque {attack_type} e causa {damage} de dano!"

            
                self.player.current_hp -= damage
                self.defending = False
            
                if self.player.current_hp <= 0:
                    self.player.current_hp = 0  # Para evitar vida negativa
                    self.message += "\nVocê foi derrotado..."
                    self.phase = 'defeat'
                else:
                    self.phase = 'player_turn'
            elif self.phase == 'end':
                game.change_scene("post_combat")   
            elif self.phase == 'defeat':
                game.change_scene("death")

class PostCombatScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
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
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 200)
        draw_hud_box(screen, hud_rect, self.font, self.message)

        draw_text(screen, "Pressione qualquer tecla para seguir até o castelo.", (60, 280), self.font)

 

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            game.change_scene("king")

class KingScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
        self.player = player
        self.phase = 0

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 250)
        if self.phase == 0:
            text = (
                "Você é levado até o rei. Ele diz:\n"
                "\"Um orc ancestral ameaça nossas terras. Você aceita o desafio?\"\n\n"
                "1. Aceitar o desafio"
            )
        else:
            text = "Você segue rumo à floresta sombria..."

        draw_hud_box(screen, hud_rect, self.font, text)


    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if self.phase == 0 and event.key == pygame.K_1:
                self.phase = 1
            elif self.phase == 1:
                game.change_scene("forest")
                
class ForestCrossingScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
        self.player = player
        self.phase = 0
        self.message = ""

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((15, 25, 15))

        hud_rect = pygame.Rect(50, 50, WIDTH - 100, 300)

        if self.phase == 0:
            text = (
                "A caminho do covil do orc, você cruza uma floresta antiga.\n"
                "Há algo místico ali. Você encontra um altar de pedras\n"
                "com três símbolos brilhando à sua frente...\n\n"
                "Pressione qualquer tecla para se aproximar."
            )
        elif self.phase == 1:
            text = (
                "Qual símbolo você toca?\n\n"
                "1. A folha sagrada (cura total)\n"
                "2. A lâmina ardente (+3 ATK)\n"
                "3. A rocha eterna (+3 DEF)"
            )
        else:
            text = self.message + "\n\nPressione qualquer tecla para continuar..."

        draw_hud_box(screen, hud_rect, self.font, text)


            
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
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
        self.player = player
        self.reset_combat()

    def reset_combat(self):
        self.enemy = {
            'name': 'Orc Bravio',
            'hp': 120,
            'max_hp': 120,
            'atk': 20,
            'def': 5
        }
        self.phase = 'player_turn'
        self.message = ""
        self.defending = False

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((10, 10, 25))

        draw_hud(screen, self.font, self.player, self.enemy)

        hud_rect = pygame.Rect(40, 140, WIDTH - 80, 200)
        draw_hud_box(screen, hud_rect, self.font, self.message)

        if self.phase == 'player_turn':
            draw_text(screen, "1. Atacar | 2. Ataque Especial | 3. Defender", (50, 340), self.font)
        elif self.phase == 'end':
            draw_text(screen, "Pressione qualquer tecla para ver o desfecho...", (50, 390), self.font)
        elif self.phase == 'defeat':
            draw_text(screen, "Pressione qualquer tecla para ver seu destino...", (50, 440), self.font)


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
                # Calcula chance de ataque especial
                base_chance = 33.3
                defense_modifier = self.player.defense * 1.5  # 1.5% a menos por ponto de defesa
                final_chance = max(5, base_chance - defense_modifier)
                
                if random.random() * 100 < final_chance:
                    # Ataque especial do inimigo
                    damage = self.enemy['atk'] + 10  # ou outro bônus
                    attack_type = "especial"
                else:
                    damage = self.enemy['atk']
                    attack_type = "normal"
                
                if self.defending:
                    self.message = f"O {self.enemy['name']} tentou um ataque {attack_type}, mas você se defendeu!"
                    damage = 0
                else:
                    self.message = f"O {self.enemy['name']} usa um ataque {attack_type} e causa {damage} de dano!"

            
                self.player.current_hp -= damage
                self.defending = False
            
                if self.player.current_hp <= 0:
                    self.player.current_hp = 0  # Para evitar vida negativa
                    self.message += "\nVocê foi derrotado..."
                    self.phase = 'defeat'
                else:
                    self.phase = 'player_turn'
            elif self.phase == 'defeat':
                game.change_scene("death")
            elif self.phase == 'end':
                game.change_scene("final")

class FinalScene(Scene):
    def __init__(self, font, player, background=None):
        self.font = font
        self.background = background
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
        # Desenha o background
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((10, 10, 10))

        # Desenha a caixa HUD semitransparente
        hud_rect = pygame.Rect(40, 350, WIDTH - 80, 180)
        hud_surface = pygame.Surface(hud_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(hud_surface, (20, 20, 40, 220), hud_surface.get_rect(), border_radius=12)
        screen.blit(hud_surface, hud_rect.topleft)

        # Desenha o texto dentro da caixa HUD, com padding interno
        draw_text(screen, self.message, (hud_rect.x + 20, hud_rect.y + 20), self.font)

        # Instruções de saída, fora da caixa para ficar mais clean
        draw_text(screen, "Pressione qualquer tecla para sair...", (60, 540), self.font)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            game.change_scene("menu")

class DeathScene(Scene):
    def __init__(self, font, background=None):
        self.font = font
        self.background = background

    def render(self, screen):
        if self.background:
            screen.blit(pygame.transform.scale(self.background, (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill((0, 0, 0))

        hud_rect = pygame.Rect(50, 60, WIDTH - 100, 200)
        text = (
            "Seu corpo cai ao chão...\n"
            "A lenda do Guardião termina aqui.\n\n"
            "Pressione qualquer tecla para sair."
        )
        draw_hud_box(screen, hud_rect, self.font, text)



    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            game.change_scene("menu")
            

# controlador do quê vai acontecer no jogo
class Game:
    def __init__(self, background=None):
        self.player = Player("Kael")
        self.sword = Sword()
        self.font = font
        self.backgrounds = {
            "menu": pygame.image.load("menu.png").convert(),
            "intro": pygame.image.load("intro.png").convert(),
            "village": pygame.image.load("village.png").convert(),
            "village_combat": pygame.image.load("village_combat.png").convert(),
            "king": pygame.image.load("king.png").convert(),
            "forest": pygame.image.load("forest.png").convert(),
            "orc_combat": pygame.image.load("orc_combat.png").convert(),
            "final_dark": pygame.image.load("dark_final.png").convert(),
            "final_light": pygame.image.load("light_final.png").convert(),
            "final_neutral": pygame.image.load("neutral_final.png").convert(),
            "death": pygame.image.load("death.png").convert(),
            }
        self.current_scene = MainMenuScene(self.font, self.backgrounds["menu"])


    def change_scene(self, name):
        scenes = {
        "intro": IntroScene(self.font, self.backgrounds["intro"]),
        "accepted": AcceptedScene(self.font, self.backgrounds["intro"]),
        "ignored": IgnoredScene(self.font, self.backgrounds["intro"]),
        "alignment_choice": AlignmentChoiceScene(self.font, self.backgrounds["intro"]),
        "village": VillageScene(self.font, self.player, self.backgrounds["village"]),
        "combat": CombatScene(self.font, self.player, self.backgrounds["village_combat"]),
        "post_combat": PostCombatScene(self.font, self.player, self.backgrounds["village_combat"]),
        "king": KingScene(self.font, self.player, self.backgrounds["king"]),
        "forest": ForestCrossingScene(self.font, self.player, self.backgrounds["forest"]),
        "final_combat": FinalCombatScene(self.font, self.player, self.backgrounds["orc_combat"]),
        "death": DeathScene(self.font, self.backgrounds["death"]),
        "menu": MainMenuScene(self.font, self.backgrounds["menu"]),
        "final": FinalScene(
            self.font,
            self.player,
            self.backgrounds.get(f"final_{self.player.alignment}", None))
        }
        self.current_scene = scenes[name]


# loop principal
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
