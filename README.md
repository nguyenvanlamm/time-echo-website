# Time Echo website

The official coming-soon, support, privacy, and changelog website for Time Echo.
A static site with locally hosted assets, no production dependencies, no trackers,
and no form backend. Built for GitHub Pages at:
https://luongnv.com/time-echo-website/

## Develop

Requires Python 3.10 or newer.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8080 --directory dist
```

Open http://localhost:8080. Rebuild after editing `scripts/build.py` or `assets/`.
Page content and shared markup live in `scripts/build.py`; CSS and browser
interactions live in `assets/site.css` and `assets/site.js`.

## Deploy

Enable GitHub Pages with **GitHub Actions** as its source. Push to `main`.
The workflow builds and checks local links, then deploys only `dist/`.
Pull requests run the build and link checks without deploying.
Keep Issues enabled: the support page links to this repository's issue forms.

## App Store Connect URLs

- Marketing: https://luongnv.com/time-echo-website/
- Support: https://luongnv.com/time-echo-website/support.html
- Privacy Policy: https://luongnv.com/time-echo-website/privacy.html
- User Privacy Choices (optional): https://luongnv.com/time-echo-website/privacy.html#your-choices
- Changelog: https://luongnv.com/time-echo-website/changelog.html

Check these URLs are publicly reachable before submitting. Apple also requires
an easily accessible privacy-policy link inside the app; the inspected game's
Settings screen currently has no policy or support link. Add those in the game
repository as a separate app change before submission. Website completion alone
is not an App Store compliance audit.

References checked September 22, 2026:
- https://developer.apple.com/app-store/review/guidelines/ (1.5, 2.1, 5.1.1)
- https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## Support

The GitHub flow follows `textwiz-website`: bug, feature, and general feedback
issue forms. Public reports require a GitHub account. The email form validates
input and prepares an encoded `mailto:` draft; visitors explicitly open and send
it from their mail client. A copy fallback and direct email address are provided.
No message is submitted or stored by the website. The contact address is taken
from the game's existing store metadata: `lamnv260398@gmail.com`.

## Release content

Version 1.0.0 is labeled **In preparation** because public availability has not
been confirmed. At launch, replace the coming-soon status with verified store
links and add an actual release date. Do not imply availability or add a store
badge before the listing is live.

The privacy page includes progress, tutorial state, language, sound, and haptic
preferences verified in `time_echo/lib/data/`. It distinguishes offline app
behavior from GitHub Pages hosting and voluntary email/GitHub support.
The developer should keep the support retention statement aligned with practice.

## Design & copy

Approved direction: midnight palette, cyan present self, violet echoes, gold
exit; bundled Baloo 2 typography and a level-03 illustration. The hero preview is
a user-controlled three-scene explanation, not a playable copy of the game.
Reduced motion preferences are respected. The AIDA structure introduces the
mechanic, builds interest through specific benefits, and directs readers to
learn about the upcoming release. No testimonials or user counts are invented.

After launch, compare “Your best teammate is your past self” with “Solve puzzles
with your past selves.” Test “Download Time Echo” against the platform-specific
store CTA. Prioritize the real store link above the fold; add player quotes only
with permission and attribution. No analytics is currently installed.

## Assets

Baloo 2 is copied from the game's bundled font and covered by `assets/OFL.txt`.
The app icon comes from the game's store assets. Board artwork follows the
actual level-03 grid. `assets/social.png` is an exported website preview.
