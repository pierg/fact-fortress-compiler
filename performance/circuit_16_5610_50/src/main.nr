use dep::std;
mod data;



    
// Compute the dot product of two one dimensional arrays of the same size
// x : first array, y : second array
fn dot_product(x : [u16; data::D2_SHAPE_0], y : [u16; data::D2_SHAPE_0]) -> u32 {
    let mut result = 0;

    // Loop through the elements of the arrays and compute the dot product
    for i in 0..2 {
        result = result + (x[i] as u32 * y[i] as u32); // Cast to avoid overflow
    }
    result
}


// Unroll the two dimensional array x into a one dimensional array, 
// then compute the dot products of the unrolled arrays with y
// Returns an array of DP1_SHAPE_1 dot products
fn unroll_and_compute(x : [u16; data::D1_SIZE], 
                    y : [u16; data::D2_SHAPE_0]) -> [u32; 2805] {
    let mut result = [0; 2805];
    // For each row of x, unroll it and compute dot product with y
    for i in 0..2805 {
        let start = i * 2 as Field;
        let end = start + 2 as Field;
        let mut x_slice = [0; 2];
        for j in start..end {
            let mut slice_index = j - start;
            x_slice[slice_index] = x[j] as u16;
            result[i] = dot_product(x_slice, y);
        }
    }
    result
}

// Compute the average of the values in an array
// x : array of values for which the average will be computed
fn average(x: [u32; 2805]) -> u32 {
    let mut sum = 0;
    for i in 0..2805 as Field {
        sum += x[i] as u64;
    }
    let avg = sum / 2805 as u64; // Cast to u32 to avoid overflow
    avg as u32 // Cast back to u16 to match the function signature
}

// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> u32 {
    
    let dot_products = unroll_and_compute(data.d1, data.d2);

    let average = average(dot_products);

    average

}






fn main(
    public : pub data::Public,    // Data containing the expected result.
    private : data::Private,    // Data to be verified and processed.
    ) -> pub u32{


    // Perform some meaningful operations on the private data.
    let result = perform_computation_on_data(private.data);

    // Verify that the obtained result matches the value specified in the public statement.
    constrain result == public.statement.value;

    // Return result, for debugging
    result

}

        