import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.utils import platform
import random
import math
import json
import os
import time
import sqlite3

# For network connectivity check (simulated for now)
import socket

# Android-specific imports with error handling
try:
    if platform == 'android':
        from jnius import autoclass, cast
        ANDROID_AVAILABLE = True
    else:
        ANDROID_AVAILABLE = False
except ImportError:
    ANDROID_AVAILABLE = False

# Start.io AdManager (Fixed Implementation)
class AdManager:
    def __init__(self, app_id):
        self.app_id = app_id
        self.interstitial_loaded = False
        self.rewarded_loaded = False
        
        if ANDROID_AVAILABLE and platform == 'android':
            try:
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                StartAppSDK = autoclass('com.startapp.sdk.adsbase.StartAppSDK')
                StartAppSDK.init(activity, app_id, True)
                print(f"Start.io SDK initialized with App ID: {app_id}")
            except Exception as e:
                print(f"Start.io SDK initialization failed: {e}")
        else:
            print(f"Start.io SDK simulated with App ID: {app_id}")

    def load_interstitial_ad(self):
        """Load interstitial ad"""
        self.interstitial_loaded = True
        return True

    def show_interstitial_ad(self):
        """Show interstitial ad"""
        if self.interstitial_loaded:
            if ANDROID_AVAILABLE and platform == 'android':
                try:
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    StartAppAd = autoclass('com.startapp.sdk.adsbase.StartAppAd')
                    interstitial = StartAppAd(activity)
                    interstitial.showAd()
                    print("Interstitial ad shown")
                    return True
                except Exception as e:
                    print(f"Error showing interstitial ad: {e}")
                    return False
            else:
                print("Interstitial ad shown (simulated)")
                return True
        return False

    def load_rewarded_ad(self):
        """Load rewarded ad"""
        self.rewarded_loaded = True
        return True

    def show_rewarded_ad(self):
        """Show rewarded ad"""
        if self.rewarded_loaded:
            if ANDROID_AVAILABLE and platform == 'android':
                try:
                    # Start.io uses interstitial as rewarded
                    return self.show_interstitial_ad()
                except Exception as e:
                    print(f"Error showing rewarded ad: {e}")
                    return False
            else:
                print("Rewarded ad shown (simulated)")
                return True
        return False

    def show_banner_ad(self):
        """Show banner ad"""
        if ANDROID_AVAILABLE and platform == 'android':
            try:
                print("Banner ads are automatically handled by Start.io SDK")
                return True
            except Exception as e:
                print(f"Error with banner ad: {e}")
                return False
        else:
            print("Banner ad shown (simulated)")
            return True

# Mobile optimization
if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.INTERNET, Permission.ACCESS_NETWORK_STATE])
    except ImportError:
        pass

# Adaptive window size for low-end devices
if platform in ('android', 'ios'):
    Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
    Window.softinput_mode = "below_target"
else:
    Window.size = (360, 640)

