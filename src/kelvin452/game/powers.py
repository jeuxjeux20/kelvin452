from collections import namedtuple
from typing import Callable, Any

import pygame

from kelvin452.engine import *
import kelvin452.game.enemy as enemy_module
import kelvin452.game.inventory as inventory


class Powers:
    Upgrade = namedtuple('Upgrade', ['old_value', 'new_value', 'cost'])

    def __init__(self):
        self.coins_pierced = 1
        self.coins_pierced_upgrade_cost = 50
        self.fire_rate = 1
        self.fire_rate_upgrade_cost = 10
        self.damage = 1
        self.damage_upgrade_cost = 96

    def next_fire_rate_upgrade(self):
        return Powers.Upgrade(self.fire_rate, self.fire_rate * 0.78, self.fire_rate_upgrade_cost)

    def upgrade_fire_rate(self):
        upgrade = self.next_fire_rate_upgrade()
        if upgrade.cost <= enemy_module.enemy:
            enemy_module.modify_enemy(-upgrade.cost)
            self.fire_rate = upgrade.new_value

            self.fire_rate_upgrade_cost *= 1.4
            self.fire_rate_upgrade_cost += 2
            self.fire_rate_upgrade_cost = int(self.fire_rate_upgrade_cost)

    def next_coins_pierced_upgrade(self):
        return Powers.Upgrade(self.coins_pierced, self.coins_pierced + 1, self.coins_pierced_upgrade_cost)

    def upgrade_coins_pierced(self):
        upgrade = self.next_coins_pierced_upgrade()
        if upgrade.cost <= enemy_module.enemy:
            enemy_module.modify_enemy(-upgrade.cost)
            self.coins_pierced = upgrade.new_value

            self.coins_pierced_upgrade_cost += 15
            self.coins_pierced_upgrade_cost **= 1.15
            self.coins_pierced_upgrade_cost = int(self.coins_pierced_upgrade_cost)

    def next_damage_upgrade(self):
        return Powers.Upgrade(self.damage, self.damage + 1, self.damage_upgrade_cost)

    def upgrade_damage(self):
        upgrade = self.next_damage_upgrade()
        if upgrade.cost <= enemy_module.enemy:
            enemy_module.modify_enemy(-upgrade.cost)
            self.damage = upgrade.new_value

            self.damage_upgrade_cost += 43
            self.damage_upgrade_cost **= 1.15
            self.damage_upgrade_cost = int(self.damage_upgrade_cost)


def _make_filled_surface(dimensions, color):
    surface = pygame.Surface(dimensions)
    surface.fill(color)
    return surface


