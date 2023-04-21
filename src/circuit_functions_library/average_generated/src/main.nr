use dep::std;
mod data;

fn dot_product(x : [u8; data::D2_SHAPE_0], y : [u8; data::D2_SHAPE_0]) -> u16 {
    let mut result = 0;
    for i in 0..2 {
        result = result + (x[i] as u16 * y[i] as u16);
    }
    result
}

fn unroll_and_compute(x : [u8; data::D1_SIZE], 
                    y : [u8; data::D2_SHAPE_0]) -> [u16; 4] {
    let mut result = [0; 4];
    for i in 0..4 {
        let start = i * 2 as Field;
        let end = start + 2 as Field;
        let mut x_slice = [0; 2];
        for j in start..end {
            let mut slice_index = j - start;
            x_slice[slice_index] = x[j] as u8;
            result[i] = dot_product(x_slice, y);
        }
    }
    result
}

fn average(x: [u16; 4]) -> u16 {
    let mut sum = 0;
    for i in 0..4 as Field {
        sum += x[i] as u32;
    }
    let avg = sum / 4 as u32;
    avg as u16
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

        