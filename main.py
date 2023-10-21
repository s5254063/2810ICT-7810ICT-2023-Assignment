#Data Analysis Tool for Sydney AirBnB

#importing the different packages needed for the project
import pandas as pd
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import wx
import re

# Function definitions

def visualize_room_types():
    data = pd.read_csv('./listings_dec18.csv',low_memory=False)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    ax.set_title("Room Type, Airbnb Sydney", fontsize=20, pad=20)
    ax = sns.countplot(y='room_type', data=data, order=data['room_type'].value_counts().index, palette="Set3")
    ax.set_xlabel('Number of Listings', fontsize=14, labelpad=15)
    ax.set_ylabel('Type of Room', fontsize=14, labelpad=15)
    ax.xaxis.set_tick_params(labelsize=10)
    ax.yaxis.set_tick_params(labelsize=10)
    plt.show()


def visualize_top_neighbourhoods():
    data = pd.read_csv('./listings_dec18.csv',low_memory=False)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 15)
    ax.set_title("Most Popular Neighbourhoods", fontsize=40, pad=40)
    ax = sns.countplot(y='neighbourhood', data=data, order=data['neighbourhood'].value_counts().iloc[:20].index, palette="Set3")
    ax.set_xlabel('Number of Listings', fontsize=30, labelpad=30)
    ax.set_ylabel('Neighbourhood', fontsize=30, labelpad=30)
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)
    plt.show()

def visualize_prices_of_top_listings():
    data = pd.read_csv('./listings_dec18.csv',low_memory=False)
    fig, ax = plt.subplots()
    fig.set_size_inches(25, 15)
    ax.set_title("Room Price, Airbnb Sydney", fontsize=40, pad=40)
    ax = sns.barplot(x='price', y='neighbourhood', data=data, palette='Set3', dodge=False)
    ax.set_xlabel('Avg. Price', fontsize=30, labelpad=30)
    ax.set_ylabel('Neighbourhood', fontsize=20, labelpad=20)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
    ax.xaxis.set_tick_params(labelsize=20)
    plt.show()

def visualize_ratings_of_listings():
    data = pd.read_csv('./listings_dec18.csv',low_memory=False)

    fig, ax = plt.subplots(figsize=(20, 10))
    ax = sns.boxplot(x=data["review_scores_rating"], linewidth=1, palette='Set2')
    ax.set_title('Avg. Rating, Airbnb Sydney', fontsize=30, pad=30)
    ax.set_xlabel('Rating', fontsize=20, labelpad=15)
    sns.despine(offset=5, left=True)
    plt.show()


class MyApp(wx.App):
    def OnInit(self):
        self.InitFrame()
        return True

    def InitFrame(self):
        frame = MyFrame(parent=None, title="Main Window", pos=(100, 100))
        frame.SetSize(500, 500)
        frame.SetBackgroundColour(wx.Colour(0, 255, 0))
        frame.CenterOnScreen()
        frame.Show()


class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos):
        super().__init__(parent=parent, title=title, pos=pos)
        self.OnInit()

    def OnInit(self):
        panel = MyPanel(parent=self)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        welcomeText = wx.StaticText(self, id=wx.ID_ANY, label="Welcome to Sydney Data Analysis Tool", pos=(70, 30))
        button1 = wx.Button(parent=self, label="Find Stuff", pos=(20, 65))
        button2 = wx.Button(parent=self, label="Most Popular Neighbourhood", pos=(20, 200))
        button3 = wx.Button(parent=self, label="Average Rating", pos=(20, 135))
        button4 = wx.Button(parent=self, label="Look for Cleanliness Factors", pos=(20, 265))

        button1.Bind(event=wx.EVT_BUTTON, handler=self.date_window)
        button2.Bind(event=wx.EVT_BUTTON, handler=self.on_submit3)
        button3.Bind(event=wx.EVT_BUTTON, handler=self.on_submit5)
        button4.Bind(event=wx.EVT_BUTTON, handler=self.clean_window)

    def date_window(self, event):
        secondwindow = Window_For_Dates(parent=self,id=-1)
        secondwindow.Show()
    def on_submit3(self, event):
        visualize_top_neighbourhoods()

    def on_submit5(self, event):
        visualize_ratings_of_listings()

    def clean_window(self, event):
        thirdwindow = Window_For_Cleanliness(parent=self,id=-1)
        thirdwindow.Show()

