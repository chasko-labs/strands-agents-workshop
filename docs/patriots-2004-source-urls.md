# patriots.com 2004 source URLs — confirmed accessible 2026-08-05

systematic ingestion target. all free, all text, all still live on patriots.com.
next session: fetch each URL → extract article body → store in s3vectors.

---

## press conferences — belichick (full Q&A transcripts)

- https://www.patriots.com/news/bill-belichick-post-game-press-conf-transcript-128821
- https://www.patriots.com/news/bill-belichick-press-conf-transcript-9-14-2004-129021
- https://www.patriots.com/news/bill-belichick-press-conf-transcript-8-8-04-164536
- https://www.patriots.com/news/bill-belichick-press-conf-transcript-7-31-04-164361
- https://www.patriots.com/news/bill-belichick-press-conf-transcript-6-12-04-127701
- https://www.patriots.com/news/bill-belichick-press-conf-transcript-1-19-2004-173246
- https://www.patriots.com/news/bill-belichick-press-transcript-1-30-136136
- https://www.patriots.com/news/bill-belichick-press-conference-129791
- https://www.patriots.com/news/bill-belichick-conference-call-transcript-151476

## press conferences — brady

- https://www.patriots.com/news/tom-brady-post-game-press-transcript-173501
- https://www.patriots.com/news/tom-brady-post-game-press-conference-128136
- https://www.patriots.com/news/tom-brady-afc-press-transcript-173316

## game recaps (staff-written, 500-2000 words each)

- https://www.patriots.com/news/patriots-and-colts-kickoff-2004-season-in-foxboro-128886
- https://www.patriots.com/news/patriots-beat-bills-in-wild-one-31-17-128881
- https://www.patriots.com/news/patriots-win-defensive-tussle-13-7-129596
- https://www.patriots.com/news/patriots-streak-ends-at-21-129346
- https://www.patriots.com/news/patriots-escape-bengals-claws-35-28-128396
- https://www.patriots.com/news/miami-shocks-new-england-29-28-128391
- https://www.patriots.com/news/patriots-advance-with-17-14-win-173406
- https://www.patriots.com/news/bill-belichick-wins-ap-coach-of-the-year-169486

## news blitz (daily media roundups — cite Globe, Herald, Providence Journal, USA Today)

- https://www.patriots.com/news/patriots-com-news-blitz-10-4-04-129266
- https://www.patriots.com/news/patriots-com-news-blitz-10-8-04-129366
- https://www.patriots.com/news/patriots-com-news-blitz-10-11-04-129306
- https://www.patriots.com/news/patriots-com-news-blitz-10-19-04-129196
- https://www.patriots.com/news/patriots-com-news-blitz-10-26-04-129291
- https://www.patriots.com/news/patriots-com-news-blitz-11-5-04-128031
- https://www.patriots.com/news/patriots-com-news-blitz-11-8-04-128111
- https://www.patriots.com/news/patriots-com-news-blitz-11-15-04-127811
- https://www.patriots.com/news/patriots-com-news-blitz-12-6-04-127796
- https://www.patriots.com/news/patriots-com-news-blitz-12-13-04-128601
- https://www.patriots.com/news/patriots-com-news-blitz-12-27-04-128456

## super bowl XXXIX

- https://www.patriots.com/press-room/super-bowl-xxxix
- https://www.patriots.com/news/super-bowl-xxxix-daily-summary-friday-130521

## other confirmed 2004 sources (non-patriots.com)

### wayback machine — NFL.com AP game recaps

- https://web.archive.org/web/20070612053723/http:/www.nfl.com/gamecenter/recap/NFL_20040919_NE@ARI
- https://web.archive.org/web/20070629150650/http:/www.nfl.com/gamecenter/recap/NFL_20041010_MIA@NE
- https://web.archive.org/web/20070614202216/http:/www.nfl.com/gamecenter/recap/NFL_20041003_NE@BUF

### espn.com — Len Pasquarelli columns

- https://espn.com/nfl/playoffs03/columns/story?columnist=pasquarelli_len&id=1725473
- https://espn.com/nfl/columns/story?columnist=pasquarelli_len&id=1879010
- https://espn.com/nfl/columns/story?columnist=pasquarelli_len&id=1823826
- https://espn.com/nfl/columns/story?columnist=pasquarelli_len&id=2046784

### sf gate (free, no paywall)

- https://sfgate.com/sports/article/Hey-19-Pats-can-t-lose-Team-stumbles-but-2688303.php
- https://sfgate.com/sports/article/interconference-the-beat-goes-on-in-new-england-2687458.php
- https://sfgate.com/sports/article/On-verge-of-a-record-Patriots-play-it-down-2689810.php
- https://sfgate.com/sports/article/New-England-quite-simply-knows-how-to-win-2687297.php
- https://sfgate.com/sports/article/Pats-smarts-poise-will-prove-decisive-2826297.php
- https://sfgate.com/sports/article/Silencing-skeptics-Patriots-McGinest-excels-2827754.php

### la times (may have paywall)

- https://latimes.com/archives/la-xpm-2004-oct-11-sp-penner11-story.html
- https://latimes.com/archives/la-xpm-2004-oct-04-sp-patriots4-story.html
- https://latimes.com/archives/la-xpm-2004-nov-01-sp-steelers1-story.html
- https://latimes.com/archives/la-xpm-2005-feb-07-sp-super7-story.html

### patriots.com video (highlights, need transcription for narration)

- https://www.patriots.com/video/throwback-tom-brady-and-peyton-manning-match-up-in-2004-afc-divisional-game
- https://www.patriots.com/video/throwback-highlights-2004-afc-championship-game-new-england-patriots-vs-pittsburgh-steelers
- https://www.patriots.com/video/memorable-moment-patriots-bring-home-third-lombardi
- https://www.patriots.com/video/throwback-patriots-win-super-bowl-xxxix-vs-eagles

---

## ingestion plan

total estimated: 150-200 articles/transcripts, all already text.

priority order:

1. belichick press conferences (most quotable, reveals coaching philosophy)
2. game recaps (narrative + player quotes per game)
3. news blitz (local media ecosystem, multiple writer perspectives per game)
4. brady transcripts (player voice)
5. ESPN columns (national narrative)
6. wayback machine AP recaps (official wire coverage)
7. SF Gate / LA Times (west coast perspective)

approach: batch fetch via web_fetch → extract article body → chunk if > 2048 chars → store in s3vectors with metadata (week, date, type, players mentioned)
