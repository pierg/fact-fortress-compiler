use dep::std;
mod data;

// global D1_SIZE: Field = 50;
// global D1_SHAPE: [u8; 2] = [5, 10];

// global D2_SIZE: Field = 5;
// global D2_SHAPE: [u8; 2] = [5, 1];
// global D2_PRECISION: u4 = 2;

// global DATA_SIZE: Field = 55;

// struct Data {
//     // Alleles of individuals from Hospital A
//     d1: [u8; 50],
//     // Beta values of heart conditions from Hospital A
//     d2: [u8; 5],
// }

fn dotproduct(d1 : [u8; 50], d2 : [u8; 5]) -> u8 {
    let mut out = 0;
    for i in 0..2 {
        out = out + x[i] * y[i];
    }
    out
}

fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : data::Private,    // Data to be verified and processed.
    ){

    // Verify the authenticity and integrity of the private data.
    constrain verify_data_provenance(private.data, public.keys, private.provenance) == 1;

    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

}

        