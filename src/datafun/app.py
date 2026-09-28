"""src/datafun/app.py - Project script.

Author: Josiah Davis
Date: 2026-09

RUN:

Open this project folder in VS Code.
Open an integrated Terminal in the root project folder
and paste the following command.

uv run python -m datafun.app

DOMAIN: Penguins

Explore a dataset of penguins using a simple,
repeatable exploratory data analysis (EDA) process.

CUSTOM PROBLEM:

The example reports a single correlation between flipper length
and body mass for all penguins together (r = 0.871). This project
asks whether that number holds up when the penguins are separated
by species, or whether the strong overall relationship is partly
an artifact of pooling three different-sized species into one
group.

EDA:

Exploratory Data Analysis helps us understand a new dataset.
A simple EDA process is:

1. LOAD the data.
2. INSPECT the data.
3. CHECK data quality.
4. DESCRIBE numeric variables.
5. VISUALIZE distributions.
6. EXPLORE relationships.
7. SUMMARIZE what you found.
8. DISPLAY the visualizations.

DESIGN:

Use this file to document your analysis
and orchestrate the work.

The reusable functions that do the data work live in utils_eda.py.
Reusable visualization functions come from eda-vizkit.
We import functions and pass in what they need.

SKILLS:

This project illustrates several core Python and analytics skills:

- calling functions in another file
- passing information to functions
- working with pandas DataFrames
- filtering a DataFrame to a subgroup
- looping over groups to compare results
- exploratory data analysis

"""

# === DECLARE IMPORTS (BRING IN FREE CODE) ===

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header
from eda_vizkit import (
    save_chart,
    show_categorical_distribution,
    show_missing_values,
    show_numeric_distribution,
    show_numeric_relationship,
)
import matplotlib.pyplot as plt
import pandas as pd

from datafun.utils_eda import (
    build_data_dictionary,
    get_correlation,
    get_duplicate_count,
    get_missing_counts,
    get_numeric_summary,
    inspect,
    load_data,
)

# === CONFIGURE LOGGER ONCE FOR THE APPLICATION ===

