# Импорт библиотек
import cocos
from cocos.actions import *
from math import *


# Стрела - полёт
class ArrowMove(Move):
    # Определение направления движения по переданной цели
    def init2(self, collman, purp):
        self.collman = collman
        x = (purp.x - self.target.x)
        y = (purp.y - self.target.y)
        d = hypot(x, y)
        # В случае нулевого расстояния
        if not d:
            x, y, d = 1, 0, 1
        self.dx = x/d
        self.dy = y/d
        # Поворот в сторну цели
        self.target.rotation = self.target.define_angle(purp)
        # Задание скорости передвижения
        self.target.velocity = (self.dx * self.target.move_speed,
                                self.dy * self.target.move_speed)

    def step(self, dt):
        super().step(dt)
        self.target.move_hitbox(*self.target.position)
        for obj in self.collman.iter_colliding(self.target):
            if obj.name in self.target.aim_list and obj.active:
                obj.take_damage(self.target.attack_damage)
                self.target.death()


# Лучник - поиск и поворот к цели, атака
class BowmanAttack(Action):
    def init(self, range, reload):

        self.range = range
        self.reload = reload
        self.cd = 0         # Время до перезарядки
        self.purp = None    # Активная цель

    def init2(self, spawn_bullet, collman, animation):
        self.collman = collman
        self.spawn_bullet = spawn_bullet        # Команда при выстреле
        self.animation = animation

    # Обновление текущей цели
    def update_target(self):
        # Проверка нахождения цели в зоне поражения
        if self.purp is not None:
            if not self.collman.knows(self.purp):
                self.purp = None
            elif self.target.define_distance(self.purp) > self.range:
                self.purp = None
        # Поиск новой цели
        if self.purp is None:
            for temp in self.collman.ranked_objs_near(self.target, self.range):
                if self.target.is_attack_target(temp[0]):
                    self.purp = temp[0]
                    break

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt

        self.update_target()
        # Действия при наличии активной цели
        if self.purp is None:
            if self.cd <= 0:
                self.animation.stop()
            return

        # Угол поворота до цели
        turn = (180 + self.target.define_angle(self.purp) -
                self.target.rotation) % 360 - 180
        # Если поворот завершён
        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
            self.animation.update(dt)
            if self.cd <= 0:
                if self.animation.do_action():
                    self.spawn_bullet(self.target, self.purp)
                    self.cd = self.reload
        else:
            self.target.rotation += copysign(self.target.rotation_speed,
                                             turn) * dt


class DevilAttack(Action):
    def init(self, trigger_range, attack_range, reload):
        self.trigger_range = trigger_range
        self.attack_range = attack_range
        self.reload = reload
        self.cd = 0         # Время до перезарядки
        self.purp = None    # Активная цель

    def init2(self, collman, attack_ani, move_ani):
        self.collman = collman
        self.attack_ani = attack_ani
        self.move_ani = move_ani

    # Обновление текущей цели
    def update_target(self):
        for temp in self.collman.ranked_objs_near(self.target,
                                                  self.trigger_range):
            if self.target.is_attack_target(temp[0]):
                self.purp = temp[0]
                break
        else:
            self.purp = None

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt
        self.update_target()

        if self.purp is None:
            if self.cd <= 0:
                self.move_ani.stop()
                self.attack_ani.stop()
            return

        dist = self.target.define_distance(self.purp)
        turn = (180 + self.target.define_angle(self.purp) -
                self.target.rotation) % 360 - 180

        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
        else:
            self.target.rotation += copysign(self.target.rotation_speed, turn) * dt

        if dist <= self.attack_range:
            self.move_ani.stop()
            self.attack_ani.update(dt)
            if self.cd <= 0:
                if self.attack_ani.do_action():
                    self.purp.take_damage(self.target.attack_damage)
                    self.cd = self.reload
        else:
            self.attack_ani.stop()
            self.move_ani.update(dt)
            self.move_ani.do_action()
            x, y = self.target.position
            x0, y0 = self.purp.position
            self.target.position = (x + (x0-x)/dist*self.target.move_speed*dt,
                                    y + (y0-y)/dist*self.target.move_speed*dt)
            self.target.move_hitbox(*self.target.position)


