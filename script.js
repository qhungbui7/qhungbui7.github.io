const element = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};

const addLink = (parent, link, className = "") => {
  const anchor = element("a", className, link.label);
  anchor.href = link.href;
  parent.append(anchor);
};

const renderHero = (hero) => {
  const container = document.querySelector("#hero");
  const copy = element("div", "hero-copy");
  copy.append(
    element("p", "eyebrow", hero.eyebrow),
    element("h1", "", hero.title),
    element("p", "intro", hero.description)
  );
  const links = element("div", "links");
  hero.links.forEach((link) => addLink(links, link));
  copy.append(links);
  container.replaceChildren(copy);
  if (hero.portrait) {
    const portrait = element("img", "portrait");
    portrait.src = hero.portrait.src;
    portrait.alt = hero.portrait.alt;
    portrait.width = 190;
    portrait.height = 238;
    container.append(portrait);
  }
};

const renderProjects = (research) => {
  document.querySelector("#research-eyebrow").textContent = research.eyebrow;
  document.querySelector("#research-note").textContent = research.note;
  const list = document.querySelector("#research-list");
  research.projects.forEach((project) => {
    const article = element("article", `research-item${project.compactMedia ? " text-only" : ""}`);
    const copy = element("div", "research-text");
    copy.append(
      element("p", "project-type", project.type),
      element("h2", "", project.title),
      element("p", "", project.description)
    );
    addLink(copy, { label: "Repository ↗", href: project.repository });
    article.append(copy);

    const artifacts = project.artifacts || (project.artifact ? [project.artifact] : []);
    if (artifacts.length) {
      const gallery = element("div", artifacts.length > 1 ? "artifact-gallery" : "artifact-gallery single");
      artifacts.forEach((artifact) => {
        const media = element("div", "artifact");
        const image = element("img");
        image.src = artifact.src;
        image.alt = artifact.alt;
        image.loading = "lazy";
        media.append(image);
        if (artifact.caption) media.append(element("p", "artifact-caption", artifact.caption));
        gallery.append(media);
      });
      article.append(gallery);
    }
    list.append(article);
  });
};

const renderExperience = (items) => {
  const block = element("div", "resume-block");
  block.append(element("h2", "", "Experience"));
  items.forEach((item) => {
    const row = element("div", "resume-row");
    const copy = element("div", "resume-copy");
    copy.append(
      element("h3", "", item.role),
      element("p", "resume-meta", `${item.company} · ${item.location}`),
      element("p", "resume-description", item.description)
    );
    row.append(copy, element("time", "", item.period));
    block.append(row);
  });
  return block;
};

const renderEducation = (items) => {
  const block = element("div", "resume-block");
  block.append(element("h2", "", "Education"));
  items.forEach((item) => {
    const row = element("div", "resume-row");
    const copy = element("div", "resume-copy");
    copy.append(element("h3", "", item.degree), element("p", "resume-meta", item.institution));
    const main = element("div", "education-main");
    if (item.logo) {
      const logo = element("img", "university-logo");
      logo.src = item.logo.src;
      logo.alt = item.logo.alt;
      logo.loading = "lazy";
      logo.width = 90;
      logo.height = 44;
      main.append(logo);
    }
    main.append(copy);
    row.append(main, element("time", "", item.period));
    block.append(row);
  });
  return block;
};

const renderPublications = (items) => {
  const block = element("div", "resume-block publications");
  block.append(element("h2", "", "Publications"));
  items.forEach((item) => {
    const publication = element("p");
    publication.append(document.createTextNode(`“${item.title}” `), element("em", "", item.venue));
    block.append(publication);
  });
  return block;
};

const renderBackground = (background) => {
  document.querySelector("#background-eyebrow").textContent = background.eyebrow;
  document.querySelector("#background-note").textContent = background.note;
  document.querySelector("#background-content").replaceChildren(
    renderExperience(background.experience),
    renderEducation(background.education),
    renderPublications(background.publications)
  );
};

const renderContact = (contact) => {
  const email = element("a", "email", contact.email);
  email.href = `mailto:${contact.email}`;
  document.querySelector("#contact").replaceChildren(
    element("p", "eyebrow", contact.eyebrow),
    element("h2", "", contact.name),
    element("p", "intro", contact.description),
    email
  );
};

const renderSite = (content) => {
  document.title = content.site.title;
  document.querySelector("#meta-description").content = content.site.description;
  document.querySelector("#brand").textContent = content.site.brand;
  const navigation = document.querySelector("#nav-links");
  content.site.navigation.forEach((link) => addLink(navigation, link));
  renderHero(content.hero);
  renderProjects(content.research);
  renderBackground(content.background);
  renderContact(content.contact);
  document.querySelector("#footer").replaceChildren(...content.footer.map((item) => element("span", "", item)));
};

const showLoadError = (error) => {
  console.error(error);
  document.querySelector("#hero").replaceChildren(
    element("p", "eyebrow", "Content unavailable"),
    element("h1", "", "The portfolio could not be loaded."),
    element("p", "intro", "Check that content.json is valid and serve this folder through a local web server.")
  );
};

fetch("content.json", { cache: "no-cache" })
  .then((response) => {
    if (!response.ok) throw new Error(`content.json returned ${response.status}`);
    return response.json();
  })
  .then(renderSite)
  .catch(showLoadError);
