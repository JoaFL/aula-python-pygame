import json
import math
import os
import random
import sys
from dataclasses import dataclass

import pygame


pygame.init()
pygame.mixer.quit()

WIDTH = 1280
HEIGHT = 720
FPS = 60
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1350
PATH_Y = WORLD_HEIGHT // 2
PATH_START = 480
PATH_END = WORLD_WIDTH - 70
SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "savegame.json")

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roube um Brainrot - Arena Neon")
CLOCK = pygame.time.Clock()

FONT_TINY = pygame.font.SysFont("consolas", 13)
FONT_SMALL = pygame.font.SysFont("consolas", 17)
FONT_BODY = pygame.font.SysFont("consolas", 21)
FONT_TITLE = pygame.font.SysFont("consolas", 36, bold=True)
FONT_BIG = pygame.font.SysFont("consolas", 60, bold=True)

WHITE = (242, 247, 255)
MUTED = (151, 169, 193)
INK = (13, 18, 31)
PANEL = (20, 29, 49)
PANEL_LIGHT = (29, 42, 68)
CYAN = (70, 225, 224)
PINK = (255, 91, 161)
YELLOW = (255, 204, 74)
GREEN = (77, 222, 143)
RED = (255, 92, 96)
PURPLE = (158, 114, 255)
ORANGE = (255, 145, 70)


def clamp(value, low, high):
    return max(low, min(high, value))


def lerp(a, b, amount):
    return a + (b - a) * amount


def distance(first, second):
    return math.hypot(first[0] - second[0], first[1] - second[1])


def draw_text(surface, text, position, font=FONT_BODY, color=WHITE, anchor="topleft"):
    image = font.render(str(text), True, color)
    rectangle = image.get_rect()
    setattr(rectangle, anchor, position)
    surface.blit(image, rectangle)
    return rectangle


def draw_panel(surface, rectangle, fill=PANEL, border=PANEL_LIGHT, radius=12):
    pygame.draw.rect(surface, fill, rectangle, border_radius=radius)
    pygame.draw.rect(surface, border, rectangle, width=2, border_radius=radius)


def draw_bar(surface, rectangle, value, maximum, color, background=(39, 52, 76)):
    pygame.draw.rect(surface, background, rectangle, border_radius=5)
    ratio = 0 if maximum <= 0 else clamp(value / maximum, 0, 1)
    filled = rectangle.copy()
    filled.width = int(rectangle.width * ratio)
    if filled.width > 0:
        pygame.draw.rect(surface, color, filled, border_radius=5)


def world_to_screen(point, camera):
    return int(point[0] - camera[0]), int(point[1] - camera[1])


def screen_to_world(point, camera):
    return point[0] + camera[0], point[1] + camera[1]


@dataclass
class Particle:
    x: float
    y: float
    color: tuple
    life: float = 0.8
    size: float = 4
    vx: float = 0
    vy: float = 0

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 30 * dt
        self.life -= dt

    def draw(self, surface, camera):
        if self.life <= 0:
            return
        x, y = world_to_screen((self.x, self.y), camera)
        radius = max(1, int(self.size * min(1, self.life)))
        pygame.draw.circle(surface, self.color, (x, y), radius)


@dataclass
class FloatingText:
    text: str
    x: float
    y: float
    color: tuple
    life: float = 1.3

    def update(self, dt):
        self.y -= 34 * dt
        self.life -= dt

    def draw(self, surface, camera):
        if self.life <= 0:
            return
        draw_text(surface, self.text, world_to_screen((self.x, self.y), camera), FONT_SMALL, self.color, "center")


@dataclass
class Brainrot:
    name: str
    rarity: str
    income: int
    color: tuple
    x: float
    y: float
    state: str = "wild"
    owner: str = ""
    wiggle: float = 0
    pulse: float = 0
    stolen_time: float = 0
    path_speed: float = 110

    def __post_init__(self):
        self.radius = 30
        self.wiggle = random.random() * 6

    @property
    def position(self):
        return self.x, self.y

    def update(self, dt):
        self.wiggle += dt * 3.1
        self.pulse += dt * 4
        if self.state == "carried":
            self.stolen_time += dt

    def draw(self, surface, camera, selected=False):
        sx, sy = world_to_screen(self.position, camera)
        bob = math.sin(self.wiggle) * 3
        glow = int(5 + (math.sin(self.pulse) + 1) * 3)
        pygame.draw.circle(surface, tuple(min(255, value + glow) for value in self.color), (sx, int(sy + bob)), 38)
        pygame.draw.circle(surface, INK, (sx, int(sy + bob)), 31)
        pygame.draw.circle(surface, self.color, (sx, int(sy + bob)), 27)
        pygame.draw.circle(surface, WHITE, (sx - 9, int(sy - 4 + bob)), 5)
        pygame.draw.circle(surface, WHITE, (sx + 9, int(sy - 4 + bob)), 5)
        pygame.draw.circle(surface, INK, (sx - 8, int(sy - 3 + bob)), 2)
        pygame.draw.circle(surface, INK, (sx + 8, int(sy - 3 + bob)), 2)
        pygame.draw.arc(surface, INK, (sx - 12, int(sy + 1 + bob), 24, 16), 0.2, 2.9, 3)
        if selected:
            pygame.draw.circle(surface, YELLOW, (sx, int(sy + bob)), 42, 3)
        if self.state == "carried":
            pygame.draw.circle(surface, PINK, (sx, int(sy + bob)), 45, 2)
        draw_text(surface, self.name, (sx, sy + 48 + bob), FONT_TINY, WHITE, "midtop")
        draw_text(surface, self.rarity.upper(), (sx, sy + 64 + bob), FONT_TINY, self.color, "midtop")


