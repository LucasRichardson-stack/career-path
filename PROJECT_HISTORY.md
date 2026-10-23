# Career Path Page: Project History and Next Steps

This documents how the career page for my Kettering University guest talk came together, what was tried along the way, and where it's going next. For the technical details (how the code works and how to edit it) see `CAREER_PAGE.md`.

## Background

I'd been seeing TikTok and YouTube tutorials for PowerPoint decks with moving, interactive elements, like a curved image carousel that rotates as you advance slides. I wanted to know whether an AI assistant could build that kind of deck if I gave it the right inputs.

Kettering University asked me to speak to their robotics class about my career, which gave me a real use case to test it on.

## Phase 1: Can an AI learn a PowerPoint trick from a video?

I uploaded a 44-second screen recording of a "curved carousel" tutorial. Claude pulled still frames out of the video and worked out the technique from them:

- A row of portrait images runs off both edges of the slide.
- Two large ellipses, filled with the background color, cover the top and bottom of the row so it looks curved.
- The slide is duplicated, the images shift one position on each copy, and the **Morph** transition animates between them.

What I learned about giving an AI tutorial material:

- Short videos work; the AI extracts frames itself. GIFs aren't needed.
- Transcripts alone aren't enough, since these tutorials are mostly visual. Frames plus transcript is best.
- The single most useful input is the creator's finished .pptx file, because the AI can read the exact settings.
- The AI can write Morph into a .pptx but can't play it back, so the first real test always happens in PowerPoint.

## Phase 2: Seven Wonders test deck (PowerPoint)

Test subject: the Seven Wonders of the Ancient World, with illustrations Claude drew (only the Great Pyramid still exists, and image sites were blocked).

- **v1** worked, but the text morph looked unnatural. Every slide reused the same text box names, so Morph blended one wonder's text into the next.
- **v2** gave each wonder's text its own names and parked the neighboring wonders' text just off screen, so text slides in and out in the same direction as the images. Much better.
- **v3** added clickable cards to jump straight to any wonder, with Morph gliding the whole ring there in one motion.

The limit we hit: PowerPoint has no logic, so a ring of cards can't truly loop. Depending on which copy of a card you tapped, the ring could slide the "wrong" way. There were workarounds (only linking certain copies, or hidden snap-back slides), but each one broke something else, such as the keyboard Back key.

## Phase 3: Seven Wonders as a web page

We rebuilt the same idea as a web page:

- A real 3D curved ring instead of masked shapes.
- An endless loop: tap any card and it takes the shortest way round.
- Text slides in the direction of travel.
- A bonus chart of how long each wonder stood (the Colossus about 54 years, the Pyramid 4,500+ and counting).

The web version solved every limitation from the PowerPoint version, and the AI could check its own work instead of me testing each version in PowerPoint.

## Phase 4: The career page

Same concept, applied to my career for the Kettering talk.

Design decisions:

- **No loop.** A career has a beginning and an end, so the ring is a straight path with a start and finish. A loop would put my current job next to my undergrad.
- **Robot program framing.** Stops are labeled as waypoints P[1] to P[8], like points in a robot program, which fits a robotics class.
- **Built for presenting.** One screen at projector resolution, clicker and arrow-key support, full-screen button.
- **Each organization has its own look.** The page cross-fades into each stop's brand colors (MSU green and white, Peace Corps red, white and blue, Liberty green and black, Kawasaki red and white, UR light blue and white, Illinois orange and blue, Apera red and white, Kettering blue and yellow) with the real logos on the cards.

Content came from my resume, then my own edits: what I did, what each role taught me, a favorite project per stop, skills, and three pieces of advice for the students on the final stop.

Fixes made along the way:

- Waypoint numbers didn't line up with their cards. They now move with the cards and always sit underneath them.
- A focus box stayed stuck on whichever card was last clicked. Fixed so only the current card is highlighted.
- The MSU name overlapped the Sparty logo. Logos are now locked to their own area.
- A taller text panel squeezed the carousel. The panel now has a fixed height.

## Where it's going

Moving the project to Cursor and GitHub, for three reasons:

1. **Media.** I want photos and short videos for each stop, like a Kawasaki robot running a welding application. That works best with real files in a `media/` folder, which GitHub Pages can serve and a local copy can play offline.
2. **Version control.** Every change is tracked and easy to roll back.
3. **Hosting.** It can live alongside my portfolio site on GitHub Pages.

Planned next steps:

1. Add the page and this documentation to the repo.
2. Move the logos out of the HTML into `media/logos/`.
3. Build the media viewer: a "Media" button (or the Down arrow) opens full-screen photos and videos for the current stop without leaving the one-screen layout.
4. Gather and compress media (720p, short clips), with a caption for each.
5. Fix the remaining typos and placeholder brackets (listed in `CAREER_PAGE.md`).
6. Rehearse on a projector, especially the bright white themes in a dim room.
7. Only publish footage I have rights to, since GitHub Pages sites are public.

## Takeaways for future decks

- For presentations meant to be watched rather than edited, an interactive web page beats PowerPoint on motion, theming and navigation.
- When a deck must stay in PowerPoint (for colleagues to edit), Morph tricks are very doable: name objects with `!!`, park off-screen objects for smooth entrances and exits, and expect a round or two of playback fixes.
- The best input to give an AI for copying a design is the original file. A screen recording is a close second.
