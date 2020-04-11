from datetime import timedelta
from corona.src import corona_gobals
from corona.src import plotting_utils
from corona.src import utils


class Corona(object):
    def __init__(self):
        self.description = "COVID-19 analysis class"
        self.corona_gobals = corona_gobals
        self.plotting_utils = plotting_utils
        self.utils = utils
        self.pull_latest_data()

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
            by=[corona_gobals.COUNTRY_COLUMN, corona_gobals.DATE_COLUMN]
        )

        self._integrate_numbers_by_country(
            input_column=self.corona_gobals.VALUE_COLUMN_LIST
        )

    def _integrate_numbers_by_country(self, input_column):
        print("compute cumulative values ... working ... ", end="")

        input_column_list = self.utils.generate_list(input_column)
        new_value_column_list = []

        for input in input_column_list:
            new_key = f"cumulative_{input}"
            new_value_column_list.append(new_key)

            for country in self.data[corona_gobals.COUNTRY_COLUMN].unique():
                mask = self.data[corona_gobals.COUNTRY_COLUMN] == country
                self.data.loc[
                    mask, f"cumulative_{input}"
                ] = self.utils.integrate_numbers(self.data.loc[mask, input])
            self.data[new_key] = self.data[new_key].astype(int)
        self.value_column_list = input_column_list + new_value_column_list
        print("done.\n")

    def print_latest_case_numbers(self, day_range=3):
        print(f"Case and death numbers for the last {day_range} days.")
        max_date_min_d = self.data[self.corona_gobals.DATE_COLUMN].max() - timedelta(
            days=day_range
        )
        country_list = self.corona_gobals.COUNTRY_LIST
        return (
            self.data.query(
                f"{self.corona_gobals.DATE_COLUMN} > @max_date_min_d"
                f" & {self.corona_gobals.COUNTRY_COLUMN} in @country_list"
            )
            .reset_index()
            .sort_values(by=[self.corona_gobals.COUNTRY_COLUMN, self.corona_gobals.DATE_COLUMN], ascending=False)[
                [
                    self.corona_gobals.DATE_COLUMN,
                    self.corona_gobals.COUNTRY_COLUMN,
                    "cases",
                    "cumulative_cases",
                    "deaths",
                    "cumulative_deaths",
                ]
            ]
        )

    def plot_data(self, fontsize=14):
        initial_y_list = [
            "cases",
            "deaths",
        ]
        cumulative_y_list = ["cumulative_" + elem for elem in initial_y_list]

        for y_list in [
            cumulative_y_list,
            initial_y_list,
        ]:
            country_list = self.corona_gobals.COUNTRY_LIST

            self.plotting_utils.plot_time_series(
                data=self.data.query(f"{self.corona_gobals.COUNTRY_COLUMN} in @country_list"),
                x="date",
                y=y_list,
                ax_factor="countries_and_territories",
                fontsize=fontsize,
            )
            print("\n\n")
