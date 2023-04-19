global D1_SIZE: Field = 6;
global D1_SHAPE: [u8; 2] = [3, 2];

global D2_SIZE: Field = 3;
global D2_SHAPE: [u8; 2] = [3, 1];
global D2_PRECISION: u4 = 1;

global DATA_SIZE: Field = 9;

struct Data {
    // Alleles of individuals from Hospital A
    d1: [u8; 6],
    // Beta values of heart conditions from Hospital A
    d2: [u8; 3],
}

struct Public{
    keys: Keys,
    statement: Statement
}

struct Keys {
    pub_key_x: Field,
    pub_key_y: Field,
}

struct Statement {
    value: u8,
}

struct Private {
    provenance: Provenance,
    data: Data,
}

struct Provenance {
    signature: [u8; 64],
    hash: [u8; 32],
}
