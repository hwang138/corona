import datetime
import re

import pandas as pd


def pull_latest_data(
    verbose=True, uri="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv",
):
    """
    Pull the latest dataset from ecdc.

    Parameters
    ----------
    verbose: bool (default: True)
    uri: http str
        location of latest dataset

    Returns
    -------
        pandas df
    """
    dt_string = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if verbose:
        print(
            "############"
            "\nData Ingest"
            "\n############"
            f"\nUTC date and time: {dt_string}"
            f"\nDataset pulled from: {uri}\n"
        )

    df = pd.read_csv(uri)
    df = correct_date_format(
        df=df, input_column="dateRep", input_format="%d/%m/%Y", output_column="date"
    )
    df = convert_camel_case(df=df)
    return df, dt_string


def correct_date_format(df, input_column, input_format, output_column):
    """
    Correct dt format to dt

    Parameters
    ----------
    df: pandas df
    input_column: str
        input date column name
    input_format: str
        input date format str
    output_column: str
        output column name

    Returns
    -------
        df[{output_column}]
    """
    df[output_column] = df[input_column].apply(
        lambda x: datetime.datetime.strptime(x, input_format)
    )
    return df


def convert_camel_case(df):
    """
    Convert all header from camelCase ot lower_under_score_case.

    Parameters
    ----------
    df: pandas df

    Returns
    -------
        The same df
    """

    key_list = list(df.keys())
    rename_dict = {}
    for key in key_list:
        rename_dict[key] = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
    return df.rename(columns=rename_dict)


def integrate_numbers(array):
    """
    Integrate an 1-d array into a 1-d array of the same length, but with sequential accumulation.

    Parameters
    ----------
    array: 1-d numeric array

    Returns
    -------
        1-d numeirc array
    """
    integrated_array = None
    for elem in array:
        if integrated_array is None:
            integrated_array = [elem]
        else:
            integrated_array.append(integrated_array[-1] + elem)
    return integrated_array


def generate_list(str):
    """
    Identify if an obj is a str or [str] and return a [str].

    Parameters
    ----------
    str: str or [str]

    Returns
    -------
        [str]
    """
    if type(str) is not list:
        str_list = [str]
    else:
        str_list = str
    return str_list
