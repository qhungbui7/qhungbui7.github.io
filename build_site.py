"""Render the editable content.json into the static GitHub Pages index.html."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT_PATH = ROOT / "content.json"
OUTPUT_PATH = ROOT / "index.html"
STYLESHEET = "styles.css?v=20260912-4"


def text(value: object) -> str:
    return escape(str(value), quote=True)


def href(value: object) -> str:
    return text(value)


def link(link_data: dict[str, str], *, class_name: str = "") -> str:
    classes = f' class="{text(class_name)}"' if class_name else ""
    external = str(link_data["href"]).startswith(("http://", "https://"))
    target = ' target="_blank" rel="noreferrer"' if external else ""
    return f'<a{classes} href="{href(link_data["href"])}"{target}>{text(link_data["label"])}</a>'


def artifact_markup(project: dict[str, object]) -> str:
    artifacts = project.get("artifacts") or ([project["artifact"]] if project.get("artifact") else [])
    if not artifacts:
        return ""
    gallery_class = "artifact-gallery" if len(artifacts) > 1 else "artifact-gallery single"
    media = []
    for artifact in artifacts:
        caption = (
            f'<p class="artifact-caption">{text(artifact["caption"])}</p>'
            if artifact.get("caption")
            else ""
        )
        media.append(
            "<div class=\"artifact\">"
            f'<img src="{href(artifact["src"])}" alt="{text(artifact["alt"])}" loading="lazy">'
            f"{caption}</div>"
        )
    return f'<div class="{gallery_class}">' + "".join(media) + "</div>"


def project_markup(project: dict[str, object], index: int) -> str:
    extra_class = " text-only" if project.get("compactMedia") else ""
    parity_class = " project-even" if index % 2 else ""
    details = []
    if project.get("approach"):
        details.append(
            f'<div class="project-detail"><span>Approach</span><p>{text(project["approach"])}</p></div>'
        )
    if project.get("focus"):
        details.append(
            f'<div class="project-detail"><span>Focus</span><p>{text(project["focus"])}</p></div>'
        )
    details_markup = f'<div class="project-details">{"".join(details)}</div>' if details else ""
    return (
        f'<article class="research-item{extra_class}{parity_class}">'
        '<div class="research-text">'
        f'<p class="project-type">{text(project["type"])}</p>'
        f'<h3>{text(project["title"])}</h3>'
        f'<p>{text(project["description"])}</p>'
        f"{details_markup}"
        f'<p class="project-links">{link({"label": "Repository ↗", "href": project["repository"]})}</p>'
        "</div>"
        f"{artifact_markup(project)}"
        "</article>"
    )


def section(heading: str, note: str, body: str, section_id: str) -> str:
    return (
        f'<section class="section container" id="{text(section_id)}">'
        '<div class="section-heading">'
        f'<p class="eyebrow">{text(heading)}</p>'
        f'<p class="section-note">{text(note)}</p>'
        "</div>"
        f'<div class="section-body">{body}</div>'
        "</section>"
    )


def project_group(label: str, projects: list[dict[str, object]], start_index: int) -> str:
    rendered = "".join(
        project_markup(project, index)
        for index, project in enumerate(projects, start=start_index)
    )
    return (
        '<div class="research-subsection">'
        f'<p class="subheading">{text(label)}</p>'
        f'<div class="research-list">{rendered}</div>'
        '</div>'
    )


def render(content: dict[str, object]) -> str:
    site = content["site"]
    hero = content["hero"]
    research = content["research"]
    background = content["background"]
    base_url = str(site["url"]).rstrip("/")
    portrait = hero.get("portrait", {})
    social_image = portrait.get("src", "")
    if social_image and not str(social_image).startswith("http"):
        social_image = f"{base_url}/{str(social_image).lstrip('/')}"

    navigation = "".join(link(item) for item in site["navigation"])
    hero_links = "".join(link(item) for item in hero["links"])
    portrait_markup = (
        f'<img class="portrait" src="{href(portrait["src"])}" alt="{text(portrait["alt"])}" width="190" height="238">'
        if portrait
        else ""
    )
    interests = "".join(f'<span>{text(item)}</span>' for item in research.get("interests", []))
    core_projects = [project for project in research["projects"] if project.get("section") == "core"]
    technical_projects = [project for project in research["projects"] if project.get("section") == "technical"]

    research_body = (
        f'<div class="research-interests"><p class="subheading">Research interests</p>'
        f'<div class="interest-list">{interests}</div></div>'
        f'{project_group("Core research", core_projects, 0)}'
        f'{project_group("Selected technical work", technical_projects, len(core_projects))}'
    )

    publication_items = []
    for publication in background["publications"]:
        pub_links = " ".join(link(item) for item in publication.get("links", []))
        links_markup = f'<p class="publication-links">{pub_links}</p>' if pub_links else ""
        publication_items.append(
            '<article class="publication">'
            f'<p class="publication-authors">{text(publication["authors"])}</p>'
            f'<h3>{text(publication["title"])}</h3>'
            f'<p class="publication-venue">{text(publication["venue"])}</p>'
            f"{links_markup}</article>"
        )

    experience_items = []
    for item in background["experience"]:
        experience_items.append(
            '<article class="resume-row">'
            '<div class="resume-copy">'
            f'<h3>{text(item["role"])}</h3>'
            f'<p class="resume-meta">{text(item["company"])} · {text(item["location"])}</p>'
            f'<p class="resume-description">{text(item["description"])}</p>'
            "</div>"
            f'<time>{text(item["period"])}</time>'
            "</article>"
        )

    education_items = []
    for item in background["education"]:
        logo = item.get("logo")
        logo_markup = (
            f'<img class="university-logo" src="{href(logo["src"])}" alt="{text(logo["alt"])}" loading="lazy" width="90" height="44">'
            if logo
            else ""
        )
        status = f'<span class="status">{text(item["status"])}</span>' if item.get("status") else ""
        education_items.append(
            '<article class="resume-row">'
            '<div class="education-main">'
            f"{logo_markup}"
            '<div class="resume-copy">'
            f'<h3>{text(item["degree"])}</h3>'
            f'<p class="resume-meta">{text(item["institution"])} {status}</p>'
            "</div></div>"
            f'<time>{text(item["period"])}</time>'
            "</article>"
        )

    contact = content["contact"]
    footer = "".join(f"<span>{text(item)}</span>" for item in content["footer"])
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{text(site["description"])}">
    <meta name="theme-color" content="#fafaf7">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{text(site["title"])}">
    <meta property="og:description" content="{text(site["description"])}">
    <meta property="og:url" content="{href(site["url"])}">
    <meta property="og:image" content="{href(social_image)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{text(site["title"])}">
    <meta name="twitter:description" content="{text(site["description"])}">
    <meta name="twitter:image" content="{href(social_image)}">
    <link rel="canonical" href="{href(site["url"])}">
    <title>{text(site["title"])}</title>
    <link rel="stylesheet" href="{STYLESHEET}">
  </head>
  <body>
    <header class="site-header">
      <nav class="nav container" aria-label="Main navigation">
        <a class="brand" href="#top">{text(site["brand"])}</a>
        <div class="nav-links">{navigation}</div>
      </nav>
    </header>
    <main id="top">
      <section class="hero container" aria-labelledby="hero-title">
        <div class="hero-copy">
          <p class="eyebrow">{text(hero["eyebrow"])}</p>
          <h1 id="hero-title">{text(hero["title"])}</h1>
          <p class="intro">{text(hero["description"])}</p>
          <div class="links">{hero_links}</div>
        </div>
        {portrait_markup}
      </section>
      {section(research["eyebrow"], research["note"], research_body, "research")}
      {section("Publications", "Selected academic work", f'<div class="publication-list">{"".join(publication_items)}</div>', "publications")}
      {section("Experience", "Research and engineering", f'<div class="resume-block">{"".join(experience_items)}</div>', "experience")}
      {section("Education", "Academic background", f'<div class="resume-block">{"".join(education_items)}</div>', "education")}
      <section class="contact container" id="contact">
        <p class="eyebrow">{text(contact["eyebrow"])}</p>
        <h2>{text(contact["name"])}</h2>
        <p class="intro">{text(contact["description"])}</p>
        <a class="email" href="mailto:{href(contact["email"])}">{text(contact["email"])}</a>
      </section>
    </main>
    <footer class="site-footer container">{footer}</footer>
  </body>
</html>
'''


def main() -> None:
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    OUTPUT_PATH.write_text(render(content), encoding="utf-8")
    print(f"Rendered {OUTPUT_PATH.name} from {CONTENT_PATH.name}")


if __name__ == "__main__":
    main()
