#YASHWANTH_SAI_BATHINI
#1017917780
#DATE_OF_CREATION : 05/DECEMBER/2023
'''This Python program uses web scraping to extract mobile phone listings from eBay, creating a
structured DataFrame. It analyzes the data to identify gadgets with the highest and lowest prices, as well as those
with the highest and lowest ratings. It employs regular expressions to extract numerical information like ratings.
The program visualizes the relationship between price and rating using Seaborn and Matplotlib, displaying a bar graph
in green to represent the analyzed data for quick and clear insights into the mobile phone listings' price-rating 
distribution.'''
#Imported the list of multiple libraries that used in the below code
import requests  #For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
import re  #For working with regular expressions
import pandas as pd  #For data manipulation and analysis
import matplotlib.pyplot as plt  #For creating plots and visualizations
import seaborn as sns  #For statistical data visualization
def create_dataframe(): #It is the function to create dataframe from eBay website for the Mobile Phones listings
    url = "https://www.ebay.com/t/Cell-Phones-Smartphones/9355/bn_320094" #It is URL to scrape the website
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    title = [] #Multiple lists were created to store the product details
    price = []
    category = []
    rating = []
    rate = []
    count = []
    product_list = []
    products = soup.find_all('div', class_='app-tp-product-card') #Here it will Scrap the data for each product on the web page
    for product in products:
        title = product.find('h2', class_='title').text #It is used for extracting product details
        price_elem = product.find('span', class_='cc-ts-BOLD')
        if price_elem: #Here it will check if price element exists and extract price information
            price_text = price_elem.text.strip().split(" ")[0]
            if price_text != '----': #Here it will check if the price text is not '----'indicating that unavailability of price
                price_text = price_text.replace(',', '').replace('$', '')
                price = float(price_text)
            else: #Here it set price to None if price text is '----'unavailable price
                price = None
        else: #If the price element doesn't exist then set price to None
            price = None
        category_elem = product.find('span', class_='cc-ts-BOLD')
        if category_elem: #Here it will check if category element exists and extract category information
            category_text = category_elem.text.strip().split(" ")[1] #It will extract text and split to get the specific category information
        else: #If category element doesn't exist then set category_text to None
            category_text = None
        ratings = product.find('div', class_='reviews-aggregated-stars')
        rating = ratings.find('span', class_='clipped').text
        try: #Here it is used to define a regular expression pattern to extract the numeric part of the rating
            regex = re.compile('(.+)out')
            rate = regex.search(rating).group(1)
            rating = float(rate)
        except: #Here if the regular expression doesn't find a match, set 'rating' to 0
            rating = 0
        try: #Here by using regular expression to find and extract the count of product ratings
            count = re.search(r'based on(.*?)product ratings', rating).group(1)
        except: #Here if the regular expression doesn't find a match then it will be set the count to 0
            count = 0
        product_list.append([title, price, category_text, rating, count])
    df = pd.DataFrame(product_list, columns=['title', 'price', 'category', 'rating', 'rating_count'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce') 
    return df
def get_analysis(df): #Function to print the analysis results
    max_price = df['price'].idxmax()
    min_price = df['price'].idxmin()
    max_rating = df['rating'].idxmax()
    min_rating = df['rating'].idxmin()
    #Here it will print the details of the mobile gadgets with the highest,lowest price and highest,lowest rating
    print("Gadget with the highest price is: {} - Worth: ${}".format(df['title'].iloc[max_price], df['price'].iloc[max_price]))
    print("Gadget with the lowest price is: {} - Worth: ${}".format(df['title'].iloc[min_price], df['price'].iloc[min_price]))
    print("Gadget with the highest rating is: {} - {} stars".format(df['title'].iloc[max_rating], df['rating'].iloc[max_rating]))
    print("Gadget with the lowest rating is: {} - {} stars".format(df['title'].iloc[min_rating], df['rating'].iloc[min_rating]))
def display_graph(df): #This function used for pictorial representation of analysis by using bar graphs
    new_df = df.sort_values(["price", "rating"], ascending=(True, True))
    sns.barplot(x=new_df['rating'], y=new_df['price'], color='#3D9970', edgecolor='none', errorbar=None) #The bar graph will be represented in Olive green color
    plt.title('Smartphone Price-Rating Analysis on eBay')
    plt.xlabel('Rating')
    plt.ylabel('Price')
    plt.show()
def main(): #Main function that coordinates and manages the complete workflow
    df = create_dataframe()
    get_analysis(df)
    display_graph(df)
if __name__ == "__main__":
    main()