class MyPanel2(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.label1 = wx.StaticText(self, label= "Start Date",pos=(20,20))
        self.textbox1 = wx.TextCtrl()
        self.textbox2 = wx.TextCtrl()
        self.label2 = wx.StaticText(self, label="End Date",pos=(250,20))
        bSizer1.Add(self.label1,0,wx.EXPAND)
        bSizer1.Add(self.textbox1,1,wx.EXPAND)
        bSizer1.Add(self.label2,2,wx.EXPAND)
        bSizer1.Add(self.textbox2,3,wx.EXPAND)
        self.button_find_listings = wx.Button(parent=self, label="Find Listings ",pos=(20,75))
        self.button_get_price_distribution = wx.Button(parent=self, label="Get_Price_Distribution",pos=(155,75))
        self.button_find_amenities = wx.Button(parent=self, label="Find Listings with Amenities",pos=(330,75))
        bSizer2.Add(self.button_find_listings)
        bSizer2.Add(self.button_get_price_distribution)
        bSizer2.Add(self.button_find_amenities)

        self.button_find_listings.Bind(event=wx.EVT_BUTTON, handler=self.process_listings_data)
        self.button_get_price_distribution.Bind(event=wx.EVT_BUTTON, handler=self.get_price_distribution)
        self.button_find_amenities.Bind(event=wx.EVT_BUTTON, handler=self.process_listings_with_amenities)

        # Function to get all the listings for a given range of date
    def process_listings_data(self,id=None):
        calendar_data = pd.read_csv('./calendar_dec18.csv',low_memory=False, na_values=[""])
        date_end   = '2019-09-19'
        date_start = '2019-09-12'

        df = pd.read_csv('./listings_dec18.csv',
                             usecols=['id', 'host_name', 'host_location', 'host_neighbourhood', 'street', 'city',
                                      'bathrooms', 'bedrooms', 'price', 'has_availability'],
                             na_values=[""],low_memory=False)
        #start_date = datetime.strptime(date_start,"%Y-%m-%d")
        #end_date = datetime.strptime(date_end, "%Y-%m-%d")

        df1 = df[(df['has_availability'] =='t') & (df['street'].str.match('.*Pyrmont.*'))]
        df2 = calendar_data[(calendar_data['available'] == 't') & (calendar_data['date'] >= date_start) & (calendar_data['date'] <= date_end)]
        df3 = df1[~df1['id'].isin(df2['listing_id'])]
        df3.to_csv('./listings_avail.csv', index=False)

        print("Done")

#Function to get price distribution for a given range of date
    def get_price_distribution(self, id=None):
        data = pd.read_csv('./listings_dec18.csv',usecols=['id','price','street'],
                               low_memory=False)
        calendar_data = pd.read_csv('./calendar_dec18.csv',
                                    low_memory=False, na_values=[""])
        date_end = '2019-09-19'
        date_start = '2019-09-12'

        df2 = calendar_data[(calendar_data['available'] == 't') & (calendar_data['date'] >= date_start) & (
                    calendar_data['date'] <= date_end)]

        df3 = data[~data['id'].isin(df2['listing_id'])]
        df3['price'] = df3['price'].str.replace(r'\D', '', regex=True).astype(float)

        fig, ax = plt.subplots()
        fig.set_size_inches(25, 15)
        ax.set_title("Price Distribution, Airbnb Sydney", fontsize=40, pad=40)
        ax = sns.barplot(x='street', y='price', data=df3, palette='Set3', dodge=False)
        ax.set_xlabel('Price', fontsize=30, labelpad=30)
        ax.set_ylabel('Neighbourhood', fontsize=20, labelpad=20)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=45)
        ax.xaxis.set_tick_params(labelsize=20)

        plt.show()
        print("Price Distribution")

    # Function to get all the listings with certain amenities for a given range of date
    def process_listings_with_amenities(self, id = None):
        keywords = ['Pool','pet','spa']
        df = pd.read_csv('./listings_dec18.csv',usecols=['id','name','host_name','summary','amenities','has_availability'],
                               low_memory=False)
        calendar_data = pd.read_csv('./calendar_dec18.csv',
                                    low_memory=False, na_values=[""])

        date_end = '2019-09-19'
        date_start = '2019-09-12'

        df2 = calendar_data[(calendar_data['available'] == 't') & (calendar_data['date'] >= date_start) & (
                    calendar_data['date'] <= date_end)]

        df3 = df[~df['id'].isin(df2['listing_id'])]
        df4 = df3.loc[df3['amenities'].str.contains("pool",case=False)]
        df4.to_csv('./listings_amenities_avail.csv', index=False)
        print("Amenities")


class MyPanel3(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.label1 = wx.StaticText(self, label= "Enter Search Criteria", pos=(25,25))
        self.textbox1 = wx.TextCtrl()
        button_search = wx.Button(parent=self, label="Search", pos=(20, 100))
        button_search.Bind(event=wx.EVT_BUTTON, handler=self.search_cleanliness)

    def search_cleanliness(self,id=None):
        #print(keyword)
        data = pd.read_csv('./reviews_dec18.csv',usecols=['comments'],
                           low_memory=False)
        df = data.loc[data['comments'].str.contains("clean",case=False,na=False)]
        print("The number of customer commented is  ",df.count())
        print("Its CLean")

class Window_For_Dates(wx.Frame):
    title = "Search Range "

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, 1, 'Date Range', size=(700, 200))
        #panel2 = wx.Panel(self, -1)
        panel2 = MyPanel2(self)

        self.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.Centre()
        self.Show()


class Window_For_Cleanliness(wx.Frame):
    title = "Search for Cleanliness Factors "

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, 1, 'Cleanliness', size=(700, 200))
        panel3 = MyPanel3(self)

        self.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.Centre()
        self.Show()


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
