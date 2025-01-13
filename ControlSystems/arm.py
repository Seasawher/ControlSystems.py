import numpy as np

from ControlSystems.constants import G
from ControlSystems.typing import Time, State, Input
from ControlSystems.main import ControlSystem
from numpy import float64

class VerticalDrivingArm(ControlSystem):
    """垂直駆動アーム。「Pythonによる制御工学入門」の3.1.2参照。"""

    def __init__(self, J : float = 0.3, M : float = 1.5, l : float = 0.7, μ : float = 0.1) -> None:  # noqa: E741
        self.J = J
        self.M = M
        self.l = l
        self.μ = μ

    J : float
    """アームの回転軸の周りの慣性モーメント[kg⬝m²]"""

    M : float
    """アームの質量[kg]"""

    l : float  # noqa: E741
    """アームの重心までの長さ[m]"""

    μ : float
    """粘性摩擦係数[Ns/m]"""

    @property
    def constant_names(self) -> list[str]:
        return ["J", "M", "l", "μ"]

    @property
    def state_names(self) -> list[str]:
        return ["θ", "ω"]

    @property
    def input_names(self) -> list[str]:
        return ["T"] # アームに与えるトルク

    def ssmodel(self, t : Time, x : State, u : Input) -> State:
        J = self.J
        M = self.M
        l = self.l  # noqa: E741
        μ = self.μ

        θ_index = self.state_names.index("θ")
        ω_index = self.state_names.index("ω")
        θ = x[θ_index]
        ω = x[ω_index]

        dθ = ω
        dω = (- μ * ω - M * G * l * np.sin(θ) + u) / J
        return np.array([dθ, dω])
