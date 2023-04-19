global D1_SIZE: Field = 6;
global D1_SHAPE: [u8; 2] = [2, 3];

global D2_SIZE: Field = 2;
global D2_SHAPE: [u8; 2] = [2, 1];
global D2_PRECISION: u4 = 1;

global DATA_SIZE: Field = 8;


struct Data {
    // Alleles of individuals
    d1: [u2; 6],
    // Risk factor
    d2: [u8; 3],
}
