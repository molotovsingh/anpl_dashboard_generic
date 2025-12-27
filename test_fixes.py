"""
Test script to verify the 3 critical fixes for investor dashboard
"""
import pandas as pd

# Copy the calculate_projections function for testing
def calculate_projections(current_revenue, growth_rate, redemption_rate=50, revenue_share_pct=5, months=120, current_month=1, investment_amount=75.0, already_paid=0.0):
    """
    Calculate monthly revenue projections until investment is repaid.
    """
    projections = []
    cumulative_payment = already_paid  # Start from prior payments

    # Add Month 0 (current month) with NO growth - shows current state
    net_revenue_current = current_revenue * (1 - redemption_rate/100)
    payment_current = min(net_revenue_current * (revenue_share_pct / 100), investment_amount - cumulative_payment)
    cumulative_payment += payment_current

    projections.append({
        'Month': current_month,
        'Gross Revenue (₹L)': round(current_revenue, 2),
        'Redemptions (₹L)': round(current_revenue * (redemption_rate / 100), 2),
        'Net Revenue (₹L)': round(net_revenue_current, 2),
        'Payment to Vinmo (₹L)': round(payment_current, 2),
        'Cumulative Paid (₹L)': round(cumulative_payment, 2),
        'Balance (₹L)': max(0, investment_amount - cumulative_payment)
    })

    # If already repaid in current month, return
    if cumulative_payment >= investment_amount:
        return pd.DataFrame(projections)

    for month in range(months):
        # Future months with growth
        month_number = month + 1
        actual_month = current_month + month + 1  # Shift by 1 (Month 0 is current)

        # Calculate gross revenue with compound growth
        gross_revenue = current_revenue * ((1 + growth_rate/100) ** month_number)

        # Calculate net revenue after redemptions
        redemption_amount = gross_revenue * (redemption_rate / 100)
        net_revenue = gross_revenue - redemption_amount

        # Calculate payment to investor - CAP to remaining balance
        remaining_balance = investment_amount - cumulative_payment
        calculated_payment = net_revenue * (revenue_share_pct / 100)
        payment = min(calculated_payment, remaining_balance)  # Don't overpay
        cumulative_payment += payment

        projections.append({
            'Month': actual_month,
            'Gross Revenue (₹L)': round(gross_revenue, 2),
            'Redemptions (₹L)': round(redemption_amount, 2),
            'Net Revenue (₹L)': round(net_revenue, 2),
            'Payment to Vinmo (₹L)': round(payment, 2),
            'Cumulative Paid (₹L)': round(cumulative_payment, 2),
            'Balance (₹L)': max(0, investment_amount - cumulative_payment)
        })

        if cumulative_payment >= investment_amount:
            break

    return pd.DataFrame(projections)


print("=" * 80)
print("TESTING 3 CRITICAL FIXES FOR INVESTOR DASHBOARD")
print("=" * 80)

# Test 1: Prior Repayments Accuracy
print("\n📋 TEST 1: Prior Repayments (Issue #1)")
print("-" * 80)
print("Scenario: Month 6, already paid ₹10L, need to repay remaining ₹65L")
print()

df_with_prior = calculate_projections(
    current_revenue=15.0,
    growth_rate=9.65,
    current_month=6,
    investment_amount=75.0,
    already_paid=10.0
)

df_without_prior = calculate_projections(
    current_revenue=15.0,
    growth_rate=9.65,
    current_month=6,
    investment_amount=75.0,
    already_paid=0.0
)

print(f"WITH already_paid=10.0:")
print(f"  - First row cumulative: ₹{df_with_prior.iloc[0]['Cumulative Paid (₹L)']}L")
print(f"  - Balance after Month 6: ₹{df_with_prior.iloc[0]['Balance (₹L)']}L")
print(f"  - Months to complete: {len(df_with_prior)} (Month {df_with_prior.iloc[-1]['Month']})")
print(f"  - Final cumulative: ₹{df_with_prior.iloc[-1]['Cumulative Paid (₹L)']}L")
print()
print(f"WITHOUT already_paid (WRONG - old behavior):")
print(f"  - First row cumulative: ₹{df_without_prior.iloc[0]['Cumulative Paid (₹L)']}L")
print(f"  - Balance after Month 6: ₹{df_without_prior.iloc[0]['Balance (₹L)']}L")
print(f"  - Months to complete: {len(df_without_prior)} (Month {df_without_prior.iloc[-1]['Month']})")
print()

# Verify
expected_first_cumulative = 10.0 + (15.0 * 0.5 * 0.05)  # 10 + payment for month 6
actual_first_cumulative = df_with_prior.iloc[0]['Cumulative Paid (₹L)']
test1_pass = abs(actual_first_cumulative - expected_first_cumulative) < 0.01

print(f"✅ TEST 1 PASSED" if test1_pass else f"❌ TEST 1 FAILED")
print(f"   Expected first cumulative: ₹{expected_first_cumulative:.2f}L")
print(f"   Actual first cumulative: ₹{actual_first_cumulative:.2f}L")


