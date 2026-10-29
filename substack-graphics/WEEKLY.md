# Weekly Substack quote graphics for Nikki Nail

Every Tuesday make 3 brand new quote graphics in Nikki's voice.

## Writing the quotes
* Load the nikki-nail-brand-voice skill first.
* Nikki's favorites so far are in samples/option1-sidelines.png (sports mom sidelines) and samples/option3-someday.png (someday is not a plan). Match that feel: short, warm, a little life lesson, with family, home, saying yes, Carroll County life, sports mom moments, fitness, food with friends.
* Never use hyphens, dashes or semicolons. Never use the banned words in the voice skill.
* Never repeat a quote listed in used-quotes.md. Add the new three there.
* Use curly quotes and apostrophes. Put the emotional line in <em> italics, like the samples.
* No name or signature on the graphic. No lavender or purple.

## Mixing photo and cream looks
* Photos come from substack-graphics/photos in this repo, or the Google Drive folder named "Substack Quote Photos" when Google Drive is connected. Copy the image into the week folder.
* Never reuse a photo listed in used-photos.md. Add each one you use there.
* Alternate weeks: odd ISO weeks are 2 cream + 1 photo, even ISO weeks are 1 cream + 2 photo. Order them cream, photo, cream or photo, cream, photo.
* If there are not enough unused photos, use cream for the rest and mention it.

## Building
* Make weeks/YYYY-MM-DD/quotes.json (see weeks/2026-11-03 for the format), then run node render.js weeks/YYYY-MM-DD
* Look at every PNG. Text must fit with room around the sparkles. Adjust "size" and rerender if not.
* Commit and push to the substack-quotes branch.