# Database Manager (Fixed)
class DatabaseManager:
    def __init__(self, db_name='game_data.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        try:
            # Player table with consistent schema
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    diamonds INTEGER DEFAULT 500,
                    gold INTEGER DEFAULT 1000,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    rank_points INTEGER DEFAULT 0,
                    current_rank TEXT DEFAULT 'Bronze',
                    sub_level INTEGER DEFAULT 1,
                    endless_level INTEGER DEFAULT 1,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_player(self, name):
        try:
            self.cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Player {name} already exists.")
            # Return existing player ID
            self.cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error adding player: {e}")
            return None

    def get_player_data(self, player_id):
        try:
            self.cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting player data: {e}")
            return None

    def update_player_progress(self, player_id, xp=0, diamonds=0, gold=0, rank_points=0, sub_level=None, endless_level=None):
        try:
            query = "UPDATE players SET xp = xp + ?, diamonds = diamonds + ?, gold = gold + ?, rank_points = rank_points + ?"
            params = [xp, diamonds, gold, rank_points]
            
            if sub_level is not None:
                query += ", sub_level = ?"
                params.append(sub_level)
            
            if endless_level is not None:
                query += ", endless_level = ?"
                params.append(endless_level)
                
            query += " WHERE id = ?"
            params.append(player_id)
            
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating player progress: {e}")
            return False

    def get_all_players(self):
        """Get all players for debugging"""
        try:
            self.cursor.execute("SELECT * FROM players")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all players: {e}")
            return []

# AI Progression System with Endless Levels (Same as before)
class AIProgressionSystem:
    def __init__(self):
        self.player_performance = {
            'kills': 0,
            'deaths': 0,
            'accuracy': 0.0,
            'survival_time': 0,
            'damage_dealt': 0,
            'level_completion_time': 0
        }
        
        # Endless progression ranks
        self.endless_ranks = [
            {"name": "Bronze", "min_level": 1, "max_level": 10, "color": (0.8, 0.5, 0.2)},
            {"name": "Silver", "min_level": 11, "max_level": 25, "color": (0.7, 0.7, 0.7)},
            {"name": "Gold", "min_level": 26, "max_level": 50, "color": (1.0, 0.8, 0.0)},
            {"name": "Platinum", "min_level": 51, "max_level": 100, "color": (0.7, 0.9, 1.0)},
            {"name": "Diamond", "min_level": 101, "max_level": 200, "color": (0.0, 0.8, 1.0)},
            {"name": "Heroic", "min_level": 201, "max_level": 500, "color": (1.0, 0.0, 1.0)},
            {"name": "Grandmaster", "min_level": 501, "max_level": 999999, "color": (1.0, 0.0, 0.0)}
        ]
        
        # Dynamic content pools
        self.character_pool = [
            {"name": "Adam", "ability": "Damage Reduction", "unlock_level": 1},
            {"name": "Eve", "ability": "Health Boost", "unlock_level": 3},
            {"name": "Moco", "ability": "Enemy Tracking", "unlock_level": 5},
            {"name": "Kelly", "ability": "Speed Boost", "unlock_level": 8},
            {"name": "Hayato", "ability": "Armor Penetration", "unlock_level": 12},
            {"name": "Alok", "ability": "Healing Aura", "unlock_level": 18},
            {"name": "Chrono", "ability": "Time Shield", "unlock_level": 25},
            {"name": "K", "ability": "Master Mode", "unlock_level": 35}
        ]
        
        self.weapon_pool = [
            {"name": "Pistol", "damage": 25, "ammo": 15, "unlock_level": 1},
            {"name": "SMG", "damage": 35, "ammo": 30, "unlock_level": 3},
            {"name": "Shotgun", "damage": 80, "ammo": 8, "unlock_level": 6},
            {"name": "Assault Rifle", "damage": 45, "ammo": 30, "unlock_level": 10},
            {"name": "Sniper Rifle", "damage": 120, "ammo": 5, "unlock_level": 15},
            {"name": "LMG", "damage": 55, "ammo": 100, "unlock_level": 22},
            {"name": "Grenade Launcher", "damage": 200, "ammo": 3, "unlock_level": 30},
            {"name": "Plasma Rifle", "damage": 150, "ammo": 20, "unlock_level": 40}
        ]

    def get_current_rank(self, level):
        for rank in self.endless_ranks:
            if rank["min_level"] <= level <= rank["max_level"]:
                return rank
        return self.endless_ranks[-1]  # Grandmaster for very high levels

    def generate_sub_level_content(self, main_level, sub_level):
        """Generate dynamic content for each sub-level"""
        rank = self.get_current_rank(main_level)
        difficulty_multiplier = 1 + (main_level * 0.1) + (sub_level * 0.05)
        
        # Generate enemies based on level
        enemy_count = min(3 + (main_level // 5) + sub_level, 15)  # Max 15 enemies
        enemy_types = ["soldier", "sniper", "heavy", "scout"]
        
        # Unlock new enemy types at higher levels
        if main_level >= 20:
            enemy_types.append("elite")
        if main_level >= 50:
            enemy_types.append("boss")
        
        # Generate map obstacles
        obstacle_count = min(5 + (main_level // 10), 20)
        
        # Generate rewards
        base_xp = 100 * difficulty_multiplier
        base_gold = 50 * difficulty_multiplier
        base_diamonds = 5 if sub_level % 5 == 0 else 2  # Bonus diamonds every 5th sub-level
        
        return {
            "enemy_count": int(enemy_count),
            "enemy_types": enemy_types,
            "obstacle_count": int(obstacle_count),
            "difficulty_multiplier": difficulty_multiplier,
            "rewards": {
                "xp": int(base_xp),
                "gold": int(base_gold),
                "diamonds": int(base_diamonds)
            },
            "rank_info": rank
        }

    def get_unlocked_characters(self, level):
        return [char for char in self.character_pool if char["unlock_level"] <= level]

    def get_unlocked_weapons(self, level):
        return [weapon for weapon in self.weapon_pool if weapon["unlock_level"] <= level]

    def calculate_level_progression(self, performance):
        """Calculate if player should advance to next sub-level or main level"""
        score = 0
        
        # Performance scoring
        if performance['kills'] > 0:
            score += performance['kills'] * 10
        if performance['accuracy'] > 0.5:
            score += 20
        if performance['survival_time'] > 60:
            score += 15
        
        # Determine progression
        if score >= 50:  # Advance to next sub-level
            return {"advance": True, "type": "sub_level"}
        elif score >= 100:  # Advance to next main level
            return {"advance": True, "type": "main_level"}
        else:
            return {"advance": False, "type": "retry"}

# Game Data Manager (Fixed)
class GameData:
    def __init__(self):
        self.db = DatabaseManager()
        self.ai_progression = AIProgressionSystem()
        self.current_player_id = None
        self.current_level_data = None
        
    def create_player(self, name):
        player_id = self.db.add_player(name)
        if player_id:
            self.current_player_id = player_id
            return True
        return False
    
    def get_player_info(self):
        if self.current_player_id:
            return self.db.get_player_data(self.current_player_id)
        return None
    
    def generate_current_level(self):
        player_data = self.get_player_info()
        if player_data:
            # Consistent database schema access
            main_level = player_data[9] if len(player_data) > 9 else player_data[4]  # endless_level or level
            sub_level = player_data[8] if len(player_data) > 8 else 1  # sub_level
            
            self.current_level_data = self.ai_progression.generate_sub_level_content(main_level, sub_level)
            return self.current_level_data
        return None

# Player Class (Same as before)
class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (40, 40)
        self.health = 100
        self.max_health = 100
        self.armor = 0
        self.speed = 3
        self.ammo = 30
        self.max_ammo = 30
        self.weapon_damage = 25
        self.kills = 0
        self.diamonds = 500
        self.gold = 1000
        
        with self.canvas:
            Color(0, 0, 1)  # Blue player
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

    def move(self, dx, dy):
        new_x = max(0, min(Window.width - self.width, self.x + dx * self.speed))
        new_y = max(0, min(Window.height - self.height, self.y + dy * self.speed))
        self.pos = (new_x, new_y)

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            return True
        return False

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.armor)
        self.health -= actual_damage
        return self.health <= 0

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

# Enemy Class (Same as before)
class Enemy(Widget):
    def __init__(self, enemy_type="soldier", difficulty_multiplier=1.0, **kwargs):
        super().__init__(**kwargs)
        self.enemy_type = enemy_type
        self.size = (35, 35)
        
        # Base stats modified by difficulty
        base_stats = {
            "soldier": {"health": 60, "damage": 15, "speed": 1.0, "color": (1, 0, 0)},
            "sniper": {"health": 40, "damage": 35, "speed": 0.7, "color": (0.8, 0, 0.2)},
            "heavy": {"health": 120, "damage": 25, "speed": 0.5, "color": (0.6, 0, 0)},
            "scout": {"health": 35, "damage": 12, "speed": 1.8, "color": (1, 0.2, 0)},
            "elite": {"health": 150, "damage": 40, "speed": 1.2, "color": (0.5, 0, 0.5)},
            "boss": {"health": 300, "damage": 60, "speed": 0.8, "color": (0.2, 0, 0.2)}
        }
        
        stats = base_stats.get(enemy_type, base_stats["soldier"])
        self.health = int(stats["health"] * difficulty_multiplier)
        self.max_health = self.health
        self.damage = int(stats["damage"] * difficulty_multiplier)
        self.speed = stats["speed"]
        self.color = stats["color"]
        
        self.ai_state = "patrol"
        self.target = None
        self.last_shot = 0
        
        with self.canvas:
            Color(*self.color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

    def update_ai(self, player, dt):
        if not player:
            return
            
        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Simple AI behavior
        if distance < 150:
            if distance > 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                self.x += move_x
                self.y += move_y
        else:
            # Random movement when player is far
            self.x += random.uniform(-1, 1)
            self.y += random.uniform(-1, 1)
        
        # Keep within bounds
        self.x = max(0, min(Window.width - self.width, self.x))
        self.y = max(0, min(Window.height - self.height, self.y))

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

# Bullet Class (Same as before)
class Bullet(Widget):
    def __init__(self, start_pos, target_pos, damage=25, **kwargs):
        super().__init__(**kwargs)
        self.size = (5, 5)
        self.pos = start_pos
        self.damage = damage
        
        # Calculate direction
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * 8
            self.velocity_y = (dy / distance) * 8
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        with self.canvas:
            Color(1, 1, 0)  # Yellow bullet
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

    def update(self, dt):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Remove if out of bounds
        if (self.x < 0 or self.x > Window.width or 
            self.y < 0 or self.y > Window.height):
            return False
        return True

# Item Class (Same as before)
class Item(Widget):
    def __init__(self, item_type="health", **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.size = (25, 25)
        
        colors = {
            "health": (0, 1, 0),    # Green
            "ammo": (1, 1, 0),      # Yellow
            "armor": (0, 0, 1),     # Blue
            "diamond": (0, 1, 1),   # Cyan
            "gold": (1, 0.8, 0)     # Gold
        }
        
        with self.canvas:
            Color(*colors.get(item_type, (0.5, 0.5, 0.5)))
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

# Game Widget (Same as before, with minor fixes)
class GameWidget(Widget):
    def __init__(self, game_data, **kwargs):
        super().__init__(**kwargs)
        self.game_data = game_data
        self.player = Player(pos=(Window.width//2, 50))
        self.enemies = []
        self.bullets = []
        self.items = []
        
        self.add_widget(self.player)
        
        # Game state
        self.game_over = False
        self.level_complete = False
        self.game_time = 0
        self.spawn_timer = 0
        self.item_spawn_timer = 0
        
        # Performance tracking
        self.performance = {
            'kills': 0,
            'deaths': 0,
            'accuracy': 0.0,
            'survival_time': 0,
            'damage_dealt': 0,
            'shots_fired': 0,
            'shots_hit': 0
        }
        
        # Generate level content
        self.level_data = self.game_data.generate_current_level()
        if not self.level_data:
            # Default level data if generation fails
            self.level_data = {
                "enemy_count": 5,
                "enemy_types": ["soldier"],
                "obstacle_count": 5,
                "difficulty_multiplier": 1.0,
                "rewards": {"xp": 100, "gold": 50, "diamonds": 2},
                "rank_info": {"name": "Bronze", "color": (0.8, 0.5, 0.2)}
            }
        
        # Touch controls for mobile
        self.touch_start = None
        self.bind(on_touch_down=self.on_touch_down)
        self.bind(on_touch_move=self.on_touch_move)
        self.bind(on_touch_up=self.on_touch_up)

    def on_touch_down(self, touch):
        self.touch_start = touch.pos
        return True

    def on_touch_move(self, touch):
        if self.touch_start and not self.game_over:
            dx = touch.pos[0] - self.touch_start[0]
            dy = touch.pos[1] - self.touch_start[1]
            
            # Normalize movement for mobile
            if abs(dx) > 10 or abs(dy) > 10:
                self.player.move(dx * 0.1, dy * 0.1)
                self.touch_start = touch.pos
        return True

    def on_touch_up(self, touch):
        if self.touch_start and not self.game_over:
            # Shoot towards touch position
            self.shoot_bullet(touch.pos)
        self.touch_start = None
        return True

    def shoot_bullet(self, target_pos):
        if self.player.shoot():
            bullet = Bullet(self.player.center, target_pos, self.player.weapon_damage)
            self.bullets.append(bullet)
            self.add_widget(bullet)
            self.performance['shots_fired'] += 1

    def spawn_enemy(self):
        if len(self.enemies) < self.level_data["enemy_count"]:
            enemy_type = random.choice(self.level_data["enemy_types"])
            difficulty = self.level_data["difficulty_multiplier"]
            
            # Random spawn position at edges
            side = random.randint(0, 3)
            if side == 0:  # Top
                pos = (random.randint(0, int(Window.width)), Window.height - 50)
            elif side == 1:  # Right
                pos = (Window.width - 50, random.randint(0, int(Window.height)))
            elif side == 2:  # Bottom
                pos = (random.randint(0, int(Window.width)), 0)
            else:  # Left
                pos = (0, random.randint(0, int(Window.height)))
            
            enemy = Enemy(enemy_type, difficulty, pos=pos)
            self.enemies.append(enemy)
            self.add_widget(enemy)

    def spawn_item(self):
        if len(self.items) < 5:
            item_types = ["health", "ammo", "armor"]
            if random.random() < 0.1:  # 10% chance for premium items
                item_types.extend(["diamond", "gold"])
            
            item_type = random.choice(item_types)
            pos = (random.randint(50, int(Window.width-50)), 
                   random.randint(50, int(Window.height-50)))
            
            item = Item(item_type, pos=pos)
            self.items.append(item)
            self.add_widget(item)

    def update(self, dt):
        if self.game_over or self.level_complete:
            return
        
        self.game_time += dt
        self.performance['survival_time'] = self.game_time
        
        # Spawn enemies
        self.spawn_timer += dt
        if self.spawn_timer > 3.0:  # Spawn every 3 seconds
            self.spawn_enemy()
            self.spawn_timer = 0
        
        # Spawn items
        self.item_spawn_timer += dt
        if self.item_spawn_timer > 8.0:  # Spawn items every 8 seconds
            self.spawn_item()
            self.item_spawn_timer = 0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update_ai(self.player, dt)
            
            # Check collision with player
            if self.check_collision(self.player, enemy):
                if self.player.take_damage(enemy.damage):
                    self.game_over = True
                    self.performance['deaths'] += 1
        
        # Update bullets
        for bullet in self.bullets[:]:
            if not bullet.update(dt):
                self.remove_widget(bullet)
                self.bullets.remove(bullet)
                continue
            
            # Check bullet-enemy collision
            for enemy in self.enemies[:]:
                if self.check_collision(bullet, enemy):
                    self.performance['shots_hit'] += 1
                    self.performance['damage_dealt'] += bullet.damage
                    
                    if enemy.take_damage(bullet.damage):
                        self.remove_widget(enemy)
                        self.enemies.remove(enemy)
                        self.performance['kills'] += 1
                        
                        # Drop random item
                        if random.random() < 0.3:
                            self.spawn_item()
                    
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    break
        
        # Check item collection
        for item in self.items[:]:
            if self.check_collision(self.player, item):
                self.collect_item(item)
                self.remove_widget(item)
                self.items.remove(item)
        
        # Check level completion
        if len(self.enemies) == 0 and self.spawn_timer > 2.0:
            self.level_complete = True
        
        # Calculate accuracy
        if self.performance['shots_fired'] > 0:
            self.performance['accuracy'] = self.performance['shots_hit'] / self.performance['shots_fired']

    def check_collision(self, widget1, widget2):
        return (widget1.x < widget2.x + widget2.width and
                widget1.x + widget1.width > widget2.x and
                widget1.y < widget2.y + widget2.height and
                widget1.y + widget1.height > widget2.y)

    def collect_item(self, item):
        if item.item_type == "health":
            self.player.heal(30)
        elif item.item_type == "ammo":
            self.player.ammo = min(self.player.max_ammo, self.player.ammo + 15)
        elif item.item_type == "armor":
            self.player.armor += 10
        elif item.item_type == "diamond":
            self.player.diamonds += 5
        elif item.item_type == "gold":
            self.player.gold += 50

# UI Screens (Fixed MenuScreen)
class MenuScreen(Screen):
    def __init__(self, game_data, **kwargs):
        super().__init__(**kwargs)
        self.game_data = game_data
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(text='MINI FIRE MOBILE', font_size='24sp', size_hint_y=0.2)
        layout.add_widget(title)
        
        # Player info
        self.info_label = Label(text=self.get_player_info_text(), font_size='14sp', size_hint_y=0.3)
        layout.add_widget(self.info_label)
        
        # Buttons
        play_btn = Button(text='Start Game', size_hint_y=0.15)
        play_btn.bind(on_press=self.start_game)
        layout.add_widget(play_btn)
        
        shop_btn = Button(text='Shop', size_hint_y=0.15)
        shop_btn.bind(on_press=self.open_shop)
        layout.add_widget(shop_btn)
        
        profile_btn = Button(text='Profile', size_hint_y=0.15)
        profile_btn.bind(on_press=self.open_profile)
        layout.add_widget(profile_btn)

        # Watch Ad for Diamonds button
        watch_ad_btn = Button(text='Watch Ad for Diamonds', size_hint_y=0.15)
        watch_ad_btn.bind(on_press=self.watch_ad_for_diamonds)
        layout.add_widget(watch_ad_btn)
        
        self.add_widget(layout)

    def get_player_info_text(self):
        player_data = self.game_data.get_player_info()
        if player_data:
            level_data = self.game_data.generate_current_level()
            if level_data:
                rank_info = level_data["rank_info"]
            else:
                rank_info = {"name": "Bronze"}
            
            # Consistent database access
            if len(player_data) >= 10:
                name = player_data[1]
                diamonds = player_data[2]
                gold = player_data[3]
                xp = player_data[5]
                main_level = player_data[9]  # endless_level
                sub_level = player_data[8]   # sub_level
            else:
                name = player_data[1] if len(player_data) > 1 else "Player"
                diamonds = player_data[2] if len(player_data) > 2 else 500
                gold = player_data[3] if len(player_data) > 3 else 1000
                xp = player_data[5] if len(player_data) > 5 else 0
                main_level = player_data[4] if len(player_data) > 4 else 1  # level
                sub_level = 1
            
            return f"""Player: {name}\nLevel: {main_level} (Sub-Level: {sub_level})\nRank: {rank_info["name"]}\nDiamonds: {diamonds}\nGold: {gold}\nXP: {xp}"""
        return "No player found"

    def start_game(self, instance):
        self.manager.current = 'game'

    def open_shop(self, instance):
        self.manager.current = 'shop'

    def open_profile(self, instance):
        self.manager.current = 'profile'

    def watch_ad_for_diamonds(self, instance):
        app = App.get_running_app()
        if app.ad_manager.load_rewarded_ad():
            # Simulate ad watching and reward
            popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_layout.add_widget(Label(text='Watch a short ad to earn diamonds!'))
            watch_btn = Button(text='Watch Ad')
            watch_btn.bind(on_press=self._show_rewarded_ad_and_reward)
            popup_layout.add_widget(watch_btn)
            self.ad_popup = Popup(title='Free Diamonds!', content=popup_layout, size_hint=(0.7, 0.4), auto_dismiss=False)
            self.ad_popup.open()
        else:
            popup = Popup(title='Ad Not Available', content=Label(text='No ad available right now. Please check your internet connection or try again later.'), size_hint=(0.7, 0.4))
            popup.open()

    def _show_rewarded_ad_and_reward(self, instance):
        app = App.get_running_app()
        if app.ad_manager.show_rewarded_ad():
            # Reward the player
            self.game_data.db.update_player_progress(self.game_data.current_player_id, diamonds=50)
            self.ad_popup.dismiss()
            popup = Popup(title='Diamonds Earned!', content=Label(text='You earned 50 Diamonds!'), size_hint=(0.7, 0.4))
            popup.open()
            # Refresh player info display
            self.info_label.text = self.get_player_info_text()
        else:
            self.ad_popup.dismiss()
            popup = Popup(title='Ad Error', content=Label(text='Failed to show ad. Please try again.'), size_hint=(0.7, 0.4))
            popup.open()

# Other screens remain the same...
# [GameScreen, ShopScreen, ProfileScreen classes remain unchanged from your original code]

class GameScreen(Screen):
    def __init__(self, game_data, **kwargs):
        super().__init__(**kwargs)
        self.game_data = game_data
        self.game_widget = None
        
    def on_enter(self):
        if self.game_widget:
            self.remove_widget(self.game_widget)
        
        # Create new game
        self.game_widget = GameWidget(self.game_data)
        self.add_widget(self.game_widget)
        
        # Start game loop
        self.clock_event = Clock.schedule_interval(self.update_game, 1/30.0)  # 30 FPS for low-end devices
        
        # Add UI overlay
        self.add_ui_overlay()

        # Show banner ad when entering game screen
        app = App.get_running_app()
        app.ad_manager.show_banner_ad()

    def add_ui_overlay(self):
        # Health bar
        self.health_bar = ProgressBar(max=100, value=100, 
                                     pos=(10, Window.height - 30), 
                                     size=(100, 20))
        self.add_widget(self.health_bar)
        
        # Ammo counter
        self.ammo_label = Label(text='Ammo: 30', 
                               pos=(10, Window.height - 60), 
                               size=(100, 20))
        self.add_widget(self.ammo_label)
        
        # Score
        self.score_label = Label(text='Kills: 0', 
                                pos=(Window.width - 100, Window.height - 30), 
                                size=(100, 20))
        self.add_widget(self.score_label)

    def update_game(self, dt):
        if self.game_widget:
            self.game_widget.update(dt)
            
            # Update UI
            self.health_bar.value = self.game_widget.player.health
            self.ammo_label.text = f'Ammo: {self.game_widget.player.ammo}'
            self.score_label.text = f'Kills: {self.game_widget.performance["kills"]}'
            
            # Check game end conditions
            if self.game_widget.game_over:
                self.end_game(False)
            elif self.game_widget.level_complete:
                self.end_game(True)

    def end_game(self, victory):
        if hasattr(self, 'clock_event'):
            Clock.unschedule(self.clock_event)
        
        # Calculate progression
        performance = self.game_widget.performance
        progression = self.game_data.ai_progression.calculate_level_progression(performance)
        
        # Update player data
        player_data = self.game_data.get_player_info()
        if player_data and victory and progression["advance"]:
            # Consistent database access
            if len(player_data) >= 10:
                current_sub_level = player_data[8]  # sub_level
                current_main_level = player_data[9]  # endless_level
            else:
                current_sub_level = 1
                current_main_level = player_data[4] if len(player_data) > 4 else 1  # level
            
            if progression["type"] == "sub_level":
                new_sub_level = current_sub_level + 1
                new_main_level = current_main_level
            else:  # main_level
                new_sub_level = 1
                new_main_level = current_main_level + 1
            
            # Update database
            rewards = self.game_widget.level_data["rewards"]
            self.game_data.db.update_player_progress(
                self.game_data.current_player_id,
                xp=rewards["xp"],
                diamonds=rewards["diamonds"],
                gold=rewards["gold"],
                sub_level=new_sub_level,
                endless_level=new_main_level
            )
        
        # Show result popup
        self.show_result_popup(victory, progression)

        # Show interstitial ad after match ends
        app = App.get_running_app()
        if app.ad_manager.load_interstitial_ad():
            app.ad_manager.show_interstitial_ad()

    def show_result_popup(self, victory, progression):
        if victory:
            title = "Level Complete!"
            if progression["advance"]:
                if progression["type"] == "main_level":
                    message = "Congratulations! You have advanced to the next main level!"
                else:
                    message = "Great! Next sub-level unlocked!"
            else:
                message = "Well played! Try to do better."
        else:
            title = "Game Over"
            message = "Try again!"
        
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        menu_btn = Button(text='Menu')
        menu_btn.bind(on_press=lambda x: self.go_to_menu())
        btn_layout.add_widget(menu_btn)
        
        retry_btn = Button(text='Retry')
        retry_btn.bind(on_press=lambda x: self.retry_game())
        btn_layout.add_widget(retry_btn)
        
        popup_layout.add_widget(btn_layout)
        
        self.popup = Popup(title=title, content=popup_layout, 
                          size_hint=(0.8, 0.6), auto_dismiss=False)
        self.popup.open()

    def go_to_menu(self):
        self.popup.dismiss()
        self.manager.current = 'menu'

    def retry_game(self):
        self.popup.dismiss()
        self.on_enter()

class ShopScreen(Screen):
    def __init__(self, game_data, **kwargs):
        super().__init__(**kwargs)
        self.game_data = game_data
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(text='Shop', font_size='20sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        # Player currency
        player_data = self.game_data.get_player_info()
        if player_data:
            # Consistent database access
            if len(player_data) >= 10:
                diamonds = player_data[2]
                gold = player_data[3]
            else:
                diamonds = player_data[2] if len(player_data) > 2 else 500
                gold = player_data[3] if len(player_data) > 3 else 1000
            currency_text = f"Diamonds: {diamonds} | Gold: {gold}"
        else:
            currency_text = "Diamonds: 0 | Gold: 0"
        
        currency_label = Label(text=currency_text, size_hint_y=0.1)
        layout.add_widget(currency_label)
        
        # Shop items
        scroll = ScrollView()
        shop_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        shop_layout.bind(minimum_height=shop_layout.setter('height'))
        
        # Get unlocked items
        player_data = self.game_data.get_player_info()
        if player_data:
            # Consistent database access
            if len(player_data) >= 10:
                level = player_data[9]  # endless_level
            else:
                level = player_data[4] if len(player_data) > 4 else 1  # level
            
            characters = self.game_data.ai_progression.get_unlocked_characters(level)
            weapons = self.game_data.ai_progression.get_unlocked_weapons(level)
            
            # Add character items
            for char in characters:
                item_layout = BoxLayout(size_hint_y=None, height=60)
                item_layout.add_widget(Label(text=f"{char['name']} - {char['ability']}"))
                buy_btn = Button(text='Buy (100 💎)', size_hint_x=0.3)
                item_layout.add_widget(buy_btn)
                shop_layout.add_widget(item_layout)
            
            # Add weapon items
            for weapon in weapons:
                item_layout = BoxLayout(size_hint_y=None, height=60)
                item_layout.add_widget(Label(text=f"{weapon['name']} - Damage: {weapon['damage']}"))
                buy_btn = Button(text='Buy (50 💎)', size_hint_x=0.3)
                item_layout.add_widget(buy_btn)
                shop_layout.add_widget(item_layout)
        
        scroll.add_widget(shop_layout)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

class ProfileScreen(Screen):
    def __init__(self, game_data, **kwargs):
        super().__init__(**kwargs)
        self.game_data = game_data
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(text='Profile', font_size='20sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        # Player stats
        player_data = self.game_data.get_player_info()
        if player_data:
            level_data = self.game_data.generate_current_level()
            if level_data:
                rank_info = level_data["rank_info"]
            else:
                rank_info = {"name": "Bronze"}
            
            # Consistent database access
            if len(player_data) >= 10:
                name = player_data[1]
                diamonds = player_data[2]
                gold = player_data[3]
                rank_points = player_data[6]
                xp = player_data[5]
                sub_level = player_data[8]
                main_level = player_data[9]
            else:
                name = player_data[1] if len(player_data) > 1 else "Player"
                diamonds = player_data[2] if len(player_data) > 2 else 500
                gold = player_data[3] if len(player_data) > 3 else 1000
                rank_points = 0
                xp = player_data[5] if len(player_data) > 5 else 0
                sub_level = 1
                main_level = player_data[4] if len(player_data) > 4 else 1
            
            stats_text = f"""Name: {name}\nMain Level: {main_level}\nSub-Level: {sub_level}\nRank: {rank_info["name"]}\nXP: {xp}\nRank Points: {rank_points}\nDiamonds: {diamonds}\nGold: {gold}\n\nUnlocked Characters: {len(self.game_data.ai_progression.get_unlocked_characters(main_level))}\nUnlocked Weapons: {len(self.game_data.ai_progression.get_unlocked_weapons(main_level))}"""
        else:
            stats_text = "No information found"
        
        stats_label = Label(text=stats_text, text_size=(None, None))
        layout.add_widget(stats_label)
        
        # Back button
        back_btn = Button(text='Back', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

# Main App (Fixed)
class MiniFireMobileApp(App):
    
    def build(self):
        # Initialize game data
        self.game_data = GameData()
        
        # Initialize AdManager with a placeholder App ID
        # REPLACE 'YOUR_STARTAPP_APP_ID' WITH YOUR ACTUAL START.IO APP ID
        self.ad_manager = AdManager(app_id='207965871')

        # Create default player if none exists
        if not self.game_data.get_player_info():
            self.game_data.create_player("Player1")
        
        # Debug: Print all players
        all_players = self.game_data.db.get_all_players()
        print(f"Database players: {all_players}")
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MenuScreen(self.game_data, name='menu'))
        sm.add_widget(GameScreen(self.game_data, name='game'))
        sm.add_widget(ShopScreen(self.game_data, name='shop'))
        sm.add_widget(ProfileScreen(self.game_data, name='profile'))
        
        return sm

if __name__ == '__main__':
    MiniFireMobileApp().run()