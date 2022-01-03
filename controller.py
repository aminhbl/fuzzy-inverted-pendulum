# -*- coding: utf-8 -*-

# python imports
from math import degrees

# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader
import numpy as np


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    # --------------- PA

    def up_more_right(self, x):
        if 0 < x <= 30:
            return (1 / 30) * x
        elif 30 < x < 60:
            return -(1 / 30) * x + 2
        else:
            return 0

    def up_right(self, x):
        if 30 < x <= 60:
            return (1 / 30) * x - 1
        elif 60 < x < 90:
            return -(1 / 30) * x + 3
        else:
            return 0

    def up(self, x):
        if 60 < x <= 90:
            return (1 / 30) * x - 2
        elif 90 < x < 120:
            return -(1 / 30) * x + 4
        else:
            return 0

    def up_left(self, x):
        if 90 < x <= 120:
            return (1 / 30) * x - 3
        elif 120 < x < 150:
            return -(1 / 30) * x + 5
        else:
            return 0

    def up_more_left(self, x):
        if 120 < x <= 150:
            return (1 / 30) * x - 4
        elif 150 < x < 180:
            return -(1 / 30) * x + 6
        else:
            return 0

    def down_more_left(self, x):
        if 180 < x <= 210:
            return (1 / 30) * x - 6
        elif 210 < x < 240:
            return -(1 / 30) * x + 8
        else:
            return 0

    def down_left(self, x):
        if 210 < x <= 240:
            return (1 / 30) * x - 7
        elif 240 < x < 270:
            return -(1 / 30) * x + 9
        else:
            return 0

    def down(self, x):
        if 240 < x <= 270:
            return (1 / 30) * x - 8
        elif 270 < x < 300:
            return -(1 / 30) * x + 10
        else:
            return 0

    def down_right(self, x):
        if 270 < x <= 300:
            return (1 / 30) * x - 9
        elif 300 < x < 330:
            return -(1 / 30) * x + 11
        else:
            return 0

    def down_more_right(self, x):
        if 300 < x <= 330:
            return (1 / 30) * x - 10
        elif 330 < x < 360:
            return -(1 / 30) * x + 12
        else:
            return 0

    # --------------- PV

    def cw_fast(self, x):
        if -200 <= x < -100:
            return 0.01 * x - 1
        else:
            return 0

    def cw_slow(self, x):
        if -200 < x <= -100:
            return 0.01 * x + 2
        elif -100 < x < 0:
            return -0.01 * x
        else:
            return 0

    def stop(self, x):
        if -100 < x <= 0:
            return 0.01 * x + 1
        elif 0 < x < 100:
            return -0.01 * x + 1
        else:
            return 0

    def ccw_slow(self, x):
        if 0 < x <= 100:
            return 0.01 * x
        elif 100 < x < 200:
            return -0.01 * x + 2
        else:
            return 0

    def ccw_fast(self, x):
        if 100 < x <= 200:
            return 0.01 * x - 1
        else:
            return 0

    # --------------- Force

    def left_fast(self, x):
        if -100 < x <= -80:
            return 0.05 * x + 5
        elif -80 < x < -60:
            return -0.05 * x - 3
        else:
            return 0

    def left_slow(self, x):
        if -80 < x <= -60:
            return 0.05 * x + 4
        elif -60 < x < 0:
            return -(1 / 60) * x
        else:
            return 0

    def stop(self, x):
        if -60 < x <= 0:
            return (1 / 60) * x + 1
        elif 0 < x < 60:
            return -(1 / 60) * x + 1
        else:
            return 0

    def right_slow(self, x):
        if 0 < x <= 60:
            return (1 / 60) * x
        elif 60 < x < 80:
            return -0.05 * x + 4
        else:
            return 0

    def right_fast(self, x):
        if 60 < x <= 80:
            return 0.05 * x - 3
        elif 80 < x < 100:
            return -0.05 * x + 5
        else:
            return 0

    def inference(self, inputs):
        pa = inputs['pa']
        up_more_right = self.up_more_right(pa)
        up_right = self.up_right(pa)
        up = self.up(pa)
        up_left = self.up_left(pa)
        up_more_left = self.up_more_left(pa)
        down_more_left = self.down_more_left(pa)
        down_left = self.down_left(pa)
        down = self.down(pa)
        down_right = self.down_right(pa)
        down_more_right = self.down_more_right(pa)

        pv = inputs['pv']
        cw_fast = self.cw_fast(pv)
        cw_slow = self.cw_slow(pv)
        pv_stop = self.stop(pv)
        ccw_slow = self.ccw_slow(pv)
        ccw_fast = self.ccw_fast(pv)

        right_fast_rules = [
            min(up_more_right, ccw_slow),
            min(up_more_right, cw_slow),
            min(up_more_right, cw_fast),
            min(down_more_right, ccw_slow),
            min(down_right, ccw_slow),
            min(down_right, cw_slow),
            min(up_right, cw_slow),
            min(up_right, pv_stop),
            min(up_right, cw_fast),
            min(up_left, cw_fast),
            min(down, pv_stop),
            min(up, cw_fast)
        ]
        right_fast_max = max(right_fast_rules)

        left_fast_rules = [
            min(up_more_left, cw_slow),
            min(up_more_left, ccw_slow),
            min(up_more_left, ccw_fast),
            min(down_more_left, cw_slow),
            min(down_left, cw_slow),
            min(down_left, ccw_slow),
            min(up_left, ccw_slow),
            min(up_left, pv_stop),
            min(up_right, ccw_fast),
            min(up_left, ccw_fast),
            min(up, ccw_fast)
        ]
        left_fast_max = max(left_fast_rules)

        right_slow_rules = [
            min(up_more_left, cw_fast),
            min(down_right, cw_fast),
            min(up_right, ccw_slow),
            min(up, cw_slow)
        ]
        right_slow_max = max(right_slow_rules)

        left_slow_rules = [
            min(up_more_right, ccw_fast),
            min(down_left, ccw_fast),
            min(up_left, cw_slow),
            min(up, ccw_slow)
        ]
        left_slow_max = max(left_slow_rules)

        stop_rules = [
            max(min(up, pv_stop), min(up_right, ccw_slow), min(up_left, cw_slow)),
            min(down_more_right, cw_slow),
            min(down_more_left, ccw_slow),
            min(down_more_right, ccw_fast),
            min(down_more_right, cw_fast),
            min(down_more_left, cw_fast),
            min(down_more_left, ccw_fast),
            min(down_right, ccw_fast),
            min(down_left, cw_fast),
            min(down, cw_fast),
            min(down, ccw_fast),
            min(up, pv_stop)
        ]
        stop_max = max(stop_rules)

        force_points = np.linspace(-100, 100, 1000)
        force_membership = []

        for point in force_points:
            force_membership.append(max(
                min(right_fast_max, self.right_fast(point)),
                min(left_fast_max, self.left_fast(point)),
                min(right_slow_max, self.right_slow(point)),
                min(left_slow_max, self.left_slow(point)),
                min(stop_max, self.stop(point))
            ))

        mass_center_dividened = 0
        mass_center_divisor = 0
        dx = force_points[1] - force_points[0]
        for i in range(len(force_points)):
            mass_center_dividened += force_membership[i] * force_points[i] * dx
            mass_center_divisor += force_membership[i] * dx

        mass_center = mass_center_dividened / mass_center_divisor
        return mass_center

    def decide(self, world):
        output = self._make_output()
        force = self.inference(self._make_input(world))
        return force
        # self.system.calculate(self._make_input(world), output)
        # return output['force']
