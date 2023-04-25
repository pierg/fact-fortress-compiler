global D1_SIZE: Field = 80;
global D1_SHAPE_0: u8 = 2;
global D1_SHAPE_1: u8 = 40;

global D2_SIZE: Field = 2;
global D2_SHAPE_0: u8 = 2;
global D2_SHAPE_1: u8 = 1;

global DATA_SIZE: Field = 82;

struct Data {
    // Two-dimensional matrix with shape [2, 40]
    d1: [u8; 80],
    // Two-dimensional matrix with shape [2, 1]
    d2: [u8; 2],
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
    value: u16,
}

struct Private {
    provenance: Provenance,
    data: Data,
}

struct Provenance {
    signature: [u8; 64],
    hash: [u8; 32],
}
