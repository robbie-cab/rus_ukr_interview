# Visualisations on economic sanctions in the Russia Ukraine War

Data is collected and cached in `data/`. 

Static data sources are in `data/resources/`:

- Corn imports and exports - [Our World in Data](https://ourworldindata.org/explorers/global-food)
- Gas imports from Russia - [ACER Electricity and gas information system](https://aegis.acer.europa.eu/chest/dataitems/214/view)
- Sanctions against Russia -  [Reuters](https://graphics.reuters.com/UKRAINE-CRISIS/SANCTIONS/byvrjenzmve/)

Live data is pulled from:

- Ruble exchange rate - [exchangerates.org](https://www.exchangerates.org.uk/USD-RUB-exchange-rate-history.html)
- Gas price - [ONS](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/systemaveragepricesapofgas)
- [Country lookup](https://www.iban.com/country-code)

Charts are generated in the `charts/` directory. All charts can be generate with `run.py`. Charts will appear in the `figures/` directory.

To install repo and generate all charts:

```
git clone git@github.com:robbie-cab/rus_ukr_interview.git
pip install -r requirements.txt
python run.py
```
