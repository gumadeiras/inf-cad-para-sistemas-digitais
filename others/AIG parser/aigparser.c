#include "aigparser.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char* token;

int aigparser_read_info(FILE* stream, AIG_PARSER_INFO* info){
	char line[50];
	if(!fgets(line, 50, stream))
		return -1;

	token = strtok(line, " ");

	if(strcmp(token, "aig") != 0){
		return -1;
	}
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	info->max_variables = atoi(token);
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	info->inputs = atoi(token);
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	info->latches = atoi(token);
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	info->outputs = atoi(token);
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	info->ands = atoi(token);

	return 0;
}

int aigparser_read_input(FILE* stream, AIG_PARSER_INPUT* input){
	char line[50];
	if(!fgets(line, sizeof(line), stream))
		return -1;
	token = strtok(line, " ");
	input->node = atoi(token);
	return 0;
}

int aigparser_read_output(FILE* stream, AIG_PARSER_OUTPUT* output){
	char line[50];
	int n;
	if(!fgets(line, sizeof(line), stream))
		return -1;

	token = strtok(line, " ");
	n = atoi(token);
	output->node = n % 2 == 0 ? n : (n-1);
	output->inv= n % 2 == 0 ? 0 : 1;
	return 0;
}

int aigparser_read_and(FILE* stream, AIG_PARSER_AND* and){
	char line[50];
	int n;
	if(!fgets(line, sizeof(line), stream))
		return -1;

	token = strtok(line, " ");
	and->node = atoi(token);
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	n = atoi(token);
	and->input1 = n % 2 == 0 ? n : (n-1);
	and->inv1 = n % 2 == 0 ? 0 : 1;
	if((token = strtok(NULL, " ")) == NULL)
		return -1;
	n = atoi(token);
	and->input2 = n % 2 == 0 ? n : (n-1);
	and->inv2 = n % 2 == 0 ? 0 : 1;
	return 0;
}

void aigparser_print_info(FILE* stream, AIG_PARSER_INFO info){
	fprintf(stream, "INFO:\n");
	fprintf(stream, "\tMAX VARIABLES: %i\n", info.max_variables);
	fprintf(stream, "\tINPUTS: %i\n", info.inputs);
	fprintf(stream, "\tOUTPUTS: %i\n", info.outputs);
	fprintf(stream, "\tLATCHES: %i\n", info.latches);
	fprintf(stream, "\tANDS: %i\n", info.ands);
}
void aigparser_print_input(FILE* stream, AIG_PARSER_INPUT input){
	fprintf(stream, "INPUT: %i\n", input.node);
}
void aigparser_print_output(FILE* stream, AIG_PARSER_OUTPUT output){
	fprintf(stream, "OUTPUT: %s%i\n", output.inv == 1 ? "!" : "", output.node);
}
void aigparser_print_and(FILE* stream, AIG_PARSER_AND and){
	fprintf(stream, "AND: %i", and.node);
	fprintf(stream, "\tINPUT1: %s%i", and.inv1 == 1 ? "!" : "", and.input1);
	fprintf(stream, "\tINPUT2: %s%i\n", and.inv2 == 1 ? "!" : "", and.input2);
}
