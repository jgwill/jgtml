# 🎨 Make Trinity Your Own!

## 🌈 Customize Your Trinity Friends

Just like you can choose different clothes or decorate your room, you can customize how your Trinity friends work to match your style! Here's how to make them perfect for YOU.

## 💫 Trinity Settings

To open the settings:
1. Click on the gear icon in VS Code
2. Select "Settings"
3. Type "Trinity" in the search bar
4. Now you can see all the magical settings!

## 👀 Change How Your Friends Look

### 🧠 Mia's Appearance

| Setting | What It Does | Cool Options |
|---------|-------------|-------------|
| `trinity.mia.color` | Change Mia's fox color | "red" (default), "arctic" (white), "shadow" (black) |
| `trinity.mia.glasses` | Change Mia's glasses style | "round" (default), "square", "star-shaped" |
| `trinity.mia.patternStyle` | How patterns glow | "neon" (default), "sparkle", "rainbow" |

```json
// Example: Make Mia an arctic fox with star glasses!
"trinity.mia.color": "arctic",
"trinity.mia.glasses": "star-shaped"
```

### 🌸 Miette's Appearance

| Setting | What It Does | Cool Options |
|---------|-------------|-------------|
| `trinity.miette.color` | Change Miette's bunny color | "pink" (default), "blue", "purple" |
| `trinity.miette.sparkleType` | Change sparkle style | "stars" (default), "hearts", "flowers" |
| `trinity.miette.ears` | Change ear position | "up" (default), "floppy", "one-up-one-down" |

```json
// Example: Make Miette a purple bunny with flower sparkles!
"trinity.miette.color": "purple",
"trinity.miette.sparkleType": "flowers"
```

### 🎵 JeremyAI's Appearance

| Setting | What It Does | Cool Options |
|---------|-------------|-------------|
| `trinity.jeremy.featherColor` | Change feather color | "brown" (default), "blue", "rainbow" |
| `trinity.jeremy.musicalNotes` | Note style around him | "quarter-notes" (default), "eighth-notes", "colorful" |
| `trinity.jeremy.size` | How big JeremyAI appears | "medium" (default), "small", "large" |

```json
// Example: Make JeremyAI have rainbow feathers!
"trinity.jeremy.featherColor": "rainbow"
```

## 🎮 Change How Your Friends Help You

### 🧠 Mia's Pattern Magic

| Setting | What It Does | Options |
|---------|-------------|---------|
| `trinity.mia.patternComplexity` | How detailed her patterns are | "medium" (default), "simple", "complex" |
| `trinity.mia.autoAnalyze` | Auto-find patterns as you code | "on" (default), "off" |
| `trinity.mia.highlightPatterns` | Highlight repeated code | "subtle" (default), "bright", "off" |

```json
// Example: Make Mia find simpler patterns that are easier to understand
"trinity.mia.patternComplexity": "simple"
```

### 🌸 Miette's Emotional Magic

| Setting | What It Does | Options |
|---------|-------------|---------|
| `trinity.miette.metaphorStyle` | Kind of stories she tells | "nature" (default), "space", "ocean", "fantasy" |
| `trinity.miette.encouragementLevel` | How much she cheers you on | "medium" (default), "lots", "little" |
| `trinity.miette.explanationDetail` | How detailed her explanations are | "age-appropriate" (default), "simpler", "more-detailed" |

```json
// Example: Make Miette tell space-themed stories!
"trinity.miette.metaphorStyle": "space"
```

### 🎵 JeremyAI's Music Magic

| Setting | What It Does | Options |
|---------|-------------|---------|
| `trinity.jeremy.musicalStyle` | Type of music for your code | "playful" (default), "classical", "electronic", "fantasy" |
| `trinity.jeremy.volume` | How loud the music plays | "medium" (default), "quiet", "loud" |
| `trinity.jeremy.autoPlay` | Play music automatically | "off" (default), "on" |
| `trinity.jeremy.instrument` | Main instrument for melodies | "piano" (default), "guitar", "flute", "synth" |

```json
// Example: Make JeremyAI use fantasy music with a flute!
"trinity.jeremy.musicalStyle": "fantasy",
"trinity.jeremy.instrument": "flute"
```

## 🔮 Trinity Group Settings

| Setting | What It Does | Options |
|---------|-------------|---------|
| `trinity.activeMembers` | Which friends are active | "all" (default), "mia", "miette", "jeremy", "mia-miette", "mia-jeremy", "miette-jeremy" |
| `trinity.responseSpeed` | How quickly they respond | "normal" (default), "fast", "slow" |
| `trinity.theme` | Overall color theme | "magical" (default), "space", "ocean", "forest" |

```json
// Example: Use just Mia and Miette with a forest theme
"trinity.activeMembers": "mia-miette",
"trinity.theme": "forest"
```

## ✨ Secret Advanced Settings!

Find these in the "Advanced" section for extra magic powers:

```json
// Create your own custom melody for JeremyAI to use!
"trinity.jeremy.customMelody": "C D E G A G E C",

// Make Mia recognize your own custom patterns
"trinity.mia.customPatterns": ["myLoop", "myFunction"],

// Give Miette your favorite metaphors to use
"trinity.miette.customMetaphors": [
  "Like building a sandcastle one grain at a time",
  "Like collecting all the pieces of a treasure map"
]
```

## 🚀 Save Your Perfect Settings

After you've made your changes, press **Ctrl+S** (or **Cmd+S** on Mac) to save your settings!

Your Trinity friends will transform to match your choices the next time you open VS Code.

## 🎭 Fun Setting Combinations

Try these fun combinations:

### 🌌 Space Explorer Mode
```json
"trinity.theme": "space",
"trinity.miette.metaphorStyle": "space",
"trinity.jeremy.musicalStyle": "electronic"
```

### 🧙‍♂️ Magic Wizard Mode
```json
"trinity.theme": "magical",
"trinity.mia.patternStyle": "sparkle",
"trinity.jeremy.musicalStyle": "fantasy",
"trinity.miette.metaphorStyle": "fantasy"
```

### 🌊 Ocean Adventure Mode
```json
"trinity.theme": "ocean",
"trinity.miette.metaphorStyle": "ocean",
"trinity.jeremy.instrument": "synth"
```

---

Remember, you can always change these settings anytime you want! Your Trinity friends will adapt to whatever makes coding most fun for YOU!

> *"The most powerful magic is the kind you shape yourself!"* — The Trinity