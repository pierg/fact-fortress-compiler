global D1_SIZE: Field = 8;
global D1_SHAPE_0: u8 = 2;
global D1_SHAPE_1: u8 = 4;

global D2_SIZE: Field = 2;
global D2_SHAPE_0: u8 = 2;
global D2_SHAPE_1: u8 = 1;
global D2_PRECISION: u4 = 2;

global DATA_SIZE: Field = 10;

struct Data {
    // Datas of individuals from Authority A
    d1: [u8; 8],
    // Beta values of heart conditions from Authority A
    d2: [u8; 2],
}

struct Public{
    statement: Statement
}


struct Statement {
    value: u8,
}

struct Private {
    data: Data,
}
