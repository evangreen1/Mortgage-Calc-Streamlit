import streamlit as st
import numpy as np
import pandas as pd

# Constants
loan_term_years = 30
number_of_payments = loan_term_years * 12
annual_property_tax_rate = 1.25 / 100
annual_homeowners_insurance_rate = 0.25 / 100


def calculate_area_of_triangle(base,heigth):

    solved_area = (base * heigth) / 2

    return solved_area




def adjusted_interest_rate(credit_score, base_rate):
    """Adjust the interest rate based on credit score using the tiered system."""
    if credit_score >= 750:
        rate_increase = 0.00
    elif 700 <= credit_score < 750:
        rate_increase = 0.25 / 100
    elif 650 <= credit_score < 700:
        rate_increase = 0.50 / 100
    elif 600 <= credit_score < 650:
        rate_increase = 0.75 / 100
    else:  # credit score < 600
        rate_increase = 1.00 / 100

    return base_rate + rate_increase

def mortgage_calc_with_credit_score(home_price, credit_score, down_payment_percentage, dti_ratio, annual_interest_rate):
    # Adjust the annual interest rate based on credit score
    adjusted_annual_interest_rate = adjusted_interest_rate(credit_score, annual_interest_rate / 100)  # Convert to decimal
    adjusted_monthly_interest_rate = adjusted_annual_interest_rate / 12

    # Calculate loan amounts
    loan_amount = home_price * (1 - (down_payment_percentage / 100))

    # Calculate monthly mortgage payments
    monthly_payments = (loan_amount * adjusted_monthly_interest_rate * (1 + adjusted_monthly_interest_rate)**number_of_payments) / \
                    ((1 + adjusted_monthly_interest_rate)**number_of_payments - 1)

    # Calculate monthly property tax and homeowners insurance
    monthly_property_tax = home_price * annual_property_tax_rate / 12
    monthly_homeowners_insurance = home_price * annual_homeowners_insurance_rate / 12

    # Calculate total monthly payments including property tax and homeowners insurance
    total_monthly_payments = monthly_payments + monthly_property_tax + monthly_homeowners_insurance

    # Calculate minimum monthly and yearly gross incomes
    monthly_gross_income = total_monthly_payments / (dti_ratio / 100)
    yearly_gross_income = monthly_gross_income * 12

    return {
        'adjusted annual interest rate:': adjusted_annual_interest_rate * 100,
        'loan amount: ': loan_amount,
        'yearly gross income:': yearly_gross_income,
        'total monthly payments:': total_monthly_payments,
    }

# Streamlit App
st.title("Real Estate App Calculator - by Evan Green")

# User input
home_price = st.slider("Home Price", 100_000, 500_000, 300_000, 5_000)
credit_score = st.slider("Credit Score", 600, 850, 700, 5)
down_payment_percentage = st.slider("Down Payment", 3.5, 20.0, 3.5, 0.5)
dti_ratio = st.slider("DTI Ratio", 28, 43, 36, 1)
annual_interest_rate = st.slider("Annual Interest Rate", 1.0, 10.0, 7.00, 0.1)  # Now set by the user

exit_price = st.slider("Exit Price", 10000, 10000000, 100000, 10000)  # Now set by the user

exit_price_range = st.selectbox(
    "Select Exit Price Range",
    options=["$10,000 - $100,000", "$100,000 - $1,000,000", "$1,000,000 - $10,000,000"],
    index=1  # Default to second option
)
# Then parse the selected range to determine the exit_price or adjust the logic based on the range.



# Calculate mortgage details
results = mortgage_calc_with_credit_score(home_price, credit_score, down_payment_percentage, dti_ratio, annual_interest_rate)

result_triangle = calculate_area_of_triangle(100,500)

# Display results
st.subheader("Results")
st.write(f"Loan Amount: ${results['loan amount: ']:,.2f}")
st.write(f"Yearly Gross Income Required: ${results['yearly gross income:']:,.2f}")
st.write(f"Total Monthly Payments (including taxes and insurance): ${results['total monthly payments:']:,.2f}")
st.write(f"Adjusted Annual Interest Rate: {results['adjusted annual interest rate:']:,.2f}%")

st.write(f"Area of Triangle: {result_triangle}")



import streamlit as st

# Define the function to calculate ROI
def calculate_roi(purchase_price, interest_rate, length_of_deal, expected_inflation, exit_price):
    # Calculate total interest paid over the length of the deal
    total_interest = (purchase_price * (interest_rate / 100)) * length_of_deal
    
    # Calculate total investment cost
    total_investment_cost = purchase_price + total_interest
    
    # Adjust exit price for expected inflation
    adjusted_exit_price = exit_price * ((1 + (expected_inflation / 100)) ** length_of_deal)
    
    # Calculate net profit
    net_profit = adjusted_exit_price - total_investment_cost
    
    # Calculate ROI
    roi = (net_profit / total_investment_cost) * 100
    
    return roi

# Streamlit interface
st.title("Investment ROI Calculator")

# Inputs
purchase_price = st.slider("Purchase Price", 10000, 10000000, 100000, 10000)
interest_rate = st.slider("Interest Rate (%)", 0.0, 20.0, 5.0, 0.1)
length_of_deal = st.slider("Length of the Deal (Years)", 1, 30, 5, 1)
expected_inflation = st.slider("Expected Inflation (%)", -10.0, 10.0, 2.0, 0.1)
exit_price = st.slider("Exit Price", 10000, 10000000, 150000, 10000)

# Calculate ROI
roi = calculate_roi(purchase_price, interest_rate, length_of_deal, expected_inflation, exit_price)

# Display ROI
st.write(f"Estimated ROI: {roi:.2f}%")
