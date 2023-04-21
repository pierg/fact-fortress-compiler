use dep::std;
mod data;

// Declare the size of the first dimension for Data
global D1_SIZE: Field = 8;
// Declare the size of the first dimension for the first element of Data
global D1_SHAPE_0: u8 = 2;
// Declare the size of the second dimension for the first element of Data
global D1_SHAPE_1: u8 = 4;

// Declare the size of the second dimension for Data
global D2_SIZE: Field = 2;
// Declare the size of the first dimension for the second element of Data
global D2_SHAPE_0: u8 = 2;
// Declare the size of the second dimension for the second element of Data
global D2_SHAPE_1: u8 = 1;

// Calculate the total size of the two dimensional Data array
global DATA_SIZE: Field = 10;

// Define the Data struct with two arrays, d1 and d2
struct Data {
    // Two dimensional array represented in one dimension
    d1: [u8; 8],
    // One dimensional array
    d2: [u8; 2],
}

// Compute the dot product of two one dimensional arrays of the same size
// x : first array, y : second array
fn dot_product(x : [u8; D2_SHAPE_0], y : [u8; D2_SHAPE_0]) -> u16 {

    let mut result = 0;

    // Loop through the elements of the arrays and compute the dot product
    for i in 0..2 {
        result = result + (x[i] as u16 * y[i] as u16); // Cast to avoid overflow
    }
    result
}

// Unroll the two dimensional array x into a one dimensional array, 
// then compute the dot products of the unrolled arrays with y
// Returns an array of DP1_SHAPE_1 dot products
fn unroll_and_compute(x : [u8; D1_SIZE], 
                      y : [u8; D2_SHAPE_0]) -> [u16; D1_SHAPE_1] {

    let mut result = [0; D1_SHAPE_1];

    // For each row of x, unroll it and compute dot product with y
    for i in 0..4 {
        let start = i * D1_SHAPE_0 as Field;
        let end = start + D1_SHAPE_0 as Field;
        let mut x_slice = [0; D1_SHAPE_0];
        for j in start..end {
            let mut slice_index = j - start;
            x_slice[slice_index] = x[j] as u8;
            result[i] = dot_product(x_slice, y);
        }
    }
    result
}

// Compute the average of the values in an array
// x : array of values for which the average will be computed
fn average(x: [u16; D1_SHAPE_1]) -> u16 {
    let mut sum = 0;
    for i in 0..D1_SHAPE_1 as Field {
        sum += x[i] as u32; // Cast to u32 to avoid overflow
    }
    let avg = sum / D1_SHAPE_1 as u32; // Cast to u32 to avoid overflow
    avg as u16 // Cast back to u16 to match the function signature
}



// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> u16  {
    
    let dot_products = unroll_and_compute(data.d1, data.d2);

    let average = average(dot_products);

    average

}

fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : pub data::Private,    // Data to be verified and processed.
    ) -> pub u16{

    // Verify that the obtained result matches the value specified in the public statement.
    constrain public.statement.value == 14;


    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    result


}

        