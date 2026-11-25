"""TRIVORTEX MASTER — регрессионный пакет тестов (замечания научрука №4–№6).

Тесты связывают числовую лабораторию с формальной моделью:
  * data/verified_params.json — мост, экспортированный из Lean-файла
    (verification/lean4/tools/export_verified_params.py): ОЖИДАЕМЫЕ значения
    читаются отсюда, а не хардкодятся;
  * lab.physics.VortexEngine — числовое ядро Кирхгофа лаборатории;
  * config.json — фиксированные шаги/допуски (воспроизводимость, №5).

Импорты пакета: ROOT этой директории кладётся в sys.path (как в
trivortex_master.py), модули — `lab.*`, `core.*`.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER_ROOT = os.path.dirname(HERE)  # verification/trivortex_master/
LEAN4_ROOT = os.path.join(os.path.dirname(MASTER_ROOT), "lean4")

if MASTER_ROOT not in sys.path:
    sys.path.insert(0, MASTER_ROOT)

import pytest  # noqa: E402


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def bridge() -> dict:
    """Мост верифицированных параметров: {id: запись}."""
    path = os.path.join(MASTER_ROOT, "data", "verified_params.json")
    data = _load_json(path)
    return {e["id"]: e for e in data["entries"]}


@pytest.fixture(scope="session")
def bridge_linked(bridge) -> dict:
    """Мост, ПРОСОХРАНЁННЫЙ с Lean-исходником: каждый statement_sha256
    пересчитывается из Trivortex.lean и сверяется. Расхождение = сбой
    синхронизации формального и числового уровней (сигнал №6)."""
    sys.path.insert(0, os.path.join(LEAN4_ROOT, "tools"))
    import export_verified_params as evp  # noqa: E402

    src = open(os.path.join(LEAN4_ROOT, "Trivortex.lean"), encoding="utf-8").read()
    thm, df = evp.collect(src)
    for entry in bridge.values():
        stmt = (thm if entry["source_kind"] == "theorem" else df).get(entry["source"])
        assert stmt is not None, (
            f"источник {entry['source']} исчез из Trivortex.lean — "
            "мост и формализация рассинхронизированы"
        )
        d = evp.digest(stmt)
        assert d == entry["statement_sha256"], (
            f"{entry['id']}: утверждение {entry['source']} изменилось, "
            "мост устарел — перезапустите export_verified_params.py и примите "
            "изменения СОЗНАТЕЛЬНО (ревью)"
        )
    return bridge


@pytest.fixture(scope="session")
def testcfg() -> dict:
    return _load_json(os.path.join(HERE, "config.json"))


def make_vortex_scene(positions, circulations):
    """Сцена с точечными вихрями Кирхгофа на движке native_vortex."""
    from core.config import MasterConfig
    from lab.scene import Scene
    from lab.body import Body

    cfg = MasterConfig()  # фиксированные умолчания, seed = 42
    scene = Scene(cfg, name="regression")
    for k, ((x, y), gamma) in enumerate(zip(positions, circulations)):
        scene.add_body(
            Body(
                id=f"v{k}",
                name=f"вихрь {k}",
                mass=1.0,
                radius=0.01,
                position=(x, y, 0.0),
                velocity=(0.0, 0.0, 0.0),
                circulation=float(gamma),
                type="synthetic",
                source="regression",
            )
        )
    scene.apply_engine("native_vortex")
    return scene


def lagrange_positions(a=1.0):
    """Равносторонний треугольник стороны a с центроидом в нуле."""
    import math

    R = a / math.sqrt(3)
    return [
        (R * math.cos(2 * math.pi * k / 3), R * math.sin(2 * math.pi * k / 3)) for k in range(3)
    ]


def pairwise_distances(scene_or_bodies):
    import math

    bodies = scene_or_bodies.bodies
    out = []
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            dx = bodies[i].position[0] - bodies[j].position[0]
            dy = bodies[i].position[1] - bodies[j].position[1]
            out.append(math.hypot(dx, dy))
    return out