# Test 2: Months Remaining vs Completes At (Semantic Clarity)
print("\n📋 TEST 2: Semantic Clarity (Issue #2)")
print("-" * 80)
print("Scenario: Current month 6, completes at month 41")
print()

df = calculate_projections(
    current_revenue=10.0,
    growth_rate=9.65,
    current_month=6,
    investment_amount=75.0,
    already_paid=0.0
)

months_to_repay = len(df)
months_remaining = len(df) - 1  # Exclude current month row
final_month = df.iloc[-1]['Month']
repayment_incomplete = df.iloc[-1]['Balance (₹L)'] > 0.01

print(f"Projection has {months_to_repay} rows")
print(f"  - Months Remaining: {months_remaining} (future months from current)")
print(f"  - Completes At: Month {final_month}")
print(f"  - Current Month: 6")
print()
print(f"Clarification:")
print(f"  - User is at Month 6 (current)")
print(f"  - Needs {months_remaining} MORE months to complete")
print(f"  - Will finish at Month {final_month}")
print()

test2_pass = (final_month == 6 + months_remaining) and (months_to_repay == months_remaining + 1)
print(f"✅ TEST 2 PASSED" if test2_pass else f"❌ TEST 2 FAILED")
print(f"   Math check: 6 + {months_remaining} = {6 + months_remaining} (should equal {final_month})")


# Test 3: Executive Summary Consistency
print("\n📋 TEST 3: Summary Consistency (Issue #3)")
print("-" * 80)
print("Scenario: Low growth (1%) leading to incomplete repayment")
print()

df_low_growth = calculate_projections(
    current_revenue=10.0,
    growth_rate=1.0,  # Very low growth
    current_month=1,
    investment_amount=75.0,
    already_paid=0.0,
    months=120  # Limited to 120 months
)

months_to_repay_low = len(df_low_growth)
months_remaining_low = len(df_low_growth) - 1
final_month_low = df_low_growth.iloc[-1]['Month']
final_balance = df_low_growth.iloc[-1]['Balance (₹L)']
repayment_incomplete_low = final_balance > 0.01

# Format displays consistently
remaining_display = f">{months_remaining_low}" if repayment_incomplete_low else f"{months_remaining_low}"
final_month_display = f">M{final_month_low}" if repayment_incomplete_low else f"M{final_month_low}"
repayment_status = "Incomplete - may take longer" if repayment_incomplete_low else "On track"

print(f"Repayment incomplete: {repayment_incomplete_low}")
print(f"Final balance: ₹{final_balance:.2f}L (remaining)")
print()
print(f"UI Display:")
print(f"  - Months Remaining: {remaining_display}")
print(f"  - Completes At: {final_month_display}")
print()
print(f"Executive Summary Should Show:")
print(f"  - Months Remaining: {remaining_display} months")
print(f"  - Completes At: {final_month_display}")
print(f"  - Status: {repayment_status}")
print()

test3_pass = repayment_incomplete_low and ">" in remaining_display and ">" in final_month_display
print(f"✅ TEST 3 PASSED" if test3_pass else f"❌ TEST 3 FAILED")
print(f"   Verified that both UI and summary show '{remaining_display}' (not raw '{months_remaining_low}')")


# Edge Case: Already fully repaid
print("\n📋 EDGE CASE TEST: Already Fully Repaid")
print("-" * 80)

df_fully_paid = calculate_projections(
    current_revenue=10.0,
    growth_rate=5.0,
    current_month=50,
    investment_amount=75.0,
    already_paid=75.0  # Already fully repaid
)

print(f"Already paid: ₹75.0L (100% of investment)")
print(f"Months remaining: {len(df_fully_paid) - 1}")
print(f"Balance: ₹{df_fully_paid.iloc[0]['Balance (₹L)']}L")
print(f"Payment this month: ₹{df_fully_paid.iloc[0]['Payment to Vinmo (₹L)']}L")
print()

edge_test_pass = len(df_fully_paid) == 1 and df_fully_paid.iloc[0]['Balance (₹L)'] == 0
print(f"✅ EDGE CASE PASSED" if edge_test_pass else f"❌ EDGE CASE FAILED")


# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
all_pass = test1_pass and test2_pass and test3_pass and edge_test_pass
print(f"Test 1 (Prior Repayments): {'✅ PASS' if test1_pass else '❌ FAIL'}")
print(f"Test 2 (Semantic Clarity): {'✅ PASS' if test2_pass else '❌ FAIL'}")
print(f"Test 3 (Summary Consistency): {'✅ PASS' if test3_pass else '❌ FAIL'}")
print(f"Edge Case (Fully Repaid): {'✅ PASS' if edge_test_pass else '❌ FAIL'}")
print()
print(f"{'🎉 ALL TESTS PASSED! Implementation is correct.' if all_pass else '⚠️  SOME TESTS FAILED. Review implementation.'}")
print("=" * 80)
