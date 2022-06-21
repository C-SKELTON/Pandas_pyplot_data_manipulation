import pandas as pd
import plotly.express as px

ap = pd.read_csv('apps.csv')
ap.shape
#deleting two columns from the dataframe
ap.head(4)
ap.drop(columns=['Last_Updated','Android_Ver'], axis=1, inplace=True)
ap.shape
ap.isna().sum()
df_apps_clean = ap.dropna()
df_apps_clean.shape
dups = df_apps_clean.duplicated().sum()


#querying where the App column equals Instagram
df_apps_clean.query("App=='Instagram'")

#removing duplicates based on certain fields
df_apps_clean = df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'])


df_apps_clean.head()

df_apps_clean.sort_values('Rating', ascending=False).head()
df_apps_clean.sort_values('Size_MBs', ascending=False).head()
df_apps_clean.sort_values('Reviews', ascending=False).head(50)

ratings = df_apps_clean.Content_Rating.value_counts()
#pie Chart creation
fig = px.pie(labels = ratings.index
             ,values = ratings.values
             ,title="Content Rating"
             ,names = ratings.index
             ,hole = 0.6)
fig.update_traces(textposition='inside', textinfo='percent', textfont_size=15)
fig.show()


df_apps_clean.Installs.describe()

df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
df_apps_clean[['App', 'Installs']].groupby('Installs').count()

df_apps_clean.Price.describe()
df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)

df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
df_apps_clean.sort_values('Price', ascending=False).head()

#Revenue Estimate create a column via a calculation
df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
df_apps_clean.sort_values('Revenue_Estimate', ascending=False)[:10]


top10_category = df_apps_clean.Category.value_counts()[:10]

bar = px.bar(x = top10_category.index, y = top10_category.values)
bar.show()

category_installs = df_apps_clean.groupby('Category').agg({'Installs':pd.Series.sum})
category_installs.sort_values('Installs', ascending=True, inplace=True)

h_bar = px.bar(x = category_installs.Installs, y = category_installs.index
               ,orientation ='h'
               ,title = 'Cateogry Popularity')
h_bar.update_layout(xaxis_title = 'Number of Downloads', yaxis_title ='Category')
h_bar.show()

cat_number = df_apps_clean.groupby('Category').agg({'App':pd.Series.count})
cat_merged_df = pd.merge(cat_number, category_installs, on="Category", how = 'inner')
cat_merged_df
s_plot = px.scatter(cat_merged_df, x='App', y='Installs'
, title ='Category Concentration'
, size = 'App'
, hover_name = cat_merged_df.index
, color ='Installs')

s_plot.update_layout(xaxis_title = "Number of Apps (Lower =More Concentrated)", yaxis_title = "Installs", yaxis = dict(type='log'))
s_plot.show(0)



df_apps_clean.Genres.describe()
len(df_apps_clean.Genres.unique())
df_apps_clean.Genres.value_counts().sort_values(ascending=True)[:5]

stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
num_genres = stack.value_counts()[:15]


bar2 = px.bar(x = num_genres.index, y= num_genres.values, title = 'Top Genres', hover_name = num_genres.index, color = num_genres.values, color_continuous_scale='Agsunset')
bar2.update_layout(xaxis_title = 'Genre', yaxis_title ='Number of Apps', coloraxis_showscale=False)
bar2.show()


df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index = False).agg({'App':pd.Series.count})
df_free_vs_paid.head()

bar3 = px.bar(df_free_vs_paid,x= 'Category', y='App', color = 'Type', barmode = 'group', title= 'Free vs Paid Apps by Category')
bar3.update_layout(xaxis_title = 'Category', yaxis_title = 'Number of Apps', xaxis={'categoryorder': 'total descending'}, yaxis=dict(type='log'))
bar3.show()

#print(df_apps_clean)
box1 = px.box(df_apps_clean, x='Type', y = 'Installs', color = 'Type', notched = True, points = 'all', title ='How many Downloads are paid apps giving up?')
box1.update_layout(yaxis=dict(type='log'))
box1.show()

df_paid_apps = df_apps_clean[df_apps_clean['Type']=='Paid']
df_paid_apps.head()

print(df_paid_apps.median())


box2 =  px.box(df_paid_apps, x='Category', y='Revenue_Estimate')
box2.update_layout(yaxis=dict(type='log'), yaxis_title = 'Paid App Ballpark Revenue', xaxis = {'categoryorder' : 'min ascending'})
box2.show()

box3 = px.box(df_paid_apps, x='Category', y='Price', title='Price Per Category')

box3.update_layout(xaxis_title ='Category', yaxis_title='Paid App Price', xaxis={'categoryorder':'max descending'}, yaxis=dict(type='log'))
box3.show()