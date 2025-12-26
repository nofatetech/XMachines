from lifecycle import Lifecycle

def clamp(v, lo=-1.0, hi=1.0):
    return max(lo, min(hi, v))

class TankMotorController:
    def __init__(self, state):
        self.state = state

    def drive(self, linear: float, angular: float):
        if self.state.lifecycle != Lifecycle.ACTIVE:
            print("[MOTOR] Ignored (not ACTIVE)")
            return

        left = clamp(linear - angular)
        right = clamp(linear + angular)

        self._apply(left, right)

    def _apply(self, left, right):
        print(f"[MOTOR] LEFT={left:.2f} RIGHT={right:.2f}")
        # GPIO / PWM / motor driver goes here