@dataclass
class Base:
    name: str
    x: int
    y: int
    width: int
    height: int
    color: tuple
    owner: str
    capacity: int = 5
    locked: bool = False
    lock_timer: float = 0

    @property
    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def contains(self, point):
        return self.rectangle.collidepoint(point)

    @property
    def button_rectangle(self):
        return pygame.Rect(self.x + self.width - 118, self.y + 12, 100, 34)

    def update(self, dt):
        if self.lock_timer > 0:
            self.lock_timer = max(0, self.lock_timer - dt)
            self.locked = self.lock_timer > 0

    def toggle_lock(self, player_position):
        if self.owner != "player" or not self.contains(player_position):
            return False
        if self.lock_timer > 0:
            return False
        self.lock_timer = 10
        self.locked = True
        return True

    def draw(self, surface, camera, brainrots):
        rectangle = self.rectangle.move(-camera[0], -camera[1])
        pygame.draw.rect(surface, (25, 43, 63), rectangle, border_radius=16)
        pygame.draw.rect(surface, self.color, rectangle, width=4, border_radius=16)
        if self.locked:
            pygame.draw.rect(surface, (8, 12, 22, 150), rectangle, border_radius=16)
        draw_text(surface, self.name, (rectangle.centerx, rectangle.top + 14), FONT_BODY, self.color, "midtop")
        draw_text(surface, "BASE", (rectangle.centerx, rectangle.top + 42), FONT_TINY, MUTED, "midtop")
        if self.owner == "player":
            button = self.button_rectangle.move(-camera[0], -camera[1])
            button_color = RED if self.locked else GREEN
            button_text = f"FECHADA {math.ceil(self.lock_timer)}s" if self.locked else "FECHAR 10s"
            pygame.draw.rect(surface, button_color, button, border_radius=7)
            draw_text(surface, button_text, button.center, FONT_TINY, INK, "center")
        owned = [item for item in brainrots if item.owner == self.owner and item.state == "secured"]
        for index, item in enumerate(owned):
            column = index % 3
            row = index // 3
            center = (self.x + 55 + column * 83, self.y + 105 + row * 82)
            pygame.draw.circle(surface, (36, 57, 78), (center[0] - camera[0], center[1] - camera[1]), 32)
            item_copy = Brainrot(item.name, item.rarity, item.income, item.color, center[0], center[1])
            item_copy.draw(surface, camera)
        if self.locked:
            draw_text(surface, "TRANCADA", rectangle.center, FONT_BODY, RED, "center")


