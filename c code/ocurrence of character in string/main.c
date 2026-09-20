#include <stdio.h>
#include <string.h>

int main() {
    char str[100], ch;
    int count = 0;

    // Input string
    printf("Enter a string: ");
    fgets(str, sizeof(str), stdin);

    // Remove newline character from the string (if present)
    str[strcspn(str, "\n")] = '\0';

    // Input character to search for
    printf("Enter a character to find its occurrence: ");
    scanf("%c", &ch);

    // Count occurrences of the character
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ch) {
            count++;
        }
    }

    // Output the result
    printf("The character '%c' occurs %d time(s) in the string \"%s\".\n", ch, count, str);

    return 0;
}
