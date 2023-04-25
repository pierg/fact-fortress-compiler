global D1_SIZE: Field = 9260;
global D1_SHAPE_0: u16 = 2;
global D1_SHAPE_1: u16 = 4630;

global D2_SIZE: Field = 2;
global D2_SHAPE_0: u16 = 2;
global D2_SHAPE_1: u16 = 1;

global DATA_SIZE: Field = 9262;

struct Data {
    // Two-dimensional matrix with shape [2, 4630]
    d1: [u16; 9260],
    // Two-dimensional matrix with shape [2, 1]
    d2: [u16; 2],
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
    value: u32,
}

struct Private {
    provenance: Provenance,
    data: Data,
}

struct Provenance {
    signature: [u8; 64],
    hash: [u8; 32],
}
