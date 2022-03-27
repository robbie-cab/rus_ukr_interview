from charts.corn import corn_hbar, corn_map, get_corn_data
from charts.gas import gas_map
from charts.rub import rub_chart
from data.econ import gas_imports


def get_corn_charts():
    df = get_corn_data()
    corn_map(df, "Exports (t)", "corn_exports.pdf")
    corn_map(df, "Imports per capita (kg)", "corn_imports.pdf")

    corn_hbar(df, "export %", "corn_exports_hbar.pdf")
    corn_hbar(df, "Imports per capita (kg)", "corn_imports_hbar.pdf")


def gas_map_series():
    df = gas_imports()

    first = set(["Finland", "Estonia", "Latvia", "Bulgaria", "Austria"])
    second = first | set(["Germany", "France"])

    gas_map(df, "russian_gas", "gas_map0.pdf", countries=set())
    gas_map(df, "russian_gas", "gas_map1.pdf", countries=first)
    gas_map(df, "russian_gas", "gas_map2.pdf", countries=second)
    gas_map(df, "russian_gas", "gas_map3.pdf")


if __name__ == "__main__":
    get_corn_charts()
    gas_map_series()
    rub_chart("ruble.pdf")
