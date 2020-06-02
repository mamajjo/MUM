import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def setAxesRanges(axes):
    for a in axes:
        start, end = a.get_ylim()
        a.yaxis.set_ticks(np.arange(start, end, (end-start)/4))
        a.set_ylim(top=end*1.2)
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
def transform_company_size(val):
    val = val.replace('+', "").replace("<", "").replace(">", "").replace(" ", "")
    if "-" in val:
        ran = val.split("-", 1)
        if '' in ran:
            return int(ran[0]) if ran[1] == "" else int(ran[1])
        else:
            return (int(ran[0])+int(ran[1]))/2
    else:
        return int(val)

def plot_stats(df):
    X = df["company_size"].copy().values
    X = [transform_company_size(x) for x in X if hasNumbers(x)]
    first_X = [x for x in X if x < 1000]
    second_X = [x for x in X if x >= 1000 and x < 5000]
    third_X = [x for x in X if x >= 5000]

    salary_threshold = 80_000
    too_high_to_plot_count = df[df.salary_to>=salary_threshold].size
    if too_high_to_plot_count > 0:
        print(f"Found {too_high_to_plot_count} jobs with salary over {salary_threshold}, which won't be taken into account on plots below.")
    sns.set(color_codes=True)
    f, axes = plt.subplots(3, 1)
    sns.distplot(first_X, ax=axes[0], kde=False, hist=True);
    sns.distplot(second_X, ax=axes[1], kde=False, hist=True);
    sns.distplot(third_X, ax=axes[2], kde=False, hist=True);
    f.tight_layout()
    setAxesRanges(axes)
    sns.distplot(df.copy().assign(Spread=lambda df: 100*(df.salary_to-df.salary_from)/((df.salary_to+df.salary_from)/2)).Spread, kde=False, hist=True)
    with sns.axes_style("white"):
        without_outlier=df.copy()[df.salary_to<salary_threshold]
        sns.jointplot(x=without_outlier.salary_from, y=without_outlier.salary_to, kind="hex");
        sns.jointplot(x=without_outlier.salary_from, y=without_outlier.salary_to, data=df, kind="kde");
