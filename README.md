# 🏰 RealmTale（王国物语）

> A medieval fantasy city-builder inspired by 江南百景图, with D&D worldbuilding.
> Built with **Godot 4**, targeting **Android / iOS / PC** cross-platform.

---

## 🎮 Game Overview

**RealmTale** is a simulation/management game set in a rich medieval fantasy world.
Players build and manage a thriving kingdom — constructing buildings, recruiting heroes,
managing resources, and exploring a world filled with dragons, magic, and adventure.

### Core Features
- 🏗️ **City Building** — Place and upgrade medieval buildings (houses, shops, workshops, castles)
- ⚔️ **Hero Collection** — Recruit D&D-style heroes (knights, wizards, rogues, clerics)
- 📦 **Resource Management** — Produce and trade goods (iron, herbs, scrolls, enchanted items)
- 🐉 **Fantasy World** — Explore dungeons, encounter dragons, discover ancient artifacts
- 🌐 **Cross-Platform** — Play on Android, iOS, or PC with shared progress
- 🎨 **Hand-crafted Art** — AI-generated medieval fantasy art assets

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Game Engine | Godot 4.x (GDScript) |
| Backend | Go / Node.js |
| Database | PostgreSQL + Redis |
| Art Pipeline | ComfyUI + Stable Diffusion XL |
| CI/CD | GitHub Actions |
| Platforms | Android (AAB) / iOS (IPA) / Windows / macOS / Linux |

---

## 📁 Project Structure

```
RealmTale/
├── src/                    # Godot project root
│   ├── project.godot       # Godot project file
│   ├── scenes/             # Game scenes
│   │   ├── main/           # Main game scene
│   │   ├── ui/             # UI scenes
│   │   └── world/          # World/map scenes
│   ├── scripts/            # GDScript files
│   │   ├── core/           # Core game logic
│   │   ├── buildings/      # Building system
│   │   ├── characters/     # Character system
│   │   ├── economy/        # Economy/resource system
│   │   └── network/        # Network/multiplayer
│   ├── assets/             # Game assets (sprites, textures)
│   │   ├── buildings/
│   │   ├── characters/
│   │   ├── ui/
│   │   ├── terrain/
│   │   └── effects/
│   └── data/               # Game data (JSON/Resource files)
├── docs/                   # Documentation
│   ├── GDD.md              # Game Design Document
│   ├── GANTT.md            # Development timeline
│   └── ART_GUIDE.md        # AI art pipeline guide
├── tools/                  # Build & art generation tools
│   ├── ai_art/             # ComfyUI workflows
│   └── build/              # Build scripts
└── .github/
    └── workflows/          # CI/CD pipelines
```

---

## 🚀 Getting Started

### Prerequisites
- [Godot 4.x](https://godotengine.org/download) (latest stable)
- Git

### Setup
```bash
git clone https://github.com/StUBenHe/RealmTale.git
cd RealmTale/src
# Open project.godot in Godot 4
```

---

## 📅 Development Timeline

See [docs/GANTT.md](docs/GANTT.md) for the full development Gantt chart.

### Milestones
1. **M0: Project Setup** (Week 1) — Repo, engine, basic scene
2. **M1: Core Demo** (Week 2-6) — Playable city-building prototype
3. **M2: Content Drop** (Week 7-12) — Buildings, heroes, economy
4. **M3: Polish** (Week 13-16) — UI, audio, visual effects
5. **M4: Cross-Platform** (Week 17-20) — Android/iOS/PC builds
6. **M5: Alpha** (Week 21-24) — Closed alpha testing

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👥 Team

- **Ben** — Lead Developer / Technical Director
- **[Partner TBD]** — Game Designer / Art Director

---

*Built with ❤️ and Godot 4*
