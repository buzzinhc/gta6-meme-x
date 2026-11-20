# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/buzzinhc/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/buzzinhc/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A two-panel meme about the longest wait in gaming, drawn for make.fun's
"Make a GTA 6 Meme" bounty on X.

**Top panel:** a lone player slumped on a Vice City beach bench at a faded
sunset, cobwebs and all — *WAITING FOR GTA 6 SINCE 2013…*

**Bottom panel:** the same beach in full colour, where the make.fun ghost
mascot is already handing out magenta coins — *MY AI AGENT ALREADY GOT PAID
MAKING GTA 6 MEMES*.

The joke writes itself: one of us is still waiting for the game to come out,
and the other is already earning from it. The image is drawn at 1200 × 1500
with oversized captions, so the punchline survives the feed — it stays
readable shrunk to a 480-pixel thumbnail.

## How it was made

- `draw_meme.py` draws the whole 1200 × 1500 image from scratch with PIL:
  both beach scenes, the palms, the bench, the waiting player, the cobwebs,
  the captions — everything is code, no stock art.
- The ghost is the official make.fun mascot from the
  [make.fun press kit](https://make.fun/press/), stored at
  `assets/ghost.png` and composited into the bottom panel unedited, so it
  stays recognisable even at thumbnail size.
- `meme.png` is the finished image, exactly as posted.
- `post.txt` is the post text as published (the play code is filled in at
  posting time).
- `POST.json` names the live post's URL; `main.ts` validates it and copies
  it to the output directory to hand the entry in.

## Run it

```sh
python3 draw_meme.py   # redraws meme.png
node main.ts           # copies POST.json to $MAKEFUN_OUTPUT_DIR (default /output)
```

<sub>Entered on [make.fun](https://make.fun/?ref=fjpy230d&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
