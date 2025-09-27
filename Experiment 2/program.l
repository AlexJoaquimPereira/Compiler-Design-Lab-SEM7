%{
#include <stdio.h>

int line_count = 1;
%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
ID          {LETTER}({LETTER}|{DIGIT}|_)*
PHONE       ("+"?{DIGIT}{2}"-")?{DIGIT}{10}
EMAIL       [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

/* SECTION 2: RULES */

%%

"//".* { /* Ignore single-line comments */ }
"/*"([^*]|(\*+[^*/]))*\*+"/" { /* Ignore multi-line comments */ }

"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while" {
    /* --- C Keywords --- */
    printf("Line %d: KEYWORD\t\t'%s'\n", line_count, yytext);
}

"phone"|"email" {
    /* --- New Keywords for ExtendC --- */
    printf("Line %d: NEW_KEYWORD\t\t'%s'\n", line_count, yytext);
}

{PHONE}     { printf("Line %d: PHONE_NUMBER\t'%s'\n", line_count, yytext); }
{EMAIL}     { printf("Line %d: EMAIL_ADDRESS\t'%s'\n", line_count, yytext); }

{ID}        { printf("Line %d: IDENTIFIER\t\t'%s'\n", line_count, yytext); }

{DIGIT}+\.{DIGIT}+ { printf("Line %d: FLOAT_CONSTANT\t'%s'\n", line_count, yytext); }
{DIGIT}+          { printf("Line %d: INTEGER_CONSTANT\t'%s'\n", line_count, yytext); }
\"[^"\n]*\"      { printf("Line %d: STRING_CONSTANT\t%s\n", line_count, yytext); }
\'[^\']\'         { printf("Line %d: CHAR_CONSTANT\t\t'%s'\n", line_count, yytext); }

"=="|"!="|"<="|">=" { printf("Line %d: RELATIONAL_OP\t'%s'\n", line_count, yytext); }
"+"|"-"|"*"|"/"|"=" { printf("Line %d: OPERATOR\t\t'%s'\n", line_count, yytext); }
"<"|">"             { printf("Line %d: RELATIONAL_OP\t'%s'\n", line_count, yytext); }

"{"|"}"|"("|")"|";"|"," { printf("Line %d: PUNCTUATOR\t\t'%s'\n", line_count, yytext); }

[ \t]+      { /* Ignore whitespace */ }
\n          { line_count++; /* Increment line count on newline */ }

.           { printf("Line %d: ERROR: Unrecognized character '%s'\n", line_count, yytext); }

%%
/* SECTION 3: C CODE (SUBROUTINES) */

int main(int argc, char *argv[]) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Could not open file");
            return 1;
        }
        yyin = file;
    } else {
        printf("No input file specified. Reading from standard input.\n");
    }

    yylex();
}

int yywrap() {
    return 1;
}