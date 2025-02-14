def seaborn_styles(sns):
    sns.set_style("whitegrid")
    sns.set(font='serif')
    sns.set_style("white", {
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "serif"],
    })


CRIME_TYPES = ['Criminal damage and arson', 'Crimes Of Dishonesty', 'Sexual offences',
               'Violence against the person', 'Other', 'Total']
