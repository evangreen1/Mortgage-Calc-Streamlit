# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd

# Define constants
annual_interest_rate = 6.827 / 100
monthly_interest_rate = annual_interest_rate / 12
loan_term_years = 30
number_of_payments = loan_term_years * 12
# down_payment_percentage = 5 / 100
# dti_ratio = 36 / 100
annual_property_tax_rate = 1.25 / 100
annual_homeowners_insurance_rate = 0.25 / 100

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

def mortgage_calc_with_credit_score(home_price, credit_score, down_payment_percentage, dti_ratio):
    # Adjust the annual interest rate based on credit score
    adjusted_annual_interest_rate = adjusted_interest_rate(credit_score, annual_interest_rate)
    adjusted_monthly_interest_rate = adjusted_annual_interest_rate / 12

    # Calculate loan amounts
    loan_amounts = home_price * (1 - (down_payment_percentage / 100))

    # Calculate monthly mortgage payments
    monthly_payments = (loan_amounts * adjusted_monthly_interest_rate * (1 + adjusted_monthly_interest_rate)**number_of_payments) / \
                    ((1 + adjusted_monthly_interest_rate)**number_of_payments - 1)

    # Calculate monthly property tax and homeowners insurance
    monthly_property_tax = home_price * annual_property_tax_rate / 12
    monthly_homeowners_insurance = home_price * annual_homeowners_insurance_rate / 12

    # Calculate total monthly payments including property tax and homeowners insurance
    total_monthly_payments = monthly_payments + monthly_property_tax + monthly_homeowners_insurance

    # Calculate minimum monthly and yearly gross incomes
    monthly_gross_incomes = total_monthly_payments / (dti_ratio / 100)
    yearly_gross_incomes = monthly_gross_incomes * 12

    

    return {
        'adjusted annual interest rate:': adjusted_annual_interest_rate * 100,
        'adjusted monthly interest rate:': adjusted_monthly_interest_rate,
        'monthly property tax: ': monthly_property_tax, 
        'loan amount: ': loan_amounts,
        'yearly gross income:': yearly_gross_incomes,
        'total monthly gross income:': monthly_gross_incomes,
        'total monthly payments:': total_monthly_payments,
    }


# Streamlit App

st.title("Mortgage Calculator with Credit Score")

# User input
home_price = st.slider("Home Price", 100_000, 500_000, 300_000, 5_000)
credit_score = st.slider("Credit Score", 600, 850, 700, 5)
down_payment_percentage = st.slider("Down Payment", 3.5, 20.0, 3.5, 0.5)
dti_ratio = st.slider("DTI Ratio", 28, 43, 36, 1)

# Calculate mortgage details
results = mortgage_calc_with_credit_score(home_price, credit_score, down_payment_percentage, dti_ratio)

# Display results
st.subheader("Results")
st.write(f"Loan Amount: ${results['loan amount: ']:,.2f}")
st.write(f"Yearly Gross Income Required: ${results['yearly gross income:']:,.2f}")
st.write(f"Total Monthly Gross Income Required: ${results['total monthly gross income:']:,.2f}")
st.write(f"Total Monthly Payments (including taxes and insurance): ${results['total monthly payments:']:,.2f}")
st.write(f"Adjusted Annual Interest Rate: {results['adjusted annual interest rate:']}%")

# # Calculate individual components of monthly payments
# # Calculate individual components of monthly payments
# adjusted_monthly_interest_rate = results['adjusted monthly interest rate:']
# monthly_mortgage_payments = (results['loan amount: '] * adjusted_monthly_interest_rate * (1 + adjusted_monthly_interest_rate)**number_of_payments) / \
#                     ((1 + adjusted_monthly_interest_rate)**number_of_payments - 1)
# monthly_property_tax = home_price * annual_property_tax_rate / 12
# monthly_homeowners_insurance = home_price * annual_homeowners_insurance_rate / 12

# # Create a DataFrame for the bar chart
# df = pd.DataFrame({
#     'Components': ['Monthly Mortgage', 'Monthly Property Tax', 'Total Monthly Payments'],
#     'Amounts': [monthly_mortgage_payments, monthly_property_tax, results['total monthly payments:']]
# })

# st.write("")
# # Plot the bar chart
# st.bar_chart(df.set_index('Components'))
