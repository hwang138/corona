import copy

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

        print(
            "###############"
            "\nData Processing"
            "\n###############"
        )
        self.data = self.data.sort_values(
            by=[corona_gobals.COUNTRY_COLUMN, corona_gobals.DATE_COLUMN]
        )
        self._compute_per_capita_values(
            value_column_list=self.corona_gobals.VALUE_COLUMN_LIST
        )

        self._integrate_numbers_by_country(input_column=self.value_column_list)

    def _compute_per_capita_values(self, value_column_list):
        print("compute per capita values ... working ... ", end="")
        new_value_column_list = copy.copy(value_column_list)
        for key in value_column_list:
            new_key = f"{key}_per_capita"
            self.data[new_key] = self.data.apply(
                lambda x: x[key] / x[corona_gobals.CAPITA_COLUMN], axis=1
            )
            new_value_column_list.append(new_key)
        self.value_column_list = new_value_column_list
        print("done.\n")

    def _integrate_numbers_by_country(self, input_column):
        print("compute cumulative values ... working ... ", end="")

        input_list = self.utils.generate_list(input_column)

        for country in self.data[corona_gobals.COUNTRY_COLUMN].unique():
            mask = self.data[corona_gobals.COUNTRY_COLUMN] == country
            for input in input_list:
                self.data.loc[
                    mask, f"cumulative_{input}"
                ] = self.utils.integrate_numbers(self.data.loc[mask, input])
        print("done.\n")

    def plot_data(self, fontsize=14):
        initial_y_list = [
            "cases",
            "deaths",
        ]
        per_cap_y_list = [elem + "_per_capita" for elem in initial_y_list]
        cumulative_y_list = ["cumulative_" + elem for elem in initial_y_list]
        cumulative_per_cap_y_list = [elem + "_per_capita" for elem in cumulative_y_list]

        for y_list in [
            cumulative_y_list,
            cumulative_per_cap_y_list,
            initial_y_list,
            per_cap_y_list,
        ]:
            subset_country_list = [
                "United_States_of_America",
                "Taiwan",
                "Italy",
                "Spain",
                "Germany",
                "China",
            ]
            self.plotting_utils.plot_time_series(
                data=self.data.query("countries_and_territories in @subset_country_list"),
                x="date",
                y=y_list,
                ax_factor="countries_and_territories",
                fontsize=fontsize,
            )
            print("\n\n")