class PowerupMenu(Entity, EventConsumer):
    BUY_BUTTON_SIZE = Vector2(210, 100)
    RED_BUTTON_SURFACE = _make_filled_surface(BUY_BUTTON_SIZE, (220, 30, 0))
    GREEN_BUTTON_SURFACE = _make_filled_surface(BUY_BUTTON_SIZE, (50, 200, 0))
    GREY_BUTTON_SURFACE = _make_filled_surface(BUY_BUTTON_SIZE, (94, 94, 94))
    HEADER_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 40)

    def __init__(self, powers: Powers):
        super().__init__()
        self.background = self.attach_component(Image(assets.ui("shop_menu.png")))
        self.background.position = (game.viewport - self.background.size) / 2

        self.shop_text = self.background.govern(TextBlock("BOSS SHOP", font=PowerupMenu.HEADER_FONT))
        self.place_element_centered(self.shop_text, 30)

        # Mis à jour plus tard
        self.coins_pierced_upgrade = inventory.game.world.get_single_entity(inventory.Inventory).is_in_inventory(
            inventory.PiercingCrystalEntity)
        self.coins_pierced_upgrade_text = self.background.govern(TextBlock())
        if self.coins_pierced_upgrade:
            self.coins_pierced_upgrade_buy_button: Button[TextBlock] = self.background.govern(
                Button(PowerupMenu.BUY_BUTTON_SIZE,
                       PowerupMenu.GREEN_BUTTON_SURFACE,
                       TextBlock()))
            self.coins_pierced_upgrade_buy_button.on_click = self.upgrade_callback(Powers.upgrade_coins_pierced)
        else:
            self.coins_pierced_upgrade_buy_button: Button[TextBlock] = self.background.govern(
                Button(PowerupMenu.BUY_BUTTON_SIZE,
                       PowerupMenu.GREY_BUTTON_SURFACE,
                       TextBlock()))
        self.place_element_centered(self.coins_pierced_upgrade_buy_button, 120)

        self.fire_rate_upgrade = True
        self.fire_rate_upgrade_text = self.background.govern(TextBlock())
        self.fire_rate_upgrade_buy_button: Button[TextBlock] = self.background.govern(
            Button(PowerupMenu.BUY_BUTTON_SIZE,
                   PowerupMenu.GREEN_BUTTON_SURFACE,
                   TextBlock()))
        self.fire_rate_upgrade_buy_button.on_click = self.upgrade_callback(Powers.upgrade_fire_rate)
        self.place_element_centered(self.fire_rate_upgrade_buy_button, 280)

        self.damage_upgrade = True
        self.damage_upgrade_text = self.background.govern(TextBlock())
        self.damage_upgrade_buy_button: Button[TextBlock] = self.background.govern(
            Button(PowerupMenu.BUY_BUTTON_SIZE,
                   PowerupMenu.GREEN_BUTTON_SURFACE,
                   TextBlock()))
        self.damage_upgrade_buy_button.on_click = self.upgrade_callback(Powers.upgrade_damage)
        self.place_element_centered(self.damage_upgrade_buy_button, 440)

        self.enemy_text = self.background.govern(TextBlock())
        self.close_button = self.background.govern(
            Button(Vector2(160, 50),
                   PowerupMenu.RED_BUTTON_SURFACE,
                   TextBlock("FERMER")))
        self.close_button.on_click = lambda: self.destroy()
        self.place_element_centered(self.close_button, self.background.size.y - 100)

        self.powers = powers
        self.update_upgrade_state()

    def update_upgrade_state(self):
        if self.coins_pierced_upgrade:
            coins_pierced_old, coins_pierced_new, coins_pierced_cost = self.powers.next_coins_pierced_upgrade()
            self.coins_pierced_upgrade_text.text \
                = f"PIÈCES PÉNÉTRÉES PAR DRAGON : {coins_pierced_old} -> {coins_pierced_new} | " \
                  f"COÛTE {coins_pierced_cost} ennemis"
            self.coins_pierced_upgrade_text.force_update()
            self.place_element_centered(self.coins_pierced_upgrade_text, 80)
            self.update_upgrade_button(self.coins_pierced_upgrade_buy_button, coins_pierced_cost)
        else:
            self.coins_pierced_upgrade_text.text = "LOCK"
            self.place_element_centered(self.coins_pierced_upgrade_text, 80)

        if self.fire_rate_upgrade:
            fire_rate_old, fire_rate_new, fire_rate_cost = self.powers.next_fire_rate_upgrade()
            self.fire_rate_upgrade_text.text \
                = f"CADENCE DE TIR : {fire_rate_old:.2f}/sec -> {fire_rate_new:.2f}/sec | COÛTE {fire_rate_cost} ennemis"
            self.fire_rate_upgrade_text.force_update()
            self.place_element_centered(self.fire_rate_upgrade_text, 240)
            self.update_upgrade_button(self.fire_rate_upgrade_buy_button, fire_rate_cost)

        if self.damage_upgrade:
            damage_old, damage_new, damage_cost = self.powers.next_damage_upgrade()
            self.damage_upgrade_text.text \
                = f"DAMAGE : {damage_old} -> {damage_new} | COSTS {damage_cost} enemies"
            self.damage_upgrade_text.force_update()
            self.place_element_centered(self.damage_upgrade_text, 400)
            self.update_upgrade_button(self.damage_upgrade_buy_button, damage_cost)

        self.enemy_text.text = f"ENNEMIS : {enemy_module.enemy}"
        self.enemy_text.force_update()
        self.place_element_centered(self.enemy_text, self.background.size.y - 130)

    def place_element_centered(self, target, y):
        target.position.x = self.background.position.x + (self.background.size.x - target.size.x) / 2
        target.position.y = self.background.position.y + y

    def upgrade_callback(self, upgrader: Callable[[Powers], Any]):
        def callback():
            upgrader(self.powers)
            self.update_upgrade_state()

        return callback

    @staticmethod
    def update_upgrade_button(button, cost):
        if cost <= enemy_module.enemy:
            button.background = PowerupMenu.GREEN_BUTTON_SURFACE
            button.child.text = "ACHETER"
        else:
            button.background = PowerupMenu.RED_BUTTON_SURFACE
            button.child.text = "PAS ASSEZ D'ENNEMIS"

    def consume_event(self, new_event: pygame.event.Event) -> bool:
        if new_event.type == pygame.MOUSEBUTTONDOWN:
            return True
        if new_event.type == pygame.KEYDOWN:
            if new_event.key == pygame.K_ESCAPE:
                self.destroy()
                return True
        return False

    def get_priority(self):
        return 299  # UI fixme sale


if __name__ == "__main__":
    def example_game_start():
        game.log_fps = True
        enemy_module.modify_enemy(999)
        game.world.spawn_entity(PowerupMenu(Powers()))


    game.initialize_game()
    game.on_start(example_game_start)
    game.start()