class WarriorAttack(Action):
    def init(self, trigger_range, attack_range, reload):
        self.trigger_range = trigger_range
        self.attack_range = attack_range
        self.reload = reload
        self.cd = 0  # Время до перезарядки
        self.purp = None  # Активная цель

    def init2(self, collman, attack_ani):
        self.collman = collman
        self.attack_ani = attack_ani

    # Обновление текущей цели
    def update_target(self):
        for temp in self.collman.ranked_objs_near(self.target,
                                                  self.trigger_range):
            if self.target.is_attack_target(temp[0]):
                self.purp = temp[0]
                break
        else:
            self.purp = None

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt
        self.update_target()

        if self.purp is None:
            if self.cd <= 0:
                self.attack_ani.stop()
            return

        dist = self.target.define_distance(self.purp)
        turn = (180 + self.target.define_angle(self.purp) -
                self.target.rotation) % 360 - 180

        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
        else:
            self.target.rotation += copysign(self.target.rotation_speed,
                                             turn) * dt

        if dist <= self.attack_range:
            self.attack_ani.update(dt)
            if self.cd <= 0:
                if self.attack_ani.do_action():
                    self.purp.take_damage(self.target.attack_damage)
                    self.cd = self.reload
        else:
            self.attack_ani.stop()


class PriestHealing(Action):
    def init(self, heal_range, reload):
        self.heal_range = heal_range
        self.reload = reload
        self.cd = 0  # Время до перезарядки
        self.purp_list = []

    def init2(self, collman, animation):
        self.collman = collman
        self.animation = animation

    def find_targets(self):
        for temp in self.collman.ranked_objs_near(self.target,
                                                  self.heal_range):
            if (self.target.is_attack_target(temp[0]) and
                    temp[0].health != temp[0].max_health):
                self.purp_list.append(temp[0])
        return self.purp_list != []

    def heal_targets(self):
        for temp in self.purp_list:
            temp.take_heal(self.target.attack_damage)
        self.purp_list = []

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt

        if self.cd <= 0 and self.find_targets():
            self.animation.update(dt)
            if self.animation.do_action():
                self.heal_targets()
                self.cd = self.reload
                self.animation.stop()


class MermanAttack(Action):
    def init(self, attack_range, reload):
        self.attack_range = attack_range
        self.reload = reload
        self.cd = 0  # Время до перезарядки
        self.purp_pos = None

    def init2(self, boat, attack_ani, move_ani):
        self.boat = boat
        self.attack_ani = attack_ani
        self.move_ani = move_ani

    def update_target(self):
        if self.purp_pos is None or self.boat.is_block_exist(*self.purp_pos) is None:
            self.attack_ani.stop()
            self.purp_pos = self.boat.closest_block(*self.target.position)
            if self.purp_pos is None:
                return False
            dx = self.purp_pos[0] - self.target.x
            dy = self.purp_pos[1] - self.target.y
            dist = self.target.define_distance(self.purp_pos)
            if not dist:
                dist = 1
            self.target.velocity = (dx / dist * self.target.move_speed,
                                    dy / dist * self.target.move_speed)

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt

        self.update_target()
        if self.purp_pos is None:
            return
        turn = (180 + self.target.define_angle(self.purp_pos) -
                self.target.rotation) % 360 - 180

        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
        else:
            self.target.rotation += copysign(self.target.rotation_speed,
                                             turn) * dt

        # if self.boat.is_near(*self.target.position, self.attack_range):
        if self.target.define_distance(self.purp_pos) < self.attack_range + 10:
            self.move_ani.stop()
            self.attack_ani.update(dt)
            if self.cd <= 0:
                if self.attack_ani.do_action():
                    self.boat.get_damage(*self.purp_pos, self.target.attack_damage)
                    self.cd = self.reload
        else:
            self.move_ani.update(dt)
            self.move_ani.do_action()
            self.target.position = (self.target.x + self.target.velocity[0] * dt,
                                    self.target.y + self.target.velocity[1] * dt)
            self.target.move_hitbox(*self.target.position)


