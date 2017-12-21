#include "aigparser.h"
#include <stdio.h>
#include <stdlib.h>

struct _aig_pointer {
	int node;
	int inv;
	struct _aig_pointer* next;
};

typedef struct _aig_pointer AIG_POINTER;

void aig_print(FILE* stream, AIG_POINTER* aig, int len) {
	AIG_POINTER ref;
	int i;
	fprintf(stream, "AIG with pointers:\n");
	for(i = 0; i < len; i++){
		ref = aig[i];
		if(ref.next == NULL){
			fprintf(stream, "INPUT(%i) \n", i);
		} else if(ref.next->next == NULL){
			fprintf(stream, "OUTPUT(%i): %s%i\n", i, ref.next->inv == 1 ? "!" : "",
				ref.next->node);
		} else {
			fprintf(stream, "AND(%i): %s%i & %s%i\n", i,
				ref.next->inv == 1 ? "!" : "", ref.next->node,
				ref.next->next->inv == 1 ? "!" : "", ref.next->next->node);
		}
	}
}

AIG_POINTER* aig_newnode(void){
	AIG_POINTER* ref = (AIG_POINTER*) calloc(1, sizeof(AIG_POINTER));
	ref->node = 0;
	ref->inv = 0;
	ref->next = NULL;
	return ref;
}

AIG_POINTER aig_emptynode(void){
	AIG_POINTER ref;
	ref.node = 0;
	ref.inv = 0;
	ref.next = NULL;
	return ref;
}

void main(int argc, char *argv[]){
	AIG_PARSER_INFO info;
	AIG_PARSER_INPUT input;
	AIG_PARSER_OUTPUT output;
	AIG_PARSER_AND and;
	/* AIG LIST*/
	AIG_POINTER* aig;
	AIG_POINTER ref;
	char* file_name;
	int elements, index;
	FILE* fp;

	if(argc != 2){
		printf("USAGE:\n\t aigpointer <file_name>\n");
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
	aig = (AIG_POINTER*) calloc(elements, sizeof(AIG_POINTER));

	/* Passing through the inputs */
	index = info.inputs;
	while(index-- != 0){
		aigparser_read_input(fp, &input);
		aigparser_print_input(stderr, input);
		ref = aig_emptynode();
		ref.node = input.node/2 - 1;
		aig[ref.node] = ref;
	}

	index = info.outputs;
	while(index-- != 0){
		aigparser_read_output(fp, &output);
		aigparser_print_output(stderr, output);
		ref = aig_emptynode();
		ref.node = output.node/2 - 1 + info.ands;
		ref.next = aig_newnode();
		ref.next->node = output.node/2 - 1;
		ref.next->inv = output.inv;
		aig[ref.node] = ref;
	}

	index = info.ands;
	while(index-- != 0){
		aigparser_read_and(fp, &and);
		aigparser_print_and(stderr, and);
		ref = aig_emptynode();
		ref.node = and.node/2 - 1;
		ref.next = aig_newnode();
		ref.next->node = and.input1/2 - 1;
		ref.next->inv = and.inv1;
		ref.next->next = aig_newnode();
		ref.next->next->node = and.input2/2 - 1;
		ref.next->next->inv = and.inv2;
		aig[ref.node] = ref;
	}

	aig_print(stderr, aig, elements);
	exit(0);
}
