
### Observable trends for a fictional free game with MTX
  * Male players far outnumber female players with around 80% of the total. However, both genders on average spend about the same amount on MTX, with male players spending slightly more.
  
  
  * 20 - 24 year-olds make up the majority of players at 40% with 15 - 19 year-olds in second with 24%. Both of the age groups spend about the same on average, with the 20 - 24 year-olds spending slightly more. 40+ year-olds make up the smallest group with only 3%.
  
  
  * *Betrayal, Whisper of Grieving Widows* and *Arcane Gem* are the most purchased items but *Retribution Axe* with its higher price comes in at the most profitable. *Retribution Axe* is the only item to be in the top 5 lists of most popular and most profitable. 


```python
#dependencies
import pandas as pd
import numpy as np
```


```python
#filepath
purch_path = "Resources/purchase_data.json"

#read into a df
purch_df = pd.read_json(purch_path)
```


```python
'''Total Players'''

#get total # of players by getting the length of the SN column
player_count = len(purch_df["SN"].unique())

#make a dataframe with Total Players as the column title
player_count_df = pd.DataFrame({"Total Players": [player_count]})

player_count_df
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>




```python
#make a function that formats to 2 decimal places and/or adds $ sign
def formatter (df, column, *args):
    if 2 in args:
        x = df[column].map("{:,.2f}".format)
    else:
        x = df[column].map("${:,.2f}".format)
    return x
```


```python
'''Purchasing Analysis (Total)'''

#find the # of unique items
item_count = len(purch_df["Item Name"].unique())

#find the average purchase price
avg_price = purch_df["Price"].mean()

#find the total # of purchases
purch_count = purch_df["Price"].count()

#find the total revenue
rev_total = purch_df["Price"].sum()

#make a dictionary, which will be used to make the df
tot_purch_anls_dict = {"Number of Unique Items": item_count, "Average Price": avg_price, 
                       "Number of Purchases": purch_count, "Total Revenue": rev_total}
#make the df
purch_anls_tot_df = pd.DataFrame(tot_purch_anls_dict, index = [0])
purch_anls_tot_df

#format the df using the money_format function
purch_anls_tot_df["Average Price"] = formatter(purch_anls_tot_df, "Average Price")
purch_anls_tot_df["Total Revenue"] = formatter(purch_anls_tot_df, "Total Revenue")


#put the columns in the proper place
purch_anls_tot_df = purch_anls_tot_df[[ 'Number of Unique Items', 'Average Price', 'Number of Purchases', 'Total Revenue']]

