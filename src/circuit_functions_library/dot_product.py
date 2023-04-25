from shared import Aggregator


D1_SIZE = 8
D1_SHAPE_0 = 2
D1_SHAPE_1 = 4
D1_TYPE = "u8"
D2_SIZE = 2
D2_SHAPE_0 = 2
D2_SHAPE_1 = 1
D2_TYPE = "u8"
DOT_TYPE = f"u{2*int(D1_TYPE[1])}"
DIV_TYPE = f"u{4*int(D1_TYPE[1])}"


def generate_dot_product_multi(
    data_1_name: str,
    data_1_info: dict,
    data_2_name: str,
    data_2_info: dict,
    aggregator: Aggregator,
) -> str:
    D1_SIZE = len(data_1_info["values"])
    D1_SHAPE_0 = data_1_info["shape"][0]
    D1_SHAPE_1 = data_1_info["shape"][1]
    D1_TYPE = data_1_info["format"]
    D2_SIZE = len(data_2_info["values"])
    D2_SHAPE_0 = data_2_info["shape"][0]
    D2_SHAPE_1 = data_2_info["shape"][1]
    D2_TYPE = data_2_info["format"]
    DOT_TYPE = f"u{2*int(data_1_info['format'][1:])}"
    DIV_TYPE = f"u{4*int(data_1_info['format'][1:])}"

    # Noir code generation
    noir_code = f"""

    
// Compute the dot product of two one dimensional arrays of the same size
// x : first array, y : second array
fn dot_product(x : [{D1_TYPE}; data::{data_2_name}_SHAPE_0], y : [{D1_TYPE}; data::{data_2_name}_SHAPE_0]) -> {DOT_TYPE} {{
    let mut result = 0;

    // Loop through the elements of the arrays and compute the dot product
    for i in 0..{D2_SHAPE_0} {{
        result = result + (x[i] as {DOT_TYPE} * y[i] as {DOT_TYPE}); // Cast to avoid overflow
    }}
    result
}}


// Unroll the two dimensional array x into a one dimensional array, 
// then compute the dot products of the unrolled arrays with y
// Returns an array of DP1_SHAPE_1 dot products
fn unroll_and_compute(x : [{D1_TYPE}; data::{data_1_name}_SIZE], 
                    y : [{D1_TYPE}; data::{data_2_name}_SHAPE_0]) -> [{DOT_TYPE}; {D1_SHAPE_1}] {{
    let mut result = [0; {D1_SHAPE_1}];
    // For each row of x, unroll it and compute dot product with y
    for i in 0..{(D1_SHAPE_1)} {{
        let start = i * {D1_SHAPE_0} as Field;
        let end = start + {D1_SHAPE_0} as Field;
        let mut x_slice = [0; {D1_SHAPE_0}];
        for j in start..end {{
            let mut slice_index = j - start;
            x_slice[slice_index] = x[j] as {D1_TYPE};
            result[i] = dot_product(x_slice, y);
        }}
    }}
    result
}}

// Compute the average of the values in an array
// x : array of values for which the average will be computed
fn average(x: [{DOT_TYPE}; {D1_SHAPE_1}]) -> {DOT_TYPE} {{
    let mut sum = 0;
    for i in 0..{D1_SHAPE_1} as Field {{
        sum += x[i] as {DIV_TYPE};
    }}
    let avg = sum / {D1_SHAPE_1} as {DIV_TYPE}; // Cast to u32 to avoid overflow
    avg as {DOT_TYPE} // Cast back to u16 to match the function signature
}}

// Perform some meaningful operations on the data and return the result.
fn perform_computation_on_data(data: data::Data) -> {DOT_TYPE} {{
    
    let dot_products = unroll_and_compute(data.{data_1_name.lower()}, data.{data_2_name.lower()});

    let average = average(dot_products);

    average

}}




"""

    return noir_code