LOG: logging.Logger = get_logger("P04", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

# Some global variables are CONSTANT.
# They do NOT change while the program runs.
# By convention, constants use UPPERCASE_WITH_UNDERSCORES.
# Final indicates that the value should not be reassigned.

CHART_DIR: Final[Path] = Path("docs") / "images"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# === DEFINE THE DATASET ===

DATASET_NAME: Final[str] = "penguins"

# === DETERMINE WHAT ONE ROW REPRESENTS ===

# This is the GRAIN of the dataset.
# Grain answers:
# What does one row represent?

GRAIN: Final[str] = "one observed penguin"

# === CHOOSE IMPORTANT NUMERIC VARIABLES ===

# These are continuous numeric variables
# we want to inspect during EDA.

NUMERIC_COLUMNS: Final[list[str]] = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

# === CHOOSE IMPORTANT CATEGORICAL VARIABLES ===

CATEGORICAL_COLUMNS: Final[list[str]] = [
    "species",
    "island",
    "sex",
]

# === CHOOSE ONE RELATIONSHIP TO EXPLORE ===

X_COLUMN: Final[str] = "flipper_length_mm"
Y_COLUMN: Final[str] = "body_mass_g"

# === CUSTOM: CHOOSE A COLUMN TO SPLIT THE ANALYSIS BY ===

# The example computes one correlation for all rows together.
# This column lets us recompute that same correlation
# separately within each group.

GROUP_COLUMN: Final[str] = "species"


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """The main entry point where execution begins.

    Arguments:
        None.

    Returns:
        None.
    """
    log_header(LOG, "P04 - EXPLORATORY DATA ANALYSIS")

    LOG.info("===================================")
    LOG.info("START main()")
    LOG.info("===================================")

    LOG.info("-------------------------------")
    LOG.info("01. LOAD the data.")
    LOG.info("-------------------------------")

    df: pd.DataFrame = load_data(
        dataset_name=DATASET_NAME,
        log=LOG,
    )

    LOG.info("-------------------------------")
    LOG.info("02. INSPECT the data.")
    LOG.info("-------------------------------")

    inspection_string: str = inspect(
        df=df,
        grain=GRAIN,
        log=LOG,
    )

    LOG.info(inspection_string)

    LOG.info("-------------------------------")
    LOG.info("03. CHECK data quality.")
    LOG.info("-------------------------------")

    # Call the imported function build_data_dictionary()
    # to create a starter data dictionary.
    # Pass in the df and the logger.

    data_dictionary: pd.DataFrame = build_data_dictionary(
        df=df,
        log=LOG,
    )
    LOG.info(f"\n{data_dictionary}")

    # Call the imported function get_missing_counts()
    # to count missing values in each column.
    # Pass in the df and the logger.
    missing_counts: pd.Series = get_missing_counts(
        df=df,
        log=LOG,
    )

    LOG.info(f"\nMissing values:\n{missing_counts}")

    # Call the imported function get_duplicate_count()
    # to count duplicate rows.
    # Pass in the df and the logger.
    duplicate_count: int = get_duplicate_count(
        df=df,
        log=LOG,
    )

    LOG.info(f"Duplicate rows: {duplicate_count}")

    # Call the imported function show_missing_values()
    # to visualize missing values.
    # Pass in the df.
    # get back the Axes object so we can save the chart.
    missing_ax = show_missing_values(df)

    # Save the missing values chart to the designated directory.
    save_chart(
        missing_ax,
        CHART_DIR / "missing-values.png",
    )

    LOG.info("-------------------------------")
    LOG.info("04. DESCRIBE numeric variables.")
    LOG.info("-------------------------------")

    numeric_summary: pd.DataFrame = get_numeric_summary(
        df=df,
        numeric_columns=NUMERIC_COLUMNS,
        log=LOG,
    )

    LOG.info(f"\n{numeric_summary}")

    LOG.info("-------------------------------")
    LOG.info("05. VISUALIZE distributions.")
    LOG.info("-------------------------------")

    # For each column in the list of numeric columns,
    # call the imported function show_numeric_distribution()
    # to visualize the distribution of the column.

    for column in NUMERIC_COLUMNS:
        numeric_ax = show_numeric_distribution(
            df,
            column=column,
        )

        # Save the numeric distribution chart to the designated directory.
        save_chart(
            numeric_ax,
            CHART_DIR / f"{column}-distribution.png",
        )

    # For each column in the list of categorical columns,
    # call the imported function show_categorical_distribution()
    # to visualize the distribution of the column.

    for column in CATEGORICAL_COLUMNS:
        categorical_ax = show_categorical_distribution(df, column=column)

        # Save the categorical distribution chart to the designated directory.
        save_chart(
            categorical_ax,
            CHART_DIR / f"{column}-distribution.png",
        )

    LOG.info("-------------------------------")
    LOG.info("06. EXPLORE relationships (e.g., between 2 numeric variables).")
    LOG.info("-------------------------------")

    # Call the imported function get_correlation()
    # to compute the correlation between the two selected numeric variables.
    # Pass in the df, the x column, the y column, and the log.

    correlation: float = get_correlation(
        df=df,
        x=X_COLUMN,
        y=Y_COLUMN,
        log=LOG,
    )

    LOG.info(f"Correlation between {X_COLUMN} and {Y_COLUMN}: {correlation:.3f}")

    # Call the imported function show_numeric_relationship()
    # to visualize the relationship between two numeric variables.
    # Pass in the df, the x column, the y column.
    # It returns a Matplotlib Axes object representing the plot.
    relationship_ax = show_numeric_relationship(
        df,
        x=X_COLUMN,
        y=Y_COLUMN,
    )

    # CUSTOM: Analyst must customize the Matplotlib Axes object with a title and axis labels.
    relationship_ax.set_title("Penguin Flipper Length vs. Body Mass (All Species)")
    relationship_ax.set_xlabel("Flipper Length (mm)")
    relationship_ax.set_ylabel("Body Mass (g)")

    save_chart(
        relationship_ax,
        CHART_DIR / "one-relationship.png",
    )

    # === CUSTOM: RECOMPUTE THE SAME RELATIONSHIP WITHIN EACH GROUP ===

    # The correlation above pools all three species together.
    # Loop over each species, filter the DataFrame to that species,
    # and compute the same correlation on that subgroup only.

    LOG.info("-------------------------------")
    LOG.info(f"06b. CUSTOM: same relationship, split by {GROUP_COLUMN}.")
    LOG.info("-------------------------------")

    group_names: list[str] = sorted(df[GROUP_COLUMN].dropna().unique())

    for group_name in group_names:
        group_df: pd.DataFrame = df[df[GROUP_COLUMN] == group_name]

        group_correlation: float = get_correlation(
            df=group_df,
            x=X_COLUMN,
            y=Y_COLUMN,
            log=LOG,
        )

        LOG.info(
            f"{group_name}: n={len(group_df)}, "
            f"r={group_correlation:.3f} "
            f"(pooled r={correlation:.3f})"
        )

        group_ax = show_numeric_relationship(
            group_df,
            x=X_COLUMN,
            y=Y_COLUMN,
        )

        group_ax.set_title(f"Flipper Length vs. Body Mass - {group_name} only")
        group_ax.set_xlabel("Flipper Length (mm)")
        group_ax.set_ylabel("Body Mass (g)")

        save_chart(
            group_ax,
            CHART_DIR / f"relationship-{group_name.lower()}.png",
        )

    LOG.info("-------------------------------")
    LOG.info("07. SUMMARIZE what you found.")
    LOG.info("-------------------------------")

    # Run this app first.
    # Get some insights into data.
    # After seeing the information, record your CUSTOM observations
    # in a simple multi-line (triple-quoted) raw string (see the leading `r`).

    LOG.info(r"""CUSTOM OBSERVATIONS:
    Pooled across all three species, flipper length and body mass
    correlate at r = 0.871, which reads as a very strong relationship.

    Recomputing that same correlation inside each species drops it
    every time:

        Adelie      n=152   r = 0.468
        Chinstrap   n=68    r = 0.642
        Gentoo      n=124   r = 0.703
        pooled      n=342   r = 0.871

    Adelie loses almost half the apparent relationship. None of the
    three species reaches the pooled number.

    The pooled figure is inflated because Gentoo penguins are larger
    than Adelie and Chinstrap on both measurements at once. Pooling
    the species turns that between-species size gap into what looks
    like a flipper-to-mass relationship.

    The relationship is real within each species, just weaker than
    the headline number suggests. Reporting only r = 0.871 would
    overstate how well flipper length predicts body mass for any
    individual penguin.
    """)

    LOG.info("-------------------------------")
    LOG.info("08. DISPLAY the charts.")
    LOG.info("-------------------------------")

    # eda-vizkit just returns Matplotlib Axes objects.
    # The client (like this script or a marimo notebook),
    # determines how and when to display the plots).

    LOG.info("In a script, call plt.show() at the end to display all charts.")
    LOG.info("Close all chart windows (with the close button) to continue.")

    plt.show()

    LOG.info("===================================")
    LOG.info("END main() - Executed successfully!")
    LOG.info("===================================")


# === CONDITIONAL EXECUTION GUARD ===

# WHY: If this file is run as a script, call main().
#
# If another file imports this module,
# Python can reuse its definitions without automatically
# running the entire analysis.

if __name__ == "__main__":
    main()
