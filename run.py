from charts.corn import corn_hbar, corn_map, get_corn_data
from charts.gas import gas_map, gas_map_series
from charts.rub import rub_chart
from data.econ import gas_imports


def get_corn_charts():
    df = get_corn_data()
    corn_map(df, "Exports (t)", "corn_exports.pdf")
    corn_map(df, "Imports per capita (kg)", "corn_imports.pdf")

    corn_hbar(df, "export %", "corn_exports_hbar.pdf")
    corn_hbar(df, "Imports per capita (kg)", "corn_imports_hbar.pdf")


def get_gas_charts():
    df = gas_imports()
    print(df)
    gas_map(df, "russian_gas", "gas_map.pdf")


if __name__ == "__main__":
    # get_corn_charts()
    gas_map_series()
    # rub_chart("ruble.pdf")
