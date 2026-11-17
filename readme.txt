OUTPOST OMEGA: ALIEN SIEGE
CPSC 4160 - Milestone 3 (Advanced Version)
Trenton McDonald - Individual Project

==========================================================================
HOW TO RUN
==========================================================================
Requires Python 3.10+ and pygame-ce (or classic pygame 2.x - install only one).

    pip install -r requirements.txt
    python main.py

Run main.py from inside the Outpost Omega folder.

School of Computing Linux machines:
pygame is already installed there, so skip the pip step (installing
pygame-ce on top of it would conflict). Use python3, and quote the
folder name if it has a space in it.

    cd 'outpost omega'
    python3 main.py

  - On import, pygame may print a RuntimeWarning about AVX2. It is
    harmless and can be ignored.
  - The game can feel a little laggy over a remote session.

==========================================================================
CONTROLS
==========================================================================
WASD / Arrow keys ... Move Commander Vance (auto-fires at the closest alien)
E (hold) ............ Repair a nearby damaged or EMP'd tower
Q, then click ....... Orbital Strike (1 s delay, 45 s cooldown); right-click cancels
1-5 / HUD buttons ... Choose a tower; click a green tile to build
Shift + click ....... Build several towers of the same type
Click a tower ....... Select it (Upgrade / Sell / Targeting buttons appear)
Right-click tower ... Upgrade it
U / X / T ........... Upgrade / Sell (70% refund) / cycle targeting mode
Space ............... Start the next wave early
Esc or P ............ Pause
F1 .................. Debug overlay (waypoints, ranges, spatial hash, hitboxes,
                      boss pixel-mask outline)

==========================================================================
MILESTONE 3 DELIVERY CHECKLIST
==========================================================================
Final sprites ........ All 29 sprites are final pixel art, shipped as PNGs in
                       assets/sprites/ (see Task 8). Every entity in the game
                       has its final graphics.
Final game mechanics . Build/wave loop, Energy economy, 5 towers with 3 tiers,
                       7 alien types (including the boss), items, scoring and
                       stars (Tasks 3-7).
Final player mechanics Commander Vance: movement, auto-blaster, repair, Orbital
                       Strike, downed/respawn (Task 2).
Levels, menus and
game procedures ...... 3 sectors x 10 waves, Menu, Level Select, Pause,
                       Win/Lose screens, save file with sector-unlock
                       progression (Tasks 1 and 5).

==========================================================================
ITEMS DEVELOPED (100 Pts total)
==========================================================================
I worked alone, so every item below was developed by me.

* Task 1: Core Engine and Architecture
   * Trenton McDonald 20 Pts:
      * GameManager with a fixed-timestep game loop (60 updates/sec,
        independent of frame rate) and OnStart / OnUpdate / OnRender
        hooks 4 Pts.
      * SceneManager with a scene stack: Menu, Level Select, Play,
        Pause (overlay), Win and Lose screens 4 Pts.
      * EventBus so systems communicate through events instead of
        direct calls (enemy_killed, enemy_reached_core,
        item_collected, ...) 3 Pts.
      * Reusable components: Health (with armor), StateMachine, Timer
        and Cooldown, PathFollower 3 Pts.
      * Data-driven design: towers.json, enemies.json, items.json and
        levels/sector1-3.json hold all stats, waves and maps 3 Pts.
      * Save system (save.json) and progression: best stars and score
        per sector, last difficulty; Sector 1 starts unlocked and
        winning a sector unlocks the next one 3 Pts.

* Task 2: Player Character - Commander Vance
   * Trenton McDonald 10 Pts:
      * InputSystem that maps keys and mouse to named Commands 1 Pts.
      * 8-direction movement with acceleration, max speed and friction
        (Vector2 velocity, lower friction on ice tiles) 2 Pts.
      * Tile collision with axis-separated AABB resolution (slides
        along rocks, towers and the Core) 1 Pts.
      * Finite state machine: Idle, Move, Shoot, Repair, Downed 1 Pts.
      * Auto-blaster: targets the closest alien within 160 px,
        4 shots/sec, with lead targeting 2 Pts.
      * Repair ability (hold E) restores tower HP over 2 seconds 1 Pts.
      * Orbital Strike: aim, 1 s delay, splash damage with falloff,
        knockback, screen shake, 45 s cooldown 1 Pts.
      * Downed at 0 HP, respawns at the Core after 5 s 1 Pts.

* Task 3: Towers
   * Trenton McDonald 15 Pts:
      * Grid placement with green/red preview, range circle and checks
        (buildable tile, Commander not in the way, path not blocked)
        3 Pts.
      * Targeting priorities: first, last, strongest, closest 2 Pts.
      * 3 upgrade tiers per tower loaded from towers.json; selling
        refunds 70% 2 Pts.
      * Towers have HP; disabled when EMP'd or broken until repaired
        1 Pts.
      * Pulse Turret: fast single-target shots with lead targeting
        1 Pts.
      * Tesla Coil: chain lightning jumping between enemies (jittered
        lightning effect, brief stun) 2 Pts.
      * Cryo Emitter: slows all enemies in range by 40% (cryo tint)
        1 Pts.
      * Railgun: piercing beam that hits every ground enemy on the line
        and ignores armor (segment-vs-circle test) 2 Pts.
      * Missile Battery: homing missiles with a turn-rate limit and
        splash damage; can hit flyers 1 Pts.