class CarpenterFix(Action):
    def init(self, reload):
        self.reload = reload
        self.cd = 0  # Время до перезарядки
        self.purp_pos = None

    def init2(self, boat, animation):
        self.boat = boat
        self.animation = animation

    def update_target(self):
        if self.purp_pos is None or self.boat.is_block_exist(*self.purp_pos) is None:
            self.animation.stop()
            self.purp_pos = self.boat.block_to_heal(*self.target.position)

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt

        self.update_target()
        if self.purp_pos is None:
            return

        turn = (180 + self.target.define_angle(self.purp_pos) -
                self.target.rotation) % 360 - 180
        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
            self.animation.update(dt)
            if self.cd <= 0:
                if self.animation.do_action():
                    self.boat.get_repair(*self.purp_pos, self.target.attack_damage)
                    self.cd = self.reload
                    self.purp_pos = None
        else:
            self.animation.stop()
            self.target.rotation += copysign(self.target.rotation_speed,
                                             turn) * dt


class FireballMove(Move):
    def init(self, angle):
        self.angle = angle

    def init2(self, boat):
        self.boat = boat
        self.target.velocity = (self.target.move_speed * sin(self.angle),
                                self.target.move_speed * cos(self.angle))
        self.target.rotation = self.angle

    def step(self, dt):
        super().step(dt)
        self.target.move_hitbox(*self.target.position)
        if self.boat.is_block_busy(*self.target.position):
            self.explode()

    def explode(self):
        to_hit_list = self.boat.neighbor_units(*self.target.position)
        for obj in to_hit_list:
            obj.take_damage(self.target.attack_damage)
        self.target.death()


class AspidAttack(Action):
    def init(self, attack_range, reload):
        self.attack_range = attack_range
        self.reload = reload
        self.cd = 0  # Время до перезарядки
        self.shot = True

    def init2(self, boat, attack_ani, move_ani, shot_func):
        self.attack_ani = attack_ani
        self.move_ani = move_ani
        self.shot_func = shot_func
        self.boat = boat
        self.center = self.boat.get_boat_center()
        d = self.target.define_distance((self.center[0], self.center[1]))
        dx = (self.center[0] - self.target.x) / d
        dy = (self.center[1] - self.target.y) / d

        self.target.rotation = self.target.define_angle(self.center)
        self.start_vel = (dx * self.target.move_speed,
                          dy * self.target.move_speed)
        self.on_attack = False
        self.dalpha = 2*pi*self.target.move_speed / self.attack_range
        self.angle = radians(self.target.define_angle(self.center) + 180)

    def step(self, dt):
        if self.cd > 0:
            self.cd -= dt

        if not self.on_attack and self.target.define_distance(self.center) > self.attack_range:
            self.move_ani.update(dt)
            self.move_ani.do_action()

            self.target.position = (
            self.target.x + self.start_vel[0] * dt,
            self.target.y + self.start_vel[1] * dt)
            return
        else:
            self.on_attack = True

        turn = (90 + self.target.define_angle(self.center) -
                self.target.rotation) % 360 - 180

        if abs(turn) < self.target.rotation_speed * dt:
            self.target.rotation += turn
        else:
            self.target.rotation += copysign(self.target.rotation_speed, turn) * dt
            return

        self.angle += self.dalpha * dt
        self.target.position = (self.center[0] + self.attack_range * sin(self.angle),
                                self.center[1] + self.attack_range * cos(self.angle))
        if self.cd <= 0:
            self.move_ani.stop()
            self.attack_ani.do_action()
            self.cd = self.reload

        self.attack_ani.update(dt)
        if self.attack_ani.time > 0:
            if self.attack_ani.do_action() and self.shot:
                self.shot_func(self.target.position, 7)
                self.shot = False
        else:
            self.shot = True
            self.attack_ani.stop()
            self.move_ani.start()
