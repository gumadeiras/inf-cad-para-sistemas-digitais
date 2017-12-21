#include "aigparser.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct _aig_static {
	int adj1;
	int inv1;
	int adj2;
	int inv2;
} AIG_STATIC;

void aig_print(FILE* stream, AIG_STATIC* aig, int len) {
	AIG_STATIC node;
	int i;
	fprintf(stream, "AIG with integers:\n");
	for(i = 0; i < len; i++){
		node = aig[i];
		if(node.adj2 == -1 && node.adj1 == -1){
			fprintf(stream, "INPUT(%i) \n", i);
		} else if(node.adj2 == -1){
			fprintf(stream, "OUTPUT(%i): %s%i\n", i, node.inv1 == 1 ? "!" : "",
				node.adj1);
		} else {
			fprintf(stream, "AND(%i): %s%i & %s%i\n", i, node.inv1 == 1 ? "!" : "",
				node.adj1, node.inv2 == 1 ? "!" : "", node.adj2);
		}
	}
}

AIG_STATIC aig_newnode(void){
	AIG_STATIC node;
	node.adj1 = 0;
	node.inv1 = 0;
	node.adj2 = 0;
	node.inv2 = 0;
	return node;
}

void main(int argc, char *argv[]){
	AIG_PARSER_INFO info;
	AIG_PARSER_INPUT input;
	AIG_PARSER_OUTPUT output;
	AIG_PARSER_AND and;
	/* AIG LIST*/
	AIG_STATIC* aig;
	AIG_STATIC node;
	char* file_name;
	int elements, index;
	FILE* fp;

	if(argc != 2){
		printf("USAGE:\n\t aigint <file_name>\n");
		exit(1);
	}

	file_name = argv[1];
	if(!(fp = fopen(file_name, "r"))){
		printf("Error at open file %s\n", file_name);
		exit(2);
	}

	/* AIG PARSER*/
	aigparser_read_info(fp, &info);
	aigparser_print_info(stderr, info);

	/* Allocating memory for the aig*/
	elements = info.inputs + info.outputs + info.ands;
	aig = (AIG_STATIC*) calloc(elements, sizeof(AIG_STATIC));

	/* Passing through the inputs */
	index = info.inputs;
	while(index-- != 0){
		aigparser_read_input(fp, &input);
		aigparser_print_input(stderr, input);
		node = aig_newnode();
		node.adj1 = -1;
		node.adj2 = -1;
		aig[input.node/2 - 1] = node;
	}

	index = info.outputs;
	while(index-- != 0){
		aigparser_read_output(fp, &output);
		aigparser_print_output(stderr, output);
		node = aig_newnode();
		node.adj1 = output.node/2 - 1;
		node.inv1 = output.inv;
		node.adj2 = -1;
		aig[output.node/2 - 1 + info.ands] = node;
	}

	index = info.ands;
	while(index-- != 0){
		aigparser_read_and(fp, &and);
		aigparser_print_and(stderr, and);
		node = aig_newnode();
		node.adj1 = and.input1/2 - 1;
		node.inv1 = and.inv1;
		node.adj2 = and.input2/2 - 1;
		node.inv2 = and.inv2;
		aig[and.node/2 - 1] = node;
	}

	aig_print(stderr, aig, elements);
	exit(0);
}
