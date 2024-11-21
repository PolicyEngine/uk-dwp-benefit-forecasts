import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# Wide to long
def convert_to_long(df, type, year):
    year_to_forecast = {x: y for x, y in zip(df.T[0], df.T[1])}
    year_to_forecast = {int(year.split("/")[0]): value for year, value in year_to_forecast.items() if "/" in str(year)}
    # skip first row of df and move row 1 to column names
    df.columns = df.iloc[0]
    df = df[1:]
    # Remove last column
    df = df.iloc[:, 1:-1]
    df = df.melt(id_vars=[df.columns[0]], var_name="Year", value_name="Value")
    df.columns = ["Benefit", "Year", "Value"]
    df = df[~df.Year.isna()]
    df = df[df.Year.str.contains("/")]
    df.Year = df.Year.apply(lambda x: int(x.split("/")[0]))
    df["Type"] = type
    df["Forecast year"] = year
    df.Value = df.Value.str.replace(",", "").replace(" ", "").replace("-", "")
    df.Value = pd.to_numeric(df.Value, errors="coerce")
    df["Forecast"] = df.Year.map(year_to_forecast) == "Forecast"
    # Remove rows with Benefit not starting with a capital letter
    df = df[df.Benefit.apply(lambda x: str(x)[0].isupper())]
    return df

def combine_tables():
    dfs = []
    for year in range(2017, 2025):
        spending_df = pd.read_csv(f"data/raw/1a-{year}.csv", encoding="unicode_escape")
        spending_df = convert_to_long(spending_df, "Spending", year)
        dfs.append(spending_df)

        caseloads_df = pd.read_csv(f"data/raw/1c-{year}.csv", encoding="unicode_escape")
        caseloads_df = convert_to_long(caseloads_df, "Caseloads", year)
        dfs.append(caseloads_df)

    return pd.concat(dfs)

df = combine_tables()

BENEFITS = ['Armed Forces Independence Payment', 'Attendance Allowance',
       'Bereavement related benefits', "Carer's Allowance",
       'Child Benefit', 'Christmas Bonus', 'Cold Weather Payments',
       'Council Tax Benefit', 'Death Grant',
       'Disability Living Allowance', 'Disability Working Allowance',
       'Discretionary Housing Payments', 'Earnings Top Up',
       'Employment and Support Allowance', 'Family Credit',
       'Financial Assistance Scheme', 'Funeral Expenses Payments',
       "Guardian's Allowance & Child's Special Allowance",
       'Housing benefits', 'Incapacity Benefit', 'Income Support',
       'Independent Living Fund', 'Industrial injuries benefits in AME',
       'Invalidity Benefit', 'In Work Credit', 'Job Grant',
       "Jobseeker's Allowance", 'Maternity Allowance', 'Maternity Grant',
       'Mesothelioma', 'Mobility Allowance',
       'New Deal and Employment programme allowances',
       'New Enterprise Allowance', 'One Parent Benefit',
       'Over 65s Payments', 'Over 70s Payments', 'Over 75 TV Licences',
       'Pension Credit', 'Personal Independence Payment',
       'Pneumoconiosis 1979', 'Return to Work Credit', 'RPI adjustment',
       'Severe Disablement Allowance', 'Sickness Benefit',
       'Social Fund Discretionary', 'Specialised Vehicles Fund',
       'State Pension', 'State Pension transfers',
       'Statutory Maternity Pay', 'Statutory Sick Pay',
       'Sure Start Maternity Grant', 'Unemployment Benefit',
       'Vaccine Damage Payments', 'War Pensions', 'Winter Fuel Payments',
       'Minor housing-related benefits', 'Other small benefits',
       'Total benefit expenditure', 'Total contributory benefits (C)',
       'Total income-related benefits (IR)',
       'Total non contributory and non income-related benefits (NC / NIR)',
       'Total in DWP Annually Managed Expenditure',
       'Expenditure covered by Departmental Expenditure Limit',
       'Industrial Injuries benefits',
       'Invalidity Benefit & Sickness Benefit',
       'State Pension (includes contributory and non contributory)',
       'Support for Mortgage Interest loans',
       'Universal Credit', 'Benefits funded by local authorities',
       'Housing benefits (exc. Universal Credit)',
       'Cost of Living Payments',
]

df = df[df.Benefit.isin(BENEFITS)]
df.Value[df.Type == "Spending"] = df.Value[df.Type == "Spending"].values * 1_000_000
df.Value[df.Type == "Caseloads"] = df.Value[df.Type == "Caseloads"].values * 1_000
df.to_csv("data/benefits.csv", index=False)
print("Data cleaned and saved to data/benefits.csv")