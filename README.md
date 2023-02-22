# Walmart-Shopping-Tool

## Overview
This tool can be used to determine which combination of items and brands results in the cheapest cart based on your shopping list. 
This tool is extremely helpfull to shoppers on a budget who need to quickly determine exactly which products they need to get to fulfill their shopping list without breaking the bank.

<p align="center">
  <a href="https://github.com/github_Abhayparashar/price-compare-app">
    <img src="images/profile.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">price-compare-app</h3>

  <p align="center">
    It takes the name of the product as input then it compares the price of the product from different websites(flipkart,amazon,ebay,olx,croma) then return the minimun price and the url of the product 
    <br />
    <a href="https://github.com/Abhayparashar31/price-compare-app/"><strong>Explore the Project »</strong></a>
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=Mtz2GrCJVRQ">View Demo</a>
    ·
    <a>Report Bug -> parasharabhay13@gmail.com</a>
    
  </p>
</p>

### Features
* An easy to use GUI allows for customers to either upload a grocery list from a textfile or enter it in directly into the app
* A progress bar is updated as the grocery list is parsed through
* The exact price and brand for each grocery list item  is outputted to the gui 
* The total price of the shopping cart is outputted to the bottom of the screen as well
* If an item is not found then "Cannot find item X" is outputted to the screen and the item is ignored
* A reset button allows for a user to process multiple grocery lists

## Technical Details
The webscraper was built using a combination of two main libraries, **Requests** and **Beautiful Soup**.

**Requests** is a HTTP library for Python which is used to make an HTTP request to the Walmart website and store the HTML elements.

**Beautiful Soup** is a Python library used to extract usefull data from the HTML elements.

A grocery list is parsed through, and HTTP requests are sent for each item. Name and price data is extracted for all the products related to that item, and if no products are found then the item is ignored and an "not found" message is displayed to the screen.
The minimum cost product is determined and displayed for each grocery list item, and the total cost of the shopping cart is calculated and displayed as well.

The GUI was built using the **Tkinter** library.
