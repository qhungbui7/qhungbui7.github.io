# qhungbui7.github.io

Research-focused personal website for Quoc Hung BUI, published with GitHub Pages at [qhungbui7.github.io](https://qhungbui7.github.io/).

The site presents selected research in reinforcement learning, autonomous driving, scientific computing, and robotics. Its project media comes from repository artifacts and locally reproduced model checkpoints.

## Editing content

Edit [`content.json`](content.json) to update the introduction, portrait, project cards, work experience, education, publications, contact details, and footer. The JSON is the source of truth; `index.html` is the generated static page.

After editing the JSON, regenerate the page:

```bash
python3 build_site.py
```

The generated HTML contains the visible content directly, so the site does not depend on JavaScript or a loading state.

Local images and animations belong in `files/`. After replacing an asset, update its `src` in `content.json` and remove superseded files that are no longer referenced.

## Local preview

Because browsers block JSON loading from a direct `file://` URL, preview the site through a local server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/`.

## Deployment

The repository is deployed from the `main` branch as a GitHub Pages user site. Regenerate `index.html`, review the result, and push the reviewed changes to `main`; GitHub Pages then serves the repository root at `https://qhungbui7.github.io/`.

There is intentionally no `CNAME` file because the site uses the standard `.github.io` address.

`changelog.md` is a local working record and is intentionally excluded from Git.
