import os
import sys

from datetime import timedelta

import pandas as pd

# sys.path.append
current_dir = os.path.abspath(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from src import corona_gobals
from src import plotting_utils
from src import utils
from src.model.model import Model


class Corona(object):
    def __init__(self, model_type="simple_model"):
        self.description = "COVID-19 analysis class"
        self.globals = corona_gobals
        self.plotting_utils = plotting_utils
        self.utils = utils
        self.pull_latest_data()
        self.model = Model()

    def pull_latest_data(self, verbose=True):
        """
        Pull the latest data from ecdc

        Returns
        -------
            self.data
        """
        self.data, self.data_ingest_utc_time = self.utils.pull_latest_data(
            verbose=verbose
        )

        print("###############" "\nData Processing" "\n###############")
        self.data = self.data.sort_values(
            by=[self.globals.COUNTRY_COLUMN, self.globals.DATE_COLUMN]
        )

        # compute global numbers
        global_df = (
            self.data.groupby(self.globals.DATE_COLUMN)
            .agg({"cases": "sum", "deaths": "sum", "pop_data2018": "sum"})
            .reset_index()
        )
        global_df[self.globals.COUNTRY_COLUMN] = "Global"

        # bind it back to data
        self.data = pd.concat([self.data, global_df])

        self._integrate_numbers_by_country(input_column=self.globals.VALUE_COLUMN_LIST)

    def _integrate_numbers_by_country(self, input_column):
        """
        Numeric integration of daily values to cumulative values.

        Parameters
        ----------
        input_column: str or [str]
            columns in self.data of daily values

        Returns
        -------
            self.data[f"cumulative_{input_column}"] with int values.
        """
        print("compute cumulative values ... working ... ", end="")

        # nest str into list or keep as list
        input_column_list = self.utils.generate_list(input_column)

        for input_column in input_column_list:
            new_key = f"cumulative_{input_column}"
            for country in self.data[self.globals.COUNTRY_COLUMN].unique():
                mask = self.data[self.globals.COUNTRY_COLUMN] == country

                # use integrate_numbers to add daily values with the same 1-D array length
                self.data.loc[mask, new_key] = self.utils.integrate_numbers(
                    self.data.loc[mask, input_column]
                )
            # convert to int
            self.data[new_key] = self.data[new_key].astype(int)
        print("done.\n")

    def print_latest_case_numbers(self, day_range=3):
        """
        Print table of latest case numers

        Parameters
        ----------
        day_range: int
            How many days into the past to include values for.

        Returns
        -------
            pandas df
        """
        print(f"Case and death numbers for the last {day_range} days.")

        # compute dt with - day_range value
        max_date_min_d = self.data[self.globals.DATE_COLUMN].max() - timedelta(
            days=day_range
        )

        country_list = self.globals.COUNTRY_LIST + ["Global"]
        by_country_df = (
            # subset from data
            self.data.query(
                f"{self.globals.DATE_COLUMN} > @max_date_min_d"
                f" & {self.globals.COUNTRY_COLUMN} in @country_list"
            )
            .sort_values(
                by=["cumulative_cases", self.globals.DATE_COLUMN], ascending=False,
            )
            .reset_index()[  # extract columns of interest
                [
                    self.globals.DATE_COLUMN,
                    self.globals.COUNTRY_COLUMN,
                    "cases",
                    "cumulative_cases",
                    "deaths",
                    "cumulative_deaths",
                ]
            ]
        )

        return by_country_df

    def plot_data(self, fontsize=14, day_range=None):
        """
        Plot self.data

        Parameters
        ----------
        fontsize: int
        day_range: int (default: None)
            How many days into the past to include values for.

        Returns
        -------

        """
        initial_y_list = [
            "cases",
            "deaths",
        ]
        cumulative_y_list = ["cumulative_" + elem for elem in initial_y_list]

        # compute dt with - day_range value
        # default is to plot all time points
        if day_range is None:
            max_date_min_d = self.data[self.globals.DATE_COLUMN].min()
        else:
            max_date_min_d = self.data[self.globals.DATE_COLUMN].max() - timedelta(
                days=day_range
            )

        for y_list in [
            cumulative_y_list,
            initial_y_list,
        ]:
            country_list = self.globals.COUNTRY_LIST
            self.plotting_utils.plot_time_series(
                df=self.data.query(
                    f"{self.globals.DATE_COLUMN} > @max_date_min_d"
                    f"& {self.globals.COUNTRY_COLUMN} in @country_list"
                ),
                x=self.globals.DATE_COLUMN,
                y=y_list,
                ax_factor=self.globals.COUNTRY_COLUMN,
                fontsize=fontsize,
            )
            print("\n\n")
