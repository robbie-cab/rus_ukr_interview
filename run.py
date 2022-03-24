from charts.corn import corn_hbar, corn_map, get_corn_data


def get_corn_charts():
    df = get_corn_data()
    corn_map(df, "Exports (t)", "corn_exports.pdf")
    corn_map(df, "Imports per capita (kg)", "corn_imports.pdf")

    corn_hbar(df, "export %", "corn_exports_hbar.pdf")
    corn_hbar(df, "Imports per capita (kg)", "corn_imports_hbar.pdf")


if __name__ == "__main__":
    get_corn_charts()