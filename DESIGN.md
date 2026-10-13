---
version: alpha
name: Boshi Zhang — The Research Voyage
description: Academic portfolio with restrained classical Greek architecture and a Greek stairway to discovery.
colors:
  paper: '#f6f8f7'
  ink: '#193d65'
  blue: '#235bb0'
  muted: '#52677d'
  line: '#c5d1db'
  wash: '#e7eef3'
  gold: '#d9ac55'
  white: '#ffffff'
  scroll-thumb: '#7d91a6'
  scroll-hover: '#52677d'
  scroll-active: '#193d65'
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
  sans:
    fontFamily: "'Avenir Next', Avenir, 'Segoe UI', 'PingFang SC', sans-serif"
  mono:
    fontFamily: "'Courier New', monospace"
rounded:
  DEFAULT: 3px
spacing:
  section-gap: 56px
  page-max: 1200px
components:
  button: {}
  publication: {}
  photo: {}
---
# The Research Voyage

## Context
Personal academic content site for prospective research collaborators. English main content with Chinese personal accents. Global audience; no Japanese locale or Japan-market workflows. Content derives from September 2026 local CV files; public source metadata resolves author-order discrepancies. No inferred graduate degree or invented affiliation.

## Creative direction
A blue-ink manga travel journal: the one signature image is an original vector staircase from a small sailing ship to an ancient Greek temple. Golden sun, fine engraving, open ocean create a restrained classical aesthetic. The user refined the brief to prioritize ancient Greek beauty and avoid visual clutter; comic labels and tilted photo frames were removed. The architecture represents first-principles exploration. The main name uses monumental serif typography, technical captions use monospace, prose stays quiet and readable.

## Layout and restraint
1200px reading frame, compact 56px section spacing (40px mobile), responsive 700px and 1000px breakpoints. Desktop hero pairs oversized name with a bespoke illustration. Publications use a repeated image-and-text structure. Photo compositions use aligned frames; research stays flat, without decorative dashboard cards. Mobile stacks all content and keeps navigation visible.

## Runtime mapping
`style.css :root` is the canonical runtime token source; frontmatter documents matching colors, font roles, spacing and radius. Shared publication, button, gallery and timeline classes consume these variables. SVGs are static illustrations using the same ink, wash and gold palette; tiny illustration-only grid colors are not UI tokens. No generated theme adapter. No external fonts, font swaps, tracking or third-party embed. A small dependency-free motion script adds progressive enhancement.

## Interaction and accessibility
Native anchors for every link; native details for expandable material. All functionality remains usable without JavaScript. Global scrollbar baseline, visible focus, keyboard skip link, explicit image geometry, semantic landmarks, descriptive alt text, reduced motion and forced-colors fallbacks. One-shot scroll entrance (550ms), hero arrival (1s), and hover translation give feedback without continuous motion. Reduced-motion disables all animation. Content is never hidden pending JavaScript. Hover changes color or gives slight translation; it never reveals exclusive content. Public PDF omits phone/WeChat; email is the public contact. No modal, forms or loading workflow.

## Provenance
Personal photos supplied by the owner. EvoWorld and Frontier-Eng figures come from the owner's repositories. AegisFlow uses Figure 1 extracted from the user-supplied manuscript, linked as a local PDF. Frontier-Eng public author order is used instead of the inconsistent shortened CV author line. Venue statuses follow the supplied CV. Original decorative SVGs authored for this site.

## Verification
Check desktop and mobile rendering, local image and anchor resolution, links, disclosure, keyboard focus, no horizontal overflow and reduced motion. Keep static audit and browser evidence under output. Site has no sibling routes; compare repeated publication rows and photo captions for consistency.

## Density revision
User requested stronger awards, less whitespace, fewer paragraphs and more motion. Honors now use two blue-and-gold highlights (National Scholarship / Kaggle silver), followed by compact award rows. Service shows two impact numbers and two role summaries. Experience is a 2×2 desktop grid. Publication titles and author credits remain complete; redundant summaries are removed.

## October 2026 publication video update
The current homepage uses the existing Odyssey Ink v2 layout and inline tokens in `index.html`; this supersedes the earlier stylesheet mapping above. EvoWorld's thumbnail is now a native, user-initiated 16:9 video with controls, a poster, English captions, and a direct film link. It reuses the published `/EvoWorld/static/videos/evoworld-film.mp4` asset (66 seconds) instead of duplicating the film. Filtering its publication out pauses playback. Other cards and theme behavior stay as established.

## Writing subsite
`/writing/` is a quiet editorial extension of the existing Odyssey Ink homepage: the same navy/gold palette, Cinzel identity, Cormorant headings and Source Sans body; no imitation of the supplied reference's handwritten masthead or tab boxes. Compact archive rows carry date and type; the reading page uses a 730px text column and desktop section contents. The local theme preference is shared with the homepage. The builder extracts the canonical inline palette from `index.html` into generated `writing/theme.css`; `writing/writing.css` owns only writing-specific layout rules. `scripts/build_writing.py` produces the archive, articles and RSS from Markdown. The Pages workflow publishes only `_site`, excludes draft articles and source files, and never invents sample posts. A starter draft is explicitly instructional.
