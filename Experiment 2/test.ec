// Define the main function using standard C keywords
int main() {
    // 1. Test the new keywords and special token types
    phone my_phone = 9876543210;
    email support_email = "help.desk@domain.co.in";
    phone intl_phone = +91-1234567890;

    // 2. Test standard keywords, identifiers, and various constants
    int counter = 100;
    float price = 199.99;
    char grade = 'A';
    const char* message = "Test successful!"; // A string constant

    // 3. Test all specified operators and punctuators in a loop
    for (counter = 0; counter < 10; counter = counter + 1) {
        if (price >= 100.0) {
            price = price * 0.9; // Apply a discount
        } else {
            price = price - 5.0;
        }
    }

    // 4. Test remaining relational operators
    int a = 5, b = 10;
    if (a != b) {
        // This comparison should evaluate to true
    }

    // 5. Test for invalid characters to check error reporting
    // The characters '#' and '$' should be flagged as errors by the lexer.
    int invalid_test = 5 # 3; $

    return 0;
}