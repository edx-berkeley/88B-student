# DATA 88B Jupyter Notebook Materials

Public lab notebooks for **DATA 88B: Economic Analysis for Business Decisions** (edX xSeries).

This repository mirrors the [Data 8 materials-sp26](https://github.com/data-8/materials-sp26) layout: a Jupyter Book site with lab notebooks organized by course part.

## Contents

- **Part 1** (`lab/1/`): 7 labs — data management through simulation
- **Part 2** (`lab/2/`): 8 labs — hypothesis tests through chi-squared tests
- **Part 3** (`lab/3/`): 5 labs — linear regression through interaction

Student-facing notebooks are sourced from [88B-student](https://github.com/edx-berkeley/88B-student).

## Local development

```bash
pip install -r requirements.txt
jupyter lab
```

Open **http://localhost:8888/lab** and navigate to notebooks under `lab/`.

## Enable Binder (after pushing to GitHub)

Binder requires the repo to have a `main` branch on GitHub. Once pushed, change `myst.yml`:

```yaml
  jupyter:
    binder:
      repo: edx-berkeley/88B-student
      ref: main
      url: https://mybinder.org
    kernelName: python3
```

Then rebuild: `jupyter-book build --html`

## Build the book site

```bash
npm install -g jupyter-book
jupyter-book build --html
```

The built site is in `_build/html/`.

## Related courses

- [88C materials](https://github.com/edx-berkeley/88c_jupyternotebook) (when available)
- [88E materials](https://github.com/edx-berkeley/88e_jupyternotebook) (when available)
