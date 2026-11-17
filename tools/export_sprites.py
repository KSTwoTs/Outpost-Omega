"""Export every sprite in SPRITE_NAMES to assets/sprites/<name>.png.

The art is authored as pixel maps / drawing code in
game/systems/asset_manager.py. Run this after editing a sprite there:

    python tools/export_sprites.py

(run from the Outpost Omega folder)
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

from game import settings as S  # noqa: E402
from game.systems.asset_manager import SPRITE_NAMES, build_sprite  # noqa: E402


def main():
    pygame.init()
    os.makedirs(S.SPRITE_DIR, exist_ok=True)
    for name in SPRITE_NAMES:
        path = os.path.join(S.SPRITE_DIR, name + ".png")
        pygame.image.save(build_sprite(name), path)
        print("wrote", os.path.relpath(path, S.ROOT_DIR))
    pygame.quit()


if __name__ == "__main__":
    main()