@dataclass
class RivalAI:
    name: str
    owner: str
    color: tuple
    x: float
    y: float
    speed: float = 165
    target: object = None
    carrying: object = None
    think_timer: float = 0
    stun: float = 0

    @property
    def position(self):
        return self.x, self.y

    def choose_target(self, game):
        options = []
        for item in game.brainrots:
            if item.state in ("wild", "path"):
                options.append((distance(self.position, item.position), item, None))
            elif item.state == "secured" and item.owner != self.owner:
                base = game.base_for_owner(item.owner)
                if base and not base.locked:
                    options.append((distance(self.position, base.rectangle.center), item, base))
        if options:
            options.sort(key=lambda option: option[0])
            self.target = options[0][1]
        else:
            self.target = None

    def move_towards(self, point, dt, speed):
        dx = point[0] - self.x
        dy = point[1] - self.y
        length = math.hypot(dx, dy)
        if length > 2:
            self.x += dx / length * speed * dt
            self.y += dy / length * speed * dt

    def update(self, game, dt):
        if self.stun > 0:
            self.stun = max(0, self.stun - dt)
            return
        effective_speed = self.speed + game.wave * 9
        self.think_timer -= dt
        if self.carrying:
            home = game.base_for_owner(self.owner)
            if home is None:
                self.carrying = None
                return
            self.move_towards(home.rectangle.center, dt, effective_speed)
            self.carrying.x = self.x
            self.carrying.y = self.y - 55
            if home.contains(self.position):
                stored = [item for item in game.brainrots if item.owner == self.owner and item.state == "secured"]
                if len(stored) < home.capacity:
                    item = self.carrying
                    item.state = "secured"
                    item.owner = self.owner
                    item.x = home.x + 50 + (len(stored) % 3) * 83
                    item.y = home.y + 100 + (len(stored) // 3) * 82
                    self.carrying = None
                    game.add_text(f"{self.name}: +{item.income} renda", self.x, self.y - 65, GREEN)
                    game.burst(self.x, self.y, self.color, 8)
                else:
                    item = self.carrying
                    item.state = "path"
                    item.owner = ""
                    item.x, item.y = PATH_START, PATH_Y
                    self.carrying = None
                    self.target = None
                    game.add_text(f"{self.name}: base cheia", self.x, self.y - 65, YELLOW)
            return
        if self.target is None or self.target.state not in ("wild", "path", "secured") or self.think_timer <= 0:
            self.choose_target(game)
            self.think_timer = max(0.45, 1.2 - game.wave * 0.06)
        if self.target is None:
            return
        target_base = game.base_for_owner(self.target.owner) if self.target.state == "secured" else None
        target_point = target_base.rectangle.center if target_base else self.target.position
        self.move_towards(target_point, dt, effective_speed)
        if self.target.state == "secured":
            if target_base is None or target_base.locked:
                self.target = None
                return
            if distance(self.position, target_base.rectangle.center) < 90:
                self.target.state = "carried"
                self.target.owner = self.owner
                self.carrying = self.target
                self.target = None
                game.notify(f"{self.name} roubou um brainrot!", self.color)
        elif distance(self.position, self.target.position) < 75:
            self.target.state = "carried"
            self.target.owner = self.owner
            self.carrying = self.target
            self.target = None
            game.notify(f"{self.name} encontrou um brainrot.", self.color)

    def draw(self, surface, camera):
        sx, sy = world_to_screen(self.position, camera)
        pygame.draw.circle(surface, (28, 24, 47), (sx, sy), 31)
        pygame.draw.circle(surface, self.color, (sx, sy), 24)
        pygame.draw.rect(surface, INK, (sx - 13, sy - 8, 26, 16), border_radius=4)
        pygame.draw.circle(surface, WHITE, (sx - 7, sy), 3)
        pygame.draw.circle(surface, WHITE, (sx + 7, sy), 3)
        draw_text(surface, self.name, (sx, sy + 35), FONT_TINY, self.color, "midtop")
        if self.carrying:
            pygame.draw.circle(surface, PINK, (sx, sy - 30), 8, 2)


class Player:
    def __init__(self):
        self.x = 250.0
        self.y = 1130.0
        self.radius = 25
        self.speed = 260.0
        self.health = 85
        self.max_health = 85
        self.energy = 100
        self.max_energy = 100
        self.gold = 0
        self.xp = 0
        self.level = 1
        self.damage_value = 25
        self.attack_cooldown = 0
        self.dash_cooldown = 0
        self.invulnerability = 0
        self.carrying = None
        self.facing = (1, 0)

    @property
    def position(self):
        return self.x, self.y

    def update(self, game, dt):
        keys = pygame.key.get_pressed()
        horizontal = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        vertical = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        if horizontal or vertical:
            length = math.hypot(horizontal, vertical)
            horizontal /= length
            vertical /= length
            self.facing = (horizontal, vertical)
            bonus = 0.72 if self.carrying else 1
            self.x += horizontal * self.speed * bonus * dt
            self.y += vertical * self.speed * bonus * dt
        self.x = clamp(self.x, 40, WORLD_WIDTH - 40)
        self.y = clamp(self.y, 40, WORLD_HEIGHT - 40)
        if self.carrying:
            self.carrying.x = self.x
            self.carrying.y = self.y - 60
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.invulnerability = max(0, self.invulnerability - dt)
        self.energy = min(self.max_energy, self.energy + 14 * dt)

    def damage(self, amount, game):
        if self.invulnerability > 0:
            return
        self.health -= amount
        self.invulnerability = 0.7
        game.add_text(f"-{amount} HP", self.x, self.y - 40, RED)
        game.burst(self.x, self.y, RED, 8)
        if self.health <= 0:
            game.player_down()

    def attack(self, game):
        if self.attack_cooldown > 0:
            return
        self.attack_cooldown = max(0.18, 0.48 - game.upgrades["cooldown"] * 0.04)
        reach = 92
        hit_something = False
        for rival in game.rivals:
            if distance((self.x, self.y), rival.position) <= reach:
                rival.stun = 2.5
                game.add_text("IA atordoada", rival.x, rival.y - 42, YELLOW)
                game.burst(rival.x, rival.y, CYAN, 8)
                hit_something = True
        if not hit_something:
            game.burst(self.x + self.facing[0] * 45, self.y + self.facing[1] * 45, CYAN, 3)
        else:
            game.shake = 0.08

    def dash(self, game):
        if self.dash_cooldown > 0 or self.energy < 25:
            return
        self.energy -= 25
        self.dash_cooldown = 1.2
        self.invulnerability = 0.35
        self.x = clamp(self.x + self.facing[0] * 170, 40, WORLD_WIDTH - 40)
        self.y = clamp(self.y + self.facing[1] * 170, 40, WORLD_HEIGHT - 40)
        game.burst(self.x, self.y, CYAN, 14)

    def draw(self, surface, camera):
        sx, sy = world_to_screen((self.x, self.y), camera)
        if self.invulnerability > 0 and int(self.invulnerability * 15) % 2 == 0:
            return
        pygame.draw.circle(surface, (14, 72, 85), (sx, sy), 33)
        pygame.draw.circle(surface, CYAN, (sx, sy), 25)
        pygame.draw.circle(surface, WHITE, (sx - 8, sy - 5), 5)
        pygame.draw.circle(surface, WHITE, (sx + 8, sy - 5), 5)
        pygame.draw.line(surface, INK, (sx - 5, sy + 10), (sx + 7, sy + 10), 3)
        if self.carrying:
            pygame.draw.line(surface, PINK, (sx, sy - 25), (sx, sy - 54), 3)


class Game:
    def __init__(self):
        self.running = True
        self.paused = False
        self.shop_open = False
        self.message = "Colete um brainrot e leve-o para sua base."
        self.message_timer = 5
        self.camera = [0.0, 0.0]
        self.shake = 0
        self.time = 0
        self.wave = 1
        self.path_spawn_timer = 2.5
        self.round_timer = 0
        self.player = Player()
        self.particles = []
        self.texts = []
        self.rivals = []
        self.upgrades = {"damage": 0, "speed": 0, "health": 0, "cooldown": 0, "base": 0}
        self.skills = {"emp": False, "freeze": False, "pulse": False}
        self.skill_cooldowns = {"emp": 0, "freeze": 0, "pulse": 0}
        self.income_timer = 0
        self.brainrots = self.make_brainrots()
        self.bases = self.make_bases()
        self.rivals = self.make_rivals()
        self.load_game()

    def make_brainrots(self):
        data = [
            ("Pipoca", "comum", 3, (255, 199, 80)),
            ("Bananito", "comum", 4, (255, 220, 55)),
            ("Nuvemito", "raro", 8, (120, 194, 255)),
            ("Gelecao", "raro", 10, (98, 238, 185)),
            ("Foguetao", "epico", 18, (255, 111, 90)),
            ("Lunatico", "epico", 22, (187, 120, 255)),
            ("Rei Neon", "lendario", 45, (255, 98, 187)),
            ("Glitch Supremo", "mitico", 90, (92, 255, 234)),
        ]
        positions = [(540, PATH_Y), (820, PATH_Y), (1100, PATH_Y), (1380, PATH_Y), (1660, PATH_Y), (1940, PATH_Y), (720, PATH_Y), (1520, PATH_Y)]
        brainrots = [Brainrot(*item, *position, path_speed=115 + index * 10) for index, (item, position) in enumerate(zip(data, positions))]
        for item in brainrots:
            item.state = "path"
        return brainrots

    def spawn_path_brainrot(self):
        templates = [
            ("Pipoca", "comum", 3, (255, 199, 80), 130),
            ("Bananito", "comum", 4, (255, 220, 55), 142),
            ("Nuvemito", "raro", 8, (120, 194, 255), 115),
            ("Gelecao", "raro", 10, (98, 238, 185), 123),
            ("Foguetao", "epico", 18, (255, 111, 90), 105),
            ("Lunatico", "epico", 22, (187, 120, 255), 98),
            ("Rei Neon", "lendario", 45, (255, 98, 187), 85),
            ("Glitch Supremo", "mitico", 90, (92, 255, 234), 75),
        ]
        name, rarity, income, color, speed = random.choices(
            templates, weights=[35, 30, 17, 10, 5, 2, 0.8, 0.2], k=1
        )[0]
        brainrot = Brainrot(name, rarity, income, color, PATH_START, PATH_Y, path_speed=speed)
        brainrot.state = "path"
        self.brainrots.append(brainrot)
        self.burst(PATH_START, PATH_Y, color, 5)

    def make_bases(self):
        return [
            Base("SUA BASE", 50, 970, 400, 330, CYAN, "player", 5),
            Base("BASE RUBI", 1950, 50, 400, 330, PINK, "ai_rubi", 4),
            Base("BASE VIOLETA", 1950, 970, 400, 330, PURPLE, "ai_violeta", 4),
            Base("BASE LARANJA", 50, 50, 400, 330, ORANGE, "ai_laranja", 4),
        ]

    def make_rivals(self):
        return [
            RivalAI("Rubi", "ai_rubi", PINK, 2150, 220),
            RivalAI("Violeta", "ai_violeta", PURPLE, 2150, 1140),
            RivalAI("Laranja", "ai_laranja", ORANGE, 250, 220),
        ]

    def base_for_owner(self, owner):
        return next((base for base in self.bases if base.owner == owner), None)

    def load_game(self):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as save_file:
                data = json.load(save_file)
            saved = data.get("player", {})
            self.player.gold = int(data.get("gold", saved.get("gold", 0)))
            self.player.level = int(data.get("level", 1))
            self.player.xp = int(data.get("xp", 0))
            self.wave = int(data.get("wave", 1))
            upgrades = data.get("upgrades", {})
            for key in self.upgrades:
                self.upgrades[key] = int(upgrades.get(key, 0))
            saved_skills = data.get("skills", {})
            for key in self.skills:
                self.skills[key] = bool(saved_skills.get(key, False))
            self.player.max_health = 85 + self.upgrades["health"] * 20
            self.player.health = self.player.max_health
            self.player.damage_value = 25 + self.upgrades["damage"] * 8
            self.player.speed = 260 + self.upgrades["speed"] * 18
        except (OSError, ValueError, TypeError):
            pass

    def save_game(self):
        state = {
            "version": 2,
            "state": "playing",
            "gold": self.player.gold,
            "xp": self.player.xp,
            "level": self.player.level,
            "wave": self.wave,
            "upgrades": self.upgrades,
            "skills": self.skills,
            "player": {"x": self.player.x, "y": self.player.y},
        }
        try:
            with open(SAVE_PATH, "w", encoding="utf-8") as save_file:
                json.dump(state, save_file, indent=2)
        except OSError:
            self.notify("Nao foi possivel salvar", RED)

    def notify(self, message, color=WHITE):
        self.message = message
        self.message_timer = 3
        self.add_text(message, self.player.x, self.player.y - 75, color)

    def add_text(self, text, x, y, color):
        self.texts.append(FloatingText(text, x, y, color))

    def burst(self, x, y, color, amount):
        for _ in range(amount):
            angle = random.random() * math.tau
            speed = random.randint(25, 125)
            self.particles.append(Particle(x, y, color, 0.45 + random.random() * 0.5, random.randint(2, 6), math.cos(angle) * speed, math.sin(angle) * speed))

    def player_down(self):
        self.player.health = self.player.max_health
        self.player.x, self.player.y = 250, 1130
        if self.player.carrying:
            self.player.carrying.state = "wild"
            self.player.carrying.owner = ""
            self.player.carrying.x, self.player.carrying.y = 800, 600
            self.player.carrying = None
        self.player.gold = max(0, self.player.gold - 15)
        self.notify("Voce foi derrubado! Perdeu 15 moedas.", RED)

    def gain_xp(self, amount):
        self.player.xp += amount
        needed = self.player.level * 100
        while self.player.xp >= needed:
            self.player.xp -= needed
            self.player.level += 1
            self.player.max_health += 8
            self.player.health = self.player.max_health
            self.player.damage_value += 4
            self.notify(f"Nivel {self.player.level}! Poder aumentado.", YELLOW)
            needed = self.player.level * 100

    def interact(self):
        player_position = (self.player.x, self.player.y)
        if self.player.carrying:
            home = self.bases[0]
            if home.contains(player_position):
                item = self.player.carrying
                stored = [current for current in self.brainrots if current.owner == "player" and current.state == "secured"]
                if len(stored) >= home.capacity:
                    self.notify("Sua base esta cheia. Compre o upgrade BASE.", RED)
                    return
                item.state = "secured"
                item.owner = "player"
                item.x = home.x + 50 + (len(stored) % 3) * 83
                item.y = home.y + 100 + (len(stored) // 3) * 82
                self.player.carrying = None
                reward = item.income * 5
                self.player.gold += reward
                self.gain_xp(item.income * 4)
                self.burst(player_position[0], player_position[1], GREEN, 18)
                self.notify(f"{item.name} protegido! +{reward} moedas.", GREEN)
            else:
                self.notify("Leve o brainrot ate a SUA BASE.", YELLOW)
            return
        nearby = [item for item in self.brainrots if item.state in ("wild", "path") and distance(player_position, item.position) < 90]
        nearby += [
            item for item in self.brainrots
            if item.state == "secured"
            and item.owner != "player"
            and (base := self.base_for_owner(item.owner))
            and not base.locked
            and distance(player_position, item.position) < 90
        ]
        if nearby:
            item = min(nearby, key=lambda current: distance(player_position, current.position))
            item.state = "carried"
            item.owner = "player"
            self.player.carrying = item
            self.burst(item.x, item.y, PINK, 12)
            self.notify(f"{item.name} roubado! Agora corra para a base.", PINK)
        else:
            self.notify("Aproxime-se de um brainrot ou invada uma base aberta.", MUTED)

    def use_skill(self, skill):
        names = {"emp": "EMP", "freeze": "GELO", "pulse": "PULSO"}
        if not self.skills[skill]:
            self.notify(f"Compre a habilidade {names[skill]} na loja.", YELLOW)
            return
        if self.skill_cooldowns[skill] > 0:
            self.notify(f"{names[skill]} recarrega em {self.skill_cooldowns[skill]:.1f}s.", MUTED)
            return
        if skill == "emp":
            for rival in self.rivals:
                if distance(self.player.position, rival.position) < 420:
                    rival.stun = 4
            self.skill_cooldowns[skill] = 12
            self.burst(self.player.x, self.player.y, CYAN, 35)
            self.notify("EMP ativado: inimigos proximos paralisados.", CYAN)
        elif skill == "freeze":
            nearest = min(self.rivals, key=lambda rival: distance(self.player.position, rival.position), default=None)
            if nearest and distance(self.player.position, nearest.position) < 520:
                nearest.stun = 8
                self.add_text("CONGELADO", nearest.x, nearest.y - 50, CYAN)
                self.burst(nearest.x, nearest.y, CYAN, 22)
                self.notify(f"{nearest.name} ficou congelado.", CYAN)
            else:
                self.notify("Nenhuma IA esta no alcance do gelo.", MUTED)
            self.skill_cooldowns[skill] = 16
        elif skill == "pulse":
            affected = 0
            for rival in self.rivals:
                if distance(self.player.position, rival.position) < 360:
                    rival.x = clamp(rival.x + (rival.x - self.player.x) * 0.8, 40, WORLD_WIDTH - 40)
                    rival.y = clamp(rival.y + (rival.y - self.player.y) * 0.8, 40, WORLD_HEIGHT - 40)
                    rival.target = None
                    affected += 1
            self.skill_cooldowns[skill] = 10
            self.burst(self.player.x, self.player.y, PINK, 28)
            self.notify(f"Pulso empurrou {affected} IA(s).", PINK)

    def update_income(self, dt):
        self.income_timer += dt
        if self.income_timer < 1:
            return
        self.income_timer -= 1
        income = sum(item.income for item in self.brainrots if item.owner == "player" and item.state == "secured")
        if income:
            self.player.gold += income
            self.add_text(f"+{income} moedas/s", self.bases[0].x + 190, self.bases[0].y - 18, YELLOW)

    def buy_upgrade(self, key):
        if key in self.skills:
            skill_costs = {"emp": 180, "freeze": 240, "pulse": 300}
            skill_names = {"emp": "EMP", "freeze": "GELO", "pulse": "PULSO"}
            if self.skills[key]:
                self.notify(f"Habilidade {skill_names[key]} ja comprada.", MUTED)
            elif self.player.gold < skill_costs[key]:
                self.notify(f"Faltam {skill_costs[key] - self.player.gold} moedas.", RED)
            else:
                self.player.gold -= skill_costs[key]
                self.skills[key] = True
                self.notify(f"Habilidade {skill_names[key]} desbloqueada.", GREEN)
                self.save_game()
            return
        costs = {"damage": 80, "speed": 70, "health": 90, "cooldown": 110, "base": 150}
        labels = {"damage": "dano", "speed": "velocidade", "health": "vida", "cooldown": "recarga", "base": "capacidade da base"}
        cost = costs[key] * (self.upgrades[key] + 1)
        if self.player.gold < cost:
            self.notify(f"Faltam {cost - self.player.gold} moedas.", RED)
            return
        self.player.gold -= cost
        self.upgrades[key] += 1
        if key == "damage":
            self.player.damage_value += 8
        elif key == "speed":
            self.player.speed += 18
        elif key == "health":
            self.player.max_health += 20
            self.player.health = self.player.max_health
        elif key == "base":
            self.bases[0].capacity += 1
        self.notify(f"Upgrade de {labels[key]} comprado.", GREEN)
        self.save_game()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.paused and not self.shop_open:
            home = self.bases[0]
            clicked = screen_to_world(event.pos, self.camera)
            if home.button_rectangle.collidepoint(clicked) and home.contains((self.player.x, self.player.y)):
                if home.toggle_lock((self.player.x, self.player.y)):
                    self.notify("Sua base esta fechada por 10 segundos.", RED)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.shop_open:
                    self.shop_open = False
                else:
                    self.paused = not self.paused
            elif event.key == pygame.K_e and not self.paused and not self.shop_open:
                self.interact()
            elif event.key == pygame.K_SPACE and not self.paused and not self.shop_open:
                self.player.attack(self)
            elif event.key == pygame.K_LSHIFT and not self.paused and not self.shop_open:
                self.player.dash(self)
            elif event.key == pygame.K_q and not self.paused and not self.shop_open:
                self.use_skill("emp")
            elif event.key == pygame.K_f and not self.paused and not self.shop_open:
                self.use_skill("freeze")
            elif event.key == pygame.K_g and not self.paused and not self.shop_open:
                self.use_skill("pulse")
            elif event.key == pygame.K_b and not self.paused:
                self.shop_open = not self.shop_open
            elif event.key == pygame.K_F5:
                self.save_game()
                self.notify("Jogo salvo.", GREEN)
            elif self.shop_open and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                self.buy_upgrade({pygame.K_1: "damage", pygame.K_2: "speed", pygame.K_3: "health", pygame.K_4: "cooldown", pygame.K_5: "base", pygame.K_6: "emp", pygame.K_7: "freeze", pygame.K_8: "pulse"}[event.key])

    def update(self, dt):
        self.time += dt
        self.message_timer = max(0, self.message_timer - dt)
        if self.paused or self.shop_open:
            return
        for base in self.bases:
            base.update(dt)
        self.player.update(self, dt)
        for rival in self.rivals:
            rival.update(self, dt)
        self.update_income(dt)
        for skill in self.skill_cooldowns:
            self.skill_cooldowns[skill] = max(0, self.skill_cooldowns[skill] - dt)
        self.round_timer += dt
        self.path_spawn_timer -= dt
        if self.path_spawn_timer <= 0:
            self.spawn_path_brainrot()
            self.path_spawn_timer = random.uniform(0.9, 1.8)
        if self.round_timer > 45:
            self.wave += 1
            self.round_timer = 0
            self.notify(f"Onda {self.wave}! As IAs ficaram mais agressivas.", ORANGE)
        for item in self.brainrots:
            item.update(dt)
            if item.state == "path":
                item.x += item.path_speed * dt
                if item.x > PATH_END:
                    item.state = "gone"
                    item.owner = ""
                    self.add_text(f"{item.name} saiu do caminho", PATH_END - 20, PATH_Y - 48, MUTED)
                self.brainrots = [item for item in self.brainrots if item.state != "gone"]
        for particle in list(self.particles):
            particle.update(dt)
            if particle.life <= 0:
                self.particles.remove(particle)
        for text in list(self.texts):
            text.update(dt)
            if text.life <= 0:
                self.texts.remove(text)
        target_camera = [self.player.x - WIDTH / 2, self.player.y - HEIGHT / 2]
        self.camera[0] = lerp(self.camera[0], clamp(target_camera[0], 0, WORLD_WIDTH - WIDTH), min(1, dt * 7))
        self.camera[1] = lerp(self.camera[1], clamp(target_camera[1], 0, WORLD_HEIGHT - HEIGHT), min(1, dt * 7))
        self.shake = max(0, self.shake - dt)

    def draw_background(self, surface):
        surface.fill((9, 15, 28))
        start_x = int(self.camera[0] // 60) * 60
        start_y = int(self.camera[1] // 60) * 60
        for x in range(start_x, int(self.camera[0] + WIDTH) + 60, 60):
            sx = x - int(self.camera[0])
            pygame.draw.line(surface, (17, 29, 47), (sx, 0), (sx, HEIGHT))
        for y in range(start_y, int(self.camera[1] + HEIGHT) + 60, 60):
            sy = y - int(self.camera[1])
            pygame.draw.line(surface, (17, 29, 47), (0, sy), (WIDTH, sy))
        arena = pygame.Rect(-self.camera[0], -self.camera[1], WORLD_WIDTH, WORLD_HEIGHT)
        pygame.draw.rect(surface, (34, 52, 68), arena, width=4)
        for point in [(670, 190), (760, 1080), (1550, 1050), (2100, 760), (1450, 720)]:
            sx, sy = world_to_screen(point, self.camera)
            pygame.draw.circle(surface, (18, 35, 48), (sx, sy), 95)
            pygame.draw.circle(surface, (28, 67, 78), (sx, sy), 95, 2)
        path = pygame.Rect(PATH_START - self.camera[0], PATH_Y - 72 - self.camera[1], PATH_END - PATH_START, 144)
        pygame.draw.rect(surface, (30, 67, 78), path, border_radius=22)
        pygame.draw.rect(surface, (75, 177, 167), path, width=3, border_radius=22)
        for marker_x in range(PATH_START + 30, PATH_END, 90):
            sx = int(marker_x - self.camera[0])
            pygame.draw.line(surface, (112, 229, 188), (sx, int(PATH_Y - self.camera[1])), (sx + 28, int(PATH_Y - self.camera[1])), 4)
        draw_text(surface, "CAMINHO DOS BRAINROTS", (int((PATH_START + PATH_END) / 2 - self.camera[0]), int(PATH_Y - 57 - self.camera[1])), FONT_TINY, (151, 241, 206), "center")

    def draw_hud(self, surface):
        draw_panel(surface, pygame.Rect(18, 18, 300, 135))
        draw_text(surface, f"NIVEL {self.player.level}", (35, 30), FONT_BODY, CYAN)
        draw_text(surface, f"MOEDAS  {self.player.gold}", (35, 58), FONT_BODY, YELLOW)
        draw_text(surface, f"ONDA {self.wave}   IAS {len(self.rivals)}", (35, 88), FONT_SMALL, MUTED)
        draw_text(surface, f"PRESSAO +{self.wave * 9}%", (35, 108), FONT_TINY, ORANGE)
        draw_bar(surface, pygame.Rect(170, 37, 125, 12), self.player.health, self.player.max_health, RED)
        draw_bar(surface, pygame.Rect(170, 70, 125, 12), self.player.energy, self.player.max_energy, CYAN)
        draw_text(surface, "VIDA", (165, 24), FONT_TINY, MUTED)
        draw_text(surface, "ENERGIA", (165, 57), FONT_TINY, MUTED)
        if self.message_timer > 0:
            draw_panel(surface, pygame.Rect(WIDTH // 2 - 280, HEIGHT - 68, 560, 42), (20, 29, 49, 235), PANEL_LIGHT)
            draw_text(surface, self.message, (WIDTH // 2, HEIGHT - 47), FONT_SMALL, WHITE, "center")
        draw_panel(surface, pygame.Rect(WIDTH - 280, 18, 262, 125))
        draw_text(surface, "CONTROLES", (WIDTH - 262, 30), FONT_SMALL, YELLOW)
        draw_text(surface, "WASD mover   E roubar/guardar", (WIDTH - 262, 55), FONT_TINY, MUTED)
        draw_text(surface, "ESPACO atacar   SHIFT dash", (WIDTH - 262, 74), FONT_TINY, MUTED)
        draw_text(surface, "Q EMP   F GELO   G PULSO", (WIDTH - 262, 93), FONT_TINY, MUTED)
        draw_text(surface, "B loja   F5 salvar   CLIQUE fecha base", (WIDTH - 262, 112), FONT_TINY, MUTED)

    def draw_shop(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 8, 18, 190))
        surface.blit(overlay, (0, 0))
        panel = pygame.Rect(WIDTH // 2 - 350, 38, 700, 670)
        draw_panel(surface, panel, (21, 31, 52), CYAN, 18)
        draw_text(surface, "MERCADO DE UPGRADES E HABILIDADES", (WIDTH // 2, 58), FONT_TITLE, WHITE, "midtop")
        draw_text(surface, f"Saldo: {self.player.gold} moedas", (WIDTH // 2, 102), FONT_BODY, YELLOW, "midtop")
        options = [("1", "DANO", "Ataques mais fortes", "damage", 80), ("2", "VELOCIDADE", "Corra mais rapido", "speed", 70), ("3", "VIDA", "Aumenta sua vida maxima", "health", 90), ("4", "RECARGA", "Ataque volta mais rapido", "cooldown", 110), ("5", "BASE", "Mais um espaco seguro", "base", 150), ("6", "EMP [Q]", "Paralisa inimigos proximos", "emp", 180), ("7", "GELO [F]", "Congela a IA mais proxima", "freeze", 240), ("8", "PULSO [G]", "Empurra as IAs para longe", "pulse", 300)]
        for index, (number, title, description, key, base_cost) in enumerate(options):
            y = 148 + index * 64
            row = pygame.Rect(panel.x + 35, y, panel.width - 70, 52)
            draw_panel(surface, row, (27, 42, 65), (48, 72, 99), 8)
            draw_text(surface, number, (row.x + 22, row.centery), FONT_TITLE, CYAN, "center")
            draw_text(surface, title, (row.x + 52, row.y + 6), FONT_BODY, WHITE)
            draw_text(surface, description, (row.x + 52, row.y + 31), FONT_TINY, MUTED)
            cost = base_cost * (self.upgrades[key] + 1) if key in self.upgrades else base_cost
            owned = key in self.skills and self.skills[key]
            label = "COMPRADA" if owned else f"{cost} g"
            draw_text(surface, label, (row.right - 18, row.centery), FONT_SMALL, MUTED if owned else (GREEN if self.player.gold >= cost else RED), "midright")
        draw_text(surface, "Pressione B ou ESC para fechar", (WIDTH // 2, 684), FONT_SMALL, MUTED, "center")

    def draw(self):
        self.draw_background(SCREEN)
        for base in self.bases:
            base.draw(SCREEN, self.camera, self.brainrots)
        for item in self.brainrots:
            if item.state not in ("secured", "gone"):
                item.draw(SCREEN, self.camera, item.state == "carried")
        for rival in self.rivals:
            rival.draw(SCREEN, self.camera)
        self.player.draw(SCREEN, self.camera)
        for particle in self.particles:
            particle.draw(SCREEN, self.camera)
        for text in self.texts:
            text.draw(SCREEN, self.camera)
        self.draw_hud(SCREEN)
        if self.paused and not self.shop_open:
            draw_panel(SCREEN, pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 80, 420, 160), (18, 27, 47), CYAN)
            draw_text(SCREEN, "PAUSADO", (WIDTH // 2, HEIGHT // 2 - 32), FONT_BIG, WHITE, "center")
            draw_text(SCREEN, "ESC para continuar", (WIDTH // 2, HEIGHT // 2 + 35), FONT_SMALL, MUTED, "center")
        if self.shop_open:
            self.draw_shop(SCREEN)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(CLOCK.tick(FPS) / 1000, 0.05)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
        self.save_game()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()