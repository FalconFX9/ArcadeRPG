from components.stats import Stats
from components.combat import Combat
from components.initiatecombat import InitiateCombat
from components.inventory import Inventory
from components.controllable import Controllable
import constants as C
from random import randint, random, choice
import pygame


class CombatMechanic:
    def __init__(self, state):
        self.state = state
        self.enemies = {}
        self.tour = True
        self.missed_attack = False
        self.selected_entity = None
        self.defeated_enemies = False
        self.reload = C.RELOAD_ANIM
        self.counter = 0
        self.enemies_num = 0
        self.flee = False

    def turns(self):
        self.missed_attack = False
        self.selected_entity = None
        self.tour = not self.tour

    def attack(self, attacking_entity, selected_entity):
        attack_stat = attacking_entity.obtient_composant(Stats)
        selected_stats = selected_entity.obtient_composant(Stats)

        if randint(0, 100) >= selected_stats.agility:
            multiplier = randint(-30, 30) / 100
            dmg = (attack_stat.attack * ((100 - selected_stats.defence) / 100)) * (1 + multiplier)
            if randint(0, 100) <= 10:
                dmg *= 2
        else:
            self.missed_attack = True
            dmg = 0

        selected_stats.HP -= dmg

        if selected_stats.HP <= 0:
            if selected_entity.contains_component(Combat):
                for id, entity in self.enemies.items():
                    if entity == selected_entity:
                        death_id = id
                self.enemies.pop(death_id)

    def calculate_XP(self):
        XP_gain = 0
        for entity in self.state.combat_launch_entity.obtain_component(InitiateCombat).combat_entities.values():
            level = entity.obtient_composant(Stats).level
            XP_gain += C.XP_GAIN[entity.id] * (1 + (level / 5))
        return XP_gain

    def check_combat(self):
        if len(self.enemies) == 0:
            self.defeated_enemies = True
            if not self.tour:
                pygame.mixer.music.stop()
                pygame.mixer.music.reload('ressources\\Musique\\victory.mp3')
                pygame.mixer.music.play(-1)
            self.tour = True
            self.state.state = C.VICTORY_STATE
            if self.flee:
                stats_joueur = self.state.player.obtain_component(Stats)
                self.state.state = C.LEVEL_STATE
                stats_joueur.XP += self.calculate_XP()
                if stats_joueur.vérifie_niveau():
                    self.state.joueur.obtient_composant(Inventory).vérifie_stats()
                self.state.entités_détruites.append(self.state.combat_launch_entity.id)
                if 'Boss' in self.state.combat_launch_entity.id:
                    self.state.state = C.GAME_END
                self.state.entités.remove(self.state.combat_launch_entity)
                self.state.joueur.obtient_composant(Controllable).force = None
                self.flee = False
        elif self.state.bouttons['Flee'].cliqué:
            pygame.mixer.music.stop()
            musique = ['Enter the Woods.mp3', 'Nebula.mp3']
            selected_music = choice(musique)
            pygame.mixer.music.reload('ressources\\Musique\\' + selected_music)
            pygame.mixer.music.play(-1)
            self.state.bouttons['Flee'].cliqué = False
            self.state.state = C.LEVEL_STATE
            self.tour = True
            self.selected_entity = None
            self.enemies.clear()
        elif self.state.joueur.obtient_composant(Stats).HP <= 0:
            self.state.state = C.FAILURE_STATE
            pygame.mixer.music.stop()
            pygame.mixer.music.reload('ressources\\Musique\\Game Over.mp3')
            pygame.mixer.music.play(-1)
            self.enemies.clear()
            self.selected_entity = None
            self.tour = True

    def enemy_turn(self, id):
        if self.reload == C.RELOAD_ANIM:
            self.attack(self.enemies[id], self.state.joueur)
            self.reload -= 1
        elif self.reload <= 0:
            self.missed_attack = False
            self.reload = C.RELOAD_ANIM
            self.counter += 1
        else:
            self.reload -= 1

    def player_turn(self):
        if self.selected_entity:
            if self.reload == C.RELOAD_ANIM:
                self.attack(self.state.joueur, self.selected_entity)
                self.reload -= 1
            elif self.reload <= 0:
                self.turns()
                self.reload = C.RELOAD_ANIM
            else:
                self.reload -= 1
        elif self.state.bouttons['Heal'].cliqué:
            if self.reload == C.RELOAD_ANIM:
                self.healing()
                self.reload -= 1
            elif self.reload <= 0:
                self.state.bouttons['Heal'].cliqué = False
                self.turns()
                self.reload = C.RELOAD_ANIM
            else:
                self.reload -= 1

    def healing(self):
        stats = self.state.joueur.obtient_composant(Stats)
        stats.HP += (stats.HP_MAX * 0.33) * (random() / 2 + 1)
        if stats.HP > stats.HP_MAX:
            stats.HP = stats.HP_MAX

    def gestionnaire_tours(self):
        if self.tour:
            self.check_selected_enemy()
            self.player_turn()
        else:
            enemies_num = len(self.state.combat_launch_entity.obtain_component(InitiateCombat).combat_entities.values())
            if 'Boss' not in self.state.combat_launch_entity.id:
                if self.counter in self.enemies.keys():
                    self.enemy_turn(self.counter)
                else:
                    self.counter += 1

                if self.counter == enemies_num:
                    self.counter = 0
                    self.turns()
            else:
                self.enemy_turn(1)
                if self.counter == enemies_num:
                    self.counter = 0
                    self.turns()

    def check_selected_enemy(self):
        counter = 0
        for button in self.state.bouttons_cible:
            if button.cliqué and counter in self.enemies.keys():
                self.selected_entity = self.enemies[counter]
                button.clicked = False
            counter += 1