purch_anls_tot_df
```




<div>

   
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Price</th>
      <th>Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>179</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Gender Demographics'''

#make a df for unique people
unique_people_df = purch_df[["Gender", "Age", "SN"]].drop_duplicates(subset="SN")

#find total count of genders
gend_tot = unique_people_df["Gender"].count()

#find # of males and percentage
male_count = unique_people_df["Gender"].value_counts()['Male']
male_perc = (male_count / gend_tot) * 100

#find # of females and percentage
female_count = unique_people_df["Gender"].value_counts()['Female']
female_perc = (female_count / gend_tot) * 100

#find the # of other/non-disclosed and percentage
na_gend_count = gend_tot - male_count - female_count
na_gend_perc = (na_gend_count / gend_tot) * 100

#make a df for gender demographics
gend_demo_df = pd.DataFrame({
    "Gender": ["Male", "Female", "Other / Non-Disclosed"],
    "Percentage of Players": [male_perc, female_perc, na_gend_perc],
    "Total Count": [male_count, female_count, na_gend_count]})

#make gender the index
gend_demo_df = gend_demo_df.set_index("Gender")

#put the columns in the proper place
gend_demo_df = gend_demo_df[["Percentage of Players", "Total Count"]]

#remove Gender title
gend_demo_df.index.name = None

#format data
gend_demo_df["Percentage of Players"] = formatter(gend_demo_df, "Percentage of Players", 2)
gend_demo_df
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>81.15</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>17.45</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.40</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Purchasing Analysis (Gender)'''

#group by gender and assign to a df
gender_grpd = purch_df.groupby(["Gender"])

#find the purchase count
gen_purch_count = gender_grpd["Price"].count()

#find the average purch price
gen_avg_price = gender_grpd["Price"].mean()

#find the total of the purchases
gen_total_purch = gender_grpd["Price"].sum()

#find the normalized totals
gen_norm_totals = gen_total_purch / gend_demo_df["Total Count"]

#make the df
gen_purch_anls_df = pd.DataFrame({
    "Purchase Count": gen_purch_count, 
    "Average Purchase Price": gen_avg_price, 
    "Total Purchase Value": gen_total_purch,
    "Normalized Totals": gen_norm_totals})

#put the columns in the proper place
gen_purch_anls_df = gen_purch_anls_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]

#format the df
gen_purch_anls_df["Average Purchase Price"] = formatter(gen_purch_anls_df, "Average Purchase Price")
gen_purch_anls_df["Total Purchase Value"] = formatter(gen_purch_anls_df, "Total Purchase Value")
gen_purch_anls_df["Normalized Totals"] = formatter(gen_purch_anls_df, "Normalized Totals")

gen_purch_anls_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>$2.82</td>
      <td>$382.91</td>
      <td>$3.83</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>633</td>
      <td>$2.95</td>
      <td>$1,867.68</td>
      <td>$4.02</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>$3.25</td>
      <td>$35.74</td>
      <td>$4.47</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Age Demographics'''

#create bins
bins = [0, 10, 15, 20, 25, 30, 35, 40, 120]

#create the bin labels
bin_labels = [">10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#copy unique_people_df into a new df
up_bin_df = unique_people_df.copy(deep=True)

#put ages into the bins 
up_bin_df["Age Range"] = pd.cut(up_bin_df["Age"], bins, labels=bin_labels)

#group the df by the Age Range
up_age_grpd = up_bin_df.groupby("Age Range")

#find the total count
age_count = up_age_grpd["SN"].count()

#find the percentage of players
age_perc = (age_count / player_count) * 100

#make the df for age demographics
age_demo_df = pd.DataFrame({"Percentage of Players": age_perc, "Total Count": age_count})

#format the df
age_demo_df["Percentage of Players"] = formatter(age_demo_df, "Percentage of Players", 2)

#remove index title
age_demo_df.index.name = None

age_demo_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&gt;10</th>
      <td>3.84</td>
      <td>22</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>9.42</td>
      <td>54</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>24.26</td>
      <td>139</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>40.84</td>
      <td>234</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>9.08</td>
      <td>52</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>7.68</td>
      <td>44</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>4.36</td>
      <td>25</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>0.52</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Purchasing Analysis (Age)'''

#copy purch_df into a new df
purch_bin_df = purch_df.copy(deep=True)

#put ages into the bins
purch_bin_df["Age Range"] = pd.cut(purch_bin_df["Age"], bins, labels=bin_labels)

#group the df by the Age Range
purch_age_grpd = purch_bin_df.groupby("Age Range")

#find the purchase count
age_purch_count = purch_age_grpd["Price"].count()

#find the avg purch price
age_avg_price = purch_age_grpd["Price"].mean()

#find the total purchase value
age_total_purch = purch_age_grpd["Price"].sum()

#find the normalized totals
age_norm_totals = age_total_purch / age_demo_df["Total Count"]

#make the df
age_purch_anls_df = pd.DataFrame({
    "Purchase Count": age_purch_count, 
    "Average Purchase Price": age_avg_price, 
    "Total Purchase Value": age_total_purch,
    "Normalized Totals": age_norm_totals})

#remove index title
age_purch_anls_df.index.name = None

#put the columns in the proper place
age_purch_anls_df = age_purch_anls_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]

#format the df
age_purch_anls_df["Average Purchase Price"] = formatter(age_purch_anls_df, "Average Purchase Price")
age_purch_anls_df["Total Purchase Value"] = formatter(age_purch_anls_df, "Total Purchase Value")
age_purch_anls_df["Normalized Totals"] = formatter(age_purch_anls_df, "Normalized Totals")

age_purch_anls_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&gt;10</th>
      <td>32</td>
      <td>$3.02</td>
      <td>$96.62</td>
      <td>$4.39</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>78</td>
      <td>$2.87</td>
      <td>$224.15</td>
      <td>$4.15</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>184</td>
      <td>$2.87</td>
      <td>$528.74</td>
      <td>$3.80</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>305</td>
      <td>$2.96</td>
      <td>$902.61</td>
      <td>$3.86</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>76</td>
      <td>$2.89</td>
      <td>$219.82</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>58</td>
      <td>$3.07</td>
      <td>$178.26</td>
      <td>$4.05</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>44</td>
      <td>$2.90</td>
      <td>$127.49</td>
      <td>$5.10</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>3</td>
      <td>$2.88</td>
      <td>$8.64</td>
      <td>$2.88</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Top Spenders'''

#group the df by SN
sn_grpd = purch_df.groupby("SN")

#find total purch value
sn_total_purch = sn_grpd["Price"].sum()

#find purch count
sn_purch_count = sn_grpd["Price"].count()

#find the average purchase price
sn_avg_price = sn_grpd["Price"].mean()

#make a df
top_spenders_df = pd.DataFrame({
    "Purchase Count": sn_purch_count,
    "Average Purchase Price": sn_avg_price,
    "Total Purchase Value": sn_total_purch})

#get the top 5 spenders by total purch value
top_spenders_df = top_spenders_df.nlargest(5, "Purchase Count")

#put the columns in the proper place
top_spenders_df = top_spenders_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]]

#format the df
top_spenders_df["Average Purchase Price"] = formatter(top_spenders_df, "Average Purchase Price")
top_spenders_df["Total Purchase Value"] = formatter(top_spenders_df, "Total Purchase Value")

#show df with the total purch value sorted
top_spenders_df.sort_values("Total Purchase Value", ascending=True)

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Mindimnya67</th>
      <td>4</td>
      <td>$3.18</td>
      <td>$12.74</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>4</td>
      <td>$3.39</td>
      <td>$13.56</td>
    </tr>
    <tr>
      <th>Undirrala66</th>
      <td>5</td>
      <td>$3.41</td>
      <td>$17.06</td>
    </tr>
    <tr>
      <th>Hailaphos89</th>
      <td>4</td>
      <td>$1.47</td>
      <td>$5.87</td>
    </tr>
    <tr>
      <th>Qarwen67</th>
      <td>4</td>
      <td>$2.49</td>
      <td>$9.97</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Most Popular Items'''

#group the df by item id and item name 
id_grpd = purch_df.groupby(["Item ID", "Item Name"] )

#find the purchase count
id_purch_count = id_grpd["Price"].count()

#find the total purch value
id_total_purch = id_grpd["Price"].sum()

#find the item price
id_item_price = id_total_purch / id_purch_count

#make the df 
items_grpd_df = pd.DataFrame({
    "Purchase Count": id_purch_count,
    "Item Price": id_item_price,
    "Total Purchase Value": id_total_purch})

#put the columns in the proper place
items_grpd_df = items_grpd_df[["Purchase Count", "Item Price", "Total Purchase Value"]]

#copy the df
pop_items_df = items_grpd_df.copy(deep=True)

#format the df
pop_items_df["Item Price"] = formatter(pop_items_df, "Item Price")
pop_items_df["Total Purchase Value"] = formatter(pop_items_df, "Total Purchase Value")

#get the 5 most popular items by purch count
pop_items_df.nlargest(5, "Purchase Count")

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>11</td>
      <td>$2.35</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <th>Arcane Gem</th>
      <td>11</td>
      <td>$2.23</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>13</th>
      <th>Serenity</th>
      <td>9</td>
      <td>$1.49</td>
      <td>$13.41</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>9</td>
      <td>$2.07</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
  </tbody>
</table>
</div>




```python
'''Most Profitable Items'''

#copy the df
most_prof_df = items_grpd_df.copy(deep=True)

#get the 5 most profitable items by total purchase value
most_prof_df = most_prof_df.nlargest(5, "Total Purchase Value")

#format the df
most_prof_df["Item Price"] = formatter(most_prof_df, "Item Price")
most_prof_df["Total Purchase Value"] = formatter(most_prof_df, "Total Purchase Value")

most_prof_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>9</td>
      <td>$4.14</td>
      <td>$37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>7</td>
      <td>$4.25</td>
      <td>$29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <th>Orenmir</th>
      <td>6</td>
      <td>$4.95</td>
      <td>$29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>6</td>
      <td>$4.87</td>
      <td>$29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <th>Splitter, Foe Of Subtlety</th>
      <td>8</td>
      <td>$3.61</td>
      <td>$28.88</td>
    </tr>
  </tbody>
</table>
</div>


