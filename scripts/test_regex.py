
import re

# Patterns from notification_parser.py
FINANCIAL_PATTERNS = {
    "UPI": re.compile(r'\b(?:UPI|PhonePe|Paytm|GPay|Google.Pay|BHIM|Amazon.Pay)\b.*?(?:Rs\.?|INR|₹)\s*\d+', re.I),
    "BANK": re.compile(r'\b(?:credited|debited|transferred|withdrawn|deposited|balance|account|IFSC|NEFT|RTGS|IMPS)\b.*?(?:Rs\.?|INR|₹)\s*\d+', re.I)
}

test_cases = [
    "PhonePe: Paid Rs.1 to Shopkeeper",
    "GPay: ₹1 sent to Ravi",
    "Paytm: Paid Rs. 1.00 successfully",
    "UPI: Debited INR 1 for transaction",
    "HDFC Bank: Rs. 1.00 debited from a/c",
    "Sent 1 rupee via UPI" # Should fail or need adjustment?
]

print("Testing '1 Rupee' detection patterns:\n")

for test in test_cases:
    print(f"Testing: '{test}'")
    matched = False
    for category, pattern in FINANCIAL_PATTERNS.items():
        if pattern.search(test):
            print(f"  ✅ MATCHED ({category})")
            matched = True
    if not matched:
        print(f"  ❌ NO MATCH")
    print("-" * 30)
