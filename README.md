# datafun-04-eda

[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/)
[![Jupyter](https://img.shields.io/badge/Jupyter-notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![marimo](https://img.shields.io/badge/marimo-reactive_notebook-FF6B6B)](https://docs.marimo.io/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Exploratory data analysis of the Palmer Penguins dataset, testing whether a
> strong pooled correlation survives being split into subgroups.

## The Question

The starting example reports one correlation between flipper length and body
mass across all 344 penguins: **r = 0.871**. That reads as a very strong
relationship.

But the dataset holds three species of noticeably different size. If Gentoo
penguins are simply bigger than Adelie and Chinstrap on both measurements at
once, some of that 0.871 is a size gap between species rather than a
flipper-to-mass relationship within any of them.

This project recomputes the same correlation separately inside each species to
find out.

## Results

| Group | n | r |
|---|---|---|
| Adelie | 152 | 0.468 |
| Chinstrap | 68 | 0.642 |
| Gentoo | 124 | 0.703 |
| **Pooled** | **342** | **0.871** |

Every species falls below the pooled figure. Adelie loses almost half the
apparent relationship.

![Flipper length vs body mass, all species](docs/images/one-relationship.png)

![Flipper length vs body mass, Adelie only](docs/images/relationship-adelie.png)

The relationship is real within each species. It is just weaker than the
headline number suggests, and reporting only r = 0.871 would overstate how well
flipper length predicts body mass for any individual penguin.

The practical lesson generalizes past penguins: an aggregate statistic computed
across mixed groups can carry a between-group difference that looks like a
within-group relationship. Checking whether a pooled number holds inside its
subgroups is cheap and worth doing before reporting it.

## Method

The analysis follows a repeatable eight-step EDA process:

1. LOAD the data
2. INSPECT the data
3. CHECK data quality
4. DESCRIBE numeric variables
5. VISUALIZE distributions
6. EXPLORE relationships
7. SUMMARIZE what was found
8. DISPLAY the visualizations

Step 6 was extended with a loop that filters the DataFrame to one species at a
time and recomputes the correlation on that subgroup, producing a scatter plot
for each.

## Data

Palmer Penguins, 344 rows, one row per observed penguin. Seven columns covering
species, island, four body measurements, and sex.

Data quality notes: 11 rows are missing `sex` (3.2%), and 2 rows are missing all
four measurement columns (0.58%). No duplicate rows. See the
[Palmer Penguins Data Card](./docs/data-card.md).

## Produced Artifacts

- [**Reactive EDA App (marimo)**](https://jgdavis24.github.io/datafun-04-eda/app/)
  - run the analysis interactively in a browser

- [**Reactive EDA Notebook (marimo)**](./src/datafun/notebook.py)
  - view the Python source used to create the reactive app

- [**Jupyter Notebook**](./notebooks/eda.ipynb)
  - view the analysis in the traditional notebook format

## Skills Demonstrated

- pandas DataFrame filtering and subgroup analysis
- correlation analysis and interpretation of aggregate vs subgroup statistics
- matplotlib visualization through a reusable charting library
- structured logging to a persistent project log
- src-layout Python packaging managed with uv
- automated formatting and linting with Ruff, type checking with ty
- CI/CD through GitHub Actions with hosted documentation

## Important Folders and Files

- **src/datafun/app.py** - the analysis script and custom observations
- **src/datafun/utils_eda.py** - reusable data functions
- **docs/** - project narrative, documentation, and generated charts
- **notebooks/** - Jupyter notebook analysis
- **project.log** - run history

## Run It Yourself

```shell
git clone https://github.com/jgdavis24/datafun-04-eda
cd datafun-04-eda
code .
```

Then in a VS Code terminal:

```shell
uv sync
uv run python -m datafun.app
```

Twelve chart windows will open. Close each one to let the script finish. A
`project.log` file appears in the root folder and the terminal prints:

```shell
===================================
END main() - Executed successfully!
===================================
```

<details>
<summary>Show full command reference</summary>

```shell
uv self update
uv python pin 3.14

uv python install
uv lock --upgrade
uv sync

uv run pre-commit install
uv run pre-commit autoupdate

git add -A
uv run pre-commit run --all-files
# repeat if changes were made by pre-commit tasks
git add -A
uv run pre-commit run --all-files

# run the Python module
uv run python -m datafun.app

# run marimo nb as a reactive app
# press Ctrl + C in the terminal to exit
uv run marimo run src/datafun/notebook.py

# Or: run marimo nb as a notebook
uv run marimo edit src/datafun/notebook.py

# Also: See notebooks/ for Jupyter notebooks

# do chores
uv run ruff format .
uv run ruff check . --fix
uv run ty check
uv run python -m pytest
uv run python -m zensical build

# save progress as you work
git add -A
git commit -m "your message here"
# repeat if changes were made (try the UP ARROW)
git add -A
git commit -m "your message here"

git push -u origin main
```

</details>

## Notes on Tooling

Run **both** ruff commands before pushing. `ruff format` and `ruff check` are
different tools and passing one does not mean passing the other.

If VS Code does not use the project's `.venv`, open the Command Palette
(`Ctrl+Shift+P`) and run **Python: Select Interpreter**, then pick the
interpreter from this project's `.venv` folder. If it still does not pick up
newly installed tools, run **Developer: Reload Window**.

## Documentation

- [Documentation](https://jgdavis24.github.io/datafun-04-eda/)

## Citation

- [CITATION.cff](./CITATION.cff)

## License

This project is licensed under the [MIT License](./LICENSE).
