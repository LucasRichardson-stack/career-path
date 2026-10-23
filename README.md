# Career Path

Presenter-friendly web page for Lucas Richardson’s guest talk to a robotics class at Kettering University. Eight career stops on a curved 3D carousel, each themed to the organization.

**Live site:** [https://lucasrichardson-stack.github.io/career-path/](https://lucasrichardson-stack.github.io/career-path/)

## Open locally

```bash
python3 -m http.server 4317
```

Then open http://127.0.0.1:4317/

Any static file server works from the repo root so `media/logos/` resolves.

## Layout

```
index.html              # page (CSS, markup, JS)
media/logos/            # org logo PNGs
CAREER_PAGE.md          # technical brief
PROJECT_HISTORY.md      # how the project evolved
```

See `CAREER_PAGE.md` for editing stop content (`STOPS`), known fixes, and the planned media viewer.
