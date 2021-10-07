import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
file = 'medical_examination.csv'

df = pd.read_csv(file, index_col = 0)


# Add 'overweight' column
df['overweight'] = np.where(df['weight']/(df['height']/100)**2 < 25, 0, 1)


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)


# Draw Bar Plot
def draw_bar_plot():
    # Create DataFrame for bar plot using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    cardio_zero_zeros = [
    (df.loc[df['cardio'] == 0][df['active'] == 0]['active'].count()), 
    (df.loc[df['cardio'] == 0][df['alco'] == 0]['alco'].count()), 
    (df.loc[df['cardio'] == 0][df['cholesterol'] == 0]['cholesterol'].count()),
    (df.loc[df['cardio'] == 0][df['gluc'] == 0]['gluc'].count()),
    (df.loc[df['cardio'] == 0][df['overweight'] == 0]['overweight'].count()),
    (df.loc[df['cardio'] == 0][df['smoke'] == 0]['smoke'].count())
    ]

    cardio_zero_ones = [
        (df.loc[df['cardio'] == 0][df['active'] == 1]['active'].count()), 
        (df.loc[df['cardio'] == 0][df['alco'] == 1]['alco'].count()), 
        (df.loc[df['cardio'] == 0][df['cholesterol'] == 1]['cholesterol'].count()),
        (df.loc[df['cardio'] == 0][df['gluc'] == 1]['gluc'].count()),
        (df.loc[df['cardio'] == 0][df['overweight'] == 1]['overweight'].count()),
        (df.loc[df['cardio'] == 0][df['smoke'] == 1]['smoke'].count())
    ]

    cardio_one_zeros = [
        (df.loc[df['cardio'] == 1][df['active'] == 0]['active'].count()), 
        (df.loc[df['cardio'] == 1][df['alco'] == 0]['alco'].count()), 
        (df.loc[df['cardio'] == 1][df['cholesterol'] == 0]['cholesterol'].count()),
        (df.loc[df['cardio'] == 1][df['gluc'] == 0]['gluc'].count()),
        (df.loc[df['cardio'] == 1][df['overweight'] == 0]['overweight'].count()),
        (df.loc[df['cardio'] == 1][df['smoke'] == 0]['smoke'].count())
    ]

    cardio_one_ones = [
        (df.loc[df['cardio'] == 1][df['active'] == 1]['active'].count()), 
        (df.loc[df['cardio'] == 1][df['alco'] == 1]['alco'].count()), 
        (df.loc[df['cardio'] == 1][df['cholesterol'] == 1]['cholesterol'].count()),
        (df.loc[df['cardio'] == 1][df['gluc'] == 1]['gluc'].count()),
        (df.loc[df['cardio'] == 1][df['overweight'] == 1]['overweight'].count()),
        (df.loc[df['cardio'] == 1][df['smoke'] == 1]['smoke'].count())
    ]

    index = ['active', ' alco', 'cholesterol', 'gluc', 'overweight', 'smoke']

    df_0 = pd.DataFrame({
        'variables': index,
        '0': cardio_zero_zeros,
        '1': cardio_zero_ones})

    df_1 = pd.DataFrame({
        'variables': index,
        '0': cardio_one_zeros,
        '1': cardio_one_ones})

    # Draw the barplot with 'sns.barplot()'
    f, axes = plt.subplots(1, 2, figsize = (14, 6), sharey = True)
    sns.despine()

    df_0_melted = df_0.melt(id_vars = 'variables')
    p00 = sns.barplot(data=df_0_melted, x='variables', y='value', hue='variable', ax = axes[0])
    p00.set_title('cardio = 0')
    p00.set_xlabel('variable')
    p00.set_ylabel('total')
    p00.get_legend().remove()

    df_1_melted = df_1.melt(id_vars = 'variables')
    p11 = sns.barplot(data=df_1_melted, x='variables', y='value', hue='variable', ax = axes[1])
    p11.set_title('cardio = 1')
    p11.set_xlabel('variable')
    p11.set_ylabel('')
    p11.legend(loc = 'center right', bbox_to_anchor = (1.1, 0.5), title = 'value')


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df2 = df[df['ap_lo'] <= df['ap_hi']]
    df2 = df2[df2['height'] >= df['height'].quantile(0.025)]
    df2 = df2[df2['height'] <= df['height'].quantile(0.975)]
    df2 = df2[df2['weight'] >= df['weight'].quantile(0.025)]
    df2 = df2[df2['weight'] <= df['weight'].quantile(0.975)]

    # Calculate the correlation matrix
    df3 = df2.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(df3.corr(), dtype=np.bool))



    # Set up the matplotlib figure
    plt.figure(figsize = (10, 8))

    # Draw the heatmap with 'sns.heatmap()'
    p22 = sns.heatmap(df3, mask = mask, annot = True, fmt = '.1f', cbar_kws = {"shrink": 0.5})

draw_bar_plot()
draw_heat_map()
