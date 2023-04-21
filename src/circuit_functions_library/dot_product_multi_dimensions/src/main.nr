use dep::std;
mod data;

global D1_SIZE: Field = 8;
global D1_SHAPE_0: u8 = 2;
global D1_SHAPE_1: u8 = 4;

global D2_SIZE: Field = 2;
global D2_SHAPE_0: u8 = 2;
global D2_SHAPE_1: u8 = 1;

global DATA_SIZE: Field = 10;

struct Data {
    // Two dimensional array represented in one dimension
    d1: [u8; 8],
    // One dimensional array
    d2: [u8; 2],
}

// Computes the dot products. The array must be of the same sizes
fn dot_product(x : [u8; D2_SHAPE_0], y : [u8; D2_SHAPE_0]) -> u16 {
    let mut result = 0;
    // for i in 0..D2_SHAPE_0
    for i in 0..2 {
        // let mut prod = x[i] as u16 * y[i] as u16; // casting to avoid overflow
        result = result + (x[i] as u16 * y[i] as u16);
    }
    result
}

// Unroll x according to its dimensions and compute the dot product with y
// It returns an array of dot products of size D1_SHAPE_1
fn unroll_and_compute(x : [u8; D1_SIZE], 
                      y : [u8; D2_SHAPE_0]
                      ) -> [u16; D1_SHAPE_1] {

    let mut result = [0; D1_SHAPE_1];
    // let mut result = 0;
    // for i in 0..D1_SHAPE_1
    for i in 0..4 {
        let start = i * D1_SHAPE_0 as Field;
        let end = start + D1_SHAPE_0 as Field;
        let mut x_slice = [0; D1_SHAPE_0];

        // let mut slice_index = 0 - start;
        // x_slice[slice_index] = x[i] as u16;
        // x_slice[slice_index+1] = x[end] as u16;
        // result = x_slice;
        for j in start..end {
            let mut slice_index = j - start;
            x_slice[slice_index] = x[j] as u8;
            // result = dot_product(x_slice, y);
            result[i] = dot_product(x_slice, y);
        }
        // result[i] = dot_product(x_slice, y);
    }
    result
}

// // Computes the average
// fn average(x: [u8; D1_SHAPE_1]) -> u8 {
//     let mut sum = 0;
//     for i in 0..D1_SHAPE_1 as Field {
//         sum += x[i] as u32; // Cast to u32 to avoid overflow
//     }
//     let avg = sum / D1_SHAPE_1 as u32; // Cast to u32 to avoid overflow
//     avg as u8 // Cast back to u8 to match the function signature
// }



// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> [u16; D1_SHAPE_1]  {
    
    // let dot_products = unroll_and_compute(data.d1, data.d2);
    // let average = average(dot_products);

    // average

    unroll_and_compute(data.d1, 
                            data.d2
                            )
    
}

fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : pub data::Private,    // Data to be verified and processed.
    ) -> pub [u16; D1_SHAPE_1]{

    // Verify that the obtained result matches the value specified in the public statement.
    constrain public.statement.value == 14;


    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    result


}

        