* Task 4: Enemies
   * Trenton McDonald 15 Pts:
      * Enemy base class + subclasses, stats from enemies.json 2 Pts.
      * Finite state machine: Walk, Attack (ground enemies stop and hit
        the Commander when she blocks their route), Stunned, Dying;
        subclasses add their own states 1 Pts.
      * Armor rule damage = max(1, damage - armor) and status effects
        stored as timers: slow, stun, burn 2 Pts.
      * Skitter (fast, low HP, comes in swarms) and Brute (slow,
        armored, heavy Core damage) 1 Pts.
      * Glider: flies straight at the Core using seek steering, ignores
        the path 1 Pts.
      * Brood Sac: bursts into 3 Skitters on death 1 Pts.
      * Saboteur: stops near towers, charges, then EMPs them (disables
        for 3 s and damages them) 2 Pts.
      * Detonator (suicide bomber): walks the path until an active tower
        is in reach, then leaves the path and charges it (new Charge
        state), lights a 0.5 s fuse on contact and explodes, damaging
        every tower and the Commander in the blast with falloff; if its
        target is sold or broken it retargets or walks back to the path;
        killing it first defuses it 2 Pts.
      * Hive Overseer (boss, final wave): summons Skitters every 8 s,
        raises an invulnerable shield at 66% and 33% HP, boss HP bar,
        pixel-perfect hit detection (shield bubble blocks shots while
        it is up) 3 Pts.

* Task 5: Levels and Waves
   * Trenton McDonald 10 Pts:
      * Tile map loader for a 40x20 grid of 32 px tiles (path,
        buildable, blocked, spawn, core, ice, acid, hive wall), drawn
        once to a cached Surface, with per-sector visual themes 2 Pts.
      * A* pathfinding (Manhattan heuristic) builds each enemy route
        from the painted path tiles and checks that tower placement
        never blocks it 2 Pts.
      * WaveSystem: build phase (15 s countdown or Space) -> wave
        phase, spawn queue ordered by time with heapq, multiple spawn
        lanes, difficulty scaling (enemy HP x (1 + 0.15 x wave) plus
        Easy / Normal / Hard and per-sector multipliers) 2 Pts.
      * Sector 1 - Desert Outpost: tutorial sector, one winding path,
        10 scripted waves with the boss on wave 10 1 Pts.
      * Sector 2 - Frozen Relay Station: two lanes that merge before
        the Core; ice patches make the Commander slide 1 Pts.
      * Sector 3 - Hive Crash Site: acid pools damage the Commander;
        hive walls grow and recede during waves, A* recomputes the
        route and every alien already walking is rerouted from where it
        stands; branching path; boss on wave 10 2 Pts.

* Task 6: Items and Economy
   * Trenton McDonald 10 Pts:
      * Energy economy: start with 250-350 E depending on the sector,
        earn from kills and crystals, spend on building and
        upgrades 2 Pts.
      * Weighted loot table drops on enemy death 2 Pts.
      * Energy Crystal (+25 E), Repair Kit (heals a tower 40%),
        Overcharge Cell (tower fires 2x faster for 10 s), Shield
        Battery (+10 Core HP) 4 Pts.
      * Items bob and glow and stay on the map until the next wave
        starts (they blink for the last 3 s of the build countdown);
        collected by walking over them or clicking 1 Pts.
      * Scoring (kills + leftover Energy) and 1-3 star rating from
        Core HP 1 Pts.

* Task 7: Collision and Physics
   * Trenton McDonald 10 Pts:
      * Spatial hash broad phase (64 px cells) rebuilt every frame
        2 Pts.
      * Circle-vs-circle narrow phase using squared distances (no sqrt)
        2 Pts.
      * pygame.mask narrow phase for the Hive Overseer's irregular
        shape: bullets and splash use a circle mask vs. the boss sprite
        mask (mask.overlap), railgun beams are sampled along the line;
        masks are built from the current animation frame (flipped when
        it faces left) and cached 2 Pts.
      * Lead targeting by solving for the projectile intercept point
        1 Pts.
      * Homing steering with a turn-rate limit; splash damage falloff
        and knockback 2 Pts.
      * Object pooling for projectiles and particles 1 Pts.

* Task 8: Graphics, Effects, UI and Audio
   * Trenton McDonald 10 Pts:
      * Final sprite art: 29 pixel-art sprites (Commander, 7 aliens,
        5 turrets + tower base, Omega Core, 4 items) in the game
        palette, authored as pixel maps and exported to
        assets/sprites/*.png with tools/export_sprites.py; AssetManager
        loads the PNGs and caches rotated, flipped and tinted
        versions 3 Pts.
      * Sprite animations: Commander walk (2 frames), shoot and downed
        poses; 2-frame animations for all seven alien types (walk
        cycles, wing flaps, Brood Sac pulse, Detonator fuse spark, boss
        stomp) 1 Pts.
      * Pooled particle system and effects: explosions, sparks, alien
        goo, muzzle flashes, screen shake, hit flash, floating damage
        numbers, red flash on Core hits, lightning bolts, railgun
        beams, EMP and shield rings 2 Pts.
      * HUD and menus: Core HP, Energy, score, tower build buttons,
        selected-tower panel, wave info, Commander HP and Orbital
        cooldown, boss HP bar, toasts and wave banners, menu starfield,
        level select with mini-map thumbnails, F1 debug overlay 2 Pts.
      * AudioSystem: synthesized chiptune sound effects for every
        action and a looping chiptune music track
        (assets/sounds/music.ogg) 2 Pts.

==========================================================================
REMAINING FOR THE FINAL DELIVERY
==========================================================================
  - Campaign cutscenes/dialogue between sectors
  - More tower upgrade paths
  - Balancing across all sectors
