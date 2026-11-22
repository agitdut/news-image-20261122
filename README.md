# The Day in One Picture — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/agitdut/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/agitdut/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page that sums up the world's news of
Sunday, 22 November 2026, in a single 1024×1024 image.

## What is on the page

- **Lead story:** the apparent hack of the FBI's criminal database
  (NCIC) — fingerprints, wanted persons and missing-persons records —
  with President Trump confirming the breach.
- **Three featured stories:** the Trump–Xi–Putin trilateral in
  Shenzhen and its joint peace declaration; COP31 in Antalya stalling
  in overtime over fossil fuels; Max Verstappen's win in an
  extraordinary Las Vegas Grand Prix of 34 lead changes.
- **Eighteen more stories** from around the world: the “El Chapo
  Isidro” arrest and the violence it sparks in Sinaloa, a drone strike
  on a Russia-bound cargo ship in the Gulf of Finland, Russia hitting
  Kryvyi Rih, South Korea's education minister resigning over an
  exam-cheating scandal, Paolo Bulgari's death at 89, a factory fire
  in Indonesia, a boat disaster in Nigeria, Amazon's near-$7.5bn
  Decart deal, IBM's 520-qubit Nighthawk r3, Miley Cyrus's wedding,
  the UN's report on one in four women, Denmark's accusation against
  Russia, the Palisades fire conviction, California's biggest waves in
  years, Houthi strikes on Saudi Arabia, Iran's hit on Bahrain, India
  declaring 720 for 9 against New Zealand, and Nepal's PM visiting
  India.
- **A numbers strip** with the day's figures, and a source line.

Every fact was checked against reporting published on 22 November 2026
(BBC, The Guardian, CNBC, Al Jazeera, France 24, Sky Sports).

## How it is made

`draw_news.py` (Python 3, Pillow) draws the page from fixed strings
and fixed geometry — no network, no clock, no randomness — so two runs
write byte-identical PNGs. `main.ts` (Node 22, standard library only)
copies `entry.png` to the grader's output directory.
