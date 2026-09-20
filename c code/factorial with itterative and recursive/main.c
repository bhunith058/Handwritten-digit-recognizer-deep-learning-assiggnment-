#include <stdio.h>

// Function for factorial using iteration
unsigned long long factorial_iterative(int n) {
    unsigned long long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Function for factorial using recursion
unsigned long long factorial_recursive(int n) {
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial_recursive(n - 1);
}

int main() {
    int num;

    // Input number
    printf("Enter a positive integer: ");
    scanf("%d", &num);

    if (num < 0) {
        printf("Factorial is not defined for negative numbers.\n");
    } else {
        // Calculate factorial using iterative method
        unsigned long long iterative_result = factorial_iterative(num);
        printf("Factorial of %d using iteration: %llu\n", num, iterative_result);

        // Calculate factorial using recursive method
        unsigned long long recursive_result = factorial_recursive(num);
        printf("Factorial of %d using recursion: %llu\n", num, recursive_result);
    }

    return 0;
}
