#include <stdio.h>

typedef struct _iag_parser_info{
	int max_variables;
	int inputs;
	int outputs;
	int latches;
	int ands;
} AIG_PARSER_INFO;

typedef struct _iag_parser_input {
	int node;
} AIG_PARSER_INPUT;

typedef struct _iag_parser_output {
	int node;
	int inv;
} AIG_PARSER_OUTPUT;

typedef struct _iag_parser_and {
	int node;
	int input1;
	int inv1;
	int input2;
	int inv2;
} AIG_PARSER_AND;

int aigparser_read_info(FILE* stream, AIG_PARSER_INFO* info);
int aigparser_read_input(FILE* stream, AIG_PARSER_INPUT* input);
int aigparser_read_output(FILE* stream, AIG_PARSER_OUTPUT* output);
int aigparser_read_and(FILE* stream, AIG_PARSER_AND* and);

void aigparser_print_info(FILE* stream, AIG_PARSER_INFO info);
void aigparser_print_input(FILE* stream, AIG_PARSER_INPUT input);
void aigparser_print_output(FILE* stream, AIG_PARSER_OUTPUT output);
void aigparser_print_and(FILE* stream, AIG_PARSER_AND and);